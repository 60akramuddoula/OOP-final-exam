from user import Customer, Admin
from bank import Bank


def main():
    bank = Bank("Babu Mamar Bank", 80000000000)
    habib = Customer("habib", "habib@gmail.com", "123 Street", "current")
    hanif = Customer("hanif", "hanif@gmail.com", "456 Avenue", "saving")
    asif = Customer("asif", "asif@gmail.com", "789 Boulevard", "current")
    bappi = Customer("bappi", "bappi@gmail.com", "1010 Lane", "saving")

    akramuddoula = Admin("akramuddoula", "akramuddoula@gmail.com", "1020 Street")

    habib.create_account(bank)
    hanif.create_account(bank)
    asif.create_account(bank)
    bappi.create_account(bank)
    akramuddoula.create_account(bank)

    while True:
        print("\n1. Deposit Money")
        print("2. Withdraw Money")
        print("3. View Balance")
        print("4. View Transaction History")
        print("5. Take Loan")
        print("6. Transfer Money")
        print("7. Delete User Account")
        print("8. View All Users")
        print("9. View total bank balance")
        print("10. View total bank loan")
        print("11. Switch Loan Feature")
        print("12. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            depo = int(input("Enter your amount: "))
            bappi.deposit(depo)
        elif choice == 2:
            wit = int(input("Enter your withdraw amount: "))
            bappi.withdraw(wit)
        elif choice == 3:
            bappi.view_balance()
        elif choice == 4:
            bappi.view_transection_history()
        elif choice == 5:
            lon = int(input("Enter your loan amount: "))
            bappi.taking_loan(lon)
        elif choice == 6:
            trn = int(input("Enter the amount to transfer: "))
            recipient_name = input("Enter recipient name: ")
            recipient = next(
                (user for user in bank.users if user.name == recipient_name), None
            )
            bappi.transfer_money(recipient, trn)
        elif choice == 7:
            akramuddoula.delete_account(asif.acnt_number)
        elif choice == 8:
            akramuddoula.view_users()
        elif choice == 9:
            akramuddoula.view_main_balance()
        elif choice == 10:
            akramuddoula.view_total_loan()
        elif choice == 11:
            permission = input("Turn loan feature ON/OFF (y/n): ")
            akramuddoula.switching_loan(permission.lower() == "y")
        elif choice == 12:
            break


if __name__ == "__main__":
    main()
