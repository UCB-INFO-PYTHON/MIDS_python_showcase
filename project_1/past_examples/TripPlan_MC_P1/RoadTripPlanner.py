# Programmer: Muying Chen
# Project Name: West Coast Road Trip Planner
# Project Description: The purpose of this program is to create a road trip
#   planner for users who will be travelling in West Coast major cities based
#   on the entered information such as budget and preferred activities.
#   (Unfortuately, users could only choose cities between SF, LA, LV, PO, SE
#   & SD at this time)

class Route:
    """Route class contains information about the starting city and ending city
    of each route. Each object also contains distance in miles for the route
    and the weather of the destination."""
    startcity = ""
    endcity = ""
    distance = 0.0
    weather = ""

    def __init__(self, startcity, endcity, distance, weather):  # initializer
        self.startcity = startcity
        self.endcity = endcity
        self.distance = distance
        self.weather = weather

    def get_startcity(self):   # return startcity of a route object
        return self.startcity

    def get_endcity(self):   # return endcity of a route object
        return self.endcity

    def get_distance(self):   # return distance of a route
        return self.distance

    def get_weather(self):   # return expected weather of a route
        return self.weather

class Hotel:
    """Hotel class contains information about the hotel that the users choose
    to stay during the trip. It contains name, description, price per night."""
    name = ""
    description = ""
    price = 0.0

    def __init__(self, name, description, price):   # initializer
        self.name = name
        self.description = description
        self.price = price

    def get_name(self):   # return user selected hotel name
        return self.name

    def get_description(self):   # return hotel description
        return self.description

    def get_price(self):  # return user selected hotel price
        return self.price

    def print_hotel(self): # print hotel information
        print("Hotel name:", self.get_name())
        print("Hotel description:",self.get_description())
        print("Hotel price: $", self.get_price(), "per night")

class Car:
    """Car class contains information about the car that the users choose
    to rent during the trip. It contains the car brand name, price per day,
    and milage informaiton."""
    name = ""
    information = ""
    price = 0.0
    milage = 0.0

    def __init__(self, name, information, price, milage):   # initializer
        self.name = name
        self.information = information
        self.price = price
        self.milage = milage

    def get_name(self):   # return car brand name
        return self.name

    def get_information(self):   # return car informaiton
        return self.information

    def get_price(self):   # return car rental price
        return self.price

    def get_milage(self):   # return car milage
        return self.milage

    def print_car(self):   # print car information
        print("Car brand:",self.get_name())
        print("Car information:",self.get_information())
        print("Car price: $", self.get_price(),"per day")
        print("Car milage: ", self.get_milage(), "mpg")

class Activities:
    """Activities class contains the information about tourist attractions in
    the destination of each route. This class includes the name, price, and
    description of the activities to display to users."""
    name = ""
    unitprice = 0.0
    description = ""
    totalcost = 0.0

    def __init__(self, name, unitprice, description): # initializer
        self.name = name
        self.unitprice = unitprice
        self.description = description

    def get_name(self):   # return the name of the activity
        return self.name

    def get_unitprice(self):   # return the unit price of the activity
        return self.unitprice

    def get_description(self):   # return a short description of the activity
        return self.description

    def print_activities(self):   # print information about such activities
        print("Activity Name:", self.name)
        print("Cost per person: $", self.unitprice)
        print("Description:", self.description)

class Budget:
    """Budget class contains the information about the user's budget depending
    on the selection of activities and necessities. Such information will be
    displayed to users."""
    budget = 0.0
    remaining = 0.0

    def __init__(self, budget):   # initializer
        self.budget = budget

    def get_butget(self):  # return the budget/current budget
        return self.budget

    def calculate_new_budget(self, spending):  # calculate new budget
        remaining = self.budget - spending
        if remaining <= 0:
            while True:
                print("Your budget is not enough for the trip. Please enter a new budget larger than", spending)
                new_budget = int(input("Enter your new budget: "))
                if new_budget > spending:
                    self.budget = new_budget - spending
                    break
        else:
            self.budget = remaining

