# Chris Hipple's Project 1 Class Definition file

import random as rand


class Factory(object):
    '''The player is a factory in which they'll have production lines, process
    orders, and make upgrades to their equipment in order to make more money!.
    '''

    def __init__(self):
        '''The starting conditions for the factory game'''

        self.money = 250
        self.line = Line(3, self)
        self.sequencer = False
        self.marketing = 0
        self.overheadCosts = 0.2
        self.upgradeCosts = {'mkt': 2500, 'ci': 500,
                             'sp': 200, 'ot': 750}
        self.dailyProduction = 0
        self.dailyTarget = 0
        self.dailyIncome = 0

        # Logistics is where the products are moved after the last station.
        # At the end of the workday, they're shipped and money is collected.
        self.logistics = []

    def genOrders(self):
        '''At the start of each day, a few random orders will come in
        which the factory will have to produce.'''
        orderCount = rand.randint(3, 4) + self.marketing
        for i in range(orderCount):
            self.line.orders.append(Order(rand.choice('ABC'),
                                          rand.randint(5+2*self.marketing,
                                                       8+2*self.marketing)))
        self.dailyTarget = sum([order.quantity for order in self.line.orders])
        print('Today, you have', orderCount,
              'new orders from customers for', self.dailyTarget, 'Products.')

    def calcIncome(self):
        '''Calculates how much money the factory makes after each day.'''

        income = 0
        for product in self.logistics:
            income += product.value*(1 - self.overheadCosts)
        self.dailyProduction = len(self.logistics)

        self.money += income
        self.dailyIncome = income
        self.logistics = []

    def buyUpgrades(self):
        '''Allows the factory owner to purchase upgrades once a day.'''

        print('\nUpgrading Time!')

        while True:
            print('You have ', str(self.money), ' dollars to spend.')
            b = input('Which upgrade would you like to purchase? '
                      'Type "Help" to see your options. ').lower()

            if b == 'help':
                print('Your upgrade options are:')
                print('A) Station Performance, $', self.upgradeCosts['sp'])
                print('B) Marketing, $', self.upgradeCosts['mkt'])
                print('C) Cost Improvements, $', self.upgradeCosts['ci'])
                print('D) Overtime, $', self.upgradeCosts['ot'])
                print('E) None.\n')

            elif b == 'station performance' or b == 'a':
                if self.money >= self.upgradeCosts['sp']:
                    try:
                        sta = int(input('Which Station would you like to'
                                        'upgrade? 0, 1, or 2? '))
                        if sta in [0, 1, 2]:
                            self.line.stations[sta].upgrade()
                            self.money -= self.upgradeCosts['sp']
                            self.upgradeCosts['sp'] += 50
                        else:
                            print('That is not a valid station number.')
                    except:
                        print('That is not a valid station number.')
                else:
                    print("You can't afford station improvements!")

            elif b == 'marketing' or b == 'b':
                if self.money >= self.upgradeCosts['mkt']:
                    self.marketing += 1
                    self.money -= self.upgradeCosts['mkt']
                    self.upgradeCosts['mkt'] *= 1.1
                else:
                    print("You can't afford marketing improvements!")

            elif b == 'cost improvements' or b == 'c':
                if self.money >= self.upgradeCosts['ci']:
                    if self.overheadCosts > 0:
                        self.overheadCosts -= 0.05
                        self.money -= self.upgradeCosts['ci']
                        self.upgradeCosts['ci'] *= 1.5
                    else:
                        print("Upgrade already maximized!")
                else:
                    print("You can't afford cost improvements!")

            elif b == 'overtime' or b == 'd':
                if self.money >= self.upgradeCosts['ot']:
                    self.line.dayLength += 100
                    self.money -= self.upgradeCosts['ot']
                    self.upgradeCosts['ot'] *= 1.2
                else:
                    print("You can't afford overtime!")

            elif b == 'done' or b == 'none' or b == 'e':
                print('Upgrading complete.\n')
                break

            else:
                print('Invalid Entry. Please try again.')

    def checkVictory(self):
        '''Checks to see if player has achieved victory condition.'''
        return self.dailyIncome >= 3000

    def report(self, day):
        '''Prints out daily production status for player.'''

        effic = self.line.calculateEfficiencies()
        print('\n----------------------------')
        print('Daily report for production day #', day)
        print('Daily production total:', self.dailyProduction)
        print('Daily production Target:', self.dailyTarget)
        print("Today's production earned your factory: $", self.dailyIncome,
              sep="")
        if self.dailyTarget > self.dailyProduction:
            print('You ran out of production time today. '
                  'You were unable to complete all of your orders!')

        print('Your overall production line efficiency was: ',
              float("{0:.3f}".format(100*effic[0])), '%', sep="")
        for st in self.line.stations:
            print('Station ', st.stationNumber, ' Had an utilization of ',
                  float("{0:.3f}".format(100*effic[1][st.stationNumber])), '%',
                  sep="")

    def runGame(self):
        '''Start running the game engine.  Loops until game is complete.'''

        day = 0
        print('Day 0, your brand new factory is now open!')
        print('Your goal is to have an income of $3,000 in one day.')
        print("To achieve this, you'll need to upgrade your production to \n"
              "be more efficient, profitable, and to have better marketing. \n"
              "Each day, you recieve several orders from customers but \n"
              "are only able to sell what you can produce that day.")

        while True:
            self.line.reset()
            self.buyUpgrades()
            self.line.orders = []
            self.genOrders()
            self.line.runProduction()
            self.calcIncome()
            self.report(day)
            if self.checkVictory():
                print('Congratulations!')
                print('You have achieved your goals in', day, 'days!')
                break
            day += 1


