# controllers/bank_controller.py
from typing import List, Optional
from datetime import datetime
from models.account import Account
from models.checking_account import CheckingAccount
from models.savings_account import SavingsAccount
from models.credit_account import CreditAccount
from models.transaction import Transaction, TransactionType
from utils.storage import BankStorage
from utils.transaction_queue import TransactionHistoryQueue

class BankController:
    """Контроллер банковской системы."""
    
    def __init__(self, storage: BankStorage):
        self._storage = storage
        self._accounts: List[Account] = []
        self._transaction_queue = TransactionHistoryQueue()
        self._load_data()
    
    def _load_data(self):
        """Загружает данные из хранилища."""
        self._accounts = self._storage.load()
        # Восстанавливаем транзакции в очереди
        for account in self._accounts:
            for transaction in account.get_transactions():
                self._transaction_queue.add_transaction(transaction)
    
    def _save_data(self):
        """Сохраняет данные в хранилище."""
        self._storage.save(self._accounts)
    
    def _add_to_queue(self, transaction: Transaction):
        """Добавляет транзакцию в очередь."""
        self._transaction_queue.add_transaction(transaction)
    
    def create_account(self, owner_name: str, account_type: str) -> Optional[Account]:
        """Создает новый счет."""
        try:
            import uuid
            account_id = str(uuid.uuid4())[:8]
            
            if account_type == "checking":
                account = CheckingAccount(account_id, owner_name, 0.0, 10000.0)
            elif account_type == "savings":
                account = SavingsAccount(account_id, owner_name, 0.0, 0.05)
            elif account_type == "credit":
                account = CreditAccount(account_id, owner_name, 50000.0, 0.20)
            else:
                return None
            
            self._accounts.append(account)
            self._save_data()
            
            # Транзакция открытия счета
            transaction = Transaction(
                account_id=account_id,
                amount=0,
                type=TransactionType.DEPOSIT,
                description=f"Открытие счета"
            )
            account.add_transaction(transaction)
            self._add_to_queue(transaction)
            
            return account
        except Exception as e:
            print(f"❌ Ошибка создания счета: {e}")
            return None
    
    def get_all_accounts(self) -> List[Account]:
        """Возвращает все счета."""
        return self._accounts.copy()
    
    def get_account_by_index(self, index: int) -> Optional[Account]:
        """Возвращает счет по индексу."""
        if 0 <= index < len(self._accounts):
            return self._accounts[index]
        return None
    
    def deposit(self, account_index: int, amount: float) -> bool:
        """Пополняет счет."""
        account = self.get_account_by_index(account_index)
        if not account:
            return False
        
        try:
            result = account.deposit(amount)
            if result:
                self._save_data()
                # Транзакция уже добавлена в account.deposit
                transaction = account.get_transactions()[-1]
                self._add_to_queue(transaction)
                return True
        except ValueError as e:
            print(f"❌ {e}")
        return False
    
    def withdraw(self, account_index: int, amount: float) -> bool:
        """Снимает со счета."""
        account = self.get_account_by_index(account_index)
        if not account:
            return False
        
        try:
            result = account.withdraw(amount)
            if result:
                self._save_data()
                transaction = account.get_transactions()[-1]
                self._add_to_queue(transaction)
                return True
        except ValueError as e:
            print(f"❌ {e}")
        return False
    
    def transfer(self, from_index: int, to_index: int, amount: float) -> bool:
        """Переводит средства между счетами."""
        from_account = self.get_account_by_index(from_index)
        to_account = self.get_account_by_index(to_index)
        
        if not from_account or not to_account:
            return False
        
        if from_account.account_id == to_account.account_id:
            print("❌ Нельзя переводить на тот же счет")
            return False
        
        try:
            # Снимаем с отправителя
            from_account.withdraw(amount)
            
            # Отправляем получателю
            to_account.deposit(amount)
            
            # Добавляем транзакции перевода
            send_transaction = Transaction(
                account_id=from_account.account_id,
                amount=amount,
                type=TransactionType.TRANSFER_SEND,
                description=f"Перевод на счет {to_account.account_id}",
                related_account=to_account.account_id
            )
            from_account.add_transaction(send_transaction)
            
            receive_transaction = Transaction(
                account_id=to_account.account_id,
                amount=amount,
                type=TransactionType.TRANSFER_RECEIVE,
                description=f"Перевод со счета {from_account.account_id}",
                related_account=from_account.account_id
            )
            to_account.add_transaction(receive_transaction)
            
            self._save_data()
            self._add_to_queue(send_transaction)
            self._add_to_queue(receive_transaction)
            
            return True
        except ValueError as e:
            print(f"❌ {e}")
            # Откатываем изменения если ошибка
            self._load_data()
            return False
    
    def get_transactions(self, account_index: int = None, 
                         start_date: datetime = None,
                         end_date: datetime = None,
                         transaction_type: TransactionType = None) -> List[Transaction]:
        """Получает транзакции с фильтрацией."""
        if account_index is not None:
            account = self.get_account_by_index(account_index)
            if account:
                return account.get_transactions(start_date, end_date, transaction_type)
            return []
        else:
            # Все транзакции из очереди
            transactions = self._transaction_queue.get_all()
            
            if start_date:
                transactions = [t for t in transactions if t.timestamp >= start_date]
            if end_date:
                transactions = [t for t in transactions if t.timestamp <= end_date]
            if transaction_type:
                transactions = [t for t in transactions if t.type == transaction_type]
            
            return transactions
    
    def add_interest_to_savings(self) -> int:
        """Начисляет проценты на все сберегательные счета."""
        count = 0
        for account in self._accounts:
            if isinstance(account, SavingsAccount):
                interest = account.add_interest()
                self._add_to_queue(account.get_transactions()[-1])
                count += 1
                print(f"💰 Начислено процентов на счет {account.account_id}: {interest:.2f}₽")
        
        if count > 0:
            self._save_data()
        return count
    
    def delete_account(self, account_index: int) -> bool:
        """Закрывает счет."""
        if 0 <= account_index < len(self._accounts):
            account = self._accounts[account_index]
            if account.balance != 0:
                if isinstance(account, CreditAccount) and account.debt > 0:
                    print(f"❌ Нельзя закрыть кредитный счет с долгом {account.debt:.2f}₽")
                    return False
                elif not isinstance(account, CreditAccount) and account.balance > 0:
                    print(f"❌ Нельзя закрыть счет с остатком {account.balance:.2f}₽")
                    return False
            
            deleted = self._accounts.pop(account_index)
            self._save_data()
            print(f"✅ Счет {deleted.account_id} закрыт")
            return True
        
        return False
