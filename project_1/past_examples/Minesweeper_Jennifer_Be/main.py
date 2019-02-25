# Welcome to Minesweeper!
# A spin of the popular game, with a customizable board, playable on
# the terminal. This is a grid-style game with mines placed on a board.
# Figure out which squares are mines by the hint square. Each square
# displays the number of mines that surround it.

from board import BoardGenerator, Move

symbols = {"m" : "*", "h" : "♥", "c" : "☺", "s" : "☃", "f" : "%", "b" : "."}

class User():
    """User is a player that saves custom settings, records scores, and
    plays the game."""

    def __init__(self, name):
        self.name = name
        self.beg_score = [0, 0]
        self.inter_score = [0, 0]
        self.expert_score = [0, 0]
        self.custom_score = [0, 0]
        self.theme = "f"
        self.board = None
        self.last_settings = None

    def loses(self):
        settings = self.board.row, self.board.col, self.board.mines
        if settings == CLASSIC_BEGINNER:
            self.beg_score[1] += 1
        elif settings == CLASSIC_INTERMEDIATE:
            self.inter_score[1] += 1
        elif settings == CLASSIC_EXPERT:
            self.expert_score[1] += 1
        else:
            self.custom_score[1] += 1

        self.board.print_answer()
        print("G A M E  O V E R ! ! ! !")
        self.board.status = "game over"
        self.play_again()

    def wins(self):
        settings = self.board.row, self.board.col, self.board.mines
        if settings == CLASSIC_BEGINNER:
            self.beg_score[0] += 1
        elif settings == CLASSIC_INTERMEDIATE:
            self.inter_score[0] += 1
        elif settings == CLASSIC_EXPERT:
            self.expert_score[0] += 1
        else:
            self.custom_score[0] += 1

        self.board.print_answer()
        print("Y a y !  Y o u  w o n ~")
        self.board.status = "game over"
        self.play_again()

    def play_again(self):
        again = input("Play again? (y/n): ").lower()

        if again == "y":
            mode()
        elif again == "n":
            print("Thanks for playing! :)")
            return
        else:
            self.play_again()

    def scores(self):
        classic_wins = self.beg_score[0] + self.inter_score[0]
        + self.expert_score[0]
        classic_loses = self.beg_score[1] + self.inter_score[1]
        + self.expert_score[1]
        total_wins = classic_wins + self.custom_score[0]
        total_loses = classic_loses + self.custom_score[1]
        print("- - - - - - - - - - - - - - - - - - - - - - - ")
        print("scores for", self.name)
        print("- - - - - - - - - - - - - - - - - - - - - - - ")
        print("")
        print("Game Mode     | Wins & Losses")
        print("- - - - - - - - - - - - - - - -")
        print("Beginner      | ", self.beg_score[0], self.beg_score[1])
        print("Intermediate  | ", self.inter_score[0],self.inter_score[1])
        print("Expert        | ", self.expert_score[0], self.expert_score[1])
        print("Classic Total | ", classic_wins, classic_loses)
        print("Custom Total  | ", self.custom_score[0], self.custom_score[1])
        print("Total Score   | ", total_wins, total_loses)
        print("")
        print("")
        input("Input anything to return to the main screen:")
        mode()

    def change_theme(self):
        print("Current flag symbol is: " + user.theme)
        print("Options are: ♥ (h) | ☺ (c) | ☃ (s) ")
        theme = None
        while theme not in symbols:
            theme = input("What theme would you like? ")
        self.theme = theme

    def create_board(self, settings, flagged=None, move=None):
        self.board = BoardGenerator.generate_boards(settings, self.theme,
            flagged)
        self.last_settings = settings
        if move == None:
            self.first_move()
        else:
            Move.check_move(self, move)
            if self.board.status == "play mode":
                self.play()
            return
    
    def change_board(self):
        row, col, mines = 0, 0, 0
        while (row < 2) or (row > 26):
            row = input("Please enter a row size, from 2 to 26: ")
            try:
                row = int(row)
                break
            except:
                print("Please enter a valid number.")
                row = 0
                continue

        while (col < 2) or (col > 26):
            col = input("Please enter a column size, from 2 to 26: ")
            try:
                col = int(col)
                break
            except:
                print("Please enter a valid number.")
                col = 0
                continue
        while (mines < 1) or (mines >= (row * col)):
            max_mine = str((row * col) - 1)
            mines = input("Enter mine quantity, from 1 to " + max_mine + ": ")
            try:
                mines = int(mines)
                break
            except:
                print("Please enter a valid number.")
                mines = 0
                continue
        return (row, col, mines)

    def first_move(self):
        print("You have begun a game! Here are the valid moves:")
        print("reveal (r xx) | flag (f xx) | unflag (u xx) | quit (q)")
        print('replace "xx" with the two letter grid: (row)(column)')
        self.play()
    
    def play(self):
        self.board.print_board()
        if self.board.r.view == self.board.n.view:
            self.wins()
        move = input("Please make your move: ").split()
        if (len(move) == 1) and (move[0] == "q"):
            answer = input("Are you sure you want to quit? (y/n):")
            if answer == "y":
                self.board.status = "game over"
                self.play_again()
                return
            else:
                self.play()
            return
        if len(move) < 2:
            print("Please make a valid move.")
            self.play()
        else:
            Move.stop_playing(self, move[0], move[1].upper())
            if self.board.status == "play mode":
                self.play()

#### INTERFACE
CLASSIC_BEGINNER = (8, 8, 10)
CLASSIC_INTERMEDIATE = (16, 16, 40)
CLASSIC_EXPERT = (24, 24, 99)
user = None

def start():
    print("- - - - - - - - - - - - - - - - - - - - - - - ")
    print("W e l c o m e  t o  M i n e s w e e p e r !")
    print("- - - - - - - - - - - - - - - - - - - - - - - ")
    print("")
    name = input("What is your name? ")
    global user
    user = User(name)
    mode()

def mode():
    print("To begin playing, pick a mode:")
    print("")
    print("beginner (b) | intermediate (i) | expert (e)")
    print("")
    print(" in addition, you can customized your board:")
    print("")
    print("change theme (t) | make your own board (o)")
    print("")
    print("look at my scores (s)")
    print("")
    print("quit the game :( (q)")
    print("")
    print("")
    start_response()

def start_response():
    global user
    response = input("Respond here: ").lower()
    if response == "b":
        user.create_board(CLASSIC_BEGINNER)
    elif response == "i":
        user.create_board(CLASSIC_INTERMEDIATE)
    elif response == "e":
        user.create_board(CLASSIC_EXPERT)
    elif response == "t":
        user.change_theme()
        mode()
    elif response == "o":
        user.create_board(user.change_board())
    elif response == "s":
        user.scores()
    elif response == "q":
        print("Goodbye! Come again~")
        return
    else:
        start_response()

start()