class Line(object):
    '''The production line.  Contains the stations and processes orders.'''

    def __init__(self, numStations, factory):
        self.factory = factory
        # Build the stations
        self.numStations = numStations
        self.stations = []
        self.stations.append(FirstStation(0, self))
        for i in range(1, numStations - 1):
            self.stations.append(Station(i, self))
        self.stations.append(LastStation(numStations - 1, self))
        self.orders = []
        self.runTime = 0
        self.dayLength = 1500

        # Set the nextStation attribute for each station.
        for i in range(len(self.stations) - 1):
            self.stations[i].nextStation = self.stations[i+1]

    def __str__(self):
        return "Production line with " + str(self.numStations) + ' Stations.'

    def getProducts(self):
        '''Makes a list of the products currently at each station.'''
        products = []
        for station in self.stations:
            products.append(station.currentProduct)
        return products

    def calculateEfficiencies(self):
        '''
        Calculates the utilization rate for each of the stations,
        and for the line as a whole.
        '''
        effic = []
        stationEffic = []
        effic.append(sum([sta.activeCount for sta in self.stations]) /
                     (self.runTime * len(self.stations)))

        for station in self.stations:
            stationEffic.append(station.activeCount / self.runTime)

        effic.append(stationEffic)
        return effic

    def runProduction(self):
        '''
        Steps through the order sequence one product at a time until
        every order is fulfilled.  Calculates efficiencies and runtimes
        for each station and the line as a whole.
        '''

        currentTime = 0
        self.stations[0].currentOrder = self.orders.pop(0)

        while True:
            for station in self.stations:
                station.Process(currentTime)

            # if all stations have gone and None have any parts.
            if not any([station.active for station in self.stations]):
                if all(product is None for product in self.getProducts()):
                    break

            currentTime += 1
            if currentTime > self.dayLength:
                self.orders = None
                break

        self.runTime = currentTime

    def reset(self):
        '''Resets each station to be ready to start the day.'''
        for station in self.stations:
            station.reset()


