from abc import ABC, abstractmethod
import uuid


class User(ABC):
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address
        self.bank = None

    @abstractmethod
    def create_account(self, bank):
        raise NotImplementedError


class Customer(User):
    def __init__(self, name, email, address, acnt_type):
        super().__init__(name, email, address)
        self.acnt_type = acnt_type
        self.balance = 0
        self.acnt_number = str(uuid.uuid4())
        self.transection_history = []
        self.loan = 0
        self.loan_amount = 0

    def create_account(self, bank):
        self.bank = bank
        self.bank.users.append(self)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.bank.balance += amount
            print(f"Deposit successful. Current Balance: {self.balance}")
            self.transection_history.append(
                f"Deposit: {amount} | Current: {self.balance}"
            )
        else:
            print("Deposit failed")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded.")
        elif self.bank.check_bankrupt():
            print("Bank is bankrupt. Withdrawal not possible.")
        else:
            self.balance -= amount
            self.bank.balance -= amount
            print(f"{amount} successfully withdrawn. Current Balance: {self.balance}")
            self.transection_history.append(
                f"Withdraw: {amount} | Current: {self.balance}"
            )

    def view_balance(self):
        print(f"Your current balance is {self.balance}")

    def view_transection_history(self):
        print("******** Transaction History ********")
        for record in self.transection_history:
            print(record)
        print("************************************")

    def taking_loan(self, amount):
        if self.loan < 2:
            self.bank.receive_loan(amount, self)
        else:
            print("Oops, Loan limit exceeded.")

    def transfer_money(self, another, amount):
        if amount > self.balance:
            print("Transfer amount exceeded.")
        elif not another:
            print("Account does not exist.")
        else:
            self.balance -= amount
            another.receive_transfer_amount(amount)
            print(f"Transfer successful. Current Balance: {self.balance}")
            self.transection_history.append(
                f"Transferred: {amount} | Current: {self.balance}"
            )

    def receive_transfer_amount(self, amount):
        self.balance += amount
        self.bank.balance += amount
        self.transection_history.append(f"Received: {amount}")
        return f"Successfully received money. Current Balance: {self.balance}"


class Admin(User):
    def __init__(self, name, email, address):
        super().__init__(name, email, address)

    def create_account(self, bank):
        self.bank = bank
        self.bank.admins.append(self)

    def delete_account(self, account_no):
        user_to_delete = None
        for user in self.bank.users:
            if user.acnt_number == account_no:
                user_to_delete = user
                break
        if user_to_delete:
            self.bank.users.remove(user_to_delete)
            print(f"User account {account_no} deleted successfully.")
        else:
            print(f"User account {account_no} not found.")

    def view_users(self):
        for user in self.bank.users:
            print(
                f"Name: {user.name}\nEmail: {user.email}\nAddress: {user.address}\nBalance: {user.balance}\nAccount No: {user.acnt_number}\nLoan Amount: {user.loan_amount}\n"
            )
        print("----------------------------")

    def view_main_balance(self):
        print("Main balance is:", self.bank.balance)

    def view_total_loan(self):
        print("Total loan amount:", self.bank.loan_amount)

    def switching_loan(self, permission):
        self.bank.loan = permission
        print(f"Loan feature set to {'ON' if permission else 'OFF'}")


class Bank:
    def __init__(self, name, initial_amt):
        self.name = name
        self.balance = initial_amt
        self.loan_amount = 0
        self.users = []
        self.admins = []
        self.bankrupt = False
        self.loan = True

    def receive_loan(self, amount, user):
        if self.loan:
            if amount > self.balance:
                print("Sorry, Loan amount exceeded.")
            elif amount <= 0:
                print("Please provide a positive amount.")
            else:
                user.loan += 1
                user.loan_amount += amount
                user.balance += amount
                self.balance -= amount
                self.loan_amount += amount
                print(f"Successfully received loan. Updated Balance: {user.balance}")
                user.transection_history.append(
                    f"LOAN: {amount} CURRENT: {user.balance}"
                )
        else:
            print("Loan feature is currently turned off.")

    def check_bankrupt(self):
        return self.balance <= 0


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
