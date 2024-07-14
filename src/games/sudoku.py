import random

# Global board declaration
board = ["   "] * 16

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ------------------------------------------------------------------------------

def createBoard(board):
    for a in range(4):
        if a == 2:
            print(color.BOLD + color.CYAN + "---------------------" + color.END)
        else:
            print("---------------------")
        for i in range(4):
            thingy = (a * 4) + i
            if i == 1:
                print(board[thingy], end=color.BOLD + color.CYAN + " |" + color.END)
            elif thingy > 15:
                print(" |")
            elif i == 0:
                print("|" + board[thingy], end=" |")
            else:
                print(board[thingy], end=" |")

        print("")
    print("---------------------")

# ------------------------------------------------------------------------------

def randomizeBoard(difficulty):  # Diff 1-3,  1=40%, 2=32%, 3=25%
    if difficulty == 1: given = 40
    elif difficulty == 2: given = 32
    elif difficulty == 3: given = 25

    for i in range(16):
        randie = random.randrange(100) < given
        if randie:
            attempts = 0
            max_attempts = 100  # Limit to prevent infinite loops
            while attempts < max_attempts:
                board[i] = f" {random.randint(1, 4)} "
                if checkSpot(i):
                    break  # Valid spot found, exit the loop
                else:
                    attempts += 1  # Increment attempt counter

    return board

# ------------------------------------------------------------------------------

def checkSpot(spot):
    # Extract the number from the current spot
    current_number = board[spot].strip()

    # Check the row for duplicates
    row_start = (spot // 4) * 4
    for i in range(row_start, row_start + 4):
        if i != spot and board[i].strip() == current_number:
            return False

    # Check the column for duplicates
    for i in range(spot % 4, 16, 4):
        if i != spot and board[i].strip() == current_number:
            return False

    # If no duplicates are found, return True
    return True


# ------------------------------------------------------------------------------

print("hi")
createBoard(randomizeBoard(1))
