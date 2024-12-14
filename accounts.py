import csv
import os
import re


class Account:
    """
    Account Class that represents a checking account
    """
    DATA_FILE = 'data.csv'

    def __init__(self, lName:str, fName:str, pin:int) -> None:
        """
        Method that sets the default values for the checking account
        :param lName: string, Lastname
        :param fName: string, Firstname
        :param pin: int, pin
        """
        self.__account_lName = lName
        self.__account_fName = fName
        self.__account_pin = pin
        self.__account_balance = 0
        self.__total_accounts = 0
        self.__account_csv_line = {}
        self.__account_exist = self.customer_search(self.__account_lName, self.__account_fName, self.__account_pin)

    def customer_search(self, lName:str, fName:str, account_pin:int) -> bool:
        """
        This method searches the DATA_FILE given lastname, firstname, and pin
        if account is found, sets __acount_balance and sets __account_csv_line to the account entry
        Also sets, __deposit_count if called by SavingsAccount class

        :param lName: string, lastname
        :param fName: string, lastname
        :param account_pin: int pin
        :return: True if account is validated or False if it is not
        """
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, 'r') as csv_file:

                reader = csv.DictReader(csv_file)
                for row in reader:
                    if row['lName'] == "last_account":
                        self.__total_accounts = row['Customer_num']
                    if row['lName'] == lName and row['fName'] == fName:
                        if int(row['PIN']) == int(account_pin):

                            if re.search('SavingAccount', str(self.__class__)):
                                if re.match('Savings:', row['Savings']):

                                    temp = row['Savings'].lstrip('Savings:')
                                    search_temp = re.findall('[0-9.]+', temp)
                                    if len(search_temp) == 2:
                                        self.__account_balance = float(search_temp[0])
                                        self.__deposit_count = int(search_temp[1])
                                    else:
                                        print("Error")
                                    self.__account_csv_line = row
                                    return True
                                else:
                                    return False
                            elif re.search('Account', str(self.__class__)):
                                if re.match('Checking:', row['Checking']):
                                    self.__account_balance = round(
                                        float(row['Checking'].lstrip('Checking:').rstrip(',')), 2)
                                    print(self.__account_balance)
                                    self.__account_csv_line = row
                                    return True
                                else:
                                    return False
                        else:
                            return False
            return False
        else:
            print("System Error - Data does not exist")

    def validate(self):
        return self.__account_exist

    def write_data(self, old_val:str, new_val:str) -> bool:
        """
        Method updates the csv file
        :param old_val: old string to be replaced
        :param new_val: new string
        :return: True if update was successful, False if not
        """
        temp = ''
        for key, value in self.__account_csv_line.items():
            temp = temp + value + ','
        temp = temp.strip(',')
        new_temp = temp.replace(old_val, new_val)

        try:
            with open('data.csv', 'r+') as file:
                data = file.read()
                if re.search(temp, data):
                    data = data.replace(temp, new_temp)
                file.seek(0)
                file.write(data)
            del data
            return True
        except:
            return False

    def deposit(self, amount:float ) -> bool:
        """
        Method that deposits amount in to Account
        :param amount: float amount to be deposited > 0
        :return: True for successful deposit, False if not
        """
        if amount > 0:
            if self.write_data(f'Checking:{self.__account_balance}', f'Checking:{self.__account_balance + amount}'):
                self.__account_balance += amount
                self.__account_csv_line['Checking'] = f'Checking:{self.__account_balance + amount}'
                return True
            else:
                return False
        else:
            return False

    def withdraw(self, amount:float) -> bool:
        """
        Method to withdraw amount out of Account
        :param amount:
        :return: True if successful, False if not
        """
        if amount > self.__account_balance or amount <= 0:
            return False
        else:
            if self.write_data(f'Checking:{self.__account_balance}', f'Checking:{self.__account_balance + amount}'):
                self.__account_balance -= amount
                self.__account_csv_line['Checking'] = str(self.__account_balance)
                return True
            else:
                return False

    def set_balance(self, amount:float, account:str) -> None:
        """
        Method to set the balance of an account, used for SavingAccount class to access private variables
        :param amount: float value to set balance to
        :param account: string account type - either Checking or Savings to alter the correct values in the csv_line
        :return: None
        """
        self.__account_balance = amount
        self.__account_csv_line[account] = str(self.__account_balance)

    def get_balance(self) -> float:
        """
        Method to get the account balance
        :return: float account balance
        """
        return self.__account_balance

    def get_name(self):
        return self.__account_fName + ' ' + self.__account_lName

    def __str__(self):
        return f"Checking account balance = ${self.get_balance():.2f}"


class SavingAccount(Account):
    """
    Child Class of Account, representing a savings account
    """
    MINIMUM = 100
    RATE = .02

    def __init__(self, lName:str, fName:str, pin:int) -> None:
        """
        Method to set default values and verify account
        :param lName:
        :param fName:
        :param pin:
        """
        self.__deposit_count = 0
        super().__init__(lName, fName, pin)

    def apply_interest(self) -> None:
        """
        Method to apply interest to the savings account
        :return: None
        """
        temp = self.get_balance()
        new = temp * (1 + SavingAccount.RATE)
        if self.write_data(f'Savings:{temp}:{self.__deposit_count}', f'Savings:{new}:{self.__deposit_count}'):
            self.set_balance(temp, 'Savings')

    def deposit(self, amount:float) -> bool:
        """
        Method that handles deposits into a checking account
        :param amount: float amount to deposit
        :return: True if successful, False if not
        """
        if amount > 0:
            temp = self.get_balance() + amount
            print(self.__deposit_count)
            if self.write_data(f'Savings:{temp}:{self.__deposit_count}',
                               f'Savings:{temp + amount}:{self.__deposit_count + 1}'):
                self.set_balance(temp, 'Savings')
                self.__deposit_count += 1
            if self.__deposit_count % 5 == 0:
                self.apply_interest()
            return True
        else:
            return False

    def withdraw(self, amount:float) -> bool:
        """
        Method that withdraws amount from SavingAccount class
        :param amount: Amount to be withdrawn
        :return: True if successful, False if not
        """
        temp = self.get_balance()
        if SavingAccount.MINIMUM > temp - amount:
            print(f'Savings:{temp}:{self.__deposit_count}', f'Savings:{temp - amount}:{self.__deposit_count + 1}')
            if self.write_data(f'Savings:{temp}:{self.__deposit_count}',
                               f'Savings:{temp - amount}:{self.__deposit_count + 1}'):
                self.set_balance(temp - amount, 'Savings')
                self.__deposit_count += 1
                return True
        else:
            return False

    def __str__(self) -> str:
        """
        Method that returns a string when the class is printed
        :return: string
        """
        return f"Savings account balance = ${self.get_balance():.2f}"
