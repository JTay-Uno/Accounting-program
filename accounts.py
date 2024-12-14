import csv
import os
import re


class Account:
    DATA_FILE = 'data.csv'

    def __init__(self, lName, fName, pin):
        self.__account_lName = lName
        self.__account_fName = fName
        self.__account_pin = pin
        self.__account_balance = 0
        self.__total_accounts = 0
        self.__account_csv_line = {}
        self.__account_exist = self.customer_search(self.__account_lName, self.__account_fName, self.__account_pin)

    def customer_search(self, lName, fName, account_pin):
        print(self.__class__)
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, 'r') as csv_file:

                reader = csv.DictReader(csv_file)
                for row in reader:
                    if row['lName'] == "last_account":
                        self.__total_accounts = row['Customer_num']
                    if row['lName'] == lName and row['fName'] == fName:
                        if int(row['PIN']) == int(account_pin):

                            if re.search('SavingAccount', str(self.__class__)):
                                    if re.match('Savings:',row['Savings']):
                                        print(row['Savings'])
                                        print('in savings match')

                                        temp = row['Savings'].lstrip('Savings:')

                                        search_temp = re.findall('[0-9.]+', temp)
                                        if len(search_temp) == 2:
                                            self.__account_balance = float(search_temp[0])
                                            self.__deposit_count = int(search_temp[1])
                                        else:
                                            print("Error")

                                        print(self.__account_balance)
                                        print(self.__deposit_count)
                                        self.__account_csv_line = row
                                        return True
                                    else: return False
                            elif re.search('Account', str(self.__class__)):
                                if re.match('Checking:',row['Checking']):
                                    print(row['Checking'])
                                    self.__account_balance = round( float(row['Checking'].lstrip('Checking:').rstrip(',')), 2)
                                    print(self.__account_balance)
                                    self.__account_csv_line = row
                                    return True
                                else: return False
                        else:
                            return False
            return False
        else:
            print("System Error - Data does not exist")

    def validate(self):
        return self.__account_exist

    def write_data(self, old_val, new_val):
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

    def deposit(self, amount):
        if amount > 0:
            if self.write_data(f'Checking:{self.__account_balance}', f'Checking:{self.__account_balance+amount}'):
                self.__account_balance += amount
                self.__account_csv_line['Checking'] = f'Checking:{self.__account_balance+amount}'
                return True
            else:
                return False
        else:
            return False

    def withdraw(self, amount):
        if amount > self.__account_balance or amount <= 0:
            return False
        else:
            if self.write_data(f'Checking:{self.__account_balance}', f'Checking:{self.__account_balance+amount}'):
                self.__account_balance -= amount
                self.__account_csv_line['Checking'] = str(self.__account_balance)
                return True
            else:
                return False

    def set_balance(self, amount, account):
        self.__account_balance = amount
        self.__account_csv_line[account] = str(self.__account_balance)

    def get_balance(self):
        return self.__account_balance

    def get_name(self):
        return self.__account_fName + ' ' + self.__account_lName

    def __str__(self):
        return f"Checking account balance = ${self.get_balance():.2f}"


class SavingAccount(Account):
    MINIMUM = 100
    RATE = .02

    def __init__(self, lName, fName, pin):
        self.__deposit_count = 0
        super().__init__(lName, fName, pin)


    def apply_interest(self):
        temp = self.get_balance()
        new = temp * (1 + SavingAccount.RATE)
        if self.write_data(f'Savings:{temp}:{self.__deposit_count}',f'Savings:{new}:{self.__deposit_count}'):
            self.set_balance(temp, 'Savings')

    def deposit(self, amount):
        if amount > 0:
            temp = self.get_balance() + amount
            if self.write_data(f'Savings:{temp}:{self.__deposit_count}',f'Savings:{temp + amount}:{self.__deposit_count + 1}'):
                self.set_balance(temp, 'Savings')
                self.__deposit_count += 1
            if self.__deposit_count % 5 == 0:
                self.apply_interest()
            return True
        else:
            return False

    def withdraw(self, amount):
        temp = self.get_balance()
        if SavingAccount.MINIMUM > temp - amount:
            print(f'Savings:{temp}:{self.__deposit_count}', f'Savings:{temp - amount}:{self.__deposit_count+1}')
            if self.write_data(f'Savings:{temp}:{self.__deposit_count}', f'Savings:{temp - amount}:{self.__deposit_count+1}'):
                self.set_balance(temp-amount,'Savings')
                self.__deposit_count += 1
                return True
        else:
            return False

    def __str__(self):
        return f"Savings account balance = ${self.get_balance():.2f}"
