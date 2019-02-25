import random
import os
import time
import textwrap
################################################################################
class Game:

    def __init__(self, maplist = [], maxiterations = 100):
        self.maplist = maplist
        self.maxiterations = maxiterations
        self.iteration = 0
        self.asciimap = """
        Alien World                                      EM                   Planets:
                 ,MMM8&&&.      _E5/V__    ,-----E------(5)    _____          (1) Bunny Moon (BM)
            _...MMMMM88&&&&... /       \\(3)             PE\\ :` \;',`'-,       (2) Burrowton (B)
         .::'''MMMMM88&&&&&&'''::.      / LG             .'-;_,;  ':-;_,'.    (3) Leafy Giant (LG)
        ::     MMMMM88&&&&&&     ::    /                /;   '/    ,  _`.-\\   (4) Mars (M)
        '::....MMMMM88&&&&&&....::'   /MF              | '`. (`     /` ` \`|  (5) Earth's Moon (EM)
           `''''MMMMM88&&&&''''`     /                 |:.  `\`-.   \_   / |
                 'MMM8&&&'   _____(2)_________    US/FH|     (   `,  .`\ ;'|   Spaceships:
                    DA  |   /     B      P    \\(4)------\     | .'     `-'/    (1) Eagle 5 (E5)            (6) Hyperion (H)
                        \  /  H                   M      `.   ;/  Earth .'     (2) Elysium (E)             (7) Prometheus (P)
                        (1)                                 `'-._____.-        (3) Planet Express (PE)     (8) USS Saratoga (US)
                         BM                                                    (4) Millennium Falcon (MF)  (9) Vindicaar (V)
                                                                               (5) Destiny Ascension (DA)  (10) Falcon Heavy (FH)
                            """
        # ASCII art of planets above from: https://www.ascii-code.com/ascii-art/space/planets.php

    def timestep(self):
        while self.iteration < self.maxiterations:
            for item in self.maplist:
                item.timestep()
            self.score = 0
            for item in self.maplist:
                if type(item) is Planet and item.name is "Earth":
                    for member in item.inhabitants:
                        if type(member) is Bunny:
                            self.score += member.mass
                            self.score = round(self.score, 2)
            self.gamemenu()
            self.iteration += 1
        self.end_game()

    def display(self):
        horiz = "-------------------------------------------------------------------------"
        os.system('cls')
        print(self.asciimap)
        print("Current Iteration: {}/{}".format(self.iteration, self.maxiterations))
        print("\nCurrent Score: {}".format(self.score))
        print("\nPlanet Stats\n", horiz, "\n{:<20s} {:^20s} {:^15s} {:^15s}\n".format("Planet", "Bunny Population", "Average Mass", "Gender Ratio"), horiz)
        for item in self.maplist:
            if type(item) is Planet:
                print("{:<20s} {:^20s} {:^15s} {:^15s}\n".format(item.name, str(item.numbunnies) + "/" + str(item.capacity), str(item.avemass), str(item.genderratio)))
        print(horiz)

    def shipstats(self, fast=False):
        horiz = "--------------------------------------------------------------------------"*2
        os.system('cls')
        print(self.asciimap)
        print("\nShip Stats\n", horiz, "\n{:<20s} {:^18s} {:^14s} {:^14s} {:^14s} {:^14s} {:^50s}\n".format("Ship", "Bunny Population", "Average Mass", "Gender Ratio", "Docked", "Max Speed", "Route"), horiz)
        for item in self.maplist:
            if type(item) is Route:
                for member in item.inhabitants:
                    print("{:<20s} {:^18s} {:^14s} {:^14s} {:^14s} {:^14s} {:^50s}\n".format(str(member.name), str(member.numbunnies) + "/" + str(member.capacity), str(member.avemass), str(member.genderratio), str(member.docked), str(abs(member.speed)), str(member.route.start.name) + str(member.distindicator) + str(member.route.end.name)))
        for item in self.maplist:
            if type(item) is Planet:
                if list(map(type, item.inhabitants)).count(Spaceship) > 0:
                    print("\n", horiz, "\nDocked on {}:\n".format(item.name), horiz)
                    for member in item.inhabitants:
                        if type(member) is Spaceship:
                            print("{:<20s} {:^18s} {:^14s} {:^14s} {:^14s} {:^14s} {:^50s}\n".format(str(member.name), str(member.numbunnies) + "/" + str(member.capacity), str(member.avemass), str(member.genderratio), str(member.docked), str(abs(member.speed)), str(member.route.start.name) + str(member.distindicator) + str(member.route.end.name)))

        input("\nPress enter to continue.")
        self.gamemenu()

    def recentevents_decisions(self, fast=False):
        print("\nHere are the recent events!")
        #gender warning
        for item in self.maplist:
            if type(item) is Planet:
                genderlist = []
                for member in item.inhabitants:
                    if type(member) is Bunny:
                        genderlist.append(member.gender)
                if len(genderlist) != 0 and genderlist.count(1) == 0 or len(genderlist) != 0 and genderlist.count(0) == 0:
                    print("{} has only one gender of bunnies. Suggest we mix it up, commander.".format(item.name))

        self.display()
        print("\nHere are the recent events!")
        #bunny capacity warning
        for item in self.maplist:
            if type(item) is Planet:
                if list(map(type, item.inhabitants)).count(Bunny) >= item.capacity:
                    if item.name != "Earth":
                        print("\n{} is overcrowded. Bunnies are not able to reproduce on this planet.\n".format(item.name))

        self.display()
        print("\nHere are the recent events!")
        #boarding decisions
        for item in self.maplist:
            if type(item) is Planet:
                for member in item.inhabitants:
                    if type(member) is Spaceship:
                        if len(member.inhabitants) == 0:
                            print("\n{} has landed on {} but is still empty.\n".format(member.name, item.name))
                            if item.numbunnies > 0:
                                choice = input("Would you like to order bunnies to board {}? [Y/N]: ".format(member.name)).lower()
                                if choice == "":
                                    choice = random.choice(["y","n"])
                                if choice == "y":
                                    try:
                                        secondchoice = int(input("How many would you like to board? (We can fit {} more): ".format(member.capacity-len(member.inhabitants))))
                                    except:
                                        print("Better to enter an integer next time... we'll just load all of them we can, commander!")
                                        secondchoice = 1000
                                    try:
                                        thirdchoice = int(input("How would you like to prioritize boarding? (1: Random, 2: Fattest First, 3: Skinniest First): "))
                                    except:
                                        print("Looks like we'll do it live, commander!")
                                        thirdchoice = 1
                                    bunnylist = []
                                    for thing in item.inhabitants:
                                        if type(thing) is Bunny:
                                            bunnylist.append(thing)
                                    if thirdchoice == 2:
                                        bunnylist.sort(key=lambda x: x.mass, reverse=True)
                                        n = 0
                                        for bunny in bunnylist:
                                            if secondchoice > n:
                                                bunny.board(member)
                                                n +=1
                                    elif thirdchoice == 3:
                                        bunnylist.sort(key=lambda x: x.mass)
                                        n = 0
                                        for bunny in bunnylist:
                                            if secondchoice > n:
                                                bunny.board(member)
                                                n +=1
                                    else:
                                        n = 0
                                        for bunny in bunnylist:
                                            if secondchoice > n:
                                                bunny.board(member)
                                                n +=1
                                else:
                                    choice = input("Then would you like {} to depart {}? [Y/N]: ".format(member.name, item.name)).lower()
                                    if choice == "":
                                        choice = random.choice(["y","n"])
                                    if choice == "y":
                                        member.take_off()
                                    else:
                                        print("We'll wait on your orders, sir!")
                            else:
                                choice = input("There are no bunnies to board. Would you like {} to depart {}? [Y/N]: ".format(member.name, item.name)).lower()
                                if choice == "":
                                    choice = random.choice(["y","n"])
                                if choice == "y":
                                    member.take_off()
                                else:
                                    print("Awaiting your orders, sir!")
                        elif len(member.inhabitants) == member.capacity:
                            while True:
                                choice = input("\n{} is full. Should we (1) hold, (2) deboard all, (3) take off from {}? [1,2,3]: ".format(member.name, item.name))
                                if choice in {"1","2","3",""}:
                                    break
                                else:
                                    print("Sir, please give us coherent orders! The people of Earth are depending on us!\n")
                            if choice == "":
                                print("We're just going to do something and pretend you were awake to have given the order!")
                                choice = random.choice(["1","2","3"])
                            if choice == "1":
                                print("Holding!!!")
                            elif choice == "2":
                                for bunny in member.inhabitants:
                                    bunny.deboard(item)
                            elif choice == "3":
                                    member.take_off()
                            elif choice == "4":
                                member.take_off()
                        else:
                            while True:
                                choice = input("{} is still partially full. We're getting land-legs, sir, make a decision! Should we (1) hold, (2) deboard all, (3) fill the ship, or (4) take off from {}? [1,2,3,4]: ".format(member.name, item.name))
                                if choice in {"1","2","3","4",""}:
                                    break
                                else:
                                    print("Sir, please give us coherent orders! The people of Earth are depending on us!")
                            if choice == "":
                                print("We're just going to do something and pretend you were awake to have given the order!")
                                choice = random.choice(["1","2","3","4"])
                            if choice == "1":
                                print("Holding!!!")
                            elif choice == "2":
                                for bunny in member.inhabitants:
                                    bunny.deboard(item)
                            elif choice == "3":
                                for thing in item.inhabitants:
                                    if type(thing) is Bunny:
                                        thing.board(member)
                            elif choice == "4":
                                member.take_off()

        self.display()
        print("\nHere are the recent events!")
        #docking decision
        for item in self.maplist:
            if type(item) is Route:
                for member in item.inhabitants:
                    if member.location is 0:
                        print("\n{} is orbiting {} and is ready to land.\n".format(member.name, member.route.start.name))
                        choice = input("Would you like to land? [Y/N]: ").lower()
                        if choice == "":
                            choice = random.choice(["y","n"])
                        if choice == "y":
                            member.land()

                    elif member.location == member.route.distance:
                        print("\n{} is orbiting {} and is ready to land.\n".format(member.name, member.route.end.name))
                        choice = input("Would you like to land? [Y/N]: ").lower()
                        if choice == "":
                            choice = random.choice(["y","n"])
                        if choice == "y":
                            member.land()

        self.display()
        print("\nHere are the recent events!")
        print("\nEarth continues to consume all arriving bunnies. Dead bunnies cannot reproduce.\n")
        input("Press enter to continue.")

    def bunnyshipstats(self, fast=False):
        menu_options ="""
                            +-------------------------------------------+
                            | Please select a ship: (1-10):             |
                            |  (1) Eagle 5 Bunnies                      |
                            |  (2) Elysium Bunnies                      |
                            |  (3) Planet Express Bunnies               |
                            |  (4) Millennium Falcon Bunnies            |
                            |  (5) Destiny Ascension Bunnies            |
                            |  (6) Hyperion Bunnies                     |
                            |  (7) Prometheus Bunnies                   |
                            |  (8) USS Saratoga Bunnies                 |
                            |  (9) Vindicaar Bunnies                    |
                            | (10) Falcon Heavy Bunnies                 |
                            +-------------------------------------------+"""
        print(textwrap.dedent(menu_options),"\n")
        options = {"1": "Eagle 5", "2": "Elysium", "3": "Planet Express", "4": "Millennium Falcon", "5": "Destiny Ascension", "6": "Hyperion", "7": "Prometheus", "8": "USS Saratoga", "9": "Vindicaar", "10": "Falcon Heavy"}
        while True:
            entry = str(input("User Entry: "))
            if entry in options.keys():
                break
            else:
                continue

        horiz = "-----------------------------------------------------------------"
        os.system('cls')
        print(self.asciimap)
        for item in self.maplist:
            if type(item) is Route:
                for member in item.inhabitants:
                    if member.name == options[entry]:
                        print("\n{}\n".format(options[entry]), horiz, "\n{:<10s} {:^10s} {:^8s} {:^8s} {:^10s} {:^13s}\n".format("Name", "Mass", "Gender", "Age", "Libido", "Gene Strength"), horiz)
                        for individual in member.inhabitants:
                            if type(individual) is Bunny:
                                print("{:<10s} {:^10s} {:^8s} {:^8s} {:^10s} {:^13s}\n".format(str(individual.identifier), str(round(individual.mass,2)), str(individual.gender), str(individual.age), str(round(individual.libido,2)), str(round(individual.genepower,2))))
        for item in self.maplist:
            if type(item) is Planet:
                for member in item.inhabitants:
                    if type(member) is Spaceship:
                        if member.name == options[entry]:
                            print("\n{} Bunnies\n".format(options[entry]), horiz, "\n{:<10s} {:^10s} {:^8s} {:^8s} {:^10s} {:^13s}\n".format("Name", "Mass", "Gender", "Age", "Libido", "Gene Strength"), horiz)
                            for individual in member.inhabitants:
                                if type(individual) is Bunny:
                                    print("{:<10s} {:^10s} {:^8s} {:^8s} {:^10s} {:^13s}\n".format(str(individual.identifier), str(round(individual.mass,2)), str(individual.gender), str(individual.age), str(round(individual.libido,2)), str(round(individual.genepower,2))))

        input("\nPress enter to continue.")
        self.gamemenu()

    def bunnystats(self, fast=False):
        menu_options ="""
                            +-------------------------------------------+
                            | Please select a subset of bunnies: (1-7): |
                            |  (1) Alien World Bunnies                  |
                            |  (2) Bunny Moon Bunnies                   |
                            |  (3) Burrowton Bunnies                    |
                            |  (4) Leafy Giant Bunnies                  |
                            |  (5) Mars Bunnies                         |
                            |  (6) Earth Moon Bunnies                   |
                            |  (7) Spaceship Bunnies                    |
                            +-------------------------------------------+"""
        print(textwrap.dedent(menu_options),"\n")
        options = {"1": "Alien World", "2": "Bunny Moon", "3": "Burrowton", "4": "Leafy Giant", "5": "Mars", "6": "Earth's Moon", "7": "Run a different function"}
        while True:
            entry = str(input("User Entry: "))
            if entry in options.keys():
                break
            else:
                continue

        if entry == "7":
            self.bunnyshipstats()

        else:
            horiz = "-----------------------------------------------------------------"
            os.system('cls')
            print(self.asciimap)
            print("\n{} Bunnies\n".format(options[entry]), horiz, "\n{:<10s} {:^10s} {:^8s} {:^8s} {:^10s} {:^13s}\n".format("Name", "Mass", "Gender", "Age", "Libido", "Gene Strength"), horiz)
            for item in self.maplist:
                if type(item) is Planet:
                    if item.name == options[entry]:
                        for member in item.inhabitants:
                            if type(member) is Bunny:
                                print("{:<10s} {:^10s} {:^8s} {:^8s} {:^10s} {:^13s}\n".format(str(member.identifier), str(round(member.mass,2)), str(member.gender), str(member.age), str(round(member.libido,2)), str(round(member.genepower,2))))

        input("\nPress enter to continue.")
        self.gamemenu()

    def run_default(self):
        """define default map/game"""
        alienworld = Planet("Alien World", 50, numdocks = 2)
        earth = Planet("Earth", 0, numdocks = 2)
        bunnymoon = Planet("Bunny Moon", 50)
        burrowton = Planet("Burrowton", 50)
        leafygiant = Planet("Leafy Giant", 250)
        mars = Planet("Mars", 100)
        earthmoon = Planet("Earth's Moon", 50)

        route1 = Route("Paradise", 12, leafygiant, alienworld)
        route2 = Route("Desolation", 20, leafygiant, earthmoon)
        route3 = Route("Puddle Jump", 2, earthmoon, earth)
        route4 = Route("Dangerous Detour", 8, leafygiant, burrowton)
        route5 = Route("Maiden Journey", 10, bunnymoon, alienworld)
        route6 = Route("Space Faring Civilization", 12, bunnymoon, burrowton)
        route7 = Route("Bunny Thruway", 10, burrowton, mars)
        route8 = Route("Bunny Highway", 10, mars, earth)

        ship1 = Spaceship("Eagle 5", route1, 10, 4)
        ship2 = Spaceship("Elysium", route2, 100, 2)
        ship3 = Spaceship("Planet Express", route3, 25, 1)
        ship4 = Spaceship("Millennium Falcon", route4, 25, 2)
        ship5 = Spaceship("Destiny Ascension", route5, 25, 2)
        ship6 = Spaceship("Hyperion", route6, 25, 2)
        ship7 = Spaceship("Prometheus", route7, 50, 5)
        ship8 = Spaceship("USS Saratoga", route8, 50, 2)
        ship9 = Spaceship("Vindicaar", route1, 25, 2)
        ship10 = Spaceship("Falcon Heavy", route8, 10, 2)

        for i in range(10):
            Bunny(alienworld)

        self.maplist = [alienworld, bunnymoon, burrowton, leafygiant,
                        mars, earthmoon, earth, route1, route2, route3, route4, route5,
                        route6, route7, route8]

        self.timestep()

    def gamemenu(self):
        self.display()
        menu_options ="""
                            +-------------------------------------------------+
                            | Please enter an option (1-4):                   |
                            |  (1) See Recent Events and Make Decisions       |
                            |  (2) See Ship Stats                             |
                            |  (3) See Bunny Stats                            |
                            |  (4) Quit to Menu (No Saves)                    |
                            +-------------------------------------------------+"""
        print(textwrap.dedent(menu_options),"\n")
        options = {"1": self.recentevents_decisions, "2": self.shipstats, "3":self.bunnystats, "4": self.startup}
        while True:
            entry = str(input("User Entry: "))
            if entry in options.keys():
                break
            elif entry is "":
                entry = "1"
                break
            else:
                continue
        options[entry](fast=True)

    def run_developer(self):
        print("\nRunning method 'run_developer'\n")
        time.sleep(1.5)
        print("For developer mode: type 'bunny.py' into your console.")
        time.sleep(1.5)
        self.startup(fast=True)

    def end_game(self):
        self.display()
        print("\nCongratulations, you finished the game! Your score was {}. ".format(self.score))
        try:
            open("spacebunniesscores.txt", "x")
            scoredata = open("spacebunniesscores.txt", "r+")
        except:
            scoredata = open("spacebunniesscores.txt", "r+")
        scorelist = scoredata.readlines()
        scoredata.write(str(self.score)+"\n")
        scoredata.close()
        try:
            for i in range(0,len(scorelist)):
                scorelist[i] = float(scorelist[i].strip())

            maxscore = max(scorelist)
        except:
            maxscore = 0
        print("\nThe highscore for this game was previously {}.\n".format(round(float(maxscore),2)))
        if self.score > float(maxscore):
            print("You set a new highscore of {}!\n".format(self.score))
        for i in range(20, 0, -1):
            print("\rRestarting in {} seconds...".format(i), end="")
            time.sleep(1)
        start(fast=True)

    def intro(self, fast = False):
        os.system('cls')
        if fast:
            introtext = """
                        Winter is coming!\n
                        The year is 2320 and the oligarchy of Earth must devise a way to lure sufficient biomass to the planet to feed its starving population.\n
                        Luckily, a nearby civilization – much resembling what we know as “bunnies” – is extremely susceptible to “divine orders” to board spacecraft.\n
                        Can you successfully control this voracious civilization to save humanity?"""
            print(textwrap.dedent(introtext))
        else:
            print("Winter is coming!\n")
            time.sleep(1)
            print("The year is 2320 and the oligarchy of Earth must devise a way to lure sufficient biomass to the planet to feed its starving population.\n")
            time.sleep(4)
            print("Luckily, a nearby civilization – much resembling what we know as “bunnies” – is extremely susceptible to “divine orders” to board spacecraft.\n")
            time.sleep(4)
            print("Can you successfully control this voracious civilization to save humanity?")
            time.sleep(2.5)

    def mainmenu(self):
        menu_options ="""
                        +-----------------------------------+
                        | Please enter a menu option (1-3): |
                        |   (1) Play Default Game           |
                        |   (2) Developer Mode              |
                        |   (3) Quit to Terminal            |
                        +-----------------------------------+"""
        print(textwrap.dedent(menu_options),"\n")
        options = {"1": self.run_default, "2": self.run_developer, "3": quit}
        while True:
            entry = str(input("User Entry: "))
            if entry in options.keys():
                break
            else:
                continue
        options[entry]()

    def startup(self, fast = False):
        if fast:
            self.intro(fast = True)
        else:
            self.intro()
        self.mainmenu()
