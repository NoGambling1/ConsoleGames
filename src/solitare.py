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
        return "🂠"

class Solitaire:
    def __init__(self):
        self.deck = [Card(suit, value) for suit in SUITS for value in VALUES]
        random.shuffle(self.deck)
        self.tableau = [[] for _ in range(7)]
        self.foundation = [[] for _ in range(4)]
        self.waste = []
        self.stock = []
        self.setup_game()

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
        else:
            card = self.stock.pop()
            card.visible = True
            self.waste.append(card)

    def move_card(self, from_pile, to_pile, card_index):
        card = from_pile[card_index]
        to_pile.append(card)
        from_pile.pop(card_index)
        if from_pile and not from_pile[-1].visible:
            from_pile[-1].visible = True

def play_game(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    game = Solitaire()
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # drawing the tableau
        for i, pile in enumerate(game.tableau):
            for j, card in enumerate(pile):
                y = 3 + j
                x = 5 + i * 8
                if card.suit in ['♥', '♦']:
                    stdscr.addstr(y, x, str(card), curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, str(card), curses.color_pair(2))

        # drawing the foundation
        for i, pile in enumerate(game.foundation):
            if pile:
                y = 1
                x = 5 + i * 8
                card = pile[-1]
                if card.suit in ['♥', '♦']:
                    stdscr.addstr(y, x, str(card), curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, str(card), curses.color_pair(2))

        # drawing the stock and waste piles
        stdscr.addstr(1, width - 10, "🂠" if game.stock else " ", curses.color_pair(2))
        if game.waste:
            card = game.waste[-1]
            if card.suit in ['♥', '♦']:
                stdscr.addstr(1, width - 5, str(card), curses.color_pair(1))
            else:
                stdscr.addstr(1, width - 5, str(card), curses.color_pair(2))

        # draw instructions
        instructions = "D: Draw | Q: Quit"
        stdscr.addstr(height - 2, (width - len(instructions)) // 2, instructions)

        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('d') or key == ord('D'):
            game.draw_card()

if __name__ == "__main__":
    curses.wrapper(main)