from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
colorama_init()

board = [" O ", "  "] * 4 + ["  ", " O "] * 4 + [" O ", "  "] * 4 + ["  "] * 16 + ["  ", " X "] * 4 + [" X ", "  "] * 4 + ["  ", " X "] * 4

def createBoard(board):
    boardToUse = board
    for count in range(8):
        print(Fore.CYAN + f"{count+1} |",end="  " + Style.RESET_ALL)

        for newCount in range(8):
            spot = (count* 8) + newCount
            print("[" + board[spot] + "]",end=" ")
        
        print("\n  |  ")
    print("   ----------------------------------------------")
    print("      A     B    C     D     E    F    G     H")
createBoard(board)  
