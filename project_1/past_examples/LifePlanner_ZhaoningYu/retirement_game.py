from random import choice, normalvariate
from copy import deepcopy
from sys import exit
from math import floor
import time

## Defining of classes and functions #############################################################################
class Person:
    def __init__(self, name):
        self._name = name
        self._age = 20
        self._skill = 0
        self._health = 200
        self._work_time = 8
        self._study_time = 2
        self._spending = 10000
        self._wage = 12.5         # wage/hr x 8 hr/day x 200 days ~ $20000/yr

    def getName(self):
        return self._name

    def getAge(self):
        return self._age

    def getSkill(self):
        return self._skill

    def getHealth(self):
        return self._health

    def getWorkTime(self):
        return self._work_time

    def getStudyTime(self):
        return self._study_time

    def getSpending(self):
        return self._spending

    def getIncome(self):
        return self._wage * (1 + self._skill/50)* self._work_time * 200

    def grow(self):
        self._age += 1
        self._health += min((-1, 8- self._work_time - self._study_time)) + (self._spending - 15000)/20000
        self._skill += self._study_time

    def __str__(self):
        return "NAME:   {} \nage:    {:.0f} \nhealth: {:.0f} \nskill:  {:.0f} \nwork:   {:.0f} hrs/day \nstudy:  {:.0f} hrs/day \npersonal spending: $ {:,.2f}/yr \n"\
            .format(self._name, self._age, self._health, self._skill, self._work_time, self._study_time, self._spending)


class Account:
    def __init__(self, initial_amount = 0.0, yield_pct = 0.0):
        self._balance = initial_amount
        self._yield = yield_pct

    def getBalance(self):
        return self._balance

    def addToBalance(self,amount):
        self._balance += amount

    def subtractFromBalance(self, amount):
        self._balance -= amount

    def grow(self):
        self._balance += self._balance * self._yield

    def __str__(self):
        return 'cash:   $ {:,.2f}'.format(self._balance)


class BondAccount(Account):
    def __init__(self, initial_amount, yield_pct):
        super().__init__(initial_amount, yield_pct)

    def __str__(self):
        return 'bonds:  $ {:,.2f}'.format(self._balance)


class StockAccount(Account):
    def __init__(self, initial_amount):
        super().__init__(initial_amount)

    def grow(self):
        self._balance += self._balance * normalvariate(0.08, 0.17)  # simulate stock returns to save code

    def __str__(self):
        return 'stocks: $ {:,.2f}'.format(self._balance)


class House:
    def __init__(self, name):
        self._name = name
        self._age = 0
        self._type = 'shed'
        self._equity = 0.0
        self._price = 100000

    def getName(self):
        return self._name

    def getAge(self):
        return self._age

    def getType(self):
        return self._type

    def getEquity(self):
        return self._equity

    def getExpense(self):
        if self._age < 20:
            return self._price/10
        else:
            return -self._price/50

    def grow(self):
        self._age += 1
        if self._age < 21:
            self._equity += self._price/20
        else:
            self._equity += self._price/100

    def __str__(self):
        return "'{}'({}) age: {} cost: ${:,.2f}/yr equity: ${:,.2f}".format(self._name, self._type, self._age, self.getExpense(), self.getEquity())

    def __repr__(self):
        return "({}) age: {} cost: ${:,.2f}/yr equity: ${:,.2f}".format(self._type, self._age, self.getExpense(), self.getEquity())

class cottageHouse(House):
    def __init__(self, name):
        super().__init__(name)
        self._type = 'cottage'
        self._price = 200000

class mansionHouse(House):
    def __init__(self, name):
        super().__init__(name)
        self._type = 'mansion'
        self._price = 500000

