import unittest
from tennis import TennisGame


class TestTennisGame(unittest.TestCase):

    def test_initial_score(self):
        game = TennisGame("player1", "player2")
        self.assertEqual(game.score(), "Love-All")

    def test_player1_scores(self):
        game = TennisGame("player1", "player2")
        game.won_point("player1")
        self.assertEqual(game.score(), "Fifteen-Love")

    def test_player2_scores(self):
        game = TennisGame("player1", "player2")
        game.won_point("player2")
        self.assertEqual(game.score(), "Love-Fifteen")

    def test_deuce(self):
        game = TennisGame("player1", "player2")
        for _ in range(4):
            game.won_point("player1")
            game.won_point("player2")
        self.assertEqual(game.score(), "Deuce")

    def test_advantage_player1(self):
        game = TennisGame("player1", "player2")
        for _ in range(3):
            game.won_point("player1")
            game.won_point("player2")
        game.won_point("player1")
        self.assertEqual(game.score(), "Advantage player1")

    def test_win_player1(self):
        game = TennisGame("player1", "player2")
        for _ in range(4):
            game.won_point("player1")
        self.assertEqual(game.score(), "Win for player1")

    def test_win_player2(self):
        game = TennisGame("player1", "player2")
        for _ in range(4):
            game.won_point("player2")
        self.assertEqual(game.score(), "Win for player2")


if __name__ == "__main__":
    unittest.main()
