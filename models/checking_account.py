# models/checking_account.py
from models.account import Account
from models.transaction import Transaction, TransactionType

class CheckingAccount(Account):
    """Расчетный счет (обычные операции)."""
    
    def __init__(self, account_id: str, owner_name: str, balance: float = 0.0, overdraft_limit: float = 0.0):
        super().__init__(account_id, owner_name, balance)
        self._overdraft_limit = overdraft_limit
    
    def get_account_type(self) -> str:
        return "Расчетный"
    
    def withdraw(self, amount: float) -> bool:
        """Снятие с учетом овердрафта."""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        if self._balance + self._overdraft_limit >= amount:
            self._balance -= amount
            transaction = Transaction(
                account_id=self._account_id,
                amount=amount,
                type=TransactionType.WITHDRAW,
                description=f"Снятие со счета"
            )
            self._transactions.append(transaction)
            return True
        else:
            raise ValueError(f"Недостаточно средств. Доступно: {self._balance + self._overdraft_limit:.2f}")
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["overdraft_limit"] = self._overdraft_limit
        return data
