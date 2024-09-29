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
