class TennisGame:
    SCORE_NAMES = ["Love", "Fifteen", "Thirty", "Forty"]
    DEUCE_THRESHOLD = 3

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1_points = 0
        self.p2_points = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.p1_points += 1
        else:
            self.p2_points += 1

    def score(self):
        if self.p1_points == self.p2_points:
            return self._tied_score()
        elif self.p1_points >= 4 or self.p2_points >= 4:
            return self._advantage_or_win()
        else:
            return f"{self.SCORE_NAMES[self.p1_points]}-{self.SCORE_NAMES[self.p2_points]}"

    def _tied_score(self):
        if self.p1_points > self.DEUCE_THRESHOLD:
            return "Deuce"
        return f"{self.SCORE_NAMES[self.p1_points]}-All"

    def _advantage_or_win(self):
        score_diff = self.p1_points - self.p2_points
        if abs(score_diff) == 1:
            return f"Advantage {self._leading_player()}"
        return f"Win for {self._leading_player()}"

    def _leading_player(self):
        return self.player1_name if self.p1_points > self.p2_points else self.player2_name
