# utils/transaction_queue.py
from collections import deque
from typing import List, Optional
from models.transaction import Transaction

class TransactionHistoryQueue:
    """Очередь для хранения истории транзакций."""
    
    def __init__(self, max_size: int = 100):
        self._queue = deque(maxlen=max_size)
    
    def add_transaction(self, transaction: Transaction):
        """Добавляет транзакцию в очередь."""
        self._queue.append(transaction)
    
    def get_all(self) -> List[Transaction]:
        """Возвращает все транзакции в порядке FIFO."""
        return list(self._queue)
    
    def get_last(self, count: int = 10) -> List[Transaction]:
        """Возвращает последние N транзакций."""
        return list(self._queue)[-count:]
    
    def clear(self):
        """Очищает очередь."""
        self._queue.clear()
    
    def __len__(self) -> int:
        return len(self._queue)
