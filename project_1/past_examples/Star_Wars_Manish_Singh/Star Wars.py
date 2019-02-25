#STAR WARS ADVENTURE GAME!
#Manish Singh
import os
import time
import numpy as np
import sys
class item:
	def __init__(self, properties, name):
		self.properties = properties
		self.name = name
	def used(self):
		self.properties = None

class player:
	def __init__(self, character):
		if character == "Luke":
			self.name = "Luke"
			self.last_name = "Skywalker"
			self.weapon = "Lightsaber"
			self.weapon_damage = 8
			self.partner = "R2-D2"
			self.health = 10
		elif character == "Han":
			self.name = "Han"
			self.last_name = "Solo"
			self.weapon = "Blaster"
			self.weapon_damage = 5
			self.partner = "Chewbacca"
			self.health = 13
		self.fanny_pack = ["bread", "bread"]
	def hit(self, dam):
		self.health -= dam
	def weapon_plus(self, val):
		self.weapon_damage += val
	def use(self, thing, jj):
		if thing in self.fanny_pack:
			print("You use your " + thing.name)
			if thing.properties[0:3] == 'hit':
				print(thing.properties[4:], "has been added to your health.")
				self.hit(-int(thing.properties[3:]))
				print("HEALTH:", self.health)
			elif thing.properties[0:6] == 'weapon':
				print(thing.properties[7:], "has been added to your weapon damage.")
				self.weapon_damage += int(thing.properties[6:])
			elif thing.properties[0:2] == "JJ":
				if jj == True:
					print("JAR JAR: " + thing.properties[4:])
				elif jj == False:
					print("You don't have a Gungan to use this on.")
		else:
			print("You cannot use an item that's not in your fanny pack. \n")
		self.fanny_pack.remove(thing)
	def fight(self, character_, JJ):
		"""The fighting interface as the user fights characters."""
		os.system('clear')
		print("You run into " + character_.name+". You must fight him.")
		if JJ == True:
			print("JAR JAR: OH NO!!! RUN, " +seos.systelf.name.upper()+ "!!!!! AAAAAAHHHHHHHHH!\n")
		print(character_.name.upper() + ": " + character_.catch_phrase)
		while self.health>0 and character_.health>0:
			print("\nHEALTH:", self.health)
			print("ENEMY HEALTH:", character_.health)
			rr = input("Press [ENTER] to attack.")
			character_.hit(self.weapon_damage)
			self.hit(np.random.randint(1,character_.damage+1))
			print(character_.name + " hit you.")
			print("You hit him back.")
		if self.health <=0:
			print("Your health is now 0. "+character_.name+" has killed you.")
			time.sleep(6)
			lose()
		elif character_.health <=0:
			print("\nYou won the fight.\nHEALTH:", self.health,"\n")
			if JJ == True:
				print("JAR JAR: How wude of him!\n\n\n")
				time.sleep(5.7)
			print()
			return "Victory"
	def trade(self, character_, thing):
		if "bread" in self.fanny_pack or "water" in self.fanny_pack:
			print(character_.name, " would like to trade a " + thing.name + " for bread.")
			print("You currently have", self.fanny_pack.count('bread'), " breads in your fanny pack.")
			choice = input("Reply 'yes' or 'no'.  ")
			if choice.lower() == "yes":
				self.fanny_pack.append(thing)
				self.fanny_pack.remove("bread")
				print(thing.name.title(),"has been added to your fanny pack. You may use this on the final planet, whatever that is. \n")
				time.sleep(.5)
		else:
			pass
	def fanny(self):
		f = ", ".join([i.name for i in self.fanny_pack if type(i) != str])
		print("Your fanny pack contains: " + f +".")


class character:
	def __init__(self, nam, weapo, damag, catch_phras, heal):
		self.name = nam
		self.weapon = weapo
		self.damage = damag
		self.catch_phrase = catch_phras
		self.health = heal
	def hit(self, dam):
		self.health -= dam

class planet:
	def __init__(self, nam, probab, ene, mess, neighb):
		self.name = nam
		self.message =mess
		self.neighbors = neighb
		self.probability = probab
		self.characters = ene
	def disp(self):
		"""An easy way to display a planet's properties"""
		print("You arrive on "+self.name+". The planet is"+self.message)