class Kid:
    def __init__(self, name):
        self._name = name
        self._age = 0
        self._breed = 'FreeRange'
        self._cost = 10000.00

    def getName(self):
        return self._name

    def getAge(self):
        return self._age

    def getBreed(self):
        return self._breed

    def getExpense(self):
        if self._age < 17:
            return self._cost
        elif self._age < 21:
            return self._cost * 3
        else:
            return -self._cost/2

    def grow(self):
        self._age += 1

    def __str__(self):
        return "name: {} ({}) age: {} cost: ${:,.2f}/yr".format(self.getName(), self.getBreed(), self.getAge(), self.getExpense())

    def __repr__(self):
        return "({}) age: {} cost: ${:,.2f}/yr".format(self.getBreed(), self.getAge(), self.getExpense())

class fancyKid(Kid):
    def __init__(self,name):
        super().__init__(name)
        self._breed = 'Attentive'
        self._cost = 20000.00

class Node():
    def __init__(self, person, cash, bonds, stocks, houses, kids, step_size=1):
        self._person = deepcopy(person)  # need deepcopy(), otherwise all nodes change if piggy changes
        self._cash = deepcopy(cash)
        self._bonds = deepcopy(bonds)
        self._stocks = deepcopy(stocks)
        self._houses = deepcopy(houses)
        self._kids = deepcopy(kids)
        self._step_size = step_size

    def getNodeData(self):
        return self._person, self._cash, self._bonds, self._stocks, self._houses, self._kids, self._step_size

    def getStepSize(self):
        return self._step_size

    def setStepSize(self):
        try:
            step_size = round(float(input("Please enter the step size: ")))   # in case user input a float
            if step_size > 0:
                self._step_size = step_size
                print("You have decided to check you finance in every {} years.".format(step_size))
            else:
                print("Invalid entry.")
        except:
            print("Invalid entry, step size unchanged.")

    def getExpense(self):
        expense =  self._person.getSpending()
        if len(self._houses)>0:
            expense += sum([house.getExpense() for house in self._houses.values()])
        if len(self._kids)>0:
            expense += sum([kid.getExpense() for kid in self._kids.values()])
        return expense

    def getCash(self):
        return self._cash.getBalance() + self._person.getIncome()

    def getAssets(self):
        assets = self._cash.getBalance()\
                 + self._bonds.getBalance()\
                 + self._stocks.getBalance()\
                 + sum([house.getEquity() for house in self._houses.values()])
        return assets

    def buyBonds(self):
        print("You have cash: ${:,.2f} bonds: ${:,.2f}".format(self._cash.getBalance(), self._bonds.getBalance()))
        try:
            amount = floor(float((input("How much bonds would you like to buy? "))))
            while amount > self._cash.getBalance():
                amount = floor(float(input("You do not have that much cash, please re-enter the amount: ")))
        except:
            print("Invalid entry. No bonds bought.")
            amount = 0

        self._cash.subtractFromBalance(amount)
        self._bonds.addToBalance(amount)
        print("Now you have cash: ${:,.2f} bonds: ${:,.2f}".format(self._cash.getBalance(), self._bonds.getBalance()))

    def sellBonds(self):
        print("You have bonds: ${:,.2f} cash: ${:,.2f}".format(self._bonds.getBalance(), self._cash.getBalance()))
        try:
            amount = floor(float((input("How much bonds would you like to sell? "))))
            while amount > self._bonds.getBalance():
                amount = floor(float((input("You do not have that much bonds to sell, please re-enter the amount: "))))
        except:
            print("Invalid entry. No bonds sold.")
            amount = 0

        self._bonds.subtractFromBalance(amount)
        self._cash.addToBalance(amount)
        print("Now you have bonds: ${:,.2f} cash: ${:,.2f}".format(self._bonds.getBalance(), self._cash.getBalance()))

    def buyStocks(self):
        print("You have cash: ${:,.2f} stocks: ${:,.2f}".format(self._cash.getBalance(), self._stocks.getBalance()))
        try:
            amount = floor(float(input("How much stocks would you like to buy? ")))
            while amount > self._cash.getBalance():
                amount = floor(float(input("You do not have that much cash, please re-enter the amount: ")))
        except:
            print("Invalid entry. No stocks bought.")
            amount = 0

        self._cash.subtractFromBalance(amount)
        self._stocks.addToBalance(amount)
        print("Now you have cash: ${:,.2f} stocks: ${:,.2f}".format(self._cash.getBalance(), self._stocks.getBalance()))

    def sellStocks(self):
        print("You have stocks: ${:,.2f} cash: ${:,.2f}".format(self._stocks.getBalance(), self._cash.getBalance()))
        try:
            amount = floor(float(input("How much stocks would you like to sell? ")))
            while amount > self._stocks.getBalance():
                amount = floor(float(input("You do not have that much stocks to sell, please re-enter the amount: ")))
        except:
            print("Invalid entry. No stocks sold.")
            amount = 0

        self._stocks.subtractFromBalance(amount)
        self._cash.addToBalance(amount)
        print("Now you have stocks: ${:,.2f} cash: ${:,.2f}".format(self._stocks.getBalance(), self._cash.getBalance()))

    def buyHouse(self):
        print('\nYou will pay off the house over 20 years, you have 3 choices: ')
        print("'shed':    $10,000/yr\n'cottage': $20,000/yr \n'mansion': $50,000/yr")
        house_key = input("What kind of house do you want to buy ('[s]hed', '[c]ottage', or '[m]ansion')? ").lower()

        if house_key in ['s','c','m']:
            if (house_key == 's' and self._cash.getBalance() < 10000) \
                    or(house_key == 'c' and self._cash.getBalance() < 20000)\
                    or (house_key == 'm' and self._cash.getBalance() < 50000):
                print('You do not have enough cash to buy this house.')
            else:
                house_name = input('How do you name this house? ')
                while house_name in self._houses.keys():
                    house_name = input("You already have a house with that name, please enter another name: ")
                if house_key =='s':
                    house = House(house_name)
                elif house_key == 'c':
                    house = cottageHouse(house_name)
                else:
                    house = mansionHouse(house_name)
                self._houses.update({house_name:house})
                print("Now you have:\n", self._houses)
        else:
            print("Invalid entry. No house bought.")

    def sellHouse(self):
        try:
            if self._houses == {}:
                print("You have no houses to sell.")
            else:
                print("You have following houses: ")
                for house in self._houses.values():
                    print(house)
                house_name = input("Which house do you want to sell? ")
                self._cash.addToBalance(self._houses[house_name].getEquity())
                del self._houses[house_name]
                print("Now you have:\n", self._houses)
        except:
            print("Invalid entry. No house sold.")

    def raiseKid(self):
        print("The kid needs your support until he/she reaches the age 20. \nThere are two ways to raise a kid:")
        print("'FreeRange': $10,000/yr (age: 0-16)  $30,000/yr (age: 17-20)")
        print("'Attentive': $20,000/yr (age: 0-16)  $60,000/yr (age: 17-20)")
        kid_breed = input("How would you like to raise this kid ('[f]reeRange' or '[a]ttentive')? ").lower()
        if (kid_breed == 'f' and self._cash.getBalance() < 10000 ) or (kid_breed == 'a' and self._cash.getBalance() < 20000):
            print("You do not have enough money to raise this kid.")
        elif kid_breed not in ['f','a']:
            print("The entry is invalid.")
        else:
            kid_name = input("How would you like to name this kid? ")
            while kid_name in self._kids.keys():
                kid_name = input("You already have a kid with that name, please choose another name: ")

            if kid_breed == 'f':
                kid = Kid(kid_name)
            else:
                kid = fancyKid(kid_name)

            self._kids.update({kid_name:kid})
            print("Now you have kids:")
            print(self._kids)

    def setWorkTime(self):
        try:
            print("Currently you work {} hrs and study {} hrs per day and you have total 12 hours per day for work and study.".format(self._person.getWorkTime(), self._person.getStudyTime()))
            work_hours = round(float(input("How many hours would you like work per day? ")))
            if work_hours < 0:
                print("You working hours cannot be negative.")
            elif work_hours + self._person.getStudyTime() > 12:
                print("You cannot work and study for more than 12 hours per day.")
            else:
                self._person._work_time = work_hours
                print("Now you will work {} hours and study {} hours per day.".format(self._person._work_time, self._person._study_time))
        except:
            print("Invalid entry. No change in work time.")

    def setStudyTime(self):
        try:
            print("Currently you work {} hrs and study {} hrs per day and you have total 12 hours per day for work and study.".format(self._person.getWorkTime(), self._person.getStudyTime()))
            study_hours = round(float(input("How many hours would you like study per day? ")))
            if study_hours < 0:
                print("You study hours cannot be negative.")
            elif study_hours + self._person.getWorkTime() > 12:
                print("You cannot work and study for more than 12 hours per day.")
            else:
                self._person._study_time = study_hours
                print("Now you will work {} hours and study {} hours per day.".format(self._person._work_time, self._person._study_time))
        except:
            print("Invalid entry. No change in study time.")

    def setSpending(self):
        try:
            print("Currently you have ${:,.2f} in cash and you will earn ${:,.2f} this year".format(self._cash.getBalance(), self._person.getIncome()))
            print("Currently you are spending ${:,.2f}/yr on yourself. You need to spend at least $10,000/yr for basic needs.".format(self._person.getSpending()))
            spend_amount = round(float(input("How much per year would you like to spend on yourself for basic needs, fun, and pleasure? ")))

            if spend_amount < 10000:
                print("You need to spend at least $10,000/yr on yourself for basic needs.")
            elif spend_amount + self.getExpense() - self._person.getSpending() > self.getCash():
                print("You do not have that much money to spend on your self.")
            else:
                self._person._spending = spend_amount
                print("Now you will spend ${:,.2f}/yr on yourself.".format(self._person._spending))
        except:
            print("Invalid entry. No change in spending.")

    def buyLottery(self):
        try:
            print('You have ${:,.2f} in cash.'.format(self._cash.getBalance()))
            amount = floor(float(input("How much lottery would you like to buy? ")))
            while amount > self._cash.getBalance():
                amount = int(input("You do not have that much cash, please re-enter the amount: "))

            chances = [0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
            self._cash.subtractFromBalance(amount)
            jackpot = amount * choice(chances)

            if jackpot == 0:
                print("Sorry, you have won nothing, now you have cash: ${:,.2f} ".format(self._cash.getBalance()))
            else:
                print("You have won ${:,.2f}!".format(jackpot))
                self._cash.addToBalance(jackpot)
                print("Now you have cash: ${:,.2f}".format(self._cash.getBalance()))
        except:
            print("Invalid entry. No lottery bought.")

    def checkBankrupcy(self):
        if self.getAssets() + self._person.getIncome() < self.getExpense():
            return True
        else:
            return False

    def checkCashFlow(self):
        if self.getExpense() < self.getCash():
            return True
        else:
            return False

    def printMainMenu(self):
        print("\nQ: quit")
        print("H: 'help'")
        print("S: sell bonds, stocks, houses")
        print("B: buy bonds, stocks, houses, or lottery")
        print("E: expenses - how much to spend on yourself for fun and pleasure ")
        print("R: raise kids")
        print("T: how much time per day to allocate for work or study")
        print("Z: set 'step size' - how many years to run each time without checking finance")
        print("P: print current finance status")
        print("G: show data graphics")
        print("Enter: run\n")

    def getAction(self):
        action = input("\nWhat would you like to do? ('h' for help, 'enter' to run) ").upper()

        while action not in ["H", "S", "B", "E", "R", "T", "Z", "P", "G", "Q"]:
            if len(action) < 1:    # allows the user to use enter to exit
                break
            else:
                action = input("\nInvalid entry, please re-enter would you like to do? ").upper()

        if action == "S":      # "S" "B" "T" require a second entry:
            item = " "         # a space here so the loop can use 'return" to exit
            while item not in ["B", "S", "H"]:
                if len(item)<1:
                    break
                else:
                    item = input("\nWhat would you like to sell? [B]onds, [S]tocks, [H]ouse ").upper()
            action += item
        elif action == "B":
            item = " "
            while item not in ["B", "S", "H", "L"]:
                if len(item)<1:
                    break
                else:
                    item = input("\nWhat would you like to buy? [B]onds, [S]tocks, [H]ouse, [L]ottery ").upper()
            action += item
        elif action == "T":
            item = " "
            while item not in ["W","S"]:
                if len(item)<1:
                    break
                else:
                    item = input("\nWould you like change how much time you [W]ork or [S]tudy? ").upper()
            action += item

        return action

    def executeAction(self, action):
        if action == "Q":
            print("Thank you for playing, exiting the game.")
            exit(1)
        elif action == "H":
            self.printMainMenu()
        elif action == "E":
            self.setSpending()
        elif action == "BB":
            self.buyBonds()
        elif action == "SB":
            self.sellBonds()
        elif action == "BS":
            self.buyStocks()
        elif action == "SS":
            self.sellStocks()
        elif action == "BH":
            self.buyHouse()
        elif action == "SH":
            self.sellHouse()
        elif action == "BL":
            self.buyLottery()
        elif action == "R":
            self.raiseKid()
        elif action == "TW":
            self.setWorkTime()
        elif action == "TS":
            self.setStudyTime()
        elif action == "Z":
            self.setStepSize()
        elif action == "P":
            self.printNode()
        elif len(action) < 1 or action in ["B","S","T"]:     # Enter to continue
            pass

    def printNode(self):
        print(self._person)
        print("FINANCE:")
        print(self._cash)
        print(self._bonds)
        print(self._stocks)
        print('houses:', self._houses)
        print('kids:  ',self._kids)
        print("income:  $ {:,.2f}/yr".format(self._person.getIncome()))
        print("expense: $ {:,.2f}/yr".format(self.getExpense()))

    def grow(self):
        self._person.grow()
        self._cash.addToBalance(self._person.getIncome())
        self._cash.subtractFromBalance(self.getExpense())
        self._cash.grow()
        self._bonds.grow()
        self._stocks.grow()
        for house in self._houses.values():
            house.grow()
        for kid in self._kids.values():
            kid.grow()


class NodeChain:
    def __init__(self,start_node):
        self._chain = [start_node]

    def getChain(self):
        return self._chain

    def addNode(self, new_node):
        self._chain.append(new_node)

    def evaluate(self):
        finish_node = self._chain[-1]
        retire_income = finish_node.getAssets()*0.025
        retire_expense = finish_node.getExpense() + max(200 - finish_node._person.getHealth(),0) * 200
        print('You have reached age 65, you have accumulated ${:,.2f} in total assets:'.format(finish_node.getAssets()))
        finish_node.printNode()

        if retire_income > retire_expense*2:
            print('Your estimated income of ${:,.2f}/yr for retirement is much higher than expenses: ${:,.2f}/yr.'.format(retire_income,retire_expense))
            print('\nEXCELLENT JOB! {}! You can start to enjoy your life in retirement now.'.format(finish_node._person.getName().upper()))
        elif retire_income >= retire_expense:
            print('Your estimated income of ${:,.2f}/yr for retirement can cover your expenses: ${:,.2f}/yr.'.format(retire_income,retire_expense))
            print('\nCONGRATULATIONS! {}! You can retire now if you manage your finance wisely.'.format(finish_node._person.getName().upper()))
        else:
            print('Your estimated income of ${:,.2f}/yr for retirement cannot cover your expenses: ${:,.2f}/yr.'.format(retire_income,retire_expense))
            print('\nSorry, {}, but you CANNOT retire, you have to keep working after 65.'.format(finish_node._person.getName().upper()))

    def displayMenu(self):
        print("\nGRAPHICS MENU: \nhea[L]th \ns[K]ill \n[T]ime spent on work and study \n[I]ncome \n[C]ash \n[B]onds \n[S]tocks \n[A]ssets \n[E]xpenses \nhome equit[Y]")

    def drawGraph(self, Y, Y_title, symbol = ".", x_scale = 1, y_scale = 15):
        map = []
        for i in range(y_scale):
            map.append([" "] * 46 * x_scale)

        if max(Y)==0:
            y_max = y_scale
        else:
            y_max = max(Y)

        y_min = 0
        y_range = y_max - y_min

        for i in range(len(Y)):
            if round(Y[i]) <= 0:
                pass  # this case will show nothing
            else:
                j = int((y_scale - 1) - (round(Y[i] * (y_scale - 1) / y_range) - round(y_min * (y_scale - 1) / y_range)))
                map[j][i * x_scale] = symbol

        # convert map data to string for output
        ans = " " * round((46 * x_scale + len(str(int(y_max))) - len(Y_title)) * 0.5) + Y_title + '\n'
        for i in range(len(map)):
            row_str = "".join(map[i]) + "  " + str(round(y_max - i * (y_range / y_scale))) + "\n"
            ans += row_str
        ans += "_" * 46 * x_scale + "  " + str(round(y_min)) + "\n"
        ans += "20" + "".join([" " * (x_scale * 5 - 2) + str(x) for x in range(25, 66, 5)]) + "  " + "AGE"

        print("\n"+ans+"\n")

    def getData(self, show):
        if show == "L":
            (Y, Y_title) =([node._person.getHealth() for node in self._chain], "HEALTH")
        elif show == "K":
            (Y, Y_title) = ([node._person.getSkill() for node in self._chain], "SKILL")
        elif show == "T":
            (Y, Y_title) = ([node._person.getWorkTime() + node._person.getStudyTime() for node in self._chain], "TIME FOR WORK & STUDY (hrs/day)")
        elif show =="I":
            (Y, Y_title) = ([node._person.getIncome() for node in self._chain], "INCOME($/yr)")
        elif show == "C":
            (Y, Y_title) = ([node._cash.getBalance() for node in self._chain], "CASH($)")
        elif show == "B":
            (Y, Y_title) = ([node._bonds.getBalance() for node in self._chain], "BONDS($)")
        elif show == "S":
            (Y, Y_title) = ([node._stocks.getBalance() for node in self._chain], "STOCKS($)")
        elif show == "A":
            (Y, Y_title) = ([node.getAssets() for node in self._chain], "ASSETS($)")
        elif show == "E":
            (Y, Y_title) = ([node.getExpense() for node in self._chain], "EXPENSES($/yr)")
        elif show == "Y":
            (Y, Y_title) = ([sum([house.getEquity() for house in node._houses.values()]) for node in self._chain], "HOME EQUITY($)")
        else:
            (Y, Y_title) =([],"")
        return (Y, Y_title)

    def displayData(self):
        show = input("Please choose what data want to display ('h' for help, 'enter' to skip): ").upper()

        while len(show) > 0:
            if show not in ["L", "K", "T", "I", "C", "B", "S", "A", "E", "Y", "Q", "H"]:
                show = input("Please enter a valid entry: ").upper()
            elif show == "H":
                self.displayMenu()
                show = input("\nPlease choose what data you want to display ('h' for menu, 'enter' to skip): ").upper()
            elif show == "Q":
                print ('\nThank you for playing, exiting the game.')
                exit(1)
            else:
                (Y, Y_title) = self.getData(show)
                self.drawGraph(Y, Y_title)
                show = input("Please choose what data you want to display ('h' for menu, 'enter' to skip): ").upper()


def initialize():
    player_name = input("Please enter your name: ")
    if len(player_name)<1:
         player_name='person'
    person  = Person(player_name)
    cash = Account(10000, -0.02)             # yield -0.02 for inflation
    bonds = BondAccount(1000, 0.025)
    stocks = StockAccount(1000)
    houses = {}
    kids = {}
    step_size = 1
    return (person, cash, bonds, stocks, houses, kids, step_size)

## MAIN PROGRAM:   THE RETIREMENT GAME   by Zhaoning Yu (MIDS-INFO-W18 project 1, 03/2017)#######################
## STEP 0: Initializes and sets the scene #######################################################################
(person, cash, bonds, stocks, houses, kids, step_size) = initialize()
new_node = Node(person, cash, bonds, stocks, houses, kids, step_size)

print('\nHello, {}! welcome to the retirement game!'.format(new_node._person.getName().upper()))
time.sleep(1.55)
print('\nImagine you are a 20 year old new graduate...')
time.sleep(2.75)
print('fresh out of school, you make little and you own little...')
time.sleep(2.75)
print('what you have, is your youthful energy and unbridled optimism about the future...')
time.sleep(2.75)
print("\nYou will take on life's challenges by making wise financial decisions, the goal is to accumulate the assets for your retirement at age 65.")
time.sleep(3.00)
input("\nAre you ready? use 'enter' to start the game, let the journey begin! ")
print('\nHere is a summary of your situation at the beginning of your adult life:')
new_node.printNode()

ans = " "
while len(ans)>0 and ans != 'Q':
    ans = input("\nUse 'q' to quit, 'enter' to continue, good luck! ").upper()

if ans == 'Q':
    print("\nThank you for playing, exiting the game.")
    exit(1)

## STEP 1: Engine: to loop through ages 20-65 ##################################################################
history = NodeChain(new_node)
check_point = 21                       # always asks for user action at age 21

for  i in range(45):
    new_node = Node(person, cash, bonds, stocks, houses, kids, step_size)

    # 1: exits program if fails bankrupcy check, prompts user action if fails cashflow check:
    while new_node.checkCashFlow() == False:
        if new_node.checkBankrupcy() == True:
            break
        else:
            new_node.printNode()
            print('\nFor this year, you will have ${:,.2f} in cash  and expense will be ${:,.2f}'.format(new_node.getCash(), new_node.getExpense()))
            print('Please take actions to get more cash to cover your expenses.')
            action = new_node.getAction()
            if action == "G":
                history.displayData()
            else:
                new_node.executeAction(action)

    # 2: asks for user action if this is a check point, and reset the next check point:
    if new_node._person.getAge() == check_point and new_node.checkBankrupcy() == False:
        print("\nYou have reached age {}, this is a check point:".format(new_node._person.getAge()))
        new_node.printNode()
        action = " "   # need space to make "enter" work
        while len(action)>0:
            if new_node.checkCashFlow() == False:
                if new_node.checkBankrupcy() == True:
                    break
                else:
                    new_node.printNode()
                    print('\nFor this year, you will have ${:,.2f} in cash  and expense will be ${:,.2f}'.format(
                        new_node.getCash(), new_node.getExpense()))
                    print('Please take actions to get more cash to cover your expenses.')
                    action = new_node.getAction()
                    if action == "G":
                        history.displayData()
                    else:
                        new_node.executeAction(action)
            else:
                 action = new_node.getAction()
                 if action == "G":
                     history.displayData()
                 else:
                     new_node.executeAction(action)
        check_point = new_node._person.getAge() + new_node.getStepSize()

    #3: grow and add node to the chain if it passes bankrupcy test:
    if new_node.checkBankrupcy() == False:
        new_node.grow()
        (person, cash, bonds, stocks, houses, kids, step_size) = new_node.getNodeData()
        history.addNode(new_node)
    else:
        break

## STEP 2: Evaluates player performance ########################################################################
if new_node.checkBankrupcy() == True:      # exits because of bankrupcy
    new_node.printNode()
    print("\nYou will be BANKRUPT this year, GAME OVER.")
else:                                      # exits because age = 65
    history.evaluate()

## STEP 3: Displays graphics and exits the game ################################################################
print("\nYou can choose to view your performance data before exiting the game.")
history.displayData()
print("\n\nThank you for playing, exiting the game.")

## END OF MAIN PROGRAM #########################################################################################