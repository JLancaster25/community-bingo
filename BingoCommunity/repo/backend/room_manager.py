from bingo_engine import BingoGame, BingoCard


class Room:
  def __init__(self, code, password=None):
    self.code = code
    self.password = password
    self.game = BingoGame()
    self.players = {} # sid -> BingoCard


  def add_player(self, sid):
    self.players[sid] = BingoCard()
    return self.players[sid]


  def remove_player(self, sid):

    self.players.pop(sid, None)

