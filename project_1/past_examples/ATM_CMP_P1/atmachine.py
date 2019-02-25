import sys

#Model
#takes care of transactions involving atm, by manipulating bank_of_charles dictionary 
class Bank: 

  #initialize empty dictionary to which I will append accounts as they are created
  def __init__(self):
    self.bank_of_charles = {}

  def create_account(self,name, pin):
    if name in self.bank_of_charles.keys():
       return False
    account = Account(name, pin)
    self.bank_of_charles[name] = account
    return True
  
  def delete_account(self, name):
    del self.bank_of_charles[name]
  
  #identifies by name and pin number
  def authentification(self, name, pin):
    if name in self.bank_of_charles.keys():
      if pin == self.bank_of_charles[name].pin:
        return True
    return False
  
  def get_savings_balance(self, name):
      return self.bank_of_charles[name].savings_balance
  
  def get_checking_balance(self, name):
      return self.bank_of_charles[name].checking_balance
  
  def deposit_savings(self, name, amount):
    self.bank_of_charles[name].savings_balance += amount 
  
  def deposit_checking(self, name, amount):
    self.bank_of_charles[name].checking_balance += amount

  #will print warning mssge if overdrawn!
  def withdraw_savings(self, name, amount):
    if self.bank_of_charles[name].savings_balance < amount:
      print ('you have a negative balance')
      self.bank_of_charles[name].savings_balance -= amount
    else:
      self.bank_of_charles[name].savings_balance -= amount

  #will print warning mssge if overdrawn!
  def withdraw_checking(self, name, amount):
    if self.bank_of_charles[name].checking_balance < amount:
      print ('you have a negative balance')
      self.bank_of_charles[name].checking_balance -= amount
    else:
      self.bank_of_charles[name].checking_balance -= amount

#important for the creation of individual accounts which will have characteristics of username, pin, and account balances
class Account:
  def __init__(self, username, pin, checking_balance = 0, savings_balance = 0):
    self.username = username
    self.pin = pin
    self.checking_balance = checking_balance 
    self.savings_balance = savings_balance

#Controller
#will send desired transactions such as deposit and withdraw to the Bank class
class Atm:
  
  def __init__(self, bank):
    self.bank = bank
    self.name = None
    self.logged_in = False
    

  def make_account(self, name, pin):
    if not self.bank.create_account(name,pin):
      raise DuplicateAccountError
  
  #will show savings once user is logged in!
  def show_savings(self):
    if not self.logged_in:#<------------------------look at this to make sure how it works
      raise NotLoggedInError
    return bank.get_savings_balance(name)
  
  #will show checking balance once the user is logged in!
  def show_checking(self):
    if not self.logged_in:#<------------------------look at this to make sure how it works
      raise NotLoggedInError
    return bank.get_checking_balance(name)
  
  #only when you logged in can you delete the account. If not, must raise error!
  def erase_account(self):
    if self.logged_in:
      self.bank.delete_account(name)
    else:
      raise NotLoggedInError
      
  def login(self, name, pin):
    if not bank.authentification(name, pin):
      raise AuthenticationError
    else:
      self.logged_in = True
      self.name = name
    
  def deposit_savings(self, amount):
    if not self.logged_in:
      raise NotLoggedInError
    bank.deposit_savings(name, amount)
      
  def deposit_checking(self, amount):
    if not self.logged_in:
      raise NotLoggedInError
    bank.deposit_checking(name, amount)

  def withdraw_saving(self,amount):
    if not self.logged_in:
      raise NotLoggedInError
    bank.withdraw_savings(name, amount)

  def withdraw_checkin(self,amount):
    if not self.logged_in:
      raise NotLoggedInError
    bank.withdraw_checking(name, amount)
    
  def logout(self):
    self.logged_in = False
    self.name = None

#These classes handle different types of errors that might come from operating the atm machine   
class AuthenticationError(Exception):
  pass;

class DuplicateAccountError(Exception):
  pass;

class NotLoggedInError(Exception):
  pass;

class InsuffficientFundsError(Exception): #<---------------------------------------make sure to implement this for the withdraw function
  pass;

#secondary main prompt that gets initiated once the customer is logged in!
def central_window(atm): 
      closed = False
      while not closed:

        print("1-check balance\n")
        print("2-deposit\n")
        print("3-withdraw\n")
        print("4-logout\n")
        print("5-delete account\n")
        command = int(input("Choose one of the above actions to take\n"))
      
      # while not closed:
        
        if command == 1:
          answer = int(input("Would like to check the balance of your checking account(1) or savings account(2)?"))
          if answer == 1:
            print("Checking account balance: " + str(atm.show_checking()))

          elif answer == 2:
            print("Savings account balance:  " + str(atm.show_savings()))
          else: 
            print("You picked an invalid choice, try again!")
        
        elif command == 2:
          deposit_answer = int(input("How much would you like to deposit?"))
          which_account = int(input("To which account would you prefer the deposit? Savings(1) or Checking(2)? Choose one of the two numbers please\n"))
          if which_account == 1:
            atm.deposit_savings(deposit_answer)
            print("You have successfully deposited " + str(deposit_answer) + " dollars!")
          elif which_account == 2: 
            atm.deposit_checking(deposit_answer)
            print("You have successfully deposited" + str(deposit_answer) + " dollars!")
          else:
            print("You picked an invalid choice, try again!")

        elif command == 3:
          withdraw_answer = int(input("How much would you like to withdraw?"))
          wich_account = int(input("To which account would you prefer the withdrawal? Savings(1) or Checking(2)? Choose one of the two numbers please\n"))
          if wich_account == 1:
            atm.withdraw_saving(withdraw_answer)
            print("You have successfully withdrawn " + str(withdraw_answer) + " dollars from your savings account!\n")
          elif wich_account == 2:
            atm.withdraw_checkin(withdraw_answer)
            print("You have successfully withdrawn " + str(withdraw_answer) + " dollars from your checking account!\n")
          else:
            print("You picked an invalid choice, try again!")

        elif command == 4:
          print("It seems that you have chosen to cancel this transaction... See you again!")
          atm.logout()
          closed = True 

        elif command == 5:
          print("Deleting the entire account!")
          atm.erase_account()
          atm.logout()
          closed = True
          

#---------------------------------------------------------------------------------------------------------------------------->Everything below is prompt
if __name__ == "__main__":
  # Initialization
  bank = Bank()
  atm = Atm(bank)
  
  # Main Page -> Account page
  print("Welcome to the ATM machine!")
  while True:
    cmd = input("Please enter a command([l]ogin - Log in to your account, [c]reate - Create a new account, [q]uit - Close the application) or 'h' for help\n")
    if cmd == "h":
      print("[l]ogin - Log in to your account")
      print("[c]reate - Create a new account")
      print("[q]uit - Close the application")
    elif cmd == "login" or cmd == "l":
      #login
      name = input("Enter your name: ")
      pin = int(input("Enter your pin: "))
      try:
        atm.login(name, pin)
        print("")
        central_window(atm)
      except AuthenticationError as err:
        print("Incorrect account information!")      
  
    elif cmd == "create" or cmd == "c":
      name = input("Enter your name: ")
      pin = int(input("Enter your pin: "))
      try:
        atm.make_account(name, pin)
        print("")
      except DuplicateAccountError as err:
        print("There is already an account under that name!")  
      
    elif cmd == "quit" or cmd == "q":
      sys.exit()

