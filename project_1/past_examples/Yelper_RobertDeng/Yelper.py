import rauth
import json
import math
import sys
import os
from datetime import datetime, timedelta, time
from pandas.io.json import json_normalize
import pandas as pd
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

class menuPrompt():
    def __init__(self):
        """Sets up the API Keys and intro prints"""
        #Don't show traceback errors for good UI        
        sys.tracebacklimit = 0

        #Key Setup
        self.__consumer_key = '--pC7dWY8GpTHvZrKcgbTA'
        self.__consumer_secret = 'PvcLYiyFpBVlkr52w0Fa0ZpsZpA'
        self.__token = '72c5s14EN7EYamz0i35seYjaNVYiAJm2'
        self.__token_secret = '0hW44AqzAzPGY2MMOOytJihPM6k'
        
        self.session = rauth.OAuth1Session(consumer_key = self.__consumer_key, 
        consumer_secret = self.__consumer_secret, 
        access_token = self.__token,
        access_token_secret = self.__token_secret)
        
        #Personal name
        self.personalName = str(input("What's your name? "))
        
        print(str("**********************************************************************************************************"))
        print("""
        
                   `..`                                                                                     
             `:/osyyyyy.                                                                                    
            `yyyyyyyyyy-                                                                                    
            `-syyyyyyyy:                                                         ``                         
              .oyyyyyyy+                                                       .dmms                        
               `/yyyyyyo                                                       :mmmd                        
                `:yyyyys       :so:        `           .`        `....`        :mmmd      -:`  `---.        
                  .syyyy     `oyyyyo.    -dmmo       .dmmo    -sdmmmmmmho`     :mmmd     ymmmsdmmmmmmy:     
                   `+yyy`   -syyyyyyy.   -mmmms      hmmm+   ommmhssydmmmd-    :mmmd     hmmmmmmmyooymmo    
          :o+/-`    `-/-  `+yyyyyyyyy/    :mmmms    /mmmh   /mmh.     smmmh    :mmmd     hmmmmmd`    /mm.   
         `yyyyyys+:-`     -syso+/:-.`      /mmmmy` `dmmm.   ymms//////ommmm`   :mmmd     hmmmmmo      mm/   
         -yyyyyyyyyyo      ```              /mmmmh`smmmo    hmmmmmmmmmmmmmm`   :mmmd     hmmmmm/      dm+   
         .yyyyyyso/:`      .:-.              /mmmmdmmmh     ymmms--------.`    :mmmd     hmmmmmo     `mm:   
         `:+/:.``   `//-   syyyys+/-.         /mmmmmmm-     /mmmd-    .+hh:    :mmmd     hmmmmmm:   `smm`   
                   :syyy   .syyyyyyyys         /mmmmmo       ommmmdyydmmmm/    :mmmd     hmmmmmmmmddmmm:    
                 .oyyyyy    `+yyyyyys.          +mmmd`        .ohmmmmmdy+.     .dmms     hmmmssdmmmmy+`     
               `+yyyyyyy     `/yyyy+`       ./++dmmm:             ```            ``      hmmm/   ``         
               :yyyyyyyy      `-+/.         mmmmmmm/                                     hmmm/              
               ``-/+syyo                    `/++/:`                                      :yhs`              
                    ```                                                                                     
                                                                                                            
                                                                                                            """)
        print(str("**********************************************************************************************************"))  
        
        print(str("\n\nHey "+ self.personalName + " you awesome person you. You have just " +
                  "completed a grueling python course at the University of " +
                  "Berkeley, and it's time for a break! You just won a Data " +
                  "Science Yelp Competition and $3000! Your new Chase Sapphire " +
                  "Reserve card just gave you basically a free flight anywhere " +
                  "in the US! Now it's time to go on an adventure. AirBnb gave " +
                  "you unlimited stay for the next week. Plan the next " +
                  "X days starting from Thursday 5/4/17. \n\n"))
                  
        self.daysPlayed = int(input("How many days do you wanna play? "))
        
        print(str("**********************************************************************************************************"))
        
        print(str("\n\nHere's how to play. Simply plan your vacation itinerary " +
                  "anywhere in the US! Enter your starting activity and location." +
                  "Type quit in the what and where prompts to quit. It's currently " +
                  "Thursday 9AM. Enter your starting activity and location\n\n"))
                  
        print(str("**********************************************************************************************************"))
        
    def ask(self):
        """Prompts user asking for yelp food/restuarant and location queries"""
        self.term = str(input("What are you looking for? (Coffee, Restaurants, Museums, Bars) "))
        if self.term.lower() == 'quit':
                sys.exit()
        self.destination = str(input("Where are you looking to go? (Neighborhood, City or City, State) "))
        if self.destination.lower() == 'quit':
                sys.exit()
                
                
        #Request/JSON
        self.request = self.session.get("http://api.yelp.com/v2/search", params={'term': self.term,'location': self.destination})
        self.request = self.request.json()
        
        #Dataframing
        self.menu = json_normalize(self.request['businesses'])
        self.menu.index = list(range(1, 21))
        self.menu = self.menu[['name', 'categories', 'location.address', 'location.city', 'location.coordinate.latitude', \
                               'location.coordinate.longitude', 'review_count', 'rating', 'snippet_text']]\
                               .sort_values(['rating'], ascending=False).sort_index()

    def menuPrint(self):
        """Prints subset of total menu and confirms with the user this is what they're looking for"""
        print(self.menu[['name', 'review_count', 'rating']].sort_values(['rating'], ascending = False).sort_index())
        
        menuCheck = str(input("\nIs this what you're looking for? (Yes (y) or No (n)) "))
        #If no, prompt ask question again
        while menuCheck not in ['yes', 'y']:
            menuPrompt.ask(self)
            print(self.menu[['name', 'review_count', 'rating']].sort_values(['rating'], ascending = False).sort_index())
            menuCheck = str(input("\nIs this what you're looking for? (Yes (y) or No (n)) "))
            
    def menuSelection(self):
        """Allows user to select the index of the menu"""
        
        self.selection = int(input("\nWhere do you want to go? Make a selection: "))
        
        while self.selection not in self.menu.index:
                self.selection = int(input("\nWhere do you want to go? Make a selection: "))
                   
        menuCheck = str(input(str("\n" + self.menu.ix[self.selection]['name']) + " eh? I hope it's good, People say: " + \
                                      str(self.menu.ix[self.selection]['snippet_text']) + "\n\nIs this where you want to go? (Yes (y) or No (n)) "))
        while menuCheck.lower() not in ['yes', 'y', 'no', 'n']:
            menuCheck = str(input(str("\n" + self.menu.ix[self.selection]['name']) + " eh? I hope it's good, People say: " + \
                                      str(self.menu.ix[self.selection]['snippet_text']) + "\n\nIs this where you want to go? (Yes (y) or No (n)) "))
        
        os.system('clear')
        