#############################################
#                 Database                  #
#############################################
# Create West Coast route database and a list of these routes
r1 = Route("San Francisco", "Seattle", 808, "Gloomy")
r2 = Route("San Francisco", "Los Angeles", 383, "Sunny")
r3 = Route("San Francisco", "Portland", 636, "Rainy")
r4 = Route("San Francisco", "Las Vegas", 569, "Dry")
r5 = Route("San Francisco", "San Diego", 502, "Sunny")
r6 = Route("Los Angeles", "San Francisco", 383, "Foggy")
r7 = Route("Los Angeles", "San Diego", 120, "Sunny")
r8 = Route("Los Angeles", "Seattle", 1135, "Gloomy")
r9 = Route("Los Angeles", "Portland", 963, "Rainy")
r10 = Route("Los Angeles", "Las Vegas", 269, "Dry")
r11 = Route("Las Vegas", "San Francisco", 569, "Foggy")
r12 = Route("Las Vegas", "Los Angeles", 269, "Sunny")
r13 = Route("Las Vegas", "Seattle", 1125, "Gloomy")
r14 = Route("Las Vegas", "San Diego", 332, "Sunny")
r15 = Route("Las Vegas", "Portland", 966, "Rainy")
r16 = Route("San Diego", "San Francisco", 502, "Foggy")
r17 = Route("San Diego", "Los Angeles", 120, "Sunny")
r18 = Route("San Diego", "Portland", 1083, "Rainy")
r19 = Route("San Diego", "Las Vegas", 332, "Dry")
r20 = Route("San Diego", "Seattle", 1255, "Gloomy")
r21 = Route("Seattle", "San Francisco", 808, "Foggy")
r22 = Route("Seattle", "Los Angeles", 1135, "Sunny")
r23 = Route("Seattle", "San Diego", 1255, "Sunny")
r24 = Route("Seattle", "Las Vegas", 1125, "Dry")
r25 = Route("Seattle", "Portland", 173, "Rainy")
r26 = Route("Portland", "Seattle", 173, "Gloomy")
r27 = Route("Portland", "San Francisco", 636, "Foggy")
r28 = Route("Portland", "Los Angeles", 963, "Sunny")
r29 = Route("Portland", "San Diego", 1083, "Sunny")
r30 = Route("Portland", "Las Vegas", 966, "Dry")
route_list = [r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,
    r18,r19,r20, r21, r22,r23,r24,r25,r26,r27,r28,r29,r30]

