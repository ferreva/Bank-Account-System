# models/account.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
from models.transaction import Transaction, TransactionType

class Account(ABC):
    """Абстрактный базовый класс для всех счетов."""
    
    def __init__(self, account_id: str, owner_name: str, balance: float = 0.0):
        self._account_id = account_id
        self._owner_name = owner_name
        self._balance = balance
        self._transactions: List[Transaction] = []
        self._created_at = datetime.now()
    
    @property
    def account_id(self) -> str:
        return self._account_id
    
    @property
    def owner_name(self) -> str:
        return self._owner_name
    
    @owner_name.setter
    def owner_name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Имя владельца не может быть пустым")
        self._owner_name = value.strip()
    
    @property
    def balance(self) -> float:
        return self._balance
    
    @abstractmethod
    def get_account_type(self) -> str:
        """Возвращает тип счета."""
        pass
    
    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        """Снятие средств (логика зависит от типа счета)."""
        pass
    
    def deposit(self, amount: float) -> bool:
        """Пополнение счета."""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        self._balance += amount
        transaction = Transaction(
            account_id=self._account_id,
            amount=amount,
            type=TransactionType.DEPOSIT,
            description=f"Пополнение счета"
        )
        self._transactions.append(transaction)
        return True
    
    def add_transaction(self, transaction: Transaction):
        """Добавляет транзакцию в историю."""
        self._transactions.append(transaction)
    
    def get_transactions(self, start_date: datetime = None, 
                         end_date: datetime = None,
                         transaction_type: TransactionType = None) -> List[Transaction]:
        """Получает транзакции с фильтрацией."""
        filtered = self._transactions.copy()
        
        if start_date:
            filtered = [t for t in filtered if t.timestamp >= start_date]
        if end_date:
            filtered = [t for t in filtered if t.timestamp <= end_date]
        if transaction_type:
            filtered = [t for t in filtered if t.type == transaction_type]
        
        return filtered
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует счет в словарь для JSON."""
        return {
            "account_id": self._account_id,
            "owner_name": self._owner_name,
            "balance": self._balance,
            "account_type": self.get_account_type(),
            "created_at": self._created_at.isoformat(),
            "transactions": [t.to_dict() for t in self._transactions]
        }
    
    def __str__(self) -> str:
        return f"{self.get_account_type()} | {self._account_id} | {self._owner_name} | {self._balance:.2f}₽"
