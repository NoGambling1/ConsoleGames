import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board(board):
    output = "\n"
    output += "    A B C   D E F   G H I\n"
    output += "  +-------+-------+-------+\n"
    for i in range(9):
        output += f"{i+1} |"
        for j in range(9):
            if board[i][j] == 0:
                output += " ."
            else:
                output += f" {board[i][j]}"
            if (j + 1) % 3 == 0:
                output += " |"
        output += "\n"
        if (i + 1) % 3 == 0:
            output += "  +-------+-------+-------+\n"
    return output

def is_valid(board, num, pos):
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_x, box_y = pos[1] // 3, pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def solve(board):
    find = find_empty(board)
    if not find:
        return True
    row, col = find
    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def generate_sudoku(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve(board)
    remove = {1: random.randint(40, 50),
              2: random.randint(51, 60),
              3: random.randint(61, 70)}[difficulty]
    while remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            remove -= 1
    return board

def play_game():
    while True:
        try:
            difficulty = int(input("Choose difficulty (1-Easy, 2-Medium, 3-Hard): "))
            if difficulty not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 3.")

    board = generate_sudoku(difficulty)
    original_board = [row[:] for row in board]

    while True:
        clear_screen()
        print(create_board(board))
        print("\nInstructions:")
        print("Enter your move as 'row column number' (e.g., '1A 5' or '3C 7')")
        print("Enter 'q' to quit, 's' to solve, or 'r' to reset")

        move = input("\nEnter your move: ").lower()

        if move == 'q':
            break
        elif move == 's':
            solution = [row[:] for row in board]
            if solve(solution):
                clear_screen()
                print("Solved board:")
                print(create_board(solution))
                input("Press Enter to continue...")
            else:
                print("No solution exists!")
                input("Press Enter to continue...")
        elif move == 'r':
            board = [row[:] for row in original_board]
        else:
            try:
                pos, num = move.split()
                row = int(pos[0]) - 1
                col = ord(pos[1].upper()) - ord('A')
                num = int(num)

                if 0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9:
                    if original_board[row][col] == 0:
                        if is_valid(board, num, (row, col)):
                            board[row][col] = num
                        else:
                            print("Invalid move!")
                            input("Press Enter to continue...")
                    else:
                        print("Can't modify original numbers!")
                        input("Press Enter to continue...")
                else:
                    print("Invalid input! Row should be 1-9, column A-I, and number 1-9.")
                    input("Press Enter to continue...")
            except (ValueError, IndexError):
                print("Invalid input! Format should be 'row column number' (e.g., '1A 5' or '3C 7').")
                input("Press Enter to continue...")

        if find_empty(board) is None:
            clear_screen()
            print(create_board(board))
            print("Congratulations! You've solved the puzzle!")
            break

if __name__ == "__main__":
    play_game()