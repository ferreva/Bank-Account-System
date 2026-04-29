# main.py
from utils.storage import BankStorage
from controllers.bank_controller import BankController
from views.console_view import ConsoleView
from datetime import datetime

def main():
    storage = BankStorage("bank_data.json")
    controller = BankController(storage)
    view = ConsoleView()
    
    while True:
        view.display_main_menu()
        choice = view.get_input("Выберите действие (0-9): ")
        
        if choice == "1":  # Открыть счет
            details = view.get_account_creation_details()
            if details:
                account = controller.create_account(details["owner"], details["type"])
                if account:
                    view.display_message(f"Счет открыт! ID: {account.account_id}")
        
        elif choice == "2":  # Показать все счета
            accounts = controller.get_all_accounts()
            view.display_accounts(accounts, "Все счета")
        
        elif choice == "3":  # Пополнить счет
            accounts = controller.get_all_accounts()
            index = view.select_account(accounts, "пополнения")
            if index is not None:
                amount = view.get_number("Введите сумму пополнения: ")
                if amount:
                    if controller.deposit(index, amount):
                        view.display_message("Счет пополнен!")
        
        elif choice == "4":  # Снять со счета
            accounts = controller.get_all_accounts()
            index = view.select_account(accounts, "снятия")
            if index is not None:
                amount = view.get_number("Введите сумму снятия: ")
                if amount:
                    if controller.withdraw(index, amount):
                        view.display_message("Средства сняты!")
        
        elif choice == "5":  # Перевод между счетами
            accounts = controller.get_all_accounts()
            if len(accounts) < 2:
                view.display_message("Нужно минимум 2 счета для перевода", True)
                continue
            
            from_index = view.select_account(accounts, "перевода (ОТКУДА)")
            if from_index is not None:
                to_index = view.select_account(accounts, "перевода (КУДА)")
                if to_index is not None and from_index != to_index:
                    amount = view.get_number("Введите сумму перевода: ")
                    if amount:
                        if controller.transfer(from_index, to_index, amount):
                            view.display_message("Перевод выполнен!")
        
        elif choice == "6":  # История транзакций
            accounts = controller.get_all_accounts()
            if not accounts:
                view.display_message("Нет счетов", True)
                continue
            
            print("\n1. История всех транзакций")
            print("2. История конкретного счета")
            sub_choice = view.get_input("Выберите (1-2): ")
            
            if sub_choice == "1":
                transactions = controller.get_transactions()
                view.display_transactions(transactions, "Все транзакции")
            elif sub_choice == "2":
                index = view.select_account(accounts, "просмотра истории")
                if index is not None:
                    transactions = controller.get_transactions(account_index=index)
                    account = controller.get_account_by_index(index)
                    view.display_transactions(transactions, f"История счета {account.account_id}")
        
        elif choice == "7":  # Фильтрация транзакций
            criteria = view.get_filter_criteria()
            if criteria:
                transactions = controller.get_transactions(**criteria)
                view.display_transactions(transactions, "Отфильтрованные транзакции")
        
        elif choice == "8":  # Начислить проценты
            count = controller.add_interest_to_savings()
            if count > 0:
                view.display_message(f"Проценты начислены на {count} сберегательных счетов")
            else:
                view.display_message("Нет сберегательных счетов для начисления процентов")
        
        elif choice == "9":  # Закрыть счет
            accounts = controller.get_all_accounts()
            index = view.select_account(accounts, "закрытия")
            if index is not None:
                if controller.delete_account(index):
                    view.display_message("Счет закрыт")
        
        elif choice == "0":  # Выход
            view.display_message("До свидания! 👋")
            break
        
        else:
            view.display_message("Неверный выбор! Попробуйте снова.", True)

if __name__ == "__main__":
    print("\n🏦 Добро пожаловать в Bank Account System!")
    print("📱 Управляйте счетами, переводами и отслеживайте транзакции.\n")
    main()
