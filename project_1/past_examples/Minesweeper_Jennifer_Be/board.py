# Board, Square, and Move classes.
# This navigates all of the changes to the board.

import random

key_to_index = {"A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6,
                "H" : 7, "I" : 8, "J" : 9, "K" : 10, "L" : 11, "M" : 12,
                "N" : 13, "O" : 14, "P" : 16, "Q" : 17, "R" : 18, "S" : 19,
                "T" : 20, "U" : 21, "V" : 22, "W" : 23, "X" : 24, "Y" : 25,
                "Z" : 26}
index_to_key = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                "Y", "Z"]
symbols = {"m" : "*", "h" : "♥", "c" : "☺", "s" : "☃", "f" : "%", "b" : "."}

class BoardGenerator:
    """This class generates a board with the settings: row, column, 
    mine amount. In addition, it can take in a theme (symbol for
    flagged squares). The flagged parameter keeps flagged objects when
    the board is restarted."""

    def generate_boards(settings, theme, flagged=None):
        rows, cols, mines = settings
        fin_board = {}
        blank_board = {}

        while (mines != 0):
            rand_sq = (random.randint(0, rows-1), random.randint(0, cols-1))
            if rand_sq not in fin_board:
                fin_board[rand_sq] = symbols["m"]
                mines -= 1

        for row in range(rows):
            for col in range(cols):
                blank_board[(row, col)] = symbols["b"]
                if (row, col) not in fin_board:
                    mine_count = 0
                    for row1 in range(row - 1, row + 2):
                        for col1 in range(col - 1, col + 2): 
                            if (row1, col1) in fin_board:
                                if fin_board[(row1, col1)] == symbols["m"]:
                                    mine_count += 1
                    fin_board[(row, col)] = mine_count
        return Board(settings, theme, fin_board, blank_board, flagged)


class Board():
    """Takes in board settings and valid board answers, and initiates a
    board and corresponding squares."""

    def __init__(self, settings, theme, answer, blank, flagged=None):
        self.row, self.col, self.mines = settings
        self.theme = theme
        self.answer = answer
        self.view = blank
        self.mine_counter = self.mines
        self.status = "play mode"
        self.r, self.n, self.b = Square(self), NotMines(self), Blank(self)
        if flagged == None:
            self.f = Square(self)
        else:
            self.f = flagged
        self.u = Unrevealed(self)
        
    def print_board(self, answer=False):
        print("")
        print("")
        print("")
        print("  | ", end="")
        for col in range(self.col):
            print(index_to_key[col], " ", end="")
        print("")
        for col in range(self.col + 2):
            print("-", " ", end="")
        print("")

        for row in range(self.row):
            print(index_to_key[row] + " | ", end="")
            for col in range(self.col):
                if answer:
                    print(str(self.answer[(row, col)]), " ", end="")
                else:
                    sq = symbols["b"]
                    if (row, col) in self.r.view:
                        sq = self.answer[(row, col)]
                    elif (row, col) in self.f.view:
                        sq = symbols[self.theme]
                    print(sq, " ", end="")
            print("")
        print("")
        if not answer:
            print("There are ", self.mine_counter, " of ", self.mines,
                " mines left.")

    def print_answer(self):
        self.print_board(True)

class Square:
    """Takes in a board that records grid positions."""

    def __init__(self, board):
        self.view = set()
        self.board = board


class Unrevealed(Square):
    """Computes and stores the grid positions for squares that have not
    been revealed."""

    def __init__(self, board):
        self.view = self.computeSquare(board)

    def computeSquare(self, board):
        view = set()
        for each in board.answer.keys():
            view.add(each)
        return view

class NotMines(Square):
    """Computes and stores the grid positions for squares that have are
    not mines."""

    def __init__(self, board):
        self.view = self.computeSquare(board)
        self.board = board

    def computeSquare(self, board):
        view = set()
        for row in range(board.row):
            for col in range(board.col):
                if board.answer[(row, col)] != "*":
                    view.add((row, col))
        return view

class Blank(Square):
    """Computes and stores the grid positions for squares that surround
    a 0 square. Neighbors that are squares are also computed, such that
    there are a border of hint squares."""

    def __init__(self, board):
        self.view = self.computeSquare(board)
        self.board = board

    def computeSquare(self, board):
        view = set()
        for row in range(board.row):
            for col in range(board.col):
                if board.answer[(row, col)] == 0:
                    view.add((row, col))
        return view

    def neighbors(self, sq):
        neighbors = set()
        row, col = sq
        for row1 in range(row - 1, row + 2):
            for col1 in range(col - 1, col + 2):
                if (row1, col1) in self.board.view:
                    neighbors.add((row1, col1))
        return neighbors

    def find_all_connecting(self, sq):
        neighbors = set(sq)
        row, col = sq
        neighbor_queue = self.neighbors(sq)
        while neighbor_queue != set():
            neighbor = neighbor_queue.pop()
            if neighbor not in neighbors:
                neighbors.add(neighbor)
                if neighbor in self.view:
                    neighbor_queue.update(self.neighbors(neighbor))
        return neighbors

class Move:
    """Makes changes to the board and corresponding changes to Square
    objects."""

    def check_move(user, move):
        square = user.board.answer[move]
        if square == symbols["m"] and len(user.board.r.view) == 0:
            user.create_board(user.last_settings, user.board.f, move)
            return
        user.board.r.view.add(move)

        if square == symbols["m"]:
            user.board.answer[move] = "X"
            user.loses()
            return
        if move in user.board.u.view:
            user.board.u.view.remove(move)
        if square == 0:
            for sq in user.board.b.find_all_connecting(move):
                if sq not in user.board.f.view:
                    user.board.r.view.add(sq)   
        return False

    def flag_move(user, move):
        if move in user.board.r.view:
            print("Grid position is has already been revealed.")
            return False
        else:
            user.board.f.view.add(move)
            user.board.mine_counter -= 1
            return False
        
    def unflag_move(user, move):
        if move not in user.board.f.view:
            print("Grid position is not flagged.")
            return False
        else:
            user.board.f.view.remove(move)
            user.board.mine_counter += 1
            return False
        
    def stop_playing(user, move_type, grid_pos):
        if move_type not in ["r", "f", "u"]:
            print("Invalid move: " + move_type)
            return False
        
        if (len(grid_pos) != 2):
            print("Invalid grid position: " + grid_pos)
            return False

        row = key_to_index[grid_pos[0]]
        col = key_to_index[grid_pos[1]]
        if (row, col) not in user.board.view:
            print("Invalid grid position: " + grid_pos)

        else:
            if move_type == "r":
                Move.check_move(user, (row, col))
            if move_type == "f":
                Move.flag_move(user, (row, col))
            if move_type == "u":
                Move.unflag_move(user, (row, col))
