import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from model.ball import Ball

class TestBall(unittest.TestCase):
    def test_move(self):
        ball = Ball(100, 100, 5, 50, 60)
        ball.move(0.1)
        self.assertAlmostEqual(ball.x, 105.0)
        self.assertAlmostEqual(ball.y, 106.0)

    def test_bounce_x(self):
        ball = Ball(0, 0, 5, 100, 0)
        ball.bounce_x()
        self.assertEqual(ball.vx, -100)

if __name__ == '__main__':
    unittest.main()