################################################################################
class Location:

    def __init__(self, name):
        self.inhabitants = set()
        self.additions = set()
        self.removals = set()
        self.name = name

    def timestep(self):
        self.inhabitants.update(self.additions)
        self.inhabitants.difference_update(self.removals)
        self.additions.clear()
        self.removals.clear()
################################################################################
class Spaceship(Location):

    def __init__(self, name, route, capacity, speed):
        super().__init__(name)
        self.speed = speed
        self.route = route
        self.location = 0
        self.capacity = capacity
        self.docked = False
        self.name = name
        route.inhabitants.add(self)
        self.numbunnies = list(map(type, self.inhabitants)).count(Bunny)
        self.avemass = "N/A"
        self.genderratio = "N/A"
        self.distindicator = ""

    def take_off(self):
        if self.docked:
            self.route.additions.add(self)
            self.docked = False
            self.route.start.removals.add(self)
            self.route.end.removals.add(self)

    def land(self):
        if self.location >= self.route.distance:
            docked = list(map(type, self.route.end.inhabitants)).count(Spaceship)
            if self.route.end.numdocks > docked:
                self.location = self.route.distance
                self.route.end.additions.add(self)
                self.route.removals.add(self)
                self.speed = -self.speed
                self.docked = True
            else:
                print("Sir, there are no available docks! We'll keep orbiting.")

        elif self.location <= 0:
            docked = list(map(type, self.route.start.inhabitants)).count(Spaceship)
            if self.route.start.numdocks > docked:
                self.location = 0
                self.route.start.additions.add(self)
                self.route.removals.add(self)
                self.speed = -self.speed
                self.docked = True
            else:
                print("Sir, there are no available docks! We'll keep orbiting.")

    def timestep(self):
        super().timestep()
        if self.docked is False:
            self.location += self.speed
            if self.location > self.route.distance:
                self.location = self.route.distance
            elif self.location < 0:
                self.location = 0
        if self.speed < 0:
            self.distindicator = " " + "-"*self.location + "<+" + "-"*(self.route.distance - self.location) + " "
        else:
            self.distindicator = " " + "-"*self.location + "+>" + "-"*(self.route.distance - self.location) + " "
        self.numbunnies = list(map(type, self.inhabitants)).count(Bunny)
        try:
            self.avemass = round(sum([item.mass for item in self.inhabitants if type(item) is Bunny])/self.numbunnies,2)
            self.genderratio = round([item.gender for item in self.inhabitants if type(item) is Bunny].count(1)/self.numbunnies,2)
        except:
            self.avemass = "N/A"
            self.genderratio = "N/A"
        for member in self.inhabitants:
            member.timestep()

    def __str__(self):
        return ("Spaceship: " + str(self.name) + "\n"
                + "Bunny Population: " + str(self.numbunnies) + "/" + str(self.capacity) + "\n"
                + "Average Mass: " + str(self.avemass) + "\n"
                + "Gender Ratio M/F: " + str(self.genderratio) + "\n"
                + "Docked: " + str(self.docked) + "\n"
                + "Speed: " + str(abs(self.speed)) + "\n"
                + "Route: " + str(self.route.start.name) + self.distindicator + str(self.route.end.name) + "\n")
