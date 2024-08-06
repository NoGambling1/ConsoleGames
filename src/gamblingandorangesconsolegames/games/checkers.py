from colorama import init as colorama_init

from colorama import Fore, Back, Style

colorama_init()
toHighlight = 0


def play_game():
    """main function to play checkers."""
    global toHighlight
    board = (
        [" O ", "  "] * 4
        + ["  ", " O "] * 4
        + [" O ", "  "] * 4
        + ["  "] * 16
        + ["  ", " X "] * 4
        + [" X ", "  "] * 4
        + ["  ", " X "] * 4
    )


    current_player = "O"  # Start with player 'O'
    print("\n" + Fore.YELLOW + "welcome to checkers!" + Style.RESET_ALL)
    print(Fore.CYAN + "\ncurrent board:" + Style.RESET_ALL)
#------------------------------

    def create_board(board, hee): #Draws the board
        whatShouldIHighlight = hee #25
        for count in range(8):
            print(Fore.CYAN + f"{count+1} |", end="  " + Style.RESET_ALL)

            for newCount in range(8):
                spot = (count * 8) + newCount
                if (int(spot) == int(whatShouldIHighlight)): #highlights the last move made

                    if board[spot] == " O ":
                        print(
                            Fore.RED
                            + Back.RED
                            + "["
                            + board[spot]
                            + "]"
                            + Style.RESET_ALL,
                            end=" ",
                        )
                    elif board[spot] == " X ":
                        print(
                            Fore.GREEN
                            + Back.GREEN
                            + "["
                            + board[spot]
                            + "]"
                            + Style.RESET_ALL,
                            end=" ",
                        )

                    else:
                        print(Back.CYAN + "[" + board[spot] + "]" + Back.RESET, end=" " )
                else:
                    if board[spot] == " O ":
                        print(
                            Fore.RED + "[" + board[spot] + "]" + Style.RESET_ALL,
                            end=" ",
                        )
                    elif board[spot] == " X ":
                        print(
                            Fore.GREEN + "[" + board[spot] + "]" + Style.RESET_ALL,
                            end=" ",
                        )

                    else:
                        print("[" + board[spot] + "]", end=" ")

            print("\n  |  ")
        print("   ----------------------------------------------") #Draws lettering
        print("      A     B    C     D     E    F    G     H")

    def cord_to_num(coordinate): #Takes a position (A4) and finds it's place in the game array
        coord_arr = list(coordinate.lower())
        return (int(coord_arr[1]) - 1) * 8 + (ord(coord_arr[0]) - 97)
        global otherPiece
    def add_move(move): #Makes a move and checks if its the players turn
        global toHighlight
        move_from, move_to = move.split("-")
        from_num = cord_to_num(move_from)
        to_num = cord_to_num(move_to)
        diff = to_num - from_num
        toHighlight = to_num

        piece = board[from_num]
        
        if piece.replace(" ","") != current_player:
            print("It's not your turn.")
            return

        if (abs(diff) != 7 and abs(diff) != 9) and (abs(diff) != 18 and abs(diff) != 14):   # 7 and 9 are the differences when capturing diagonally
            print("Move is not diagonal.")
            return

        # Check if the piece is a king and moving backwards
        if piece == "K" and to_num == from_num - 8:
            print("Cannot move backwards.")
            return

        # Check if the piece is an 'O' and moving forwards
        if piece == "O" and to_num == from_num + 8:
            print("Cannot move forwards.")
            return

        # Promotion logic
        if piece == "O" and to_num >= 48:  # Assuming the board is 8x8 and 'O' pieces promote after reaching row 7
            board[to_num] = " K "
        elif piece == "X" and to_num <= 15:  # Assuming 'X' pieces promote after reaching row 0
            board[to_num] = " K "

        board[from_num] = piece  # Keep the piece in place if the move is illegal
        board[to_num] = piece
        toHighlight = to_num
        if piece == "X": otherPiece = "O"
        else: otherPiece = "X"
        
        # Capture logic
        # After determining a capture...
        if abs(from_num - to_num) == 14 or abs(from_num - to_num) == 18:  # Diagonal capture
            captured_pos = (from_num + to_num) // 2
            board[captured_pos] = "  "  # Clear the captured piece
            # Update the board to reflect the capture
            board[from_num] = "  "
            board[to_num] = piece
            if (board[abs(to_num - 7)].replace(" ","") == otherPiece): 
                if(board[abs(to_num - 14)] == "  "): print("YOU CAN ATTACK AGAIN")
            elif (board[abs(to_num - 9)].replace(" ","") == otherPiece):
                if (board[abs(to_num - 18)] == "  "): print("YOU CAN ATTACK AGAIN")

    def get_valid_move(): #Takes the move as input
        while True:
            move = input(
                Fore.GREEN
                + "\nEnter your move (for example, A3-B4) or 'q' to quit: "
                + Style.RESET_ALL
            )
            if move.lower() == "q":
                return None
            if (
                len(move) == 5
                and move[2] == "-"
                and move[0].isalpha()
                and move[3].isalpha()
                and move[1].isdigit()
                and move[4].isdigit()
            ):
                return move
                
            print(
                Fore.RED
                + "Invalid move format. Please use the format 'A3-B4' to play a move."
                + Style.RESET_ALL
            )

    def count_valid_moves(player_piece):
        count = 0
        for i in range(len(board)):
            if board[i] == player_piece:
                for j in range(i + 8, len(board), 8):
                    if board[j] == "  ":
                        continue
                    # Check if the piece can move forward
                    if (player_piece == "O" and j <= 47) or (player_piece == "X" and j >= 0):
                        count += 1
        return count

    def check_win_condition(player_piece): #Checks if there's a winner
        # Check if all pieces of the opponent are captured
        opponent_piece = "X" if player_piece == "O" else "O"
        if all(cell == "  " for cell in board if cell != opponent_piece):
            return True
        if opponent_piece not in board:
            return True
        # Check if any piece of the current player is immobilized
        if player_piece == "O":
            for i in range(8):
                if board[i] == player_piece and board[i + 8] == "  ":
                    if board[i + 16] == " O ":  # Blocked by another 'O' piece
                        return False
        else:  # player_piece == "X"
            for i in range(56, 48, -8):
                if board[i] == player_piece and board[i - 8] == "  ":
                    if board[i - 16] == " X ":  # Blocked by another 'X' piece
                        return False
                        return False

        # If neither condition is met, it's not a win yet
        return False

        # If none of the above conditions are met, it's a draw
    # Main game loop
    count = 0
    while True:

        if count % 2 == 0:
            current_player = "O"
        else:
            current_player = "X"

        print(f"It is currently \'{current_player}\'s\' move.")
        if count == 0:
            create_board(board, -1)  # Don't highlight anything if it's the first move
        else:
            print(toHighlight)
            create_board(board, toHighlight)  # Pass toHighlight to create_board
            print(board)

        move = get_valid_move()
        if move is None:
            break
        add_move(move)

        # Count valid moves for both players after each move
        o_moves = count_valid_moves("O")
        x_moves = count_valid_moves("X")

        # Proceed to check for win condition only if both players have no valid moves left
        if (o_moves == 0 and x_moves == 0) or ' O ' not in board or ' X ' not in board:
            if check_win_condition(" O "):
                print(Fore.YELLOW + "Player O wins!" + Style.RESET_ALL)
                break  # Exit the loop since Player O wins
            elif check_win_condition(" X "):
                print(Fore.YELLOW + "Player X wins!" + Style.RESET_ALL)
                break  # Exit the loop since Player X wins
        else:
                print(Fore.YELLOW + "It's a draw." + Style.RESET_ALL)

        count += 1
        count += 1

    print(Fore.YELLOW + "\nThanks for playing checkers!" + Style.RESET_ALL)


if __name__ == "__main__":

    play_game()
