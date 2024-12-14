
from PyQt6.QtWidgets import *
from gui import *
from accounts import *
import csv
import os
import re

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__account = None
        self.__savings = None
        self.submit_pushButton.clicked.connect(lambda : self.submit())
        self.enter_pushButton.clicked.connect(lambda : self.enter())
        self.exit_pushButton.clicked.connect(self.close)
        self.account_frame.hide()
        self.checking_Radio.hide()
        self.savings_Radio.hide()

    def submit(self):
        try:
            fname = self.fname_Entry.text().strip()
            lname = self.lname_Entry.text().strip()
            if len(fname) < 1 or len(lname) < 1: raise NameError
            pin = self.pin_Entry.text()
            if len(pin) != 5: raise ValueError
            pin = int(pin)
        except ValueError:
            self.prompt_label.setText("Enter a five digit numeric PIN")
        except NameError:
            self.prompt_label.setText("Enter at least one character for first and last name.")
        else:
            self.__account = Account(lname, fname, pin)
            self.__savings = SavingAccount(lname, fname, pin)

            if self.__account.validate() or self.__savings.validate():
                self.prompt_label.setText(f"Welcome {fname} {lname}!")
                self.account_frame.show()
                self.submit_pushButton.setEnabled(False)
            else:
                self.prompt_label.setText(f"The account credentials are not valid. Try again.")
                self.fname_Entry.clear()
                self.lname_Entry.clear()
                self.fname_Entry.setFocus()
                self.pin_Entry.clear()

            if self.__account.validate() and self.__savings.validate(): #editing/showing/checking savings_Radio/checking_Radio where appropriate
                self.savings_Radio.setText(f'{self.__savings}')
                self.savings_Radio.show()
                self.checking_Radio.setText(f'{self.__account}')
                self.checking_Radio.show()
            elif self.__savings.validate():
                self.savings_Radio.setText(f'{self.__savings}')
                self.savings_Radio.show()
                self.savings_Radio.setChecked(True)
            elif self.__account.validate():
                self.checking_Radio.setText(f'{self.__account}')
                self.checking_Radio.show()
                self.checking_Radio.setChecked(True)

    def enter(self):

        try:
            amount = float(self.amount_Entry.text())
            if amount <= 0: raise ValueError
        except ValueError:
            self.output_text_Label.setText("Please enter a valid amount up to two decimal places.")
            self.amount_Entry.clear()
            self.amount_Entry.setFocus()
        else:
            if self.action_buttonGroup.checkedButton() == None:
                self.output_text_Label.setText("Please select Withdraw or Deposit.")
                return
            if self.account_buttonGroup.checkedButton() == None:
                self.output_text_Label.setText("Please select an account.")
                return

            states = self.account_buttonGroup.checkedId()   # = -2 for Checking, = -3 for Savings
            match self.action_buttonGroup.checkedButton().text(), states:
                case 'Deposit', -2:
                    print("deposit - checking")
                    if self.__account.deposit(amount):
                        self.checking_Radio.setText(f'{self.__account}')
                        self.output_text_Label.setText(f'Successfully deposited ${amount:.2f} into checking account.')
                case 'Deposit', -3:
                    print("deposit - savings")
                    if self.__savings.deposit(amount):
                        self.savings_Radio.setText(f'{self.__savings}')
                        self.output_text_Label.setText(f'Successfully deposited ${amount:.2f} into savings account.')
                case 'Withdraw', -2:            # withdraw - checking
                    if self.__account.withdraw(amount):
                        self.checking_Radio.setText(f'{self.__account}')
                        self.output_text_Label.setText(f'Successfully withdrew ${amount:.2f} out of checking account.')
                case 'Withdraw', -3:            # withdraw - savings
                    if self.__savings.withdraw(amount):
                            print("withdraw savings")
                            self.savings_Radio.setText(f'{self.__savings}')
                            self.output_text_Label.setText(f'Successfully withdrew ${amount:.2f} out of savings account.')
                    else:
                        self.output_text_Label.setText("Please enter a value that will maintain a minimum balance of $100")
                        self.amount_Entry.clear()
                        self.amount_Entry.setFocus()
                case _:
                    self.output_text_Label.setText(f'Error - action was not completed')
