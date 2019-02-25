import curses
from simpleRoomBuilder import room
import walker
from random import randint,choice
import os




class maze():
    '''Contains the state of the game and methods to advance the game'''
    number_of_fires = 10
    number_of_treasures = 10

    def __init__(self, miniMaze_filename = None):


        #create full size maze map from minimap string located in file
        mstring = build_maze(miniMaze_filename)

        #define height and width then remove \n to formad for curses pad
        self.height, self.width = mstring.count('\n'), mstring.find('\n')
        mstring = mstring.replace('\n', '');

        #I need to keep a copy maze as a 2D list updated to check UTF character
        #locations because curses won't return the utf-8 encoding of a character
        #at a location and I'm using utf-8 characters for walls and characters
        self.maze_list = [[mstring[h*self.width+w] for w in range(self.width)] \
                          for h in range(self.height)]


        #initialize curses pad and add maze string to it
        self.pad = curses.newpad(self.height+1, self.width)
        self.pad.addstr(mstring)

        #player score
        self.score = 0
        #walkers list contains the
        self.walkers =[[],[],[]]

        #create hero walker
        self.walkers[0].append(walker.hero(self))

        #create all fire walkers
        for fire in range(self.number_of_treasures):
            self.walkers[1].append(walker.fire(self))

        #create all treasures
        for treasure in range(self.number_of_treasures):
            self.walkers[2].append(walker.treasure(self))


    def __str__(self):
        return('\n'.join([''.join(row) for row in self.maze_list]))

    def update(self,direction):
        '''the method moves the hero in the direction or changes direction to [0,0]
        if movement is not possible.  It then moves all the fire walkers in a
        semi-random direction.  If any collisions occur between the Hero and
        another walker, update resolves the collision appropriately'''

        #move every walker object of every walker type in the maze
        for walker_type in self.walkers:
            for walker_instance in walker_type:
                walker_instance.move(direction, self)

        #for each walker erase character at prev_loc
        for walker_group in self.walkers:
            for walker in walker_group:
                self.change(walker.prev_loc, ' ')

        #for each walker write new character at location
        for walker_group in self.walkers:
            for walker in walker_group:
                self.change(walker.location, walker.char)

        #if any fire walkers are in teh same direction as teh hero walker
        #fill empty spaces with fire and raise Exception 'game over'
        if any([self.walkers[0][0].location == w.location for w in self.walkers[1]]) :
            for row in range(len(self.maze_list)):
                for col in range(len(self.maze_list[row])):
                    if self.maze_list[row][col] == ' ':
                        self.change([row,col],self.walkers[1][0].char)
            raise Exception('GameOver')

        #if the hero is in the same location as a treasure add the treasure value
        #to the score, remove the treasures, and create a new treasure in a
        #random location
        for n,treasure in enumerate(self.walkers[2]):
            if self.walkers[0][0].location == treasure.location:
                treasure.collect(self)

    def iswall(self,location):
        '''takes in location as 2d list, reutrns True if that location conains
        a wall character'''
        return self.maze_list[location[0]][location[1]] in '░▓'

    def change(self,location,char):
        '''takes in a list of length two (y,x) and changes that location to char
        updates the curses pad and the mstring'''
        if isinstance(char,walker.walker):
            char = char.char
        self.pad.addstr(location[0],location[1],char)
        self.maze_list[location[0]][location[1]] = char

def build_maze(miniMaze_filename):
    '''input: the name of a text file with a minimap drawing (made from box
    drawing characters, ╣,║,╗,╝,╚,╔,╩,╦,╠,═ and ╬, to represent different room
    options)
    output:  a string that is a rendered full size map with space characters in
    open places and ▓ or ░ (randomly chosen) for wall places.'''

    room_dic = {'╔': 'ES', '╝': 'NW', '╨': 'N', '╡': 'W', '═': 'EW', '╦': 'EWS', '╣': 'NWS',\
                '╩': 'ENW', '╗': 'WS', '╠': 'ENS', '╬': 'ENWS', '║': 'NS', '╞': 'E', '╥': 'S',\
                '╚': 'EN', 'x':'x'}

    #read in file add an x to every edge of the map to create an outer wall
    miniMazeFile = open(miniMaze_filename, "r" )
    maze_list = ['x'+line[:-1]+'x' for line in miniMazeFile]
    maze_list.append('x'*len(maze_list[0]))
    maze_list.insert(0,'x'*len(maze_list[0]))

    #room is from simpleRoomBuilder.room
    #create a 2d list that contains the 2d list representation of each "room"
    maze_list = [[room(room_dic[r].lower()).room_image for r in row] for row in maze_list]

    #merge the strings from each room into one long string line by line
    return list_of_room_lists_to_string(maze_list)

def list_of_room_lists_to_string(inp_list):
    '''input: a 2d list of two 2d lists
       output: a string representation of of all of the lists joined together
               row by row'''

    return_string = ''
    #for each row of rooms
    for row in inp_list:
        #for each row in the height of a room
        for line in range(len(row[0])):
            #join the rows of each room from that row of rooms
            return_string += ''.join([''.join(room[line]) for room in row])+'\n'

    return return_string