class Station(object):
    '''A station on the production line.'''

    def __init__(self, stationNumber, line):
        self.stationNumber = stationNumber
        self.active = False
        self.endTime = -1
        self.currentProduct = None
        self.line = line
        self.activeCount = 0
        self.upgradeLevel = 1
        # nextStation is defined after all the stations are created.
        self.nextStation = None

    def __repr__(self):
        return "Station " + str(self.stationNumber)

    def Process(self, currentTime):
        '''
        Main processing function of the product.
        Updates station's utilization and checks to see if the product is
        finished being processed.  If it is, it will try to send it to the
        next station via transferProduct().  If unsuccessful, it will try
        again next time.
        '''
        if self.active is True:
            self.activeCount += 1

        if self.endTime < currentTime and self.currentProduct is not None:
            # Product is done processing.  Try to pass it on.
            self.active = False
            self.transferProduct(currentTime)

    def transferProduct(self, currentTime):
        '''Transfers product to the next station.'''
        if self.nextStation.currentProduct is None:
            self.nextStation.recieveProduct(self.currentProduct, currentTime)
            self.currentProduct = None
            self.endTime = -1

    def recieveProduct(self, product, currentTime):
        '''Handles an incoming product from a previous station.'''
        self.currentProduct = product
        self.active = True
        self.endTime = currentTime + (product.cycleTimes[self.stationNumber] /
                                      self.upgradeLevel)

    def upgrade(self):
        self.upgradeLevel += 0.2

    def reset(self):
        '''Resets the station between sequences.'''
        self.active = False
        self.endTime = -1
        self.currentProduct = None
        self.activeCount = 0


class FirstStation(Station):
    '''
    The first station on the line.  Has special Process and recieveProduct
    method which generates the product to fulfill the production order.
    '''

    def __init__(self, stationNumber, line):
        Station.__init__(self, stationNumber, line)
        self.currentOrder = None

    def Process(self, currentTime):
        if self.currentProduct is None:
            if self.currentOrder is not None:
                self.recieveProduct(currentTime)
        super().Process(currentTime)

    def recieveProduct(self, currentTime):
        '''Generates products to fill production order.'''

        if self.currentOrder.checkFinished() is True:
            try:
                self.currentOrder = self.line.orders.pop(0)
            except:
                self.currentOrder = None

        # If it was unable to get the next order, the order sequence is done.
        if self.currentOrder is None:
            self.currentProduct = None
        else:
            self.currentProduct = self.currentOrder.generate()
            super().recieveProduct(self.currentProduct, currentTime)


class LastStation(Station):
    '''
    Last station on the line.  When finished processing a product, it marks
    it as complete and removes it from the line.
    '''

    def __init__(self, stationNumber, line):
        Station.__init__(self, stationNumber, line)
        self.nextStation = None

    def transferProduct(self, currentTime):
        '''Removes product from line instead of move to next station'''
        self.currentProduct.completed = True
        # Transfer to Logistics instead of next station.
        self.line.factory.logistics.append(self.currentProduct)
        self.currentProduct = None
        self.active = False


class Product(object):
    '''An individual widgit being built on the production line.'''
    serialNumber = 1000

    def __init__(self, productType):
        self.serialNumber = Product.serialNumber
        Product.serialNumber += 1
        self.results = []
        self.completed = False

        self.productType = productType

        if productType == 'A':
            self.cycleTimes = [20, 60, 20]
            self.value = 25
        elif productType == 'B':
            self.cycleTimes = [20, 20, 60]
            self.value = 50
        elif productType == 'C':
            self.cycleTimes = [70, 15, 15]
            self.value = 75
        else:
            print(productType, 'is not a valid product type.')
            raise TypeError('Invalid Product Type!')

    def __repr__(self):
        return 'Type: %s, SN: %s' % (self.productType, self.serialNumber)


class Order(object):
    '''A production order for a certain quantity of a certain part type.'''

    def __init__(self, orderedProductType, quantity):
        self.orderedProductType = orderedProductType
        self.quantity = quantity
        self.produced = 0

    def __repr__(self):
        return ("Production order for " + str(self.quantity) +
                ' parts of type: ' + str(self.orderedProductType))

    def generate(self):
        '''Creates an instance of the product to feed the first station.'''
        self.produced += 1
        genProduct = Product(self.orderedProductType)

        return genProduct

    def checkFinished(self):
        return self.produced == self.quantity

    def reset(self):
        '''Resets the order so it can be used in a different iteration
        of the sequence tester.'''
        self.produced = 0

factory = Factory()
factory.runGame()