# Create activities database and store it in activity list for each city
SE1 = Activities("Space Needle", 25.0, "Observation Tower and Landmark")
SE2 = Activities("Pike Place Market", 0.0, "Markets, Seafood, Engagement")
SE3 = Activities("Waterfront Park", 0.0, "Views, Sculptures, Boardwalk")
SE4 = Activities("Museum of Flight", 21.0, "Airplanes and Space Vehicle Exhibits")
SE5 = Activities("Chihuly Garden and Glass", 15.0, "Indoor and Outdoor works by Dale Chilhuly")
LA1 = Activities("Universal Studio Hollywood", 80, "Movie-themed Amusement Park")
LA2 = Activities("Hollywood Walk of Fame", 0.0, "Honoring Entertainment Stars")
LA3 = Activities("Disneyland", 110, "Amusement Park with 8 Themed Lands")
LA4 = Activities("Santa Monica State Beach", 0.0, "Beach and Sunshine")
LA5 = Activities("Griffith Observatory", 20.0, "Planetarium and City Views")
SF1 = Activities("Golden Gate Bridge", 0.0, "Iconic Bridge and Landmark")
SF2 = Activities("Golden Gate Park", 40.0, "Gardens, Trails, Museums")
SF3 = Activities("Alcatraz Island", 30.0, "Notorious Prison and Historical Attractions")
SF4 = Activities("Lombard Street", 0.0, "Famous Crooked Street")
SF5 = Activities("Fisherman's Wharf", 50.0, "Sea Lions, Seafood, Museums")
LV1 = Activities("Bellagio", 100.0, "Resort and Shopping")
LV2 = Activities("Freemond Street Experience", 100.0, "Open-air Mall")
LV3 = Activities("Casinos", 500.0, "Risk 'n Gamble")
LV4 = Activities("UNLV", 0.0, "University of Nevada, Las Vegas Campus")
LV5 = Activities("Red Rock Canyon National Park", 7.0, "Views and 13-mile Drive ")
SD1 = Activities("SeaWorld", 100.0, "Aquatic Theme Park")
SD2 = Activities("San Diego Zoo", 30.0, "Zoo and Safari Park")
SD3 = Activities("Maritime Museum of San Diego", 30.0, "Meseum")
SD4 = Activities("La Jolla Cove", 0.0, "Ideal for Swimming and Scuba")
SD5 = Activities("Belmont Park", 70.0, "Beachside Amusement Park")
PO1 = Activities("Washington Park", 15.0, "Park with Zoo and Rose Garden")
PO2 = Activities("Forest Park", 0.0, "Wooded Area with Trails")
PO3 = Activities("Lan Su Chinese Garden", 20.0, "Serene Botanical Oasis")
PO4 = Activities("Pioneer Courthouse Square", 0.0, "Plaza with Music Performance")
PO5 = Activities("Hoyt Arboretum", 3.0, "Forested Park with Trails and Rare Trees")
Seattle_Activities = [SE1, SE2, SE3, SE4, SE5]
LosAngeles_Activities = [LA1, LA2, LA3, LA4, LA5]
SanFrancisco_Activities = [SF1, SF2, SF3, SF4, SF5]
LasVegas_Activities = [LV1, LV2, LV3, LV4, LV5]
SanDiego_Activities = [SD1, SD2, SD3, SD4, SD5]
Portland_Activities = [PO1, PO2, PO3, PO4, PO5]

# Create hotel and car rental database for users to choose and to make a list
h1 = Hotel("Four Seasons", "5-star", 489.0)
h2 = Hotel("Marriott", "4-star", 199.0)
h3 = Hotel("Hilton", "4-star", 159.0)
h4 = Hotel("Crowne Plaza", "3-star", 119.0)
h5 = Hotel("Holiday Inn", "2-star", 109.0)
h6 = Hotel("Motel", "Quick and cheap", 69.0)
h7 = Hotel("Airbnb", "Comfortable", 79.0)
hotel_list = [h1, h2, h3, h4, h5, h6, h7]

c1 = Car("Ford Focus or similar", "Compact 5 Passengers", 30.0, 30.0)
c2 = Car("Toyota Corolla or similar", "Intermediate 5 Passengers", 32.0, 35.0)
c3 = Car("Toyota Yaris or similar", "Economy 5 Passengers", 35.0, 35.0)
c4 = Car("Jeep Compass or similar", "SUV 5 Passengers", 50, 20.0)
c5 = Car("Dodge Challenger or similar", "Sports 5 Passengers", 40.0, 20.0)
c6 = Car("Toyota Sienna or similar", "Van 7 Passengers", 60.0, 250)
car_list = [c1, c2, c3, c4, c5, c6]

#############################################
#          Facilitating Functions           #
#############################################
def return_city(n):
    """return the string for the city based on numbers(from 1 to 6)"""
    if n == 1:
        return "San Francisco"
    elif n == 2:
        return "Los Angeles"
    elif n == 3:
        return "Las Vegas"
    elif n == 4:
        return "Portland"
    elif n == 5:
        return "San Diego"
    else:
        return "Seattle"

