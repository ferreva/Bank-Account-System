# models/savings_account.py
from models.account import Account
from models.transaction import Transaction, TransactionType

class SavingsAccount(Account):
    """Сберегательный счет (с процентами)."""
    
    def __init__(self, account_id: str, owner_name: str, balance: float = 0.0, interest_rate: float = 0.05):
        super().__init__(account_id, owner_name, balance)
        self._interest_rate = interest_rate
    
    def get_account_type(self) -> str:
        return "Сберегательный"
    
    def withdraw(self, amount: float) -> bool:
        """Снятие без возможности уйти в минус."""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        if self._balance >= amount:
            self._balance -= amount
            transaction = Transaction(
                account_id=self._account_id,
                amount=amount,
                type=TransactionType.WITHDRAW,
                description=f"Снятие со сберегательного счета"
            )
            self._transactions.append(transaction)
            return True
        else:
            raise ValueError(f"Недостаточно средств. Доступно: {self._balance:.2f}")
    
    def add_interest(self) -> float:
        """Начисляет проценты на остаток."""
        interest = self._balance * self._interest_rate
        self._balance += interest
        transaction = Transaction(
            account_id=self._account_id,
            amount=interest,
            type=TransactionType.INTEREST,
            description=f"Начисление процентов ({self._interest_rate*100}%)"
        )
        self._transactions.append(transaction)
        return interest
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["interest_rate"] = self._interest_rate
        return data
