board = [" E "] * 16 + [""] * 6

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
    #print("----------------------------------------------")
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
createBoard(board)

    