import curses
import random
import time

# const const constant (bun)
WALL = '#'
PELLET = '·'
POWER_PELLET = '●'
EMPTY = ' '
PACMAN = ['c', 'C']
GHOST = 'G'

# dir
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

class PacmanGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.score = 0
        self.lives = 3
        self.pacman_animation_state = 0
        self.level = self.generate_level()
        self.pacman_pos = (self.height // 2, self.width // 2)
        self.ghosts = [
            {'pos': (self.height // 2 - 4, self.width // 2 - 1), 'dir': UP, 'char': 'G'},
            {'pos': (self.height // 2 - 4, self.width // 2), 'dir': UP, 'char': 'G'},
        ]
        self.power_mode = 0

        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # pacman
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # ghost
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)    # wall
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)   # pellet
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # power pellet
        
    def generate_level(self):
        level = []
        for y in range(self.height - 1):
            row = ""
            for x in range(self.width - 1):
                if y == 0 or y == self.height - 2 or x == 0 or x == self.width - 2:
                    row += WALL
                elif (y % 2 == 0 and x % 2 == 0) and random.random() < 0.3:
                    row += WALL
                elif random.random() < 0.02:
                    row += POWER_PELLET
                else:
                    row += PELLET
            level.append(row)
        return level

    def draw(self):
        self.stdscr.clear()
        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                if (y, x) == self.pacman_pos:
                    self.stdscr.addch(y, x, PACMAN[self.pacman_animation_state], curses.color_pair(1))
                elif any(ghost['pos'] == (y, x) for ghost in self.ghosts):
                    self.stdscr.addch(y, x, GHOST, curses.color_pair(2))
                elif cell == WALL:
                    self.stdscr.addch(y, x, cell, curses.color_pair(3))
                elif cell == PELLET:
                    self.stdscr.addch(y, x, cell, curses.color_pair(4))
                elif cell == POWER_PELLET:
                    self.stdscr.addch(y, x, cell, curses.color_pair(5))
                else:
                    self.stdscr.addch(y, x, cell)
        
        score_text = f"Score: {self.score} Lives: {self.lives}"
        self.stdscr.addstr(self.height - 3, (self.width - len(score_text)) // 2, score_text)
        
        directions = "Use arrow keys to move. Press 'q' to quit."
        self.stdscr.addstr(self.height - 2, (self.width - len(directions)) // 2, directions)
        
        self.stdscr.refresh()
        
    def move_pacman(self, direction):
        new_y, new_x = self.pacman_pos[0] + direction[0], self.pacman_pos[1] + direction[1]
        if self.level[new_y][new_x] != WALL:
            self.pacman_pos = (new_y, new_x)
            if self.level[new_y][new_x] == PELLET:
                self.score += 10
                self.level[new_y] = self.level[new_y][:new_x] + EMPTY + self.level[new_y][new_x+1:]
            elif self.level[new_y][new_x] == POWER_PELLET:
                self.score += 50
                self.power_mode = 20
                self.level[new_y] = self.level[new_y][:new_x] + EMPTY + self.level[new_y][new_x+1:]
        self.pacman_animation_state = 1 - self.pacman_animation_state
                        
    def move_ghost(self, ghost):
        directions = [UP, DOWN, LEFT, RIGHT]
        new_pos = None
        while not new_pos or self.level[new_pos[0]][new_pos[1]] == WALL:
            direction = random.choice(directions)
            new_pos = (ghost['pos'][0] + direction[0], ghost['pos'][1] + direction[1])
        ghost['pos'] = new_pos
        
    def check_collision(self):
        for ghost in self.ghosts:
            if ghost['pos'] == self.pacman_pos:
                if self.power_mode > 0:
                    self.score += 200
                    ghost['pos'] = (self.height // 2 - 4, self.width // 2)
                else:
                    self.lives -= 1
                    if self.lives == 0:
                        return False
                    self.pacman_pos = (self.height // 2, self.width // 2)
        return True
        
    def run(self):
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        
        while True:
            self.draw()
            
            key = self.stdscr.getch()
            if key == ord('q'):
                break
            elif key == curses.KEY_UP:
                self.move_pacman(UP)
            elif key == curses.KEY_DOWN:
                self.move_pacman(DOWN)
            elif key == curses.KEY_LEFT:
                self.move_pacman(LEFT)
            elif key == curses.KEY_RIGHT:
                self.move_pacman(RIGHT)
                
            for ghost in self.ghosts:
                self.move_ghost(ghost)
                
            if not self.check_collision():
                break
                
            if self.power_mode > 0:
                self.power_mode -= 1
                
            time.sleep(0.1)
        
        self.stdscr.addstr(self.height - 1, (self.width - 20) // 2, "game over! press any key to exit...")
        self.stdscr.refresh()
        self.stdscr.getch()

def play_game():
    curses.wrapper(lambda stdscr: PacmanGame(stdscr).run())

if __name__ == "__main__":
    play_game()