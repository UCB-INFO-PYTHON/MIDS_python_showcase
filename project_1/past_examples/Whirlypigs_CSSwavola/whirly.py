class Fan():

    fans=[]

    def __init__(self,position):
        self.operate=False
        self.name=len(Fan.fans)
        self.oldpos=position
        self.newpos=position
        self.oldpower=5
        self.newpower=5
        self.mobile=2
        Fan.fans.append(self)

    def mobility(self,power):
        #unused....
        if power>=2:
            return 2
        else:
            return power

    def fanop(self,phrase):
        operate={'#':True,"X":False}
        self.newpower=self.oldpower
        if '#' in phrase:
            self.operate=True
        elif 'X' or 'x' in phrase:
            self.operate=False
        else:
            self.operate=self.operate
        if self.operate:
            self.newpower=self.oldpower-1
        newphrase=""
        for i in phrase:
            if i not in 'X#x':
                newphrase+=i
        return newphrase

    def recharge(self):
        self.oldpower+=4
        if self.oldpower>12:
            self.oldpower=12

    def pos(self, phrase):
        sym={"<":-1,">":1}
        dpos=0
        for i in phrase:
            if i in sym.keys():
                dpos=dpos+sym[i]
            else:
                continue
        dirphrase=""
        if dpos ==0:
            phrase="The fan is perfectly happy where it is."
            dirphrase="units moved"
        else:
            phrase="The fan has been moved"
        if dpos>0:
            dirphrase="to the right"
        elif dpos<0:
            dirphrase="to the left"
        self.newpos=self.oldpos+dpos
        self.newpower=self.newpower-abs(self.newpos-self.oldpos)
        #new power already decreased by power operator
        print(phrase,abs(dpos),dirphrase)
        return(self.newpos)


#pig class
class Pig():
    pignames={'bessy':4, 'phil':3, 'sherman':2, 'madge':2, 'hector':6, 'virginia':5}
    num_pigs=0

    def __init__(self,name,position):
        Pig.num_pigs+=1
        self.name=name
        self.weight=Pig.pignames[name]
        self.position=position
        self.symbol=name[0]
        self.altitude=10

    def lift(self,modifier):
        dalt=round((10-self.weight)/(2*modifier))
        self.altitude+=dalt
        if self.altitude>10:
            self.altitude=10

    def fall(self):
        self.altitude-=1


#    pigs={bessy:4, phil, sherman, madge, hector, virginia}


