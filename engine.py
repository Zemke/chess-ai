import requests

class Engine:
  COLOR = 'BLACK'

  def __init__(self, board_id, url=None):
    self.board_id = board_id
    self.url = url if url is not None else "http://localhost:9999/api"

  def board(self):
    return requests.get(url = f'{self.url}/board/{self.board_id}').json()

  def next_turns(self, piece_id):
    return requests.get(url = f'{self.url}/board/{self.board_id}/piece/{piece_id}/allowed-next-positions').json()

  def turn(self, piece, target):
    pl = {"piece": piece, "target": target}
    print('turn', pl)
    print('  at', f'{self.url}/board/{self.board_id}/turn')
    return requests.post(url = f'{self.url}/board/{self.board_id}/turn', json=pl)


"""
Board statte

class State:
  "captured" : [],
  "castlingAllowed" : [],
  "grid" : [ [
        {
           "color" : "BLACK",
           "id" : "8c8ee347-f88e-45a0-be57-c9322154bab2",
           "name" : "Rook",
           "position" : {
              "file" : 0,
              "rank" : 0
           },
           "side" : "QUEENSIDE"
  .
  .
  .
  "id" : "d87ba920-8fcc-4539-9186-5e142c1ce5bf",
  "movements" : [],
  "nextTurn" : "WHITE",
  "uuidBlack" : null,
  "uuidWhite" : "fcd1c27e-8e11-412f-8de8-4ee54b8b9ea7"
  def __init__(self, grid, next_turn):
    self.grid = grid
    next_turn = next_turn

  def from_engine(self, json):
    return State(
      grid = json.
    )
"""

