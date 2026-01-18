class StatsManager:
  def __init__(self):
    self.stats = {}


  def record_win(self, username):
    s = self.stats.setdefault(username, {"wins":0,"games":0})
    s["wins"] += 1
    s["games"] += 1


  def record_game(self, username):
    s = self.stats.setdefault(username, {"wins":0,"games":0})
    s["games"] += 1


  def leaderboard(self):

  return sorted(self.stats.items(), key=lambda x: x[1]["wins"], reverse=True)
