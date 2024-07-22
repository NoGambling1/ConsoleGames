# Chess Game Documentation

## Module Overview
this module implements a console-based version of chess. it provides a fully functional chess game with a graphical board display, move validation, check/checkmate detection, and FEN (Forsyth–Edwards Notation) support

## Dependencies
- os
- sys
- time
- pyperclip

## Constants
- `PIECES`: a dictionary mapping chess piece symbols to their Unicode representations

## Classes

### ChessGame
manages the game state and logic for a chess game.

#### Attributes
- `board` (List[List[str]]): 2D list representing the chess board
- `current_player` (str): currnet player ('white' or 'black')
- `move_history` (List[str]): list of moves in algebraic notation
- `castling_rights` (Dict[str, bool]): castling rights for both players
- `en_passant_target` (Tuple[int, int] or None): square where en passant capture is possible
- `halfmove_clock` (int): num of halfmoves since last capture or pawn advance
- `fullmove_number` (int): num of completed turns in the game

#### Methods
- `__init__(self)`: init a new chess game
- `make_move(self, move)`: execute a move on the board
- `is_valid_move(self, move)`: check if a move is valid
- `is_in_check(self, color)`: check if the specified color is in check
- `get_legal_moves(self)`: get all legal moves for the current player
- `is_checkmate(self)`: check if the current position is checkmate
- `is_stalemate(self)`: check if the current position is stalemate
- `is_draw(self)`: check if the game is a draw
- `get_fen(self)`: generate the FEN string for the current position
- `algebraic_to_move(self, algebraic)`: convert algebraic notation to move coordinates
- `display(self)`: display the current game state in the console

## Functions

### play_game()
the main game loop function that manages user interactions and game flow

## Usage
to start a chess game, run select this game from the `main.py` selection screen. the game board will be displayed, allowing the user to:
1. enter moves in algebraic notation (e.g., 'e4', 'Nf3')
2. quit the game ('q')
3. restart the game ('r')
4. copy the current position's FEN to clipboard ('FEN')

## Game Features
- graphical representation of the chess board using Unicode characters
- move validation for all piece types
- support for special moves (castling, en passant, pawn promotion)
- check and checkmate detection
- stalemate and draw detection
- move history display
- FEN generation for the current position

## Input Handling
the game accepts moves in standard algebraic notation, including:
- pawn moves: 'e4', 'd5'
- piece moves: 'Nf3', 'Bb5'
- castling: 'O-O' (kingside), 'O-O-O' (queenside)
- capturing: 'exd5', 'Qxf7'

## Notes
- the game uses Unicode characters for piece representation, which may not display correctly in all console environments
- the board display is designed to work in both Windows and Unix-based systems
-theThe game does not include an AI opponent as it's designed for two human players

## Customization
the game can be customized by modifying the constants at the beginning of the script, such as the piece representations or board size. additional features like time controls or AI opponents could be implemented by extending the `ChessGame` class and modifying the `play_game()` function
