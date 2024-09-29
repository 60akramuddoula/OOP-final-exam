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