class room:
	def __init__(self, objects, enemies, message, neighboring_rooms):
		self.objects = objects
		self.enemies = enemies
		self.message = message
		self.neighbors = neighboring_rooms
	def inspect(self):
		if self.objects != []:
			print("This room contains: " + ", ".join([i.name for i in self.objects]) + ".")
		else:
			print("This room is empty.")
	def take(self, thing, player):
		if thing in self.objects:
			self.objects.remove(thing)
			player.fanny_pack.append(thing)
			print("You added " + thing.name.lower() + " to your fanny pack.")
		else:
			while True:
				thing = input("That is not available in this room. Please try again or type 'cancel' to do something else.\n")
				if thing in self.objects:
					self.objects.remove(thing)
					player.fanny_pack.append(thing)
					print("You added " + thing.name.lower() + "to your fanny pack.")
				elif thing.lower() == "cancel":
					break
				else:
					print()
					continue
def lose():
	os.system('clear')
	print("GAME OVER.")
	print("You have lost, and Darth Vader has won. The Dark side now rules everything. People are suffering due to your shortcomings.")
	rr = input("Press [ENTER] to return to the main menu.")
	menu()
def initialize(): #starts the game and establishes the player's character.
	os.system('clear')
	print("A long time ago in a galaxy far, far away...")
	time.sleep(3)
	os.system('clear')
	print("STAR WARS! \nPrincess Leia has been captured by the nefarious Darth Vader! You have to stop him! The fate of the galaxy rests in your hands! Go forth and save her so that she can help the rebels defeat the Empire.")
	print("Select your character.")
	char = input("Would you like to play as Han Solo or Luke Skywalker? Type your choice and press [ENTER].\n")
	if char.lower() not in ["luke", "han", "luke skywalker", "han solo"]:
		while char.lower() not in ["luke", "han", "luke skywalker", "han solo"]:
			char = input("Han Solo or Luke Skywalker? Type your choice and press [ENTER].\n")
		print("Ok, " + char.title() +", enough chit-chat. Time to save the Galaxy. Be warned, it is very easy to fail your mission. Good thing this is a computer game and you can try as many times as you want. \nMay the force be with you.")
		rr = input("\n\nPress [ENTER] to continue...")
		os.system('clear')
		return char.title().split()[0]  #in case 1st and last name are used
	else:
		print("Ok, " + char +", enough chit-chat. Time to save the Galaxy. Be warned, it is very easy to fail your mission. Good thing this is a computer game and you can try as many times as you want. \nMay the force be with you.")
		rr = input("\n\nPress [ENTER] to continue...")
		os.system('clear')
		return char.title().split()[0]
def menu(): #the main menu for the game
	os.system('clear')
	print("---------------STAR WARS---------------")  
	print("The anachronous text adventure, by Manish Singh.")
	print()
	wait = input("Press [ENTER] to play.")
	os.system('clear')
	game()

def choose_one(data):
	"""Allows for an easy way to randomly decide an event."""
	return data[np.random.randint(0,len(data))]

