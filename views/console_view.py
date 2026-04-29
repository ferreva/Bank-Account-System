# views/console_view.py
from typing import List, Optional
from models.account import Account
from models.transaction import Transaction, TransactionType
from datetime import datetime

class ConsoleView:
    """Консольное представление."""
    
    @staticmethod
    def display_main_menu():
        """Отображает главное меню."""
        print("\n" + "=" * 60)
        print("🏦 BANK ACCOUNT SYSTEM")
        print("=" * 60)
        print("1. ➕ Открыть счет")
        print("2. 📋 Показать все счета")
        print("3. 💰 Пополнить счет")
        print("4. 💸 Снять со счета")
        print("5. 📤 Перевод между счетами")
        print("6. 📜 История транзакций")
        print("7. 🔍 Фильтрация транзакций")
        print("8. 📈 Начислить проценты (сберегательный)")
        print("9. ❌ Закрыть счет")
        print("0. 💾 Сохранить и выйти")
        print("=" * 60)
    
    @staticmethod
    def display_account_type_menu():
        """Меню выбора типа счета."""
        print("\n📁 Типы счетов:")
        print("1. Расчетный счет (с овердрафтом)")
        print("2. Сберегательный счет (с процентами)")
        print("3. Кредитный счет (с лимитом)")
    
    @staticmethod
    def display_accounts(accounts: List[Account], title: str = "Счета"):
        """Отображает список счетов."""
        if not accounts:
            print(f"\n📭 {title}: нет счетов")
            return
        
        print(f"\n📊 {title} ({len(accounts)} шт.):")
        print("-" * 70)
        for i, account in enumerate(accounts, 1):
            if account.get_account_type() == "Кредитный":
                from models.credit_account import CreditAccount
                print(f"{i}. {account} | Долг: {account.debt:.2f}₽ | Доступно: {account.available_credit:.2f}₽")
            else:
                print(f"{i}. {account}")
        print("-" * 70)
    
    @staticmethod
    def display_transactions(transactions: List[Transaction], title: str = "Транзакции"):
        """Отображает список транзакций."""
        if not transactions:
            print(f"\n📭 {title}: нет транзакций")
            return
        
        print(f"\n📜 {title}:")
        print("-" * 70)
        for i, transaction in enumerate(transactions, 1):
            print(f"{i}. {transaction}")
        print("-" * 70)
    
    @staticmethod
    def display_message(message: str, is_error: bool = False):
        """Отображает сообщение."""
        prefix = "❌" if is_error else "✅"
        print(f"{prefix} {message}")
    
    @staticmethod
    def get_input(prompt: str) -> str:
        """Получает ввод пользователя."""
        return input(prompt).strip()
    
    @staticmethod
    def get_number(prompt: str) -> Optional[float]:
        """Получает числовой ввод."""
        try:
            value = float(input(prompt))
            if value <= 0:
                ConsoleView.display_message("Сумма должна быть положительной", True)
                return None
            return value
        except ValueError:
            ConsoleView.display_message("Введите корректное число", True)
            return None
    
    @staticmethod
    def get_account_creation_details() -> Optional[dict]:
        """Запрашивает данные для открытия счета."""
        print("\n📝 Открытие нового счета:")
        
        owner = input("ФИО владельца: ").strip()
        if not owner:
            ConsoleView.display_message("Имя не может быть пустым", True)
            return None
        
        ConsoleView.display_account_type_menu()
        type_choice = input("Выберите тип счета (1-3): ").strip()
        
        account_type_map = {"1": "checking", "2": "savings", "3": "credit"}
        if type_choice not in account_type_map:
            ConsoleView.display_message("Неверный тип счета", True)
            return None
        
        return {
            "owner": owner,
            "type": account_type_map[type_choice]
        }
    
    @staticmethod
    def select_account(accounts: List[Account], action: str) -> Optional[int]:
        """Позволяет пользователю выбрать счет."""
        if not accounts:
            ConsoleView.display_message("Нет доступных счетов", True)
            return None
        
        ConsoleView.display_accounts(accounts, f"Выберите счет для {action}")
        try:
            choice = int(input(f"Введите номер (1-{len(accounts)}): "))
            if 1 <= choice <= len(accounts):
                return choice - 1
            else:
                ConsoleView.display_message("Неверный номер", True)
                return None
        except ValueError:
            ConsoleView.display_message("Введите число", True)
            return None
    
    @staticmethod
    def get_filter_criteria() -> Optional[dict]:
        """Запрашивает критерии фильтрации транзакций."""
        print("\n🔍 Фильтрация транзакций:")
        print("1. По диапазону дат")
        print("2. По типу операции")
        print("3. По дате и типу")
        
        choice = input("Выберите фильтр (1-3): ").strip()
        
        criteria = {}
        
        if choice in ["1", "3"]:
            try:
                start_date = input("Начальная дата (ГГГГ-ММ-ДД): ").strip()
                if start_date:
                    criteria["start_date"] = datetime.fromisoformat(start_date)
                
                end_date = input("Конечная дата (ГГГГ-ММ-ДД): ").strip()
                if end_date:
                    criteria["end_date"] = datetime.fromisoformat(end_date)
            except ValueError:
                ConsoleView.display_message("Неверный формат даты", True)
                return None
        
        if choice in ["2", "3"]:
            print("\nТипы операций:")
            print("1. Пополнение")
            print("2. Снятие")
            print("3. Перевод (отправка)")
            print("4. Перевод (получение)")
            print("5. Проценты")
            
            type_map = {
                "1": "deposit",
                "2": "withdraw", 
                "3": "transfer_send",
                "4": "transfer_receive",
                "5": "interest"
            }
            
            type_choice = input("Выберите тип (1-5): ").strip()
            if type_choice in type_map:
                from models.transaction import TransactionType
                criteria["transaction_type"] = TransactionType(type_map[type_choice])
        
        return criteria if criteria else None
