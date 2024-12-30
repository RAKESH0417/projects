import hashlib  
import os  
from datetime import datetime  

class BankingSystem:  
    accounts_file = "accounts.txt"  
    transactions_file = "transactions.txt"  

    def __init__(self):  
        self.accounts = {}  
        self.load_accounts()  

    def load_accounts(self):  
        if os.path.exists(self.accounts_file):  
            with open(self.accounts_file, "r") as file:  
                for line in file:  
                    account_number, name, password, balance = line.strip().split(",")  
                    self.accounts[account_number] = {  
                        'name': name,  
                        'password': password,  
                        'balance': float(balance)  
                    }  

    def save_accounts(self):  
        with open(self.accounts_file, "w") as file:  
            for account_number, details in self.accounts.items():  
                file.write(f"{account_number},{details['name']},{details['password']},{details['balance']}\n")  

    def create_account(self, name, initial_deposit, password):  
        account_number = str(len(self.accounts) + 123456)  
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  
        self.accounts[account_number] = {  
            'name': name,  
            'password': hashed_password,  
            'balance': initial_deposit  
        }  
        self.save_accounts()  
        print(f"Your account number: {account_number}")  
        
    def login(self, account_number, password):  
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  
        if account_number in self.accounts and self.accounts[account_number]['password'] == hashed_password:  
            return True  
        return False  

    def deposit(self, account_number, amount):  
        self.accounts[account_number]['balance'] += amount  
        self.log_transaction(account_number, "Deposit", amount)  
        self.save_accounts()  
        print(f"Deposit successful! Current balance: {self.accounts[account_number]['balance']}")  

    def withdraw(self, account_number, amount):  
        if amount <= self.accounts[account_number]['balance']:  
            self.accounts[account_number]['balance'] -= amount  
            self.log_transaction(account_number, "Withdrawal", amount)  
            self.save_accounts()  
            print(f"Withdrawal successful! Current balance: {self.accounts[account_number]['balance']}")  
        else:  
            print("Insufficient funds.")  

    def log_transaction(self, account_number, transaction_type, amount):  
        date = datetime.now().strftime("%Y-%m-%d")  
        with open(self.transactions_file, "a") as file:  
            file.write(f"{account_number},{transaction_type},{amount},{date}\n")  

    def menu(self):  
        while True:  
            print("\nWelcome to the Banking System!")  
            print("1. Create Account")  
            print("2. Login")  
            print("3. Exit")  
            choice = input("Enter your choice: ")  
            
            if choice == "1":  
                name = input("Enter your name: ")  
                initial_deposit = float(input("Enter your initial deposit: "))  
                password = input("Enter a password: ")  
                self.create_account(name, initial_deposit, password)  
            elif choice == "2":  
                account_number = input("Enter your account number: ")  
                password = input("Enter your password: ")  
                if self.login(account_number, password):  
                    print("Login successful!")  
                    while True:  
                        print("1. Deposit")  
                        print("2. Withdraw")  
                        print("3. Logout")  
                        action = input("Choose an action: ")  
                        if action == "1":  
                            amount = float(input("Enter amount to deposit: "))  
                            self.deposit(account_number, amount)  
                        elif action == "2":  
                            amount = float(input("Enter amount to withdraw: "))  
                            self.withdraw(account_number, amount)  
                        elif action == "3":  
                            print("Logged out.")  
                            break  
                else:  
                    print("Invalid login. Please try again.")  
            elif choice == "3":  
                print("Goodbye!")  
                break  

if __name__ == "__main__":  
    banking_system = BankingSystem()  
    banking_system.menu()
