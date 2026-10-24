"""Terminal front end for the snake game. Run with: python -m snake"""

import curses

from .game import DOWN, LEFT, RIGHT, UP, SnakeGame

KEYS = {
    curses.KEY_UP: UP,
    curses.KEY_DOWN: DOWN,
    curses.KEY_LEFT: LEFT,
    curses.KEY_RIGHT: RIGHT,
    ord("w"): UP,
    ord("s"): DOWN,
    ord("a"): LEFT,
    ord("d"): RIGHT,
}

TICK_MS = 120


def draw(win, game):
    win.erase()
    win.border()
    win.addstr(0, 1, f" Score: {game.score} "[: game.width])
    fx, fy = game.food if game.food else (None, None)
    if game.food:
        win.addstr(fy + 1, fx + 1, "*", curses.color_pair(2))
    for i, (x, y) in enumerate(game.snake):
        win.addstr(y + 1, x + 1, "@" if i == 0 else "o", curses.color_pair(1))
    if game.game_over:
        msg = " GAME OVER - r: restart, q: quit "[: game.width]
        win.addstr(game.height // 2 + 1, 1 + (game.width - len(msg)) // 2, msg)
    win.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)

    rows, cols = stdscr.getmaxyx()
    width = max(5, min(40, cols - 2))
    height = max(5, min(20, rows - 3))
    game = SnakeGame(width, height)

    win = curses.newwin(height + 2, width + 2, 0, 0)
    win.keypad(True)
    win.timeout(TICK_MS)

    while True:
        draw(win, game)
        key = win.getch()
        if key in (ord("q"), 27):
            break
        if key == ord("r") and game.game_over:
            game.reset()
            continue
        if key in KEYS:
            game.change_direction(KEYS[key])
        game.step()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except curses.error:
        print("Terminal is too small. Please enlarge the window and try again.")