#gameplay class
class Game():

    def __init__(self,name):
        self.name=name
        self.play=True
        self.turncount=0
        self.pigs={}
        self.airpigs=0
        self.startpigs=0

    def boardprint(self,fanlist):
        print("\n\n\n")
        r=10
        while r>0:
            'make rows 10-1'
            print("|",end="")
            pos=0
            while pos<self.startpigs:
                'make col per row'
                if self.activepigs[pos].altitude==r and self.activepigs[pos].position==pos:
                    print(" ",self.activepigs[pos].symbol,end="")
                else:
                    print(" ` ",end="")
                pos+=1
            print("|")
            r-=1
        print("|",end="")
        'row 0, includes fan dock'
        pos=0
        while pos<self.startpigs:
            i=0
            while i<len(Fan.fans):
                #second i loop allows for multiple fans, maybe
                if Fan.fans[0].newpos==pos:
                    if Fan.fans[0].operate:
                        print("  #",end="")
                    else:
                        print("  X",end="")
                else:
                    if self.activepigs[pos].altitude==r and self.activepigs[pos].position==pos:
                        print(" ",self.activepigs[pos].symbol,end="")
                    else:
                        print("  -",end="")
                i+=1
            pos+=1
        if Fan.fans[0].newpos==pos:
            if Fan.fans[0].operate:
                print(" :#",end="")
            else:
                print(" :X",end="")
        else:
            print(":--",end="")
        print("|")
        print("\n")

    def gamemenu(self):
        print('To start a new game, press \'n\', or \'q\' to quit')
        gameplay=input().lower()
        if gameplay=='n':
            os.system('cls')
            gamenum='g'+str(len(gamesplayed)+1)
            activegame=Game(gamenum)
            gamesplayed[activegame.name]=0
            activegame.newgame()
        else:
            pass

    def turnread(self,phrase):
        'interpret the turn input, make it readable phrases for Fan methods'
        while len(phrase)>3 or 0>len(phrase) or  (phrase.count('#')+phrase.count('X'))>1:
            print('I can\'t follow instructions like these!')
            print("\nWhat would you like to do? ")
            phrase=input()
        powrest=0
        #estimate power to use
        for i in phrase:
            if i in '#><':
                powrest+=1
        while powrest>Fan.fans[0].oldpower:
            print('You don\'t have the power for that!')
            print("\nWhat would you like to do? ")
            phrase=input()
            powrest=0
            for i in phrase:
                if i in '#><':
                    powrest+=1

        dirphrase=Fan.fans[0].fanop(phrase)
        #returns phrase with only directionals
        return Fan.fans[0].pos(dirphrase)
        #returns position


    def turn(self):
        print("Turn",self.turncount)
        if self.turncount%5==0 and self.turncount>0:
            Fan.fans[0].recharge()
        if Fan.fans[0].oldpos==self.startpigs:
            Fan.fans[0].recharge()
        print("The fan has",Fan.fans[0].oldpower,"power left.")
        print("\n'X'-fan off (default, will turn off unless told not to)    '#'-fan on \n'>' or '<'-move fan 1 space right or left, in direction of arrow\nIf you have the power, you can move twice as far! ('>>' or '<<')")
        print("\nWhat would you like to do? ")
        turnin=input()
        if turnin.lower()=='q':
            self.gamemenu()
        else:
            fanpos=self.turnread(turnin)
            while fanpos not in range(0,self.startpigs+1):
                #fan in range
                print("Fan out of range!")
                print("\nWhat would you like to do? ")
                turnin=input()
                fanpos=self.turnread(turnin)
            self.turncount+=1
            #returns new position of fan
            for i in self.activepigs:
                if Fan.fans[0].operate:
                    if i.position!=fanpos and i.position not in range(Fan.fans[0].newpos,Fan.fans[0].oldpos):
                        #untouched by fan
                        i.fall()
                    elif i.position==fanpos:
                        #directly above fan
                        i.lift(1)
                    elif i.position in range(Fan.fans[0].newpos,Fan.fans[0].oldpos) and i.position!=fanpos:
                        #in fan sweep
                        i.lift(abs(Fan.fans[0].newpos-Fan.fans[0].oldpos))
                else:
                    i.fall()
                if i.altitude==0:
                    self.play=False
        Fan.fans[0].oldpos=Fan.fans[0].newpos
        Fan.fans[0].oldpower=Fan.fans[0].newpower
        self.boardprint(Fan.fans)
        self.gameon()


    def newgame(self):
        print('Game',self.name,"\nType 'q' to quit")
        while type(self.startpigs) is not int or self.startpigs==0:
            try:
                inp=input("How many pigs are there on the farm? ")
                if int(inp)>6:
                    raise ValueError
                self.startpigs=int(inp)
                self.airpigs=int(inp)
            except ValueError:
                if inp.lower()=='q':
                    end()
                else:
                    print("Please enter an integer less than 7. ",end="")
        print(self.startpigs,"pigs!\nThat may be a lot, but this old catapult's still got some life in her!\n")
        #generate pigs
        namelist=random.sample(Pig.pignames.keys(),self.startpigs)
        'generates a list of names, which are strings. activepigs is a list of the objects created.'
        j=0
        self.activepigs=[]
        for i in namelist:
            i=Pig(i,j)
            j+=1
            self.activepigs.append(i)
        for i in self.activepigs:
            print ("It takes",i.weight,"clicks of the catapult to launch",i.name+".")
        Fan.fans=[]
        f0=Fan(0)
        print("\nAnd of course, let's push out our trusty fan. We call it the \'Hashtag\' fan, because it looks just like one when it's on!\nIt'll recharge itself, but just in case there's a spot on the East side of the farm to boost it.\n")
        self.boardprint(Fan.fans)
        self.gameon()


    def gameon(self):
        if self.play is False:
            gamesplayed[self.name]=self.turncount
            print("You kept the pigs up for ",self.turncount," turns!")
            for i in gamesplayed.keys():
                print (i," - ",gamesplayed[i])
            self.gamemenu()
        elif self.play:
            self.turn()




#start script
import os
import random
import time
gamesplayed={}
os.system('cls')
print("\n\nWelcome to Whirlypigs Farm!")
time.sleep(3)
print("\n\nWe find that our pigs are happiest when they're floating!")
time.sleep(1)
print("So, every once in a while we launch them up, with their special piggy parachutes,")
time.sleep(1)
print("and keep them up there for as long as we can with our trusty super-fan.")
time.sleep(3)
print("\n...Truthfully, it's more of an aircannon...but hey, they love it!\n")
print('To start a new game, press \'N\', or \'q\' to quit')
gameplay=input().lower()
if gameplay=='n':
    os.system('cls')
    gamenum='g'+str(len(gamesplayed)+1)
    activegame=Game(gamenum)
    gamesplayed[activegame.name]=0
    activegame.newgame()
else:
    pass
