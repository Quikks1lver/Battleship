# Adam Fernandes
# November 2019
# Battleship Game: human v. ai; game is immediately loaded up with preset ships.
# Optimized to run from terminal/command prompt; formatting can look wonky on certain IDEs (for example: PyCharm).

import random

SHIP_TO_NAME = {'P': "patrol boat", 'D': "destroyer", 'B': "battleship", 'C': "carrier"}
TURN = 1

# Player class declaration
class Player:
    def __init__(self):
        self.board = get_new_board()
        self.goals = get_new_board()
        self.ship_to_length = {'P': 2, 'D': 3, 'B': 4, 'C': 5}
        self.lives = 14
        self.turns_row = None
        self.turns_col = None

# Returns a brand new, untarnished board.
def get_new_board():
    return [['~','~','~','~','~','~','~','~','~','~'],
          ['~','~','~','~','~','~','~','~','~','~'],
          ['~','~','~','~','~','~','~','~','~','~'],
          ['~','~','~','~','~','~','~','~','~','~'],
          ['~','~','~','~','~','~','~','~','~','~'],
          ['~','~','~','~','~','~','~','~','~','~'],
          ['~','~','~','~','~','~','~','~','~','~'],
          ['~','~','~','~','~','~','~','~','~','~'],
          ['~','~','~','~','~','~','~','~','~','~'],
          ['~','~','~','~','~','~','~','~','~','~']]

# Prints a row of a board.
def print_board_row(b, row):
    for i in range(0, 10, 1):
        if i != 10:
            print(str(b[row][i]).rjust(2), end = " ")
        else:
            print(str(b[row][i]).rjust(2), end = "")

# Just prints one board.
def print_board(b):
    print("\t", end = "")
    for i in range(1, 11, 1):
        if i == 10:
            print(str(i).rjust(2))
        else:
            print(str(i).rjust(2), end=" ")
    for i in range(0, 10, 1):
        print(str(i + 1).rjust(2), end = "\t")
        print_board_row(b, i)
        print()

# Prints both boards, with b1 being the human's playing board and b2 being the computer's.
def print_boards(b1, b2):
    # 40, a "magic number," is just the width of one player's board.
    print("Your board:".center(40), end = "")
    print("Enemy (AI's) board:".center(40))
    print("\t", end="")
    for i in range(2):
        for j in range(1, 11, 1):
            if i == 1 and j == 10:
                print(str(j).rjust(2))
            else:
                print(str(j).rjust(2), end = " ")
        # Print tabs so the enemy's board is far enough away to allow for easier viewing.
        if i == 0:
            print("\t\t", end="")

    for i in range(0, 10, 1):
        print(str(i + 1).rjust(2), end = "\t")
        print_board_row(b1, i)
        print("  |  ", end = "")
        print(str(i + 1).rjust(2), end="\t")
        print_board_row(b2, i)
        print()

# Outputs a number between [0,1] for ship orientation, [0,9] for ship row, and [0,9] for ship column
def randomize():
    orientation = random.randint(0,1)
    row = random.randint(0,9)
    col = random.randint(0,9)
    return orientation, row, col

# Takes in a board, a starting coordinate, and an ending coordinate, and outputs a 1
# if a ship is allowed to be placed within those coordinates (i.e.: free "ocean" space), otherwise, outputs 0.
def is_free_to_place_ship(b, length, row, column, orientation):
    if orientation == 1 and row + length > 9 or orientation == 0 and column + length > 9:
        return 0
    for i in range(0, length, 1):
        if orientation == 1:
            if b[row + i][column] != '~':
                return 0
        else:
            if b[row][column + i] != '~':
                return 0
    return 1

# Places a specified ship's symbols (denoting which ship it is) onto a specified board.
def place_ship(b, symbol, length, row, column, orientation):
    for i in range(0, length, 1):
        if orientation == 1:
            b[row + i][column] = symbol
        else:
            b[row][column + i] = symbol

