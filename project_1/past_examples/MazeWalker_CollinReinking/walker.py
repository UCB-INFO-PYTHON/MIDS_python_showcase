from random import randint
import curses
from random import randint,choice

class walker():
    '''Character or object in the maze that might move'''
    def __init__(self,character = '?',location = [0,0]):
        self.char = character
        self.location = location
        self.prev_loc = location
        self.prev_move = [0,0]

    def move(self,direction_unused,maze):
        pass

class hero(walker):
    '''Character that the user will move around the board'''
    char = '☺'
    def __init__(self,maze):
        #top left location in maze should be passed in
        loc = [0,0]

        #find the first open space
        for row in range(maze.width):
            for col in range(maze.height):
                if maze.iswall([col,row]):
                    continue
                else:
                    loc = [col,row]
                break
            if loc != [0,0]:
                break
                
        walker.__init__(self,self.char,loc)




    def move(self, direction,maze):
        if maze.iswall([self.location[0]+direction[0],self.location[1]+direction[1]]):
            curses.beep()
            direction = [0,0]
        self.prev_loc = self.location
        self.location = [self.location[0]+direction[0],self.location[1]+direction[1]]


class fire(walker):
    '''Character that will move autamtically around the board'''
    char = '🔥'
    def __init__(self,maze):
        #random location should be passed in

        loc = [0,0]
        #choose a random spot in maze until you choose an open space
        while maze.maze_list[loc[0]][loc[1]] != ' ':
             loc[0] = randint(0,maze.height-1)
             loc[1] = randint(0,maze.width-1)

        walker.__init__(self,self.char,loc)

    def move(self,direction_unused,maze):
        options = [[1,0],[-1,0],[0,-1],[0,1],[0,0]]

        #if moving in the same direction doesn't run you into a wall
        #increase the probability that you continue in the same direction
        if not maze.iswall([self.location[0]+self.prev_move[0],self.location[1]+self.prev_move[1]]):
             options.append(self.prev_move*5)

        #remove turning around
        options.remove([self.prev_move[0]*-1,self.prev_move[1]*-1])

        while True:
            direction = choice(options)
            if not maze.iswall([self.location[0]+direction[0],self.location[1]+direction[1]]):
                break

        self.prev_loc = self.location
        self.prev_move = direction
        self.location = [self.location[0]+direction[0],self.location[1]+direction[1]]

class treasure(walker):
    '''treasure item will have a point value that between 10 and 100'''
    char = '☆'
    def __init__(self,maze):
        #random location should be passed in

        self.value = randint(1,10)*10
        loc = [0,0]
        #choose a random spot in maze until you choose an open space
        while maze.maze_list[loc[0]][loc[1]] != ' ':
             loc[0] = randint(0,maze.height-1)
             loc[1] = randint(0,maze.width-1)

        walker.__init__(self,self.char,loc)

    def collect(self,maze):
        maze.score += self.value
        #os.system("afplay coin.wav")
        self.value = randint(1,10)*10

        loc = [0,0]
        while maze.maze_list[loc[0]][loc[1]] != ' ':
             loc[0] = randint(0,maze.height-1)
             loc[1] = randint(0,maze.width-1)

        self.prev_loc = self.location
        self.location = loc
