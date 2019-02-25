import random
import string
import sys

class City:
    """ Represents the city object. Has streets and can draw a map of the city """
    items = ['Backpack', 'Flashlight', 'Jacket', 'Computer', 'Phone']

    def __init__(self, person, x, y):
        self.person = Human(self, person)
        self.items = []
        self.x = x
        self.y = y
        self.locations = {}
        self.house = (1,1)
        self.points = self.generatePoints()
        self.person.setPos(0, 0)

    def drawMap(self):
        """ Draws a map that represents the city. Shows all positions and where you are """
        city_map = ""
        print("X marks where you are. Your position is " + str(self.person.getPos()) + ". Your home is at: " + str(self.house))
        for x in range(self.x):
            city_map += "\n"
            for y in range(self.y):
                if (y,x) == self.person.getPos():
                    city_map += 'X'
                else:
                    city_map += 'O'
                if y < self.y-1:
                    city_map += " ---- "
            city_map += "\n"
            if x < self.x-1:
                for i in range(0, self.y):
                    city_map += "|      "
        return city_map

    def drive(self, x, y):
        """ Drives to a place on the map provided you have enough gas """
        x = int(x)
        y = int(y)
        distance = abs(self.x - x) + abs(self.y - y)
        if x >= 0 and x < self.x and y >= 0 and y < self.y:
            if self.person.gas >= distance:
                self.person.setPos(x,y)
                self.person.gas -= distance
                return 'Successfully drove to ' + str((x, y))
            else:
                return 'You do not have enough gas to drive there.'
        else:
            return 'That is an invalid location'

    def getLocation(self, item):
        """ Returns the location of a given item """
        return self.locations[item]

    def addLocation(self, item, loc, building):
        """ Adds location to an item """
        self.locations[item] = (loc, building)

    def generatePoints(self):
        """ Create point nodes that represent a city area """
        points = {}
        for i in range(self.x):
            for j in range(self.y):
                points[(i,j)] = Point(self, i, j)
        return points


    def getPossiblePositions(self, x, y):
        """ Get all possible moves at a given point """
        new_possible_positions = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
        all_pos = []
        for i in new_possible_positions:
            if (i[0] < self.x and i[0] >= 0) and (i[1] < self.y and i[1] >= 0):
                if i == (x, y+1):
                    all_pos.append(('South', i))
                elif i == (x, y-1):
                    all_pos.append(('North', i))
                elif i == (x+1, y):
                    all_pos.append(('East', i))
                elif i == (x-1, y):
                    all_pos.append(('West', i))
        return all_pos

    def printBuildings(self):
        """ Print all buildings """
        string = ""
        person = self.person
        point = person.point
        buildings = point.buildings

        for i in buildings.keys():
            string += '\n'
            string += i

        return string

    def move(self, direction):
        for i in self.getPossiblePositions(self.person.point.pos[0], self.person.point.pos[1]):
            if direction.lower() == i[0].lower():
                print("Moving to " + str(i[1]))
                self.person.point = self.points[i[1]]
                print("You have successfully moved " + direction.lower())

    def human(self):
        return self.person


class Point:
    def __init__(self, city, x, y):
        self.pos = (x, y)
        self.streets = []
        self.buildings = {}
        self.city = city
        self.generateBuildings()

    def generateBuildings(self):
        for i in range(0, 5):
            randomized_name = ""
            for x in range(0, 10):
                randomized_name += random.choice('abcdefghijklmnopqrstuvwxyz')
            if i == 0:
                if self.pos == (0, 1):
                    self.buildings['The North Face'] = Building(self.city, 'The North Face', True, ('Backpack', 50))
                    self.city.addLocation('Backpack', self.pos, 'The North Face')
                elif self.pos == (1,1):
                    self.buildings['Apple Store'] = Building(self.city, 'Apple Store', True, ('Computer', 1000))
                    self.city.addLocation('Computer', self.pos, 'Apple Store')
                elif self.pos == (2,1):
                    self.buildings['Verizon Store'] = Building(self.city, 'Verizon Store', True, ('Phone', 250))
                    self.city.addLocation('Phone', self.pos, 'Verizon Store')
                elif self.pos == (3,3):
                    self.buildings['Patagonia'] = Building(self.city, 'Patagonia', True, ('Jacket', 250))
                    self.city.addLocation('Jacket', self.pos, 'Patagonia')
                elif self.pos == (2,2):
                    self.buildings['Shell'] = Building(self.city, 'Shell', True, ('Gas', 3))
                    self.city.addLocation('Gas', self.pos, 'Gas Station')
            else:
                self.buildings[randomized_name] = Building(self.city, randomized_name, True, ('Random Goods', 5))

        if self.pos == self.city.house:
            house = Building(self.city, "home", False, ('None', 0))
            self.buildings['home'] = house


class Human:
    def __init__(self, city, name):
        self.name = name
        self.money = 5000
        self.gas = 25
        self.city = city
        self.inventory = {}
        self.point = None

    def get_name(self):
        return self.name

    def get_money(self):
        return self.money

    def setPos(self, x, y):
        self.point = self.city.points[(x,y)]

    def getPoint(self):
        return self.point

    def getPos(self):
        return self.point.pos
        
    def getPosString(self):
        return "You are currently at: " + str(self.pos)

    def getGas(self):
        return self.gas

