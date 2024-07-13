from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
colorama_init()

board = [" O "] * 16 + ["   "] * 32 + [" X "] * 16

def createBoard(board):
    boardToUse = board
    for count in range(8):
        for newCount in range(8):
            spot = (count* 8) + newCount
            print("[" + board[spot] + "]",end=" ")
        print("\n")

createBoard(board)