class restauranteur(menuPrompt):
    def __init__(self):
        
        super().__init__()
        super().ask()
        super().menuPrint()
        super().menuSelection()
        
        self.yelpname = self.menu.ix[self.selection]['name']
        self.rating = self.menu.ix[self.selection]['rating']
        self.snippet = self.menu.ix[self.selection]['snippet_text']
        self.categories = self.menu.ix[self.selection]['categories']
        self.address = self.menu.ix[self.selection]['location.address']
        self.latitude = self.menu.ix[self.selection]['location.coordinate.latitude']
        self.longitude = self.menu.ix[self.selection]['location.coordinate.longitude']
        
        
        self.wallet = 3000
        self.stomach = [self.categories[0][0]]
        
        self.placesBeen = [self.yelpname]
        self.satisfactionScores = [int(self.rating)]
        
        self.historicalLocation = []
        self.previousLocation = [self.longitude, self.latitude]
        self.historicalLocation.append(self.previousLocation)
        
        self.time = datetime(2017, 5, 4, 11, 0, 0)#.strftime("%m/%d/%Y %I:%M %p")
        
        #Restaurant or Activity Categories
        self.heavyFoods = ['Steakhouse', 'Desserts', 'Donuts', 'Ice Cream & Frozen Yogurt', 'Burgers', 'Barbeque', \
                          'American (New)', 'American (Traditional)', 'Buffets', 'Mexican', 'Cupcakes', 'Desserts', \
                          'Asian Fusion', 'Breakfast & Brunch', 'Cheesesteaks', 'Chicken Shop', 'Chicken Wings', \
                          'Comfort Food', 'Fish & Chips', 'Hot Pot', 'Italian', 'Ramen', 'Japanese Curry', 'Korean', \
                          'Pizza', 'Noodles', 'Soul Food', 'Southern', 'Tex-Mex', 'Thai', 'Waffles']
                      
        self.healthFoods = ['Acai Bowls', 'Bagels', 'Farmer\'s Market', 'Kombucha', 'Juice Bars & Smoothies', 'Organic Stores', 'Poke', \
                           'French', 'Greek', 'Gluten-Free', 'Halal', 'Japanese', 'Mediterranean', 'Soup', 'Seafood', 'Salad', 'Sushi Bars', \
                           'Sandwiches', 'Tapas Bars', 'Tapas/Small Plates', 'Vietnamese', 'Wraps', 'Vegetarian', 'Vegan', 'Vitamins & Supplements']
        
        self.snacks = ['Bubble Tea', 'Bakeries', 'Coffee Roasteries', 'Gelato', \
                      'Ice Cream & Frozen Yogurt', 'Patisserie/Cake Shop', 'Pretzels', \
                      'Shaved Ice', 'Shaved Snow', 'Cafes', 'Creperies', 'Fondue']
                  
        self.ethnic = ['Asian Fusion', 'Argentine', 'Australian', 'Bangladeshi', 'Belgian', \
                      'Brazillian', 'Burmese', 'Cajun/Creole', 'Cambodian', 'Caribbean', \
                      'Dominican', 'Haitian', 'Puerto Rican', 'Trinidadian', 'Chinese', \
                      'Cantonese', 'Dim Sum', 'Szechuan', 'Cuban', 'Filipino', 'Indian', \
                      'Indonesian', 'Irish', 'Teppanyaki', 'Izakaya', 'Tacos', 'Middle Eastern', \
                      'Lebanese', 'Egyptian', 'Mongolian', 'Malaysian','Pakistani', \
                      'Persian/Iranian', 'Peruvian', 'Polish', 'Singaporean', 'Spanish', \
                      'Sri Lankan', 'Taiwanese', 'Turkish']
                  
        self.activeLife = ['ATV Rentals/Tours', 'Amateur Sports Teams', 'Archery', 'Beaches',\
                          'Baseball Fields', 'Basketball Courts', 'Batting Cages', 'Bike Rentals',\
                          'Boating', 'Bowling', 'Bocce Ball', 'Bubble Soccer', 'Bungee Jumping',\
                          'Climbing', 'Disc Golf', 'Diving', 'Escape Games', 'Fishing', \
                          'Fitness & Instruction', 'Barre Classes', 'Boxing', ' Dance Studios', 'Gyms', \
                          'Martial Arts', 'Brazillian Jiu-Jitsu', 'Karate', 'Kickboxing', 'Muay Thai', \
                          'Taekwondo', 'Pilates', 'Yoga', 'Hiking', 'Go Karts', 'Golf', 'Mini Golf', \
                          'Gun/Rifle Ranges', 'Hot Air Balloons', 'Lakes', 'Horseback Riding', \
                          'Laser Tag', 'Parks', 'Dog Parks', 'Skate Parks', 'Playgrounds', \
                          'Rock Climbing', 'Surfing', 'Tennis', 'Water Parks', 'Zoos']
                      
        self.fun = ['Arcades', 'Amuysement Parks', 'Cinema', 'Drive-In Theater', 'Outdoor Movies', \
                   'Farms', 'Ranches', 'Festivals', 'Stadiums & Arenas', 'Food Trucks', 'Pop-Up Restaurants']
               
        self.art = ['Art Galleries', 'Performing Arts', 'Paint & Sip', 'Opera & Ballet', 'Music Venues']
        
        self.museums = ['Aquariums', 'Museums', 'Art Museums', 'Botanical Gardens', 'Planetarium', \
                       'Observatories', 'Local Flavor', 'Parklets', 'Public Art']
                   
        self.therapy = ['Day Spas', 'Cosmetics & Beauty Supply', 'Hair Salons', 'Makeup Artists', \
                       'Medical Spas', 'Massage', 'Nail Salons', 'Perfume', 'Hot Springs', 'Tanning', 'Tattoo']
                   
        self.nightlife = ['Wineries', 'Beer, Wine & Spirits', 'Breweries', 'Distilleries', 'Wine Tasting Room', \
                         'Bars', 'Beer Bar', 'Champagne Bars', 'Cocktail Bars', 'Gay Bars', 'Hookah Bars', 'Irish Pub', \
                         'Lounges', 'Pubs', 'Speakeasies', 'Beer Gardens', 'Sports Bars', 'Tiki Bars', 'Whiskey Bars', \
                         'Wine Bars', 'Club Crawl', 'Comedy Clubs', 'Dance Clubs', 'Jazz & Blues', 'Karaoke', \
                         'Piano Bars', 'Pool Halls', 'Gastropubs']
        
        self.high = ['Cannabis Clinics', 'Cannabis Tours', 'Cannabis Collective', 'Canabis Dispensaries', 'Vape Shops']
        
    def askNext(self, eventHour, cost):
        self.eventHour = int(eventHour)
        self.cost = int(cost)
        #Designate the time to elapse based on the time of day
        validLoop = False
        while not validLoop:
            super().ask()
            super().menuPrint()
            super().menuSelection()

            #Things to update when considering a new location
            self.potentialYelpname = self.menu.ix[self.selection]['name']
            self.potentialCategories = self.menu.ix[self.selection]['categories']
            self.potentialAddress = self.menu.ix[self.selection]['location.address']
            self.potentialLongitude = self.menu.ix[self.selection]['location.coordinate.longitude']
            self.potentialLatitude = self.menu.ix[self.selection]['location.coordinate.latitude']
            self.potentialLocation = [self.potentialLongitude, self.potentialLatitude]
            
            #Do I want to go to this location?
            dlon = self.potentialLocation[0] - self.previousLocation[0]
            dlat = self.potentialLocation[1] - self.previousLocation[1]
            a = (math.sin(dlat/2))**2 + math.cos(self.previousLocation[1]) * math.cos(self.potentialLocation[1]) * (math.sin(dlon/2))**2 
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            
            #Food Costs
            
            #Radius of earch is 3961 miles
            self.distanceBetween = 396.1 * c
            
            #Cab cost, assuming average 30 miles per hr in most cities
            self.cabCost = 2.2 + 0.26*(self.distanceBetween/30)/60  + 1.3*self.distanceBetween 
            
            self.withinDistance = str(input(str(self.potentialYelpname) + ' at ' + str(self.potentialAddress[0]) + ' is ' +\
                                                str(round(self.distanceBetween, 2)) + ' miles away. It costs $'+\
                                                str(round(self.cabCost, 2)) + ' to cab there. Are you ok with this? '))
            
            while self.withinDistance.lower() not in ['yes', 'y', 'no', 'n']:
                self.withinDistance = str(input(str(self.potentialYelpname) + ' at ' + str(self.potentialAddress[0]) + ' is ' +\
                                                str(round(self.distanceBetween, 2)) + ' miles away. It costs $'+\
                                                str(round(self.cabCost, 2)) + ' to cab there. Are you ok with this? '))
                
            if self.withinDistance.lower() in ['yes', 'y']:
                self.previousLocation = self.potentialLocation
                self.historicalLocation.append(self.previousLocation)
                self.stomach.append(self.potentialCategories[0][0])
                self.wallet -= self.cabCost + self.cost
                self.time += timedelta(hours = self.eventHour)
                self.satisfactionScores.append(self.rating)
                self.placesBeen.append(self.potentialYelpname)
                validLoop = True
                break
                
            
    def night(self):
        self.time += timedelta(hours = 8)
        
    def dashboard(self):
        print("\nNote to self, here's what happened so far: ")
        print("\nSo far, I've been to: ", self.placesBeen)
        print("\nFrom 3,000 to now, I have $", round(self.wallet, 2), " much left.")
        print("\nSo far, I've done: ", self.stomach)
        print("\nAnd the time right now is: ", self.time.strftime("%m/%d/%Y %I:%M %p"))
        
        self.dashboardDone = str(input("\nAre you done stargazing at your amazingness?: "))
        while self.dashboardDone.lower() not in ['yes', 'y', 'no', 'n']:
            self.dashboardDone = str(input("\nAre you done stargazing at your amazingness?: "))
        if self.dashboardDone.lower() in ['yes', 'y']: 
                os.system('clear')
        
    def emoji(self):
        #Time Based Prompts to transition between meals and activities
        
        #Morning Coffee/Tea Prompt: Between 9am and 11am
        if (self.time.hour >= 7 and self.time.hour < 9):
            print("Good Morning! You can't function without coffee. Getting caffeine or tea sounds good right now.\n")
            
        if (self.time.hour >= 9 and self.time.hour < 11):
            print("I'm so down for some yoga or a run. Something to help create room for " +
                  "the mountain of food I'm eating today\n")
        
        #Lunch Prompt: Between noon and 2pm
        if (self.time.hour >= 11 and self.time.hour < 13):
            print(str("That was good, but the stomach grumbles. You want a good lunch spot. " +
                      "Maybe American or Mexican?\n"))
        
        #Afternoon Activity Prompt: between 2pm and 6pm
        if (self.time.hour >= 13 and self.time.hour < 17):
            print(str("That was satisfying. I have 4 hrs to kill. Maybe a museum, amusement park, or " +
                      "something a hike? Shopping could be good. I could get my classmates some souvenirs.\n"))
        
        #Dinner Prompt: Between 6pm and 8pm
        if (self.time.hour >= 17 and self.time.hour < 19):
            print(str("Wow that was awesome! Dinner beckons. Maybe I deserve a nice steak or chilean sea bass. " +
                      "Or something cultural?\n"))
            
        #Evening Activity Prompt: Between 8 and midnight
        if (self.time.hour >= 19 and self.time.hour < 22):
            print(str("Tonight's the night we go out! Let's look up some good bars and lounges. " +
                      "A few friends reached out and said they'd come out too.\n"))
            
        #Bedtime Prompty
        if (self.time.hour >= 22 and self.time.hour < 23):
            print(str("Yawnz. It's close to midnight, but I just can't keep going. " +
                      "Time to hit the AirBNB ... Getting old. zzzZZzzz "))
        
        #Activity Based Prompts to transition between meals and activities

        #If the most recent activity was heavy food, print food coma
        if self.stomach[len(self.stomach)-1] in self.heavyFoods:
            print("\nI feel like a donut .. I need a nap\n")
            
        if self.stomach[len(self.stomach)-1]in self.healthFoods:
            print("\nGood for you. We are eating our way to good looks\n")
        
        if self.stomach[len(self.stomach)-1] in self.snacks:
            print("\nSweet Tooth eh?\n")
        
        if self.stomach[len(self.stomach)-1] in self.ethnic:
            print("\nGood for you trying something cultured\n")
        
        if self.stomach[len(self.stomach)-1] in self.activeLife:
            print("\nGood for you doing something active!\n")
        
        if self.stomach[len(self.stomach)-1] in self.fun:
            print("\nI feel like a donut .. I need a nap\n")
        
        if self.stomach[len(self.stomach)-1] in self.art:
            print("\nArtsy aren't we?\n")
        
        if self.stomach[len(self.stomach)-1] in self.museums:
            print("\nCuriousity did NOT kill the cat. Exploring museums to find the soul?\n")
        
        if self.stomach[len(self.stomach)-1] in self.therapy:
            print("\nYea, I would have done something therapeutic too\n")
        
        if self.stomach[len(self.stomach)-1] in self.nightlife:
            print("\nGetting too old for this. Hangover city.\n")
        
        if self.stomach[len(self.stomach)-1] in self.high:
            print("\nMile high club\n")
            
        if self.stomach[len(self.stomach)-1] == 'Coffee & Tea':
            print("\nWide awake now. I can write a 300 line project like it's nothing!\n")
    
    def endGame(self):
        print("\nWow time flies when you're having fun, spending imaginary money, "+
              "and destroying data science challenges. Here's the recap of what you did: ")
              
        print("\nYou are extremely accomplished, here's a list of places you've been: ", self.placesBeen)
        print("\nYou managed to save $", round(self.wallet, 2), " much after all that spending!")
        print("\nThe time you concluded your Yelp extravaganza is: ", self.time.strftime("%m/%d/%Y %I:%M %p"))
        print("\nPlease play again!")
            
#######################################################################################################################
#########################################    Running the Actual Game   ################################################
#######################################################################################################################

#While loop timing

Player = restauranteur()

while Player.time < datetime(2017, 5, 3 + Player.daysPlayed, 23, 30):
    #Lunch Time, start at 11am
    Player.emoji()
    Player.askNext(2, 30)
    Player.dashboard()
    
    #Afternoon Activity, start at 1pm
    Player.emoji()
    Player.askNext(4, 25)
    Player.dashboard()
    
    #Dinner Time, start at 5pm
    Player.emoji()
    Player.askNext(2, 45)
    Player.dashboard()
    
    #Evening Activity, start at 7pm
    Player.emoji()
    Player.askNext(4, 100)
    Player.dashboard()
    
    #Sleep 8 hrs, start at 11pm
    Player.night()
    
    #Wake up, get coffee / run or walk in the park
    Player.emoji() #Morning Coffee, Wake up at 7
    Player.askNext(2, 5)
    Player.dashboard()
    
    #Just had morning coffee, Time for Morning Activity at 9
    Player.emoji()
    Player.askNext(2, 20)
    Player.dashboard()

Player.endGame()