class Building:
    """ Create a building. If it is not a shop, it is a place you can earn money. """

    def __init__(self, city, name, shop, item):
        self.name = name
        self.city = city
        self.type = 'house'
        if shop:
            self.type = 'shop'
            self.item = item[0]
            self.price = item[1]

    def enter(self):
        if self.type == 'house':
            prompt = input("Would you like to enter your house? Make sure that you have all of the items you need! ")
            inventory = self.city.person.inventory
            if 'Backpack' in inventory.keys() and 'Jacket' in inventory.keys() and 'Computer' in inventory.keys() and 'Phone' in inventory.keys():
                inpu = input('You have entered your house, finishing all of your errands. You have finished! Would you like to exit? ').lower()
                if inpu == "yes":
                    sys.exit()
                else:
                    return 'Okay, keep exploring!'
            else:
                string = 'You still have some errands to finish. Type todo in the command prompt to see what else you need to do. However, you can drop off random goods if you want to'
                print(string)
                inp = input("How many random goods do you want to exchange? Your mom will give you $10 for each random good. ")
                amt = int(inp)
                money = 10 * amt
                if 'Random Goods' in self.city.person.inventory.keys():
                    if self.city.person.inventory['Random Goods'] >= amt:
                        confirm = input("Are you sure you want to exchange " + str(amt) + " for " + str(money) + "? ").lower()
                        if confirm == 'yes':
                             self.city.person.money += money
                             return "You have exchanged random goods and gained " + str(money)
                        else:
                            return "Okay, continue on what you were doing before."
                else:
                    return "You do not have Random Goods."
        else:
            if self.name == 'Shell':
                confirm = input("Welcome to the gas station! Would you like to refill your gas? (reply yes or no) ").lower()
                if confirm == "yes":
                    gallons = input("How many gallons of gas would you like to pump? ")
                    cost = self.price * int(gallons)
                    if cost <= 0:
                        return "You must enter a number greater than 0."
                    if self.city.person.money >= cost:
                        self.city.person.money -= cost
                        self.city.person.gas += float(gallons)
                        return "You have successfully added " + str(gallons) + " of gas."
                    else:
                        return "You don't have enough money to fill up the gas."
                else:
                    return "Come back whenever you want!"
            else:
                prompt = input("Welcome to the " + self.name + " shop! Would you like to buy " + self.item + " for " + str(self.price) + "? ")
                if prompt == 'yes':
                    if self.city.person.money > self.price:
                        self.city.person.money -= self.price
                        if self.item in self.city.person.inventory.keys():
                            self.city.person.inventory[self.item] += 1
                        else:
                            self.city.person.inventory[self.item] = 1
                        return 'You have successfully purchased a ' + self.item
                    else:
                        return 'You do not have enough money for this.'
                else:
                    return 'Okay, thank you for coming to the shop!'

name = input("What's your name?: ")

print("You woke up with a bunch of errands to do! Type 'todo' to see what you have to do.")
print("IMPORTANT: Type the word help into the 'What would you like to do?' prompt to reveal the details of your character and the list of available commands.")

city_x = 5
city_y = 5
city = City(name, city_x, city_y)
person = city.human()

while True:
    command = input("What would you like to do, " + person.name + "? ").lower()
    if command == 'quit':
        break
    elif command == 'enter':
        print("Here are a list of buildings which you can enter:")
        for i in person.getPoint().buildings.keys():
            print(i)
        comm = input("Which building would you like to enter? ")
        if comm in person.getPoint().buildings.keys():
            print(person.getPoint().buildings[comm].enter())
        else:
            print("This is not a valid building name.")
    elif command == 'move':
        direction = input("Which direction would you like to move? ")
        city.move(direction)
    elif command == 'moves':
        possible_moves = "You can go "
        for i in city.getPossiblePositions(person.getPos()[0], person.getPos()[1]):
            possible_moves += i[0] + " " + str(i[1]) + " "
        print(possible_moves)
    elif command == 'todo':
        items_to_buy = ['Backpack', 'Jacket', 'Computer', 'Phone']
        print("Items left to buy: ")
        for i in person.inventory.keys():
            if i != 'Random Goods':
                items_to_buy.pop(items_to_buy.index(i))
        for i in items_to_buy:
            print(str(i) + " which can be located at " + str(city.getLocation(i)[0]) + " in the building called " + city.getLocation(i)[1])
    elif command == 'buildings':
        print(city.printBuildings())
    elif command == 'map':
        print(city.drawMap())
    elif command == 'drive':
        x = input("What is the x position of where you want to go? ")
        y = input("What is the y position of where you want to go? ")
        print(city.drive(x, y))
    elif command == 'help':
        print("Your name is " + person.get_name() + " and you have $" + str(person.get_money()))
        print("You are currently in the position " + str(person.getPos()))
        print("Here is a list of the possible commands:")
        print("quit: quits the game")
        print("buildings: prints a list of building names that you use to enter a building")
        print("enter: enters a building of your choice")
        print("todo: shows the items you still need to buy in order to finish the game")
        print("map: prints a map of the city, and your current location")
        print("moves: show your possible moves")
        print("move: lets you move in a direction only if it is possible")
        print("drive: lets you drive to any location on the map")
        print("You can refill your gas at (2,2) at the shell station.")
        print("You currently have " + str(person.getGas()) + " gallons of gas.")
        for i in person.inventory.keys():
            print('You have ' + str(person.inventory[i]) + ' ' + i)