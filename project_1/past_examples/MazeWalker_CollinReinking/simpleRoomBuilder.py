from random import choice


#for reasonably square rooms partitions should have a 1:3 (vert:hori) ratio
vertical_partition = 2
room_height = vertical_partition*3
horizontal_partition = 6
room_width = horizontal_partition*3

class room():
    def __init__(self, doors = 'x'):
        #room types are named by which direction (east, north, west, south)
        #they have doors in.  A "room" with all walls is called 'x'
        self.room_type = doors.lower()

         #"pixel by pixel" (actually characters) map of room
        self.room_image = []

        #each room can be broken into a 3x3 grid.  false means that section
        #is filled with wall characters.  True means that that space is "open"
        mini_room=[[False,False,False],[False,False,False],[False,False,False]]
        door_dict = {'e':[1,2],'n':[0,1],'w':[1,0],'s':[2,1]}

        ##configure mini_room based on room name
        #if the room isn't all walls
        if doors != 'x':
            #open the center of the room
            mini_room[1][1] = True
            #for each each direction in the room type open that direction
            for door in self.room_type:
                mini_room[door_dict[door][0]][door_dict[door][1]] = True


        #create a "pixel by pixel" map of the room. open space will be represent
        #with spaces.  Wall "pixels" will be random selection of ▓ or ░
        for vertical_section in range(3):
            for line_h in range(vertical_partition):
                self.room_image.append([])
                for horizontal_section in range(3):
                    for line_v in range(horizontal_partition):
                        if mini_room[vertical_section][horizontal_section]:
                            self.room_image[-1].append(' ')
                        else:
                            brick = choice(list('▓░'))
                            self.room_image[-1].append(brick)

def print_room(room):
    '''Input: room map as a 2D list
       Outpit: string representation of room map'''
    return '\n'.join([''.join(image_line) for image_line in room.room_image])
