import random

global board 
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
            print(color.BOLD + color.CYAN +"---------------------" + color.END)
        else: 
            print("---------------------")
        for i in range(4):
            thingy = (a*4) + i
            if i == 1: 
                print(board[thingy],end=color.BOLD + color.CYAN + " |" + color.END)
            elif thingy > 16: print(" |")
            elif i == 0: print("|" + board[thingy],end=" |")
            else: print(board[thingy],end=" |") # type: ignore
        
        print("")
    print("---------------------")

def randomizeBoard(difficulty): #Diff 1-3,  1=40%, 2=32%, 3=25%
    if difficulty == 1: given = 40
    elif difficulty == 2: given = 32
    elif difficulty == 3: given = 25

    for i in range(16):
        randie = random.randrange(100) < given
        if randie:
            board[i] = (" " + str(random.randint(1, 4)) + " ")
    return board

print(board[all()])
def checkSpot(spot)
    spot = spot
    #if (int(spot) - 4 == spot or int(spot) + 4 == spot)
    if spot < 4:
        if board[spot+4] != spot and board[spot+8] != spot and board[spot+12] != spot:
            print("hi")
    elif spot < 8:
    elif spot < 12:
    else:
print(randomizeBoard(1))
createBoard(randomizeBoard(1))