def return_route(start, end, r_list):
    """Return the route from route_list with correct start city and end city"""
    for i in range(len(r_list)):
        if r_list[i].get_startcity() == start and r_list[i].get_endcity() == end:
            return r_list[i]
    return "Error"

def return_activity(end):
    """return activity list based on destination"""
    if end == "Seattle":
        return Seattle_Activities
    if end == "San Francisco":
        return SanFrancisco_Activities
    if end == "Los Angeles":
        return LosAngeles_Activities
    if end == "Las Vegas":
        return LasVegas_Activities
    if end == "Portland":
        return Portland_Activities
    else:
        return SanDiego_Activities

def budget_for_necessities():
    """calculate new budget after user has chosen his/her hotel and car rental"""
    print("========== Displaying hotel options ==========")
    for i in range(len(hotel_list)):
        print("   -- Enter", i+1, "to choose --   ")
        hotel_list[i].print_hotel()
        print(" ")
    while True:
        try:
            hotel_num = int(input("Please choose your hotel option (Enter a number between 1 to 7): "))
            hotel_num -= 1
            if hotel_num in range(len(hotel_list)): break
        except ValueError:
            print("Please enter an positive integer. Try again... ")
    while True:
        try:
            hotel_stay = int(input("Please enter the duration (in days) of your stay: "))
            if hotel_stay > 0: break
        except ValueError:
            print("Please enter an positive integer. Try again... ")
    user_hotel = hotel_list[hotel_num]
    user_hotel_price = user_hotel.get_price()
    user_hotel_name = user_hotel.get_name()
    # display car option and ask for user input
    print("\n======== Displaying rental car options =========")
    for i in range(len(car_list)):
        print("  -- Enter", i+1, "to choose --   ")
        car_list[i].print_car()
        print(" ")
    while True:
        try:
            car_num = int(input("Please choose your car rental option (Enter a number between 1 to 6): "))
            car_num -= 1
            if car_num in range(len(hotel_list)): break
        except ValueError:
            print("Please enter an positive integer. Try again... ")
    while True:
        try:
            car_rental_day = int(input("Please enter the duration (in days) of your car rental: "))
            if car_rental_day > 0: break
        except ValueError:
            print("Please enter an positive integer. Try again... ")
    # calculate user's total cost for car rental and hotel
    user_car = car_list[car_num]
    user_car_price = user_car.get_price()
    user_car_name = user_car.get_name()
    total_hotel_cost = hotel_stay * user_hotel_price
    total_car_rental_cost = car_rental_day * user_car_price
    print("\n=== Displaying your hotel and car rental information ===")
    print("Hotel:  ", user_hotel.get_name())
    print("Hotel total cost: $", total_hotel_cost)
    print("Car Rental:  ", user_car.get_name())
    print("Car rental total cost: $", total_car_rental_cost)
    print(" ")
    # calculate remaining budget based on hotel and car's cost and/or ask for higher budget
    user_budget.calculate_new_budget(total_hotel_cost + total_car_rental_cost)
    print(" ")
    return total_hotel_cost, total_car_rental_cost, user_hotel_name, user_car_name

def budget_for_activities(endcity, activity_list, num_traveler):  # calculate new budget
    """Calculate user's new budget after user has chosen his/her choices of activities
    in the destination"""
    # displaying activity list based on endcity
    print("====== Displaying", endcity, "activities options =====")
    for i in range(len(activity_list)):
        print("   -- Enter", i+1, "to choose --   ")
        activity_list[i].print_activities()
        print(" ")
    print("Choose the activities you like to do in", endcity)
    print("[ Enter Q or q to quit after finish]")
    # calculate activity cost with based on number of travelers
    user_chosen_activities = []
    while True:
        try:
            user_activity_num = input("Enter an activity number: ")
            if user_activity_num == 'q' or user_activity_num == 'Q' or int(user_activity_num) == 0: break
            user_activity_num = int(user_activity_num) - 1
            while activity_list[user_activity_num] not in user_chosen_activities:
                user_chosen_activities += [activity_list[user_activity_num]]
        except ValueError:
            print("Please enter a number between 1 to 5...")
    # calculate total activity cost
    total_activity_cost = 0
    for i in user_chosen_activities:
        activity_price = i.get_unitprice() * num_traveler
        total_activity_cost += activity_price
    # calculate remaining budget and/or ask for higher budget
    user_budget.calculate_new_budget(total_activity_cost)
    return total_activity_cost, user_chosen_activities

