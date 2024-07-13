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

    def create_board(board, toHighlight):
        whatShouldIHighlight = toHighlight #25
        print("\n" + Fore.YELLOW + "welcome to checkers!" + Style.RESET_ALL)
        print(Fore.CYAN + "\ncurrent board:" + Style.RESET_ALL)
        for count in range(8):
            print(Fore.CYAN + f"{count+1} |", end="  " + Style.RESET_ALL)

            for newCount in range(8):
                spot = (count * 8) + newCount
                if (int(spot) == int(whatShouldIHighlight)):

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
                        print("[" + board[spot] + "]", end=" " + Back.CYAN)
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
        print("   ----------------------------------------------")
        print("      A     B    C     D     E    F    G     H")

    def cord_to_num(coordinate):
        coord_arr = list(coordinate.lower())
        return (int(coord_arr[1]) - 1) * 8 + (ord(coord_arr[0]) - 97)

    def add_move(move):
        global toHighlight
        move_from, move_to = move.split("-")
        from_num = cord_to_num(move_from)
        to_num = cord_to_num(move_to)
        diff = to_num - from_num

        piece = board[from_num]

        if piece != current_player:
            print("It's not your turn.")
            return

        if abs(diff) != 7 and abs(diff) != 9:  # 7 and 9 are the differences when capturing diagonally
            print("Move is not diagonal.")
            return

        # Check if the piece is a king and moving backwards
        if piece == "K" and to_num < from_num:
            print("Cannot move backwards.")
            return

        # Check if the piece is an 'O' and moving forwards
        if piece == "O" and to_num > from_num:
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

        # Capture logic
        if abs(from_num - to_num) == 7:  # Diagonal capture
            captured_pos = (from_num + to_num) // 2
            board[captured_pos] = "  "
        # Check for additional captures
            while captured_pos - 8 >= 0 and board[captured_pos - 8] == "X" and board[captured_pos - 16] == "O":
                board[captured_pos - 8] = "  "
                captured_pos -= 16
            while captured_pos + 8 < 64 and board[captured_pos + 8] == "O" and board[captured_pos + 16] == "X":
                board[captured_pos + 8] = "  "
                captured_pos += 16

    def get_valid_move():
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

    def check_win_condition(player_piece):
        for i in range(len(board)):
            if board[i] == player_piece:
                for j in range(i + 8, len(board), 8):
                    if board[j] == "  ":
                        return False
        return True

    # Main game loop
    count = 0
    while True:

        if count % 2 == 0:
            current_player = "O"
        else:
            current_player = "X"

        if count == 0:
            create_board(board, toHighlight)  # Pass toHighlight to create_board
        else:
            create_board(board, toHighlight)  # Pass toHighlight to create_board

        move = get_valid_move()
        if move is None:
            break
        add_move(move)
        if check_win_condition("O"):
            print(Fore.YELLOW + "Player O wins!" + Style.RESET_ALL)
        elif check_win_condition("X"):
            print(Fore.YELLOW + "Player X wins!" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "It's a draw." + Style.RESET_ALL)

        count += 1

    print(Fore.YELLOW + "\nThanks for playing checkers!" + Style.RESET_ALL)


if __name__ == "__main__":
    play_game()
