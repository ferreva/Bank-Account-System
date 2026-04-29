# utils/storage.py
import json
import os
from typing import List, Dict, Any
from models.account import Account
from models.checking_account import CheckingAccount
from models.savings_account import SavingsAccount
from models.credit_account import CreditAccount
from models.transaction import Transaction, TransactionType

class BankStorage:
    """Сохраняет и загружает данные банка в JSON."""
    
    def __init__(self, filename: str = "bank_data.json"):
        self._filename = filename
    
    def save(self, accounts: List[Account]) -> bool:
        """Сохраняет список счетов в файл."""
        data = []
        for account in accounts:
            account_data = account.to_dict()
            data.append(account_data)
        
        try:
            with open(self._filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False
    
    def load(self) -> List[Account]:
        """Загружает список счетов из файла."""
        if not os.path.exists(self._filename):
            return []
        
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            accounts = []
            for account_data in data:
                account_type = account_data.get("account_type")
                
                if account_type == "Расчетный":
                    account = CheckingAccount(
                        account_id=account_data["account_id"],
                        owner_name=account_data["owner_name"],
                        balance=account_data["balance"],
                        overdraft_limit=account_data.get("overdraft_limit", 0)
                    )
                elif account_type == "Сберегательный":
                    account = SavingsAccount(
                        account_id=account_data["account_id"],
                        owner_name=account_data["owner_name"],
                        balance=account_data["balance"],
                        interest_rate=account_data.get("interest_rate", 0.05)
                    )
                elif account_type == "Кредитный":
                    account = CreditAccount(
                        account_id=account_data["account_id"],
                        owner_name=account_data["owner_name"],
                        credit_limit=account_data.get("credit_limit", 50000),
                        interest_rate=account_data.get("interest_rate", 0.20)
                    )
                    # Восстанавливаем долг
                    if "debt" in account_data:
                        account._debt = account_data["debt"]
                else:
                    continue
                
                # Восстанавливаем транзакции
                for trans_data in account_data.get("transactions", []):
                    transaction = Transaction.from_dict(trans_data)
                    account._transactions.append(transaction)
                
                accounts.append(account)
            
            return accounts
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return []
