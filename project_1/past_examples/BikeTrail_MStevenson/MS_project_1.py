import sys
import random

# Vapor Trail Project by Matt Stevenson

# Start by defining the data classes


class Aid:
    '''Class aid describes the aid stations along the route,
    with altitude (in ft) and services (a string) described.
    '''

    def __init__(self, name, alt, services, phone):
        self.name = name
        self.alt = alt
        self.services = services
        self.phone = phone


class Section:
    '''A section of the race, with attributes start and stop
    (assigned to class "aid"), distance (dist) in miles,
    ascent and descent in feet, time in hrs, and difficulty ratings out of 5'''

    def __init__(self, name, dist, ascent, descent, ave_time,
                 max_time=None, com_diff=None, start=None,
                 end=None, bail_trail=None, map_pic=None):
        self.name = name
        self.dist = dist
        self.ascent = ascent
        self.descent = descent
        self.ave_time = ave_time
        self.max_time = max_time
        if com_diff is not None:
            if com_diff not in [1, 2, 3, 4, 5]:
                raise Exception("Difficulty range is based on an integer \
scale of 1-5, with 5 as the hardest")
        self.diff = com_diff
        self.start = start
        self.end = end
        self.bail_trail = bail_trail
        self.map_pic = map_pic

    @property
    def difficulty(self):
        return self.diff

    @difficulty.setter
    def difficulty(self, rider_diff):
        if rider_diff not in [1, 2, 3, 4, 5]:
            raise Exception("Difficulty range is based on an integer \
scale of 1-5, with 5 as the hardest")
        self.diff = (10*self.diff + rider_diff)/11
        # existing diff is weighted 10X the rider-inputted diff


class BailTrail(Section):
    '''Describes other routes by which to get down off the mountain.
    Child-class to "section"
    '''

    def __init__(self, services, phone, name, dist, ascent, descent,
                 ave_time, max_time=None, com_diff=None, map_pic=None):
        self.services = services
        self.phone = phone
        super().__init__(name, dist, ascent, descent, ave_time,
                         max_time=None, com_diff=None, map_pic=None)

# Fill in the data to match the trail map

aid_0 = Aid("Race Start", 7000, "Food, shelter, water", 9786543212)
aid_1 = Aid("First Aid", 9800, "Food, water, toilet", 9786543212)
section_1 = Section("Hard Uphill", 14.4, 2800, 0, 2.00, 3, 2, aid_0, aid_1)
aid_2 = Aid("2nd Aid", 8600, "Food, water", 9786543212)
bail_1 = BailTrail("Ambulance", 1234567890, "CO Trail bail", 4, 500, 3500, 1,
                   com_diff=4)
section_2 = Section("CO Trail", 12.7, 1000, 2200, 2.5, 3.5, com_diff=5,
                    start=aid_1, end=aid_2, bail_trail=bail_1)
aid_3 = Aid("3rd Aid", 11958, "Water, not much else", 9847361543)
bail_2 = BailTrail("Help", 32453672876, "St. Elmo bail", 5, 2000, 0, 1.5,
                   com_diff=2)
section_3 = Section("St. Elmo", 17, 3358, 0, 3.5, 5, 3, aid_2, aid_3, bail_2)
aid_4 = Aid("4rth Aid", 9274, "Food, water, drop bag", 9847361543)
bail_3 = BailTrail("Medivac", 9876543210, "Alpine Tunnel Bail", 5, 500, 2000,
                   1.5, com_diff=3)
section_4 = Section("Alpine Tunnel", 17, 1500, 4184, 3, 4, 4, aid_3, aid_4,
                    bail_3)
aid_5 = Aid("Aid 5", 11300, "Water, food, shelter, drop bag", 7867654326)
bail_4 = BailTrail("Exit to Highway 50", 4418769826, "White Pine Rd", 6, 0,
                   300, 1, com_diff=1)
section_5 = Section("Gunnison Rd", 14, 2300, 274, 2, 3.5, 2, aid_4, aid_5,
                    bail_4)
aid_6 = Aid("Aid 6", 10800, "Marshall Pass, with water, food, shelter", 911)
section_6 = Section("Monarch Crest", 10.5, 1000, 1500, 2, 3, 4, aid_5, aid_6)
aid_7 = Aid("Aid 7", 9400, "Nothing much!", 911)
bail_5 = BailTrail("Poncha Springs town", 911, "Poncha Creek Rd.", 10, 100,
                   600, 2, com_diff=2)
section_7 = Section("Starvation Creek Loop", 20, 3000, 4400, 3.5, 5, 5,
                    aid_6, aid_7, bail_5)
