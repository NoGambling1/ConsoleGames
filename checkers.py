board = [" "] * 64

def createBoard(board):
    boardToUse = board
    for vertical in range(1, 9):
        vert = (vertical * 8) - 7 
        for horizontal in range(8):
            print(board[vertical * horizontal])
