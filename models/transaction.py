# models/transaction.py
from datetime import datetime
from typing import Dict, Any
from enum import Enum

class TransactionType(Enum):
    """Типы транзакций."""
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER_SEND = "transfer_send"
    TRANSFER_RECEIVE = "transfer_receive"
    INTEREST = "interest"
    FEE = "fee"

class Transaction:
    """Модель транзакции."""
    
    def __init__(self, account_id: str, amount: float, type: TransactionType, 
                 description: str = "", related_account: str = None):
        self._account_id = account_id
        self._amount = amount
        self._type = type
        self._description = description
        self._related_account = related_account
        self._timestamp = datetime.now()
    
    @property
    def account_id(self) -> str:
        return self._account_id
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @property
    def type(self) -> TransactionType:
        return self._type
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def timestamp(self) -> datetime:
        return self._timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует транзакцию в словарь для JSON."""
        return {
            "account_id": self._account_id,
            "amount": self._amount,
            "type": self._type.value,
            "description": self._description,
            "related_account": self._related_account,
            "timestamp": self._timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Создает транзакцию из словаря."""
        trans = cls(
            account_id=data["account_id"],
            amount=data["amount"],
            type=TransactionType(data["type"]),
            description=data.get("description", ""),
            related_account=data.get("related_account")
        )
        trans._timestamp = datetime.fromisoformat(data["timestamp"])
        return trans
    
    def __str__(self) -> str:
        type_icons = {
            TransactionType.DEPOSIT: "💰",
            TransactionType.WITHDRAW: "💸",
            TransactionType.TRANSFER_SEND: "📤",
            TransactionType.TRANSFER_RECEIVE: "📥",
            TransactionType.INTEREST: "📈",
            TransactionType.FEE: "⚡"
        }
        icon = type_icons.get(self._type, "💳")
        return f"{icon} {self._timestamp.strftime('%Y-%m-%d %H:%M')} | {self._type.value} | {self._amount:.2f}₽ | {self._description}"
