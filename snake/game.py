"""Snake game logic, independent of any UI."""

import random

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


class SnakeGame:
    def __init__(self, width=20, height=15, rng=None):
        if width < 5 or height < 5:
            raise ValueError("board must be at least 5x5")
        self.width = width
        self.height = height
        self.rng = rng or random.Random()
        self.reset()

    def reset(self):
        cx, cy = self.width // 2, self.height // 2
        # Head first.
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self._next_direction = RIGHT
        self.score = 0
        self.game_over = False
        self.food = self._place_food()

    def _place_food(self):
        occupied = set(self.snake)
        free = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in occupied
        ]
        return self.rng.choice(free) if free else None

    def change_direction(self, direction):
        """Queue a direction change; reversing into the snake is ignored."""
        if direction != OPPOSITE[self.direction]:
            self._next_direction = direction

    def step(self):
        """Advance the game by one tick."""
        if self.game_over:
            return
        self.direction = self._next_direction
        dx, dy = self.direction
        hx, hy = self.snake[0]
        new_head = (hx + dx, hy + dy)

        eating = new_head == self.food
        # The tail moves out of the way unless the snake grows this tick.
        body = self.snake if eating else self.snake[:-1]

        x, y = new_head
        if not (0 <= x < self.width and 0 <= y < self.height) or new_head in body:
            self.game_over = True
            return

        self.snake = [new_head] + body
        if eating:
            self.score += 1
            self.food = self._place_food()
            if self.food is None:
                # Board is full: the player wins.
                self.game_over = True
