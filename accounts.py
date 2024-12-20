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
                            self.__account_csv_line = row

                            if re.search('SavingAccount', str(self.__class__)):
                                temp = row['Savings'].split(':')
                                self.__account_balance = float(temp[1])
                                self.__deposit_count = int(temp[2])
                                return True
                            elif re.search('Account', str(self.__class__)):
                                temp = row['Checking'].split(':')
                                self.__account_balance = float(temp[1])
                                print(f"Checking, bal: {self.__account_balance}")
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

    def write_data(self, key:str, new_val:str) -> bool:
        """
        Method updates the csv file
        :param key of value to be replaced
        :param new_val: new string
        :return: True if update was successful, False if not
        """

        temp = ','.join(self.__account_csv_line.values())
        self.__account_csv_line[key] = new_val
        new_temp = ','.join(self.__account_csv_line.values())
        print(temp)
        print(new_temp)

        try:
            with open('data.csv', 'r+') as file:
                data = file.read()
                if re.search(temp, data):
                    data = data.replace(temp, new_temp)
                else:
                    print("Write Data Error, No match")
                    return False
                file.seek(0)
                file.write(data)
        except:
            print("Write Data exception error")
            return False
        else:
            del data
            return True

    def deposit(self, amount:float ) -> bool:
        """
        Method that deposits amount in to Account
        :param amount: float amount to be deposited > 0
        :return: True for successful deposit, False if not
        """
        if amount > 0:
            if self.write_data('Checking', f'Checking:{self.__account_balance + amount:.02f}'):
                self.__account_balance += amount
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
            if self.write_data( 'Checking', f'Checking:{self.__account_balance - amount:.2f}'):
                self.__account_balance -= amount
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

    def set_deposit_count(self, count:int) -> None:
        """
        Method sets the deposit count
        :param count: int
        :return: None
        """
        self.__deposit_count = count

    def get_balance(self) -> float:
        """
        Method to get the account balance & deposit count
        :return: float account balance. int deposit count
        """
        return self.__account_balance

    def get_deposit_count(self) -> int:
        """
        Method returns deposit_count as an integer
        :return:
        """
        return self.__deposit_count

    def get_name(self) -> str:
        """
        Method returns account name
        :return:
        """
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
        super().__init__(lName, fName, pin)

    def apply_interest(self) -> None:
        """
        Method to apply interest to the savings account
        :return: None
        """
        temp = self.get_balance()
        temp2 = self.get_deposit_count()
        new = temp * (1 + SavingAccount.RATE)
        print("writing interest data")
        if self.write_data('Savings', f'Savings:{new:0.2f}:{temp2}'):
            self.set_balance(new, 'Savings')

    def deposit(self, amount:float) -> bool:
        """
        Method that handles deposits into a checking account, calls apply_interest after %5 deposits
        :param amount: float amount to deposit
        :return: True if successful, False if not
        """
        if amount > 0:
            temp = self.get_balance()
            temp2 = self.get_deposit_count()

            if self.write_data('Savings',f'Savings:{temp + amount:0.2f}:{temp2 + 1}'):
                self.set_balance(temp + amount, 'Savings')
                self.set_deposit_count(temp2+1)

            if (temp2+1) % 5 == 0:
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
        temp2 = self.get_deposit_count()

        if  temp-amount >= SavingAccount.MINIMUM:
            if self.write_data('Savings', f'Savings:{temp - amount:0.2f}:{temp2}'):
                self.set_balance(temp - amount, 'Savings')
                return True
        else:
            return False

    def __str__(self) -> str:
        """
        Method that returns a string when the class is printed
        :return: string
        """
        return f"Savings account balance = ${self.get_balance():.2f}"