#############################################
#              User Interface               #
#############################################

print("-----------------------------------------------------------")
print("       Welcome to West Coast Road Trip Planner 1.0")
print("     Using this program, you will be able to plan your")
print("     route to travel to one of the six major West Coast")
print("     cities and plan your activities based on your budget.")
print("                  So let's get started! ")
print("-----------------------------------------------------------\n")

# start user information input
user_name = input("Please enter your name: ")
while True:
    try:
        num_traveler = int(input("Please enter the number of traveler(s): "))
        break
    except ValueError:
        print("Oops! Seems like you are not travelling with human. Try again... ")
while True:
    try:
        enter_budget = int(input("Please enter a reasonable budget for the trip: "))
        break
    except ValueError:
        print("Please bring valid amount of money to the trip. Try again... ")

user_budget = Budget(enter_budget)  # create the first budget class base on user entered information

# display possible cities to travel to/from and ask for user input
print("Please choose two of these cities as your starting city and destination: \n")
print("Enter 1 -- San Francisco   Enter 2 -- Los Angeles   Enter 3 -- Las Vegas")
print("Enter 4 -- Portland        Enter 5 -- San Diego     Enter 6 -- Seattle\n")

while True:
    try:
        startcity_num = int(input("Enter the number for starting city (between 1 to 6 only): "))
        if startcity_num in range(1,7): break
    except ValueError:
        print("Please enter a number...")
while True:
    try:
        endcity_num = int(input("Enter the number for destination (between 1 to 6 only and not equal to start city): "))
        if endcity_num in range(1,7) and endcity_num != startcity_num: break
    except ValueError:
        print("Please enter a number...")
startcity, endcity = return_city(startcity_num), return_city(endcity_num)

# return correct route information base on start city and end city
user_route = return_route(startcity, endcity, route_list)
route_distance = 2 * (user_route.get_distance())

# call budget necessities function for input and calculate new budget and total spending on car and hotel
user_hotel_cost, user_rental_car_cost, hotel_name, car_name = budget_for_necessities()
# call budget activities function for input and calculate new budget and total spending on activities
user_activity_cost, user_activities = budget_for_activities(endcity, return_activity(endcity), num_traveler)  # call budget activities function for input and new budget

######### user finish entering entering information about the trip ##########
# display all results (route information, hotel, car, activities, remaining budget)
# also display travel tips
print("\n---------- Displaying",user_name, "'s Road Trip Information ----------")
print("Your will start your trip at [", user_route.get_startcity(),"]", "with", num_traveler - 1, "accompany")
print("Your destination is [", user_route.get_endcity(), "]")
print("Your roadtrip's total distance (round-trip) is [", route_distance, "] miles")
print("The weather is expected to be [", user_route.get_weather(), "]")
print("You will be staying at[", hotel_name, "] with total cost of [ $", user_hotel_cost,"]")
print("You will be driving [", car_name, "] with total cost of [ $", user_rental_car_cost,"]")
print("The activities you chose to do with a cost of [ $", user_activity_cost, "] is (are):")
for i in user_activities:
    print("          [",i.get_name(), "]")
print("Your remaining budget to spare is [ $", user_budget.get_butget(), "]")
print("-------------------------------------------------------------------------")
print("Thank you for using Road Trip Planner 1.0. Have a safe and fun trip. :) \n")
