import os
import sys
import time
import pyperclip

PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
    '.': ' '
}

class ChessGame:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.current_player = 'white'
        self.move_history = []
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1

    def make_move(self, move):
        start, end = move[:2], move[2:4]
        start_row, start_col = 8 - int(start[1]), ord(start[0]) - ord('a')
        end_row, end_col = 8 - int(end[1]), ord(end[0]) - ord('a')

        piece = self.board[start_row][start_col]
        captured_piece = self.board[end_row][end_col]

        if piece.upper() == 'K':
            self.castling_rights['K' if piece.isupper() else 'k'] = False
            self.castling_rights['Q' if piece.isupper() else 'q'] = False
        elif piece.upper() == 'R':
            if start_col == 0:
                self.castling_rights['Q' if piece.isupper() else 'q'] = False
            elif start_col == 7:
                self.castling_rights['K' if piece.isupper() else 'k'] = False

        if piece.upper() == 'K' and abs(start_col - end_col) == 2:
            if end_col == 6:  
                self.board[end_row][5] = self.board[end_row][7]
                self.board[end_row][7] = '.'
            else:  
                self.board[end_row][3] = self.board[end_row][0]
                self.board[end_row][0] = '.'

        if piece.upper() == 'P' and abs(start_row - end_row) == 2:
            self.en_passant_target = (start_row + end_row) // 2, start_col
        elif piece.upper() == 'P' and (end_row, end_col) == self.en_passant_target:
            self.board[start_row][end_col] = '.'

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '.'

        if len(move) == 5 and piece.upper() == 'P' and (end_row == 0 or end_row == 7):
            self.board[end_row][end_col] = move[4].upper() if piece.isupper() else move[4].lower()

        if piece.upper() == 'P' or captured_piece != '.':
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        if self.current_player == 'black':
            self.fullmove_number += 1

        self.current_player = 'black' if self.current_player == 'white' else 'white'

        if self.en_passant_target and (end_row, end_col) != self.en_passant_target:
            self.en_passant_target = None

    def is_valid_move(self, move):
        start, end = move[:2], move[2:4]
        start_row, start_col = 8 - int(start[1]), ord(start[0]) - ord('a')
        end_row, end_col = 8 - int(end[1]), ord(end[0]) - ord('a')

        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]

        if piece == '.' or (piece.isupper() and self.current_player == 'black') or (piece.islower() and self.current_player == 'white'):
            return False
        
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        if (piece.isupper() and target.isupper()) or (piece.islower() and target.islower()):
            return False

        piece_type = piece.lower()
        if piece_type == 'p':
            return self._is_valid_pawn_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'r':
            return self._is_valid_rook_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'n':
            return self._is_valid_knight_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'b':
            return self._is_valid_bishop_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'q':
            return self._is_valid_queen_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'k':
            return self._is_valid_king_move(start_row, start_col, end_row, end_col)

        return False

    def _is_valid_pawn_move(self, start_row, start_col, end_row, end_col):
        direction = -1 if self.current_player == 'white' else 1
        if start_col == end_col:  
            if end_row == start_row + direction and self.board[end_row][end_col] == '.':
                return True
            if (start_row == 1 and self.current_player == 'black') or (start_row == 6 and self.current_player == 'white'):
                if end_row == start_row + 2 * direction and self.board[end_row][end_col] == '.' and self.board[start_row + direction][start_col] == '.':
                    return True
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:  
            if self.board[end_row][end_col] != '.' or (end_row, end_col) == self.en_passant_target:
                return True
        return False

    def _is_valid_rook_move(self, start_row, start_col, end_row, end_col):
        if start_row != end_row and start_col != end_col:
            return False
        direction_row = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        direction_col = 0 if start_col == end_col else (1 if end_col > start_col else -1)
        current_row, current_col = start_row + direction_row, start_col + direction_col
        while (current_row, current_col) != (end_row, end_col):
            if self.board[current_row][current_col] != '.':
                return False
            current_row += direction_row
            current_col += direction_col
        return True

    def _is_valid_knight_move(self, start_row, start_col, end_row, end_col):
        return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
               (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)

    def _is_valid_bishop_move(self, start_row, start_col, end_row, end_col):
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        direction_row = 1 if end_row > start_row else -1
        direction_col = 1 if end_col > start_col else -1
        current_row, current_col = start_row + direction_row, start_col + direction_col
        while (current_row, current_col) != (end_row, end_col):
            if self.board[current_row][current_col] != '.':
                return False
            current_row += direction_row
            current_col += direction_col
        return True

    def _is_valid_queen_move(self, start_row, start_col, end_row, end_col):
        return self._is_valid_rook_move(start_row, start_col, end_row, end_col) or \
               self._is_valid_bishop_move(start_row, start_col, end_row, end_col)

    def _is_valid_king_move(self, start_row, start_col, end_row, end_col):
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return True
        if abs(start_col - end_col) == 2 and start_row == end_row:
            if self.current_player == 'white' and start_row == 7:
                if end_col == 6 and self.castling_rights['K'] and self.board[7][5] == '.' and self.board[7][6] == '.':
                    return True
                if end_col == 2 and self.castling_rights['Q'] and self.board[7][1] == '.' and self.board[7][2] == '.' and self.board[7][3] == '.':
                    return True
            elif self.current_player == 'black' and start_row == 0:
                if end_col == 6 and self.castling_rights['k'] and self.board[0][5] == '.' and self.board[0][6] == '.':
                    return True
                if end_col == 2 and self.castling_rights['q'] and self.board[0][1] == '.' and self.board[0][2] == '.' and self.board[0][3] == '.':
                    return True
        return False

    def is_in_check(self, color):
        king_pos = None
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == ('K' if color == 'white' else 'k'):
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if (piece.isupper() and opponent_color == 'white') or (piece.islower() and opponent_color == 'black'):
                    if self.is_valid_move(f"{chr(col + ord('a'))}{8-row}{chr(king_pos[1] + ord('a'))}{8-king_pos[0]}"):
                        return True
        return False

    def get_legal_moves(self):
        legal_moves = []
        for start_row in range(8):
            for start_col in range(8):
                piece = self.board[start_row][start_col]
                if (piece.isupper() and self.current_player == 'white') or (piece.islower() and self.current_player == 'black'):
                    for end_row in range(8):
                        for end_col in range(8):
                            move = f"{chr(start_col + ord('a'))}{8-start_row}{chr(end_col + ord('a'))}{8-end_row}"
                            if self.is_valid_move(move):
                                temp_board = [row[:] for row in self.board]
                                self.make_move(move)
                                if not self.is_in_check(self.current_player):
                                    legal_moves.append(move)
                                self.board = temp_board
        return legal_moves

    def is_checkmate(self):
        return self.is_in_check(self.current_player) and not self.get_legal_moves()

    def is_stalemate(self):
        return not self.is_in_check(self.current_player) and not self.get_legal_moves()

    def is_draw(self):
        if self.halfmove_clock >= 100:
            return True
        # need to implement other checks
        return False

    def get_fen(self):
        fen = ''
        for row in self.board:
            empty = 0
            for piece in row:
                if piece == '.':
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    fen += piece
            if empty > 0:
                fen += str(empty)
            fen += '/'
        fen = fen[:-1]  
        fen += f" {'w' if self.current_player == 'white' else 'b'} "
        fen += ''.join(k for k, v in self.castling_rights.items() if v)
        fen += ' - ' if not self.en_passant_target else f" {chr(ord('a') + self.en_passant_target[1])}{8 - self.en_passant_target[0]} "
        fen += f"{self.halfmove_clock} {self.fullmove_number}"
        return fen

    def algebraic_to_move(self, algebraic):
        if algebraic == "O-O": 
            return "e1g1" if self.current_player == 'white' else "e8g8"
        elif algebraic == "O-O-O": 
            return "e1c1" if self.current_player == 'white' else "e8c8"

        piece = 'P'
        if algebraic[0] in "NBRQK":
            piece = algebraic[0]
            algebraic = algebraic[1:]

        if 'x' in algebraic:
            algebraic = algebraic.replace('x', '')

        end = algebraic[-2:]
        start = ""

        if len(algebraic) > 2:
            start = algebraic[:-2]

        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

        for row in range(8):
            for col in range(8):
                if self.board[row][col].upper() == piece:
                    if start:
                        if start[0] in "abcdefgh" and col != ord(start[0]) - ord('a'):
                            continue
                        if start[0] in "12345678" and row != 8 - int(start[0]):
                            continue
                    move = f"{chr(col + ord('a'))}{8-row}{end}"
                    if self.is_valid_move(move):
                        return move

        return None

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        terminal_width = os.get_terminal_size().columns
        terminal_height = os.get_terminal_size().lines
        
        board_width = 33  
        board_height = 17  
        
        left_padding = (terminal_width - board_width) // 2
        
        print("\n" * ((terminal_height - board_height - 10) // 2))
        
        print(f"{' ' * left_padding}Current player: {self.current_player}\n")
        
        print(" " * left_padding + "    a   b   c   d   e   f   g   h")
        
        print(" " * left_padding + "  ┌───┬───┬───┬───┬───┬───┬───┬───┐")
        
        for i, row in enumerate(self.board):
            print(f"{' ' * left_padding}{8-i} │", end="")
            for piece in row:
                print(f" {PIECES[piece]} │", end="")
            print(f" {8-i}")
            if i < 7:
                print(" " * left_padding + "  ├───┼───┼───┼───┼───┼───┼───┼───┤")
        
        print(" " * left_padding + "  └───┴───┴───┴───┴───┴───┴───┴───┘")
        
        print(" " * left_padding + "    a   b   c   d   e   f   g   h")
        
        controls = [
            "Controls:",
            "- Enter move (e.g., 'e4' or 'Nf3')",
            "- 'q' to quit",
            "- 'r' to restart game",
            "- 'FEN' to copy FEN to clipboard"
        ]
        for line in controls:
            print(f"{' ' * left_padding}{line}")
        
        history_left_padding = terminal_width - 20  
        print("\n" * (-board_height - 5))  
        print(f"{' ' * history_left_padding}Move History")
        for i, move in enumerate(self.move_history):
            print(f"{' ' * history_left_padding}{i//2 + 1}. {move}", end="")
            if i % 2 == 0 and i < len(self.move_history) - 1:
                print(f"{' ' * 5}{self.move_history[i+1]}")
            else:
                print()

def play_game():
    game = ChessGame()
    while True:
        game.display()
        move_input = input(f"{' ' * ((os.get_terminal_size().columns - 50) // 2)}Enter your move: ").strip()
        if move_input.lower() == 'q':
            break
        elif move_input.lower() == 'r':
            game = ChessGame()
        elif move_input.upper() == 'FEN':
            pyperclip.copy(game.get_fen())
            print("FEN copied to clipboard!")
            time.sleep(1)
        else:
            move = game.algebraic_to_move(move_input)
            if move and game.is_valid_move(move):
                game.make_move(move)
                game.move_history.append(move_input)
                if game.is_in_check(game.current_player):
                    print("Check!")
                if game.is_checkmate():
                    game.display()
                    print(f"Checkmate! {'Black' if game.current_player == 'white' else 'White'} wins!")
                    break
                elif game.is_stalemate():
                    game.display()
                    print("Stalemate! The game is a draw.")
                    break
                elif game.is_draw():
                    game.display()
                    print("The game is a draw.")
                    break
            else:
                print("Invalid move. Please try again.")
                time.sleep(1)
    input("Press 'Enter' to return to the main menu...")

if __name__ == "__main__":
    play_game()