import curses
import random

# Initialize curses
stdscr = curses.initscr()
curses.curs_set(0)  # Hide the cursor
stdscr.keypad(True)  # Enable keypad input
curses.noecho()      # Disable echoing of keys
stdscr.timeout(100)  # Set input timeout

# Set up game variables
HEIGHT, WIDTH = 20, 40
player_char = "X"
empty_char = " "
item_char = "*"
obstacle_char = "#"
player_pos = [HEIGHT // 2, WIDTH // 2]
score = 0
items = []
obstacles = []

# Function to draw the game screen
def draw():
    stdscr.clear()
    stdscr.addstr(0, 0, "Keybored Game - Use arrow keys to move")
    stdscr.addstr(HEIGHT + 1, 0, "Score: " + str(score))
    for item in items:
        stdscr.addch(item[0], item[1], item_char)
    for obstacle in obstacles:
        stdscr.addch(obstacle[0], obstacle[1], obstacle_char)
    stdscr.addch(player_pos[0], player_pos[1], player_char)
    stdscr.refresh()

# Function to move the player
def move_player(key):
    global player_pos, score
    if key == curses.KEY_UP and player_pos[0] > 1:
        player_pos[0] -= 1
    elif key == curses.KEY_DOWN and player_pos[0] < HEIGHT:
        player_pos[0] += 1
    elif key == curses.KEY_LEFT and player_pos[1] > 1:
        player_pos[1] -= 1
    elif key == curses.KEY_RIGHT and player_pos[1] < WIDTH:
        player_pos[1] += 1
    
    # Check for collisions with items
    for item in items:
        if player_pos == item:
            score += 1
            items.remove(item)
            items.append(generate_random_pos())

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if player_pos == obstacle:
            stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 5, "Game Over!")
            stdscr.refresh()
            stdscr.getch()
            curses.endwin()
            quit()

# Function to generate random positions for items and obstacles
def generate_random_pos():
    return [random.randint(1, HEIGHT), random.randint(1, WIDTH)]

# Initialize items and obstacles
for _ in range(5):
    items.append(generate_random_pos())
    obstacles.append(generate_random_pos())

# Main game loop
while True:
    draw()
    key = stdscr.getch()
    if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
        move_player(key)
    elif key == ord("q"):  # Quit game if 'q' is pressed
        break

curses.endwin()  # End curses mode