def game():
	"""The game itself, with all levels as nested functions."""

	#Where I define all the game's enemies
	Darth_Vader = character("Darth Vader", "lightsaber", 9, "Who's your daddy?", 26)
	Wampa = character("Wampa", "claws and teeth", 4, "ROAR!", 1)
	droid = character("Battle Droid", "blaster rifle", 4, "Roger roger.", 5)
	stormtrooper = character("Stormtrooper", "blaster rifle", 4, "I've been ordered to kill you by Lord Vader. Comply and die quickly.", 10)
	Tusken = character("Sand Person", "blaster pistol", 4, "ASSDOFIANS (translation: FIGHT ME AND LOSE!)", 6)
	Wookie = character("Wookie", "he's friendly",3,None,None)
	Ewok = character("Ewok", None,None,None,None)

	#Place where I define all planets in the game
	Hoth = planet("Hoth", 1000, Wampa, " cold and snowy", ["Alderaan","Mustafar","Kashyyyk"])
	Alderaan = planet("Alderaan", 3, None, " peaceful. But suddenly, you see a green laser approaching in the sky. The planet blows up, courtesy of Darth Vader.", [])
	Mustafar = planet("the volcanic planet of Mustafar",3, None, " comletely consumed by lava. Your ship sinks into the magma.",[])
	Endor = planet("Endor",3,Ewok , " the home of the Ewoks.",["Kashyyyk"])
	Courasant = planet("Courasant", 1000, stormtrooper, " the former capital of the Republic.", ["Tatooine", "Hyperspace Teleporter", "Naboo"])
	Kashyyyk = planet("Kashyyyk", 3, Wookie, " the home of the Wookies.", ["Naboo","Hoth", "Endor"])
	Naboo = planet("Naboo", 60, droid, " birthplace of Padme Amidala and home of the Gungans.", ["Kashyyyk","Courasant","Hoth","Mustafar","Bespin"])
	Bespin = planet("Bespin", 70, stormtrooper, " the home of Lando Calrissian",['Naboo'])
	Tatooine = planet("Tatooine",100, Tusken," the birth place of Darth Vader! *gasp*", ["Courasant","Hyperspace Teleporter","Dagobah","Jakku"])
	Dagobah = planet("the Dagobah System",3,None, " resting place of the great Jedi Master Yoda",["Tatooine"])
	Jakku = planet("Jakku",53,stormtrooper," the home of Rey (remember, this game is anachronistic. She's technically not alive yet but just go with it.)",['Tatooine','Death Star'])
	hyperspace_variable = None
	Hyperspace_Teleporter = planet("The Hyperspace Teleporter!", 3,None, "... well, it's not a planet. When you press [ENTER], you will be randomly be teleported to a planet. Who knows, you may end up where you need to go! You also may teleport right back here or even teleport to your death. Good luck.", [hyperspace_variable])
	Death_Star = planet("the Death Star.", 100000000, Darth_Vader, "... THE PLACE YOU WERE SUPPOSED TO GO! Congratulations!", ['Jakku'])
	planets = {"Hoth":Hoth, "Alderaan":Alderaan, "Mustafar":Mustafar, "Endor":Endor, "Courasant":Courasant, "Kashyyyk":Kashyyyk, "Naboo":Naboo, "Bespin":Bespin, "Tatooine":Tatooine, "Dagobah":Dagobah, "Jakku":Jakku, "Hyperspace Teleporter":Hyperspace_Teleporter, "Death Star":Death_Star}

	#Where I define all items that a player will find.
	health_pack = item("hit 5", "health pack")
	gungan_juice = item("JJ Mmmmmm! Tanks for da juice! Me like!", "Gungan Juice")
	gungan_repellant = item("JJ AAAAAAAH! WHY DID YOU DO DAT??? IT STING!", "Gungan Repellant")
	crystal = item("weapon 3", "crystal")
	bomb = item("hit -2", "bomb")
	blank_item = item("","")
	items = {'health pack' : health_pack, "gungan juice" : gungan_juice, "gungan repellant" : gungan_repellant, 'crystal' : crystal, 'bomb' : bomb}

	def string_to_class(text, thing_dict):
		result = None
		for i in thing_dict:
			if thing_dict[i].name.lower() == text.lower():
				result = items[text.lower()]
			else:
				continue
		return result

	#Where I define all rooms in the Death Star.
	room_1 = room([health_pack, gungan_juice], stormtrooper, None, ["room 2"])
	room_2 = room([gungan_repellant], stormtrooper, None, ["room 1","room 3", "room 4"])
	room_3 = room([], droid, None, ["room 2"])
	room_4 = room([health_pack, crystal, bomb], stormtrooper, "Hint: room 5 has the princess.", ["room 5"])
	room_5 = room([], Darth_Vader, "You have made it to the final room.", [None])
	rooms = {"room 1":room_1, "room 2":room_2, "room 3":room_3, "room 4":room_4, "room 5":room_5}

	#Inital setup
	char = player(initialize())
	name = char.name  #will make it much easier for the rest of the code

	#Auxiliary Functions
	def travel(planet_name, planet_list, JJ):
		"""Allows a user to travel from planet to planet."""
		if JJ == True:
			print("JAR JAR: WHERE ARE WE?? OH NOOOOOOOO!")
		if planet_name.name == "The Hyperspace Teleporter!":
			print("Welcome to the Hyperspace Teleporter. You will be teleported to a random planet. Good luck!")
			k = choose_one(list(planets.keys()))
			return planets[k]
		else:
			planet_name.disp()
			print("You may travel to the following planets: " + ", ".join(planet_name.neighbors))
			choice = "dummy"
			while choice.title() not in planet_name.neighbors:
				choice = input("\nSelect a planet from the above, and type it below.\n")
			return planet_list[choice.title()]

	

	#Gameplay. Functions within this function make the most sense.

	def part1(char):
		"""This part introduces the user to the game, and presents a chance that the user dies from the start."""
		print("HEALTH: " + str(char.health))
		print("You are flying in your starfighter with " + char.partner + ". You have no idea where Darth Vader and the Princess are. You don't know where to go, and time is running out.")
		print("You start to compose a text message to Rebel Base, but you do not see an asteroid that is hurdling right toward you. " + char.partner +" tries warning you, but it's too late. You began spiraling downwards. Don't text and fly.")
		print("You have a choice here. Option 1 is to enter the escape pod, but you may not make it to a planet. Option 2 is to steer the ship near some planet, but the ship may explode or you may die in the crash. The choice is yours. \n Type [1] to enter escape pod or [2] to stay in ship.")
		c = input()
		if c=='1':
			occurance = np.random.randint(48,100)  #People should choose this one for best odds of survival.
			if occurance >= 50:  #50% odds of survival
				os.system('clear')
				part2(char, c.lower())
			else:
				print("Your escape pod never makes it to a planet.")
				rr = input("\nPress [ENTER] to continue...")
				lose()
		elif c == "2":
			occurance = np.random.randint(0,100)  #50% chance of survival
			if occurance >= 50:
				os.system('clear')
				part2(char, c.lower())
		else:
			print("Your ship crashes and you die.", char.partner,"mourns your loss.")
			rr = input("\nPress [ENTER] to continue...")
			lose()

	def part2(char, choice):
		"""Spawns the player at a random planet, displaying necessary text."""
		location = choose_one([Hoth, Courasant, Kashyyyk, Endor]) 
		hitting_counter = np.random.randint(1,3) #will have to pass this value to part 3 of the game.
		char.hit(hitting_counter) #crash landing causes damage
		print("You chose option " + choice + ". Good decision!")
		location.disp()
		time.sleep(1)
		print("Your crash landing injures you.")
		print("HEALTH: " + str(char.health))
		print("You should be happy to be alive.")
		part3(location, hitting_counter, char)

	def part3(location,hitting_counter,char):
		"""The most complex part of the game. The user must travel from planet to planet until the Death Star is found. The player is not told this."""
		char.health-= hitting_counter
		print("As a survival bonus, you have a choice. You can either add 2 to your current weapon damage, or a random number from 1 to 4 to your health. Choose wisely.")
		bonus = input("[1] for +2 weapon damage. \n[2] for +1-4 health.\n")
		if bonus == '1':
			char.weapon_plus(2)
			print("Your weapon now does", char.weapon_damage, "damage.")
		elif bonus == '2':
			char.hit(-np.random.randint(1,5))
			print("HEALTH:", char.health)
		time.sleep(1.5)
		print("\n You and "+char.partner+" find a brand new starfighter on " + location.name)
		print("You must now locate the planet where Darth Vader is holding the Princess. Good luck.")
		current_location = location
		history = []
		JJ = False	#boolean integer to represent weather Jar Jar Binks is accompanying the player on the journey. Jar Jar begins to follow the player at Naboo.
		time.sleep(3)
		while current_location != "Death Star":
			if current_location in [Mustafar, Alderaan]:
				current_location.disp()
				time.sleep(5)
				lose()
			elif current_location in [Kashyyyk, Endor]:
				print("You stumble upon a friendly " + current_location.characters.name +".")
				trade_item = np.random.choice([bomb, health_pack, crystal, health_pack, health_pack, bomb, bomb])
				char.trade(current_location.characters, trade_item)
			current_location = travel(current_location, planets, JJ)
			if current_location.name == "Naboo":
				if "Naboo" not in history:
					print("Jar Jar Binks will now accompany you on your journey. Sorry, you can't get rid of him.")
					print("JAR JAR: Meesa Jar Jar Binks! Meesa your humble servant! \n\n")
					JJ = True
				else:
					print()
			history.append(current_location.name)
			if current_location in [Jakku, Tatooine,Courasant,Naboo,Bespin,Hoth]:
				if np.random.randint(1,current_location.probability) > 50:
					char.fight(current_location.characters, JJ)
				else:
					continue
			if current_location is Death_Star:
				break
		part4(char, char.health, history, JJ)

	def part4(char, health, hist, J):
		"""The player naviages the Death Star to locate Vader and the Princess."""
		#On to the rest of the game...
		os.system('clear')
		history = hist
		JJ = J
		if JJ is True:
			print("JAR JAR: MEESA SCARED")
			print("JAR JAR: WAT IS DIS METAL TING WE JUST GOT INTO?!?! WEESA GONNA DIE!!")
		time.sleep(2)
		os.system('clear')
		print("Welcome to the Death Star. You will travel from room to room until you find Darth Vader and the Princess.")
		print("When you enter a room, you may type 'inspect' to see what items you may add to your fanny pack and what rooms you can enter from your current one, and then type 'take <item>' to add it to your fanny pack.")
		print("Type 'fanny' to see the items in your fanny pack. When you want to use an item, simply type 'use <item>' and you will use it.")
		print("To travel to a different room, type 'go <room>'.")
		rr = input("\nPress [ENTER] to continue.")
		print("\n\n")
		print("You are now in the landing hangar.")
		current_room = room_1
		while True:
			choice = input("What would you like to do?   ")
			if choice.lower() == 'inspect':
				current_room.inspect()
				print("You may travel to ", ", ".join(current_room.neighbors), "\n")
				continue
			elif choice[0:4].lower() == 'take':
				thing = string_to_class(choice[5:], items)
				if thing != None:
					current_room.take(thing, char)
					print()
				else:
					print("Error in taking that object. \n")
				continue
			elif choice[0:3].lower() == 'use':
				thing = string_to_class(choice[4:], items)
				if thing != None:
					if thing in char.fanny_pack:
						char.use(thing, JJ)
					else:
						print("You must take an item before you use it.")
				else:
					print("Sorry, item does not exist. \n")
				continue
			elif choice[0:2].lower() == 'go':
				if choice[3:] in current_room.neighbors:
					current_room = rooms[choice[3:].lower()]
					print("\nYou are now in " + choice[3:] + ".")
				else:
					print("Sorry, can't travel there.")
			elif choice[0:5].lower() == "fanny":
				char.fanny()
			else:
				print("That is not a valid command.")
			if current_room == room_4:
				print("You hear mechanic breathing. You must be getting close.")
			if current_room == room_5:
				break
		os.system('clear')
		print("Loading final battle... ")
		time.sleep(4)  #for aesthetic purposes
		os.system('clear')
		print("You have travelled to all these places: " + ", ".join(history) + ". You have escaped death by the hair on this journey. This is what it all comes down to.")
		rr = input("Press [ENTER] to enter the final battle.")
		char.fight(Darth_Vader, JJ)
		print("YOU WIN!!! CONGRATULATIONS!!!")
		time.sleep(3)
	part1(char)
	credits()

def credits():
	"""Credits. Just for fun."""
	os.system('clear')
	cred = ["-------STAR WARS-------", "The anachronous adventure.", "", "", "Produced by Manish Singh", "Produced for INFO W18", "Teacher: Chris Llop", "Summer, 2016"]
	for credit in cred:
		print(credit, "\n")
		time.sleep(.5)
	time.sleep(3)
	menu()


#Now, to play the game:
menu()