################################################################################
class Route(Location):

    def __init__(self, name, distance, start, end):
        super().__init__(name)
        self.distance = distance
        self.start = start
        self.end = end
        self.name = name

    def timestep(self):
        super().timestep()
        for member in self.inhabitants:
            member.timestep()
    def __str__(self):
        return ("-------------------" +"\n"
                + "Route: " + str(self.name) + "\n"
                + "Distance: " + str(self.distance) + "\n"
                + "-------------------")
################################################################################
class Planet(Location):

    def __init__(self, name, capacity, numdocks = 1):
        super().__init__(name)
        self.numdocks = numdocks
        self.capacity = capacity
        self.name = name
        self.numbunnies = list(map(type, self.inhabitants)).count(Bunny)
        self.avemass = "N/A"
        self.genderratio = "N/A"

    def timestep(self):
        super().timestep()
        for member in self.inhabitants:
            member.timestep()
            if type(member) is Bunny:
                member.reproduce()
        self.numbunnies = list(map(type, self.inhabitants)).count(Bunny)
        try:
            self.avemass = round(sum([item.mass for item in self.inhabitants if type(item) is Bunny])/self.numbunnies,2)
            self.genderratio = round([item.gender for item in self.inhabitants if type(item) is Bunny].count(1)/self.numbunnies,2)
        except:
            self.avemass = "N/A"
            self.genderratio = "N/A"

    def __str__(self):
        return ("Planet: " + str(self.name) + "\n"
                + "Bunny Population: " + str(self.numbunnies) + "/" + str(self.capacity) + "\n"
                + "Average Mass: " + str(self.avemass) + "\n"
                + "Gender Ratio M/F: " + str(self.genderratio) + "\n")