aid_8 = Aid("Race end", 7100, "Food, beer, people, and celebration!",
            8767656543)
bail_6 = BailTrail("Outlet on Highway 285", 9767654324, "Highway 285",
                   0, 0, 0, 0, com_diff=1)
section_8 = Section("Rainbow Trail", 20.5, 1100, 3400, 2.5, 4, 4,
                    aid_7, aid_8, bail_6)

course = [aid_0, section_1, aid_1, section_2, aid_2, section_3, aid_3,
          section_4, aid_4, section_5, aid_5, section_6, aid_6,
          section_7, aid_7, section_8, aid_8]
sections = [section_1, section_2, section_3, section_4, section_5,
            section_6, section_7, section_8]
aid_sts = [aid_0, aid_1, aid_2, aid_3, aid_4, aid_5, aid_6, aid_7, aid_8]

# define working classes


class Rider:
    '''Class that determines the position and distance, ascent and descent
    of the rider'''

    def __init__(self, sect, t_sect):
        self.sect = sect
        # current instance of class section being ridden, set by class control
        if t_sect > self.sect.ave_time:
            raise Exception("You are over the average time. \
Please reduce your estimate to below", self.sect.ave_time,
                            "hrs for this section.")
        self.t_sect = t_sect  # time on current section, set by class control

    def sect_dist(self):
        self.sect_distVal = int((self.t_sect/self.sect.ave_time) *
                                self.sect.dist)
        return self.sect_distVal

    def ridden_length(self):
        s = sections.copy()
        x = self.sect
        d_tot = [self.sect_dist()]  # total distance
        while len(s) > 0:
            if s[-1].end == x.start:    # if starts and ends
                                        # of the given sections match up
                d_tot.append(s[-1].dist)  # grab the distance for
                # that (preceding) section
                x = s[-1]
                s.pop()
            else:
                s.pop()
        self.dist_tot = sum(d_tot)
        print("Total length ridden:",
              float("{0:.1f}".format(self.dist_tot)), "mi")

    def sect_gain(self):
        self.sect_gainVal = int((self.t_sect/self.sect.ave_time) *
                                self.sect.ascent)
        return self.sect_gainVal

    def ridden_gain(self):
        s = sections.copy()
        x = self.sect
        g_tot = [self.sect_gain()]  # total gain
        while len(s) > 0:
            # print("Length of s:", len(s))
            if s[-1].end == x.start:    # if starts and ends of the given
                                        # sections match up
                g_tot.append(s[-1].ascent)  # grab the ascent for that
                # (preceding) section
                x = s[-1]
                s.pop()
            else:
                s.pop()
        print("Total elevation gained:", sum(g_tot), "ft. Ouch!")

    def sect_loss(self):
        self.sect_lossVal = int((self.t_sect/self.sect.ave_time) *
                                self.sect.descent)
        return self.sect_lossVal

    def ridden_loss(self):
        s = sections.copy()
        x = self.sect
        loss_tot = [self.sect_loss()]  # total descent
        while len(s) > 0:
            # print("Length of s:", len(s))
            if s[-1].end == x.start:    # if starts and ends of the
                                        # given sections match up
                loss_tot.append(s[-1].descent)  # grab the descent for
                # that (preceding) section
                x = s[-1]
                s.pop()
            else:
                s.pop()
        print("Gnarly downhill wracked up to date:", sum(loss_tot), "ft")


