import curses
import random

SUITS = ['♠', '♥', '♦', '♣']
VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.visible = False

    def __str__(self):
        if self.visible:
            return f"{self.value}{self.suit}"
        return "🂠 "

class Solitaire:
    def __init__(self):
        self.deck = [Card(suit, value) for suit in SUITS for value in VALUES]
        random.shuffle(self.deck)
        self.tableau = [[] for _ in range(7)]
        self.foundation = [[] for _ in range(4)]
        self.waste = []
        self.stock = []
        self.setup_game()
        self.width = 0  

    def setup_game(self):
        for i in range(7):
            for j in range(i, 7):
                card = self.deck.pop()
                if i == j:
                    card.visible = True
                self.tableau[j].append(card)
        self.stock = self.deck

    def draw_card(self):
        if not self.stock:
            self.stock = self.waste[::-1]
            self.waste = []
            for card in self.stock:
                card.visible = False
        else:
            card = self.stock.pop()
            card.visible = True
            self.waste.append(card)

    def move_card(self, from_pile, to_pile, card_index):
        cards_to_move = from_pile[card_index:]
        to_pile.extend(cards_to_move)
        del from_pile[card_index:]
        if from_pile and not from_pile[-1].visible:
            from_pile[-1].visible = True

    def can_move_to_tableau(self, card, dest_pile):
        if not dest_pile:
            return card.value == 'K'
        top_card = dest_pile[-1]
        return (VALUES.index(card.value) == VALUES.index(top_card.value) - 1 and
                ((card.suit in ['♥', '♦'] and top_card.suit in ['♠', '♣']) or
                 (card.suit in ['♠', '♣'] and top_card.suit in ['♥', '♦'])))

    def can_move_to_foundation(self, card, foundation_pile):
        if not foundation_pile:
            return card.value == 'A'
        top_card = foundation_pile[-1]
        return (card.suit == top_card.suit and
                VALUES.index(card.value) == VALUES.index(top_card.value) + 1)

    def get_card_at_position(self, x, y):
        col = (x - 5) // 10
        row = y - 3
        if 0 <= col < 7:
            if row < 0:  # foundation area
                return self.foundation[col][-1] if self.foundation[col] else None
            elif row < len(self.tableau[col]):
                return self.tableau[col][row]
        elif y == 1 and x >= self.width - 15:  # stock and waste area
            if x >= self.width - 5 and self.waste:
                return self.waste[-1]
        return None

    def is_game_won(self):
        return all(len(pile) == 13 for pile in self.foundation)

def solitaire_game(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    game = Solitaire()
    selected_card = None
    cursor_x, cursor_y = 5, 3

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        game.width = width 

        # drawing the tableau
        for i, pile in enumerate(game.tableau):
            for j, card in enumerate(pile):
                y = 3 + j
                x = 5 + i * 10
                if card.suit in ['♥', '♦']:
                    stdscr.addstr(y, x, str(card), curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, str(card), curses.color_pair(2))

        # drawing the foundation
        for i, pile in enumerate(game.foundation):
            y = 1
            x = 5 + i * 10
            if pile:
                card = pile[-1]
                if card.suit in ['♥', '♦']:
                    stdscr.addstr(y, x, str(card), curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, str(card), curses.color_pair(2))
            else:
                stdscr.addstr(y, x, "[ ]", curses.color_pair(2))

        # drawing the stock and waste piles
        stdscr.addstr(1, width - 15, "🂠 " if game.stock else "  ", curses.color_pair(2))
        if game.waste:
            card = game.waste[-1]
            if card.suit in ['♥', '♦']:
                stdscr.addstr(1, width - 5, str(card), curses.color_pair(1))
            else:
                stdscr.addstr(1, width - 5, str(card), curses.color_pair(2))

        # drawing the cursor
        stdscr.addch(cursor_y, cursor_x, '+', curses.A_REVERSE)

        # drawing instructions and selected card info
        instructions = "Arrows: Move | Space: Select/Move | D: Draw | Q: Quit"
        stdscr.addstr(height - 3, (width - len(instructions)) // 2, instructions)
        if selected_card:
            selected_info = f"Selected: {selected_card}"
            stdscr.addstr(height - 2, (width - len(selected_info)) // 2, selected_info, curses.color_pair(3))

        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('d') or key == ord('D'):
            game.draw_card()
        elif key == curses.KEY_UP:
            cursor_y = max(1, cursor_y - 1)
        elif key == curses.KEY_DOWN:
            cursor_y = min(height - 4, cursor_y + 1)
        elif key == curses.KEY_LEFT:
            cursor_x = max(5, cursor_x - 10)
        elif key == curses.KEY_RIGHT:
            cursor_x = min(width - 5, cursor_x + 10)
        elif key == ord(' '):
            card = game.get_card_at_position(cursor_x, cursor_y)
            if isinstance(card, Card):
                if selected_card:
                    # try: move the selected card
                    from_pile = next((pile for pile in game.tableau if selected_card in pile), None)
                    if from_pile is None:
                        from_pile = game.waste

                    if cursor_y >= 3:  # moving to tableau
                        to_pile = game.tableau[(cursor_x - 5) // 10]
                        if game.can_move_to_tableau(selected_card, to_pile):
                            game.move_card(from_pile, to_pile, from_pile.index(selected_card))
                    elif cursor_y == 1 and 5 <= cursor_x <= 35:  # moving to foundation
                        foundation_index = (cursor_x - 5) // 10
                        if game.can_move_to_foundation(selected_card, game.foundation[foundation_index]):
                            game.move_card(from_pile, game.foundation[foundation_index], from_pile.index(selected_card))

                    selected_card = None
                else:
                    if card.visible:
                        selected_card = card
            elif cursor_y == 1 and cursor_x >= width - 15:
                # stock and waste pile logic
                if cursor_x == width - 15 and game.stock:
                    game.draw_card()
                elif cursor_x == width - 5 and game.waste:
                    selected_card = game.waste[-1]

        if game.is_game_won():
            stdscr.addstr(height // 2, (width - 18) // 2, "winner winner chicken dinner", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
            break

def play_game():
    curses.wrapper(solitaire_game)

if __name__ == "__main__":
    play_game()