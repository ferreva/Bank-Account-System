# tests/test_accounts.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.checking_account import CheckingAccount
from models.savings_account import SavingsAccount
from models.credit_account import CreditAccount
from models.transaction import TransactionType

def test_checking_account():
    """Тест расчетного счета."""
    print("\n🧪 Тестирование расчетного счета...")
    
    account = CheckingAccount("CHK001", "Иван Петров", 1000.0, 500.0)
    
    # Пополнение
    account.deposit(500)
    assert account.balance == 1500.0
    print("✅ Пополнение работает")
    
    # Снятие в пределах баланса
    account.withdraw(300)
    assert account.balance == 1200.0
    print("✅ Снятие в пределах баланса работает")
    
    # Снятие с овердрафтом
    account.withdraw(1500)
    assert account.balance == -300.0
    print("✅ Овердрафт работает")
    
    # Попытка снятия больше овердрафта
    try:
        account.withdraw(1000)
        assert False, "Должна быть ошибка"
    except ValueError:
        print("✅ Ограничение овердрафта работает")
    
    print("✅ Расчетный счет прошел тесты!")

def test_savings_account():
    """Тест сберегательного счета."""
    print("\n🧪 Тестирование сберегательного счета...")
    
    account = SavingsAccount("SAV001", "Мария Сидорова", 10000.0, 0.05)
    
    # Пополнение
    account.deposit(2000)
    assert account.balance == 12000.0
    print("✅ Пополнение работает")
    
    # Начисление процентов
    interest = account.add_interest()
    assert interest == 600.0  # 5% от 12000
    assert account.balance == 12600.0
    print("✅ Начисление процентов работает")
    
    # Снятие (нельзя уйти в минус)
    account.withdraw(5000)
    assert account.balance == 7600.0
    
    try:
        account.withdraw(10000)
        assert False
    except ValueError:
        print("✅ Невозможно уйти в минус")
    
    print("✅ Сберегательный счет прошел тесты!")

def test_credit_account():
    """Тест кредитного счета."""
    print("\n🧪 Тестирование кредитного счета...")
    
    account = CreditAccount("CRD001", "Алексей Новиков", 50000.0, 0.20)
    
    # Снятие в кредит
    account.withdraw(30000)
    assert account.debt == 30000.0
    assert account.available_credit == 20000.0
    print("✅ Снятие в кредит работает")
    
    # Попытка превысить лимит
    try:
        account.withdraw(25000)
        assert False
    except ValueError:
        print("✅ Лимит кредита работает")
    
    # Погашение долга
    account.deposit(10000)
    assert account.debt == 20000.0
    print("✅ Погашение кредита работает")
    
    # Начисление процентов
    interest = account.charge_interest()
    assert interest == 333.33  # ~ 20000 * 0.2 / 12
    print("✅ Проценты по кредиту работают")
    
    print("✅ Кредитный счет прошел тесты!")

def test_transactions():
    """Тест транзакций."""
    print("\n🧪 Тестирование транзакций...")
    
    account = CheckingAccount("CHK002", "Тест Тестов", 1000.0)
    
    account.deposit(500)
    account.withdraw(200)
    
    transactions = account.get_transactions()
    assert len(transactions) == 2
    
    # Фильтрация по типу
    deposits = account.get_transactions(transaction_type=TransactionType.DEPOSIT)
    assert len(deposits) == 1
    
    print("✅ Фильтрация транзакций работает")
    print("✅ Транзакции прошли тесты!")

def test_error_handling():
    """Тест обработки ошибок."""
    print("\n🧪 Тестирование обработки ошибок...")
    
    account = CheckingAccount("CHK003", "Ошибка Тест", 1000.0)
    
    # Негативные суммы
    try:
        account.deposit(-100)
        assert False
    except ValueError:
        print("✅ Отрицательная сумма пополнения отклонена")
    
    try:
        account.withdraw(-50)
        assert False
    except ValueError:
        print("✅ Отрицательная сумма снятия отклонена")
    
    # Пустые имена
    try:
        account.owner_name = ""
        assert False
    except ValueError:
        print("✅ Пустое имя владельца отклонено")
    
    print("✅ Обработка ошибок работает!")

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🏦 ЗАПУСК ТЕСТОВ BANK ACCOUNT SYSTEM")
    print("=" * 50)
    
    test_checking_account()
    test_savings_account()
    test_credit_account()
    test_transactions()
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 50)