class Safety:
    '''Class that gives the rider options to get off the mountain
    when in need'''

    def __init__(self, sect, t_sect):
        # current instance of class section being ridden, set by class control
        self.sect = sect
        if t_sect > self.sect.ave_time:
            raise Exception("You are over the allowable time. \
Please reduce your estimate to below", self.sect.ave_time,
                            "hrs for this section.")
        self.t_sect = t_sect  # time on current section, set by class control

    def sect_dist(self):
        self.sect_distVal = int((self.t_sect/self.sect.ave_time) *
                                self.sect.dist)
        return self.sect_distVal

    def sect_gain(self):
        self.sect_gainVal = int((self.t_sect/self.sect.ave_time) *
                                self.sect.ascent)
        return self.sect_gainVal

    def sect_loss(self):
        self.sect_lossVal = int((self.t_sect/self.sect.ave_time) *
                                self.sect.descent)
        return self.sect_lossVal

    def prev_aid(self):
        print("Return to previous aid station:", self.sect.start.name)
        print("Distance:", float("{0:.1f}".format(self.sect_dist())),
              "mi back, Gain:", self.sect_loss(), "ft, Loss", self.sect_gain(),
              "ft")
        print("Time:", self.t_sect, "hrs, Services:", self.sect.start.services,
              ", phone:", self.sect.start.phone)

    def next_aid(self):
        print("Continue to next aid station:", self.sect.end.name)
        print("Distance:", float("{0:.1f}".format(self.sect.dist -
              self.sect_dist())),
              "mi ahead, Gain:", self.sect.ascent - self.sect_gain(),
              "ft, Loss", self.sect.descent - self.sect_loss(), "ft")
        print("Time:", self.sect.ave_time - self.t_sect, "hrs, Services:",
              self.sect.end.services, ", phone:", self.sect.end.phone)

    def bail(self):
        '''method assumes BailTrail is located halfway between start and finish,
        and that ascent and descent are equally distributed,
        though this is admittedly a poor assumption'''

        if self.sect.bail_trail:
            print("Take the bail trail:", self.sect.bail_trail.name)
            print("Distance:", float("{0:.1f}".format(abs(.5*self.sect.dist -
                  self.sect_dist()) + self.sect.bail_trail.dist)),
                  "mi, Gain:", (abs(.5*self.sect.ascent - self.sect_gain()) +
                                self.sect.bail_trail.ascent),
                  "ft, Loss", (abs(.5*self.sect.descent - self.sect_loss()) +
                               self.sect.bail_trail.descent), "ft")
            print("Time:", (abs(.5*self.sect.ave_time - self.t_sect) +
                  self.sect.bail_trail.ave_time), "hrs, Services:",
                  self.sect.bail_trail.services, ", phone:",
                  self.sect.bail_trail.phone)
        else:
            pass

# Scripting for flow of program follows

while True:
    print('''Vapor Trail Mountain Bike Race personal assistant \n
safe = Find the quickest route off the mountain \n
track = Track your progress along the course \n
quit = Get off your computer and go for a ride!''')
    print('')
    control = input("What would you like to do? \
Enter the keyword above: ")
    print('')

# Get yourself to safety!
    if control == "safe":
        print([self.name for self in sections])

        safe_sect = input("Where are you now? ")
        if safe_sect not in [self.name for self in sections]:
            print('')
            print("PLEASE ENTER SECTION NAME EXACTLY, without quotes.")
            print('')
            continue

        while True:
            try:
                safe_time = float(input("How many hours have you \
been riding this section? "))
                break
            except ValueError:
                print("Please enter a number of hours.")

        for i in sections:
            if i.name == safe_sect:
                route = Safety(i, safe_time)
                print('')
                print('Here are your options to get home safe:')
                print('')
                route.prev_aid()
                print('')
                route.bail()
                print('')
                route.next_aid()
                print('')

# Track your progress
    elif control == "track":
        print([self.name for self in sections])

        track_sect = input("Where are you now? ")
        if track_sect not in [self.name for self in sections]:
            print('')
            print("PLEASE ENTER SECTION NAME EXACTLY, without quotes.")
            print('')
            continue

        while True:
            try:
                track_time = float(input("How many hours have you been \
riding this section? "))
                break
            except ValueError:
                print("Please enter a number of hours.")

        for j in sections:
            if j.name == track_sect:
                how_far = Rider(j, track_time)
                print('')
                how_far.ridden_length()
                how_far.ridden_gain()
                how_far.ridden_loss()
                print('')

                # random spark of motivation:
                if how_far.dist_tot < 40:
                    print("Once the sun is up, there will be great views \
to reward you.")
                elif how_far.dist_tot > 80:
                    print("It hurts right now, but just think about how good \
that beer is going to taste at the finish.")
                else:
                    motiv = ["Keep it up, you're killing it out there!",
                             "You got this!", "Don't give in to the pain.",
                             "That's just another hill ahead, don't sweat it.",
                             "There's no doubt you're a glutton for pain."]
                    print(random.choice(motiv))
                print('')
                break
            else:
                continue

# Edit a difficulty
        while True:
            try:
                resp = input("Would you like to input a difficulty \
for this trail section? y/n;  ")
                if resp == "y" or "n":
                    break
            except Exception as e:
                print('Only "y" or "n" are possible selections. \
Please try again.')
        if resp == 'y':
            while True:
                try:
                    num = int(input("How would you rate this section? \
Scale: 1 easy to 5 hardest;  "))
                    break
                except ValueError:
                    print("Please enter 1, 2, 3, 4, or 5.")
        else:
            continue
        j.difficulty = num
        print("The new average difficulty rating is:",
              float("{0:.2f}".format(j.difficulty)))
        print('')

    elif control == "quit":
        sys.exit()

    else:
        print('')
        print("Watch your spelling! Try again (with no CAPS this time).")
        print('')
