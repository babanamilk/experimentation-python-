import random
import unittest

from snake.game import DOWN, LEFT, RIGHT, UP, SnakeGame


class SnakeGameTest(unittest.TestCase):
    def setUp(self):
        self.game = SnakeGame(10, 10, rng=random.Random(0))
        self.game.food = (0, 0)  # keep food out of the way

    def test_moves_forward(self):
        head = self.game.snake[0]
        self.game.step()
        self.assertEqual(self.game.snake[0], (head[0] + 1, head[1]))
        self.assertEqual(len(self.game.snake), 3)

    def test_cannot_reverse(self):
        self.game.change_direction(LEFT)
        self.game.step()
        self.assertEqual(self.game.direction, RIGHT)
        self.assertFalse(self.game.game_over)

    def test_eating_grows_and_scores(self):
        hx, hy = self.game.snake[0]
        self.game.food = (hx + 1, hy)
        self.game.step()
        self.assertEqual(len(self.game.snake), 4)
        self.assertEqual(self.game.score, 1)
        self.assertNotIn(self.game.food, self.game.snake)

    def test_wall_collision(self):
        for _ in range(10):
            self.game.step()
        self.assertTrue(self.game.game_over)

    def test_self_collision(self):
        g = self.game
        g.snake = [(5, 5), (4, 5), (3, 5), (3, 6), (4, 6), (5, 6)]
        g.direction = g._next_direction = UP
        g.change_direction(LEFT)
        g.step()  # moves to (4, 5), which is still body
        self.assertTrue(g.game_over)

    def test_moving_into_tail_is_allowed(self):
        g = self.game
        g.snake = [(5, 5), (5, 6), (4, 6), (4, 5)]
        g.direction = g._next_direction = UP
        g.change_direction(LEFT)
        g.step()  # head goes to (4, 5), where the tail just left
        self.assertFalse(g.game_over)

    def test_reset(self):
        self.game.step()
        self.game.score = 5
        self.game.reset()
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)


if __name__ == "__main__":
    unittest.main()
