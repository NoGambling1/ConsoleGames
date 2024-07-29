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

def randomizeBoard(difficulty):
    if difficulty == 1: given = 40
    elif difficulty == 2: given = 32
    elif difficulty == 3: given = 25

    for i in range(16):
        randie = random.randrange(100) < given
        if randie:
            attempts = 0
            max_attempts = 100
            while attempts < max_attempts:
                board[i] = f" {random.randint(1, 4)} "
                if checkSpot(i):
                    break
                else:
                    attempts += 1

    return board

def checkSpot(spot):
    current_number = board[spot].strip()
    row_start = (spot // 4) * 4
    for i in range(row_start, row_start + 4):
        if i != spot and board[i].strip() == current_number:
            return False

    for i in range(spot % 4, 16, 4):
        if i != spot and board[i].strip() == current_number:
            return False

    quadrant = [(0, 1, 4, 5), (2, 3, 6, 7), (8, 9, 12, 13), (10, 11, 14, 15)]
    for q in quadrant:
        if spot in q:
            for pos in q:
                if pos != spot and board[pos].strip() == current_number:
                    return False

    return True

def solveBoard(unfinished_board):
    newBoard = ["   "] * 16
    def solveUtil(spot, attempts_left=10000):
        if spot == 16:
            return True

        for number in range(1, 5):
            if isValidMove(spot, number):
                newBoard[spot] = f" {number} "
                if solveUtil(spot + 1, attempts_left - 1):
                    return True
                newBoard[spot] = "   "

        return False

    return newBoard

def isValidMove(spot, number, unfinished_board):
    current_number = unfinished_board[spot].strip()
    if current_number == "":
        row_start = (spot // 4) * 4
        for i in range(row_start, row_start + 4):
            if i != spot and unfinished_board[i].strip() == str(number):
                return False

        for i in range(spot % 4, 16, 4):
            if i != spot and unfinished_board[i].strip() == str(number):
                return False

        quadrant = [(0, 1, 4, 5), (2, 3, 6, 7), (8, 9, 12, 13), (10, 11, 14, 15)]
        for q in quadrant:
            if spot in q:
                for pos in q:
                    if pos != spot and unfinished_board[pos].strip() == str(number):
                        return False

        return True
    return False

if __name__ == "__main__":
    print("Attempting to solve the board...")
    initial_board = [item for item in board]  # Capture the initial board state
    while True:
        createBoard(board)
        print(board)
        solved_board = solveBoard(board.copy())  # Pass a copy of the unfinished board
        if solved_board != initial_board:  # Check if the board was actually solved
            print("Initial unsolved board:")
            createBoard(initial_board)
            print("Solved board:")
            createBoard(solved_board)
            break
        else:
            print("\nNo solution found. Generating a new board...")
            board = ["   "] * 16
            randomizeBoard(1)
