# models/credit_account.py
from models.account import Account
from models.transaction import Transaction, TransactionType

class CreditAccount(Account):
    """Кредитный счет (с кредитным лимитом)."""
    
    def __init__(self, account_id: str, owner_name: str, credit_limit: float = 50000.0, 
                 interest_rate: float = 0.20):
        super().__init__(account_id, owner_name, 0.0)  # Кредитный счет начинается с 0
        self._credit_limit = credit_limit
        self._interest_rate = interest_rate
        self._debt = 0.0  # Текущий долг
    
    @property
    def debt(self) -> float:
        return self._debt
    
    @property
    def available_credit(self) -> float:
        return self._credit_limit - self._debt
    
    def get_account_type(self) -> str:
        return "Кредитный"
    
    @property
    def balance(self) -> float:
        """Для кредитного счета баланс - это доступные средства."""
        return self.available_credit
    
    def withdraw(self, amount: float) -> bool:
        """Снятие в кредит."""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        if self.available_credit >= amount:
            self._debt += amount
            transaction = Transaction(
                account_id=self._account_id,
                amount=amount,
                type=TransactionType.WITHDRAW,
                description=f"Снятие в кредит"
            )
            self._transactions.append(transaction)
            return True
        else:
            raise ValueError(f"Недостаточно кредитного лимита. Доступно: {self.available_credit:.2f}")
    
    def deposit(self, amount: float) -> bool:
        """Погашение долга."""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        if amount >= self._debt:
            amount = self._debt
        
        self._debt -= amount
        
        transaction = Transaction(
            account_id=self._account_id,
            amount=amount,
            type=TransactionType.DEPOSIT,
            description=f"Погашение кредита"
        )
        self._transactions.append(transaction)
        return True
    
    def charge_interest(self) -> float:
        """Начисляет проценты на долг."""
        interest = self._debt * self._interest_rate / 12  # Месячные проценты
        self._debt += interest
        transaction = Transaction(
            account_id=self._account_id,
            amount=interest,
            type=TransactionType.INTEREST,
            description=f"Начисление процентов по кредиту ({self._interest_rate*100}%)"
        )
        self._transactions.append(transaction)
        return interest
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["credit_limit"] = self._credit_limit
        data["interest_rate"] = self._interest_rate
        data["debt"] = self._debt
        return data