################################################################################
class Bunny:

    def __init__(self, location,
                mass = 1, age = 0, libido = .5, genepower = .5):
        self.gender = random.getrandbits(1)
        self.location = location
        self.identifier = "#%X" % random.randrange(16**8)
        self.mass = mass
        self.age = age
        self.libido = libido
        self.genepower = genepower
        location.additions.add(self)

    def __str__(self):
        return ("Gender: " + str(self.gender) + "\n"
                + "Location: " + self.location.name + "\n"
                + "Name: " + self.identifier + "\n"
                + "Mass: " + str(self.mass) + "\n"
                + "Age: " + str(self.age) + "\n"
                + "Libido: " + str(self.libido) + "\n"
                + "Genes: " + str(self.genepower) + "\n"
                + "++++++++++++++++++++++++++++++++++\n")

    def reproduce(self):
        bunnies = list(map(type, self.location.inhabitants)).count(Bunny)
        if self.location.capacity > bunnies:
            if random.random() < self.libido:
                mate = random.sample(self.location.inhabitants, 1)[0]
                if type(mate) is Bunny:
                    if mate.gender != self.gender:
                        mass = abs(random.normalvariate(self.genepower*self.mass + mate.genepower*mate.mass, 1))
                        libido = random.normalvariate(self.genepower*self.libido + mate.genepower*mate.libido, .1)
                        Bunny(location = self.location, mass = mass, libido = libido, genepower = random.random())

    def board(self, spaceship):
        if spaceship.capacity > len(spaceship.additions) + len(spaceship.inhabitants) and self.location.name is not "Earth":
            self.location.removals.add(self)
            spaceship.additions.add(self)
            self.location = spaceship
        else:
            pass

    def deboard(self, planet):
        if planet.capacity > len(planet.additions) + len(planet.inhabitants) or planet.name is "Earth":
            self.location.removals.add(self)
            planet.additions.add(self)
            self.location = planet
        else:
            pass

    def timestep(self):
        self.age += 1
################################################################################
def start(fast=False):
    game = Game()
    game.startup(fast=fast)
################################################################################
start()