# Sets up all ships on a given board (fleet is a ship to length dictionary).
def set_up_all_ships(b, fleet):
    # If orientation is 1, the ship orientation is vertical. If 0, horizontal.
    # Ship row and ship column hold the corresponding coordinates of the ship for
    # when the ships are being assigned randomly to the boards.
    ship_orientation = None
    ship_row = None
    ship_column = None
    
    for k in fleet:
        ship_orientation, ship_row, ship_column = randomize()
        while is_free_to_place_ship(b, fleet[k], ship_row, ship_column, ship_orientation) == 0:
            ship_orientation, ship_row, ship_column = randomize()
        place_ship(b, k, fleet[k], ship_row, ship_column, ship_orientation)

# Gets user input for coordinates. Subtracts 1 from raw input because of how arrays'
# indices work in Python (0-9 rather than 1-10).
def get_input_from_player():
    success = False
    
    while not success:
        try:
            temp_row = int(input())
            temp_col = int(input())
            temp_row -= 1
            temp_col -= 1
            
            success = True
        except:
            print("Invalid input, Admiral. Try again.")

    return temp_row, temp_col

# Gets random input from ai.
def get_ai_input():
    temp_row = random.randint(0, 9)
    temp_col = random.randint(0, 9)
    return temp_row, temp_col

# Takes in a board and a set of guess coordinates. If the coordinate has already been input or the coordinate is out
# of bounds, returns a 1, otherwise, 0.
def invalid_input(b, row, column):
    if row < 0 or row > 9 or column < 0 or column > 9 or b[row][column] != '~':
        return 1
    return 0

# Changes the goals board and normal board based on the row and column coordinate for a torpedo attack.
def alter_boards(board, goals, lives, ship_to_length, row, column):
    if goals[row][column] != '~':
        ship_to_length[goals[row][column]] -= 1
        lives -= 1
        if ship_to_length[goals[row][column]] == 0:
            print("The " + str(SHIP_TO_NAME[goals[row][column]]) + " has been destroyed.")
        goals[row][column] = 'H'
        board[row][column] = 'H'
    else:
        goals[row][column] = 'M'
        board[row][column] = 'M'
    return lives

# Prints what happens when a winner is crowned.
def print_winner(winner, board):
    if winner == "player":
        print("You commanded well, admiral. Victory is yours!")
    else:
        print("You can't win 'em all. Rendezvous back to base; let's win the next bout.")
    print_board(board)

# End of pre-written functions and global variables

# - - - - - - - - - -

# Welcome screen and printing of boards.

print("-------> WELCOME TO BATTLESHIP <-------\nAdmiral, please type \"go\" to commence the game.")
ready_or_not = input()

while ready_or_not.lower() != "go":
    print("The fleet awaits your command. Type \"go\" to commence the game.")
    ready_or_not = input()

# Creates all boards.
user = Player()
ai = Player()

print_boards(user.board, ai.board)
print("***OBJECTIVE***: You must sink the enemy fleet using skill and some guessing. Good luck, admiral!")

# Randomly set up ships, for both the player and the ai.
set_up_all_ships(user.goals, user.ship_to_length)
set_up_all_ships(ai.goals, ai.ship_to_length)

# Loops until either the player's fleet or ai's fleet is destroyed.
while user.lives > 0 and ai.lives > 0:
    # player's turn
    if TURN % 2 == 1:
        print("Admiral, input a row and a column to fire torpedoes towards enemy vessels.")
        user.row, user.col = get_input_from_player()
        while invalid_input(user.board, user.row, user.col) == 1:
            print("Invalid coordinate, admiral. Input another set of row and column coordinates.")
            user.row, user.col = get_input_from_player()
        # at this point, input has been verified, and row and column coordinates are valid
        ai.lives = alter_boards(user.board, user.goals, ai.lives, ai.ship_to_length, user.row, user.col)
    # ai's turn
    else:
        ai.row, ai.col = get_ai_input()
        while invalid_input(ai.board, ai.row, ai.col) == 1:
            ai.row, ai.col = get_ai_input()
        # at this point, input has been verified, and row and column coordinates are valid
        user.lives = alter_boards(ai.board, ai.goals, user.lives, user.ship_to_length, ai.row, ai.col)
    # Prints both boards after the ai's turn (thus, each player will have gone once before the boards are printed).
    if TURN % 2 == 0:
        print_boards(user.board, ai.board)
    TURN += 1

# Print winner of the game.
if user.lives == 0:
    print_winner("ai", ai.goals)
else:
    print_winner("player", user.goals)