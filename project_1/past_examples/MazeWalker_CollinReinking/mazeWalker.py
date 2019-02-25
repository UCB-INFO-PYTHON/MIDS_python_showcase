import os
import curses
from curses.textpad import rectangle
from simpleRoomBuilder import room
from random import randint, choice
from maze import maze
import time

def engine(stdscr):
    '''Engine takes in a curses window and is called by curses.Wrapper()
    Engine intitalizes screen and contains the loop that takes the user input,
    sends it to an instance of the maze class and refreshes all the displays.'''

    curses.curs_set(0) # turn curser off
    stdscr.refresh() #initial screen refresh
    gMaze = maze('simpleMiniMaze.txt') #initialize Maze
    curses.halfdelay(1) #removes wait for user input on getch()

    #dict to convert keys to direction "vectors" [y,x] in the form of lists
    direction_vectors_dic = {curses.KEY_DOWN:[1,0],\
                         curses.KEY_UP:[-1,0],\
                         curses.KEY_LEFT:[0,-1],\
                         curses.KEY_RIGHT:[0,1],\
                         -1:[0,0]}

    #Dimensions and location of main game curses pad (window)
    p = {'y_loc':2,'x_loc':6,'height':16,'width':49, \
        'y_cent':min(max(gMaze.walkers[0][0].location[0],0),gMaze.height), \
        'x_cent':min(max(gMaze.walkers[0][0].location[1],0),gMaze.height)}

    #Frame around gameplay Pad
    game_frame = curses.newwin(p['y_loc']+p['height']+1, p['x_loc']+p['width']-1,p['y_loc']-1,p['x_loc']-2,)
    game_frame.border()
    game_frame.refresh()

    #lower info frame
    end_game_frame = [v[0]+v[1] for v in zip(game_frame.getmaxyx(),game_frame.getbegyx())]
    info_frame = curses.newwin(5, game_frame.getmaxyx()[1],end_game_frame[0],game_frame.getbegyx()[1])
    info_frame.border()
    info_frame.refresh()

    #this loop runs the game
    err = 'none'
    start_time = time.time()
    while True:
        curses.napms(10)#to help slow things down and smooth things out
        inp = stdscr.getch() #will be -1 if no input is used

        if inp == 27: #27 is the Ascii code for esc key
            break

        #convert user input to a direction vector
        #if no user input (or unrecognized user input), use direcion [0,0]
        direction = direction_vectors_dic.get(inp, [0,0])

        try:
            #main call to maze object that moves all objects
            gMaze.update(direction)

            #set screen center based on hero location hero = gMaze.walkers[0][0]
            p['y_cent'] = min(max(gMaze.walkers[0][0].location[0],0),gMaze.height)
            p['x_cent'] = min(max(gMaze.walkers[0][0].location[1],0),gMaze.width)

            #set parameters for pad refresh
            y_top_left = int(p['y_cent'] - p['height']/2)
            y_bottom_right = int(p['y_cent'] + p['height']/2)
            x_top_left = int(p['x_cent'] - p['width']/2)
            x_bottom_right = int(p['x_cent'] + p['width']/2)

            #Main pad refresh
            gMaze.pad.refresh(y_top_left,x_top_left,p['y_loc'],p['x_loc'],p['y_loc']+p['height'],p['x_loc']+p['width'])

            #info frame refresh
            elapsed_time = divmod(int(time.time()-start_time),60)
            formatted_time = '{}:{:0>2d}'.format(elapsed_time[0],elapsed_time[1])
            info_frame.addstr(1,1,'Time: '+formatted_time)
            info_frame.addstr(3,1,'Score: '+ '{:0>8d}'.format(gMaze.score))
            info_frame.addstr(1,20,'Use the arrow keys to control')
            info_frame.addstr(2,20,'your Hero.')
            info_frame.addstr(3,20,'Hit \'esc\' to exit the game.')
            info_frame.refresh()

        except Exception as e:
            if 'GameOver' in str(e):
                #If the game over error is raise leave the screen on until
                #the user hits the escape key.
                err = e
                gMaze.pad.refresh(y_top_left,x_top_left,p['y_loc'],p['x_loc'],p['y_loc']+p['height'],p['x_loc']+p['width'])
                while True: #leave screen on until user hits escape key.
                    inp = stdscr.getch()
                    if inp == 27:
                        break
            else:
                file = open('test_output.txt', 'w')
                file.write('testing: '+str(e)+'\n')
                file.write(str(gMaze))
                file.close()
                raise e
                exit()

            break

    # #output contents of map to text and the error thrown if game doesn't end in
    # #game over
    # file = open('test_output.txt', 'w')
    # file.write('testing, No GameOver:'+str(err)+'\n')
    # file.write(str(gMaze))
    # file.close()

curses.wrapper(engine)
