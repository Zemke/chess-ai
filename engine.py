import requests

class Engine:

  def __init__(self, url=None):
    self.url = url if url is not None else "http://localhost:9999/api"

  def board(self, board_id):
    return self.__res(requests.get(url = f'{self.url}/board/{board_id}'))

  def next_turns(self, board_id, piece_id):
    return self.__res(requests.get(url = f'{self.url}/board/{board_id}/piece/{piece_id}/allowed-next-positions'))

  def turn(self, board_id, piece, target, spinoff=False):
    pl = {"piece": piece, "target": target}
    if target['rank'] == 0 or target['rank'] == 7:
      pl['promotion'] = 'queen'
    params = {'spinoff': "1" if spinoff else "0"}
    print(f"piece{piece} target{target} promotion{pl.get('promotion', '_')} spinoff{spinoff}")
    return self.__res(requests.post(url=f'{self.url}/board/{board_id}/turn',
                                    json=pl,
                                    params=params))

  def turns(self, board_id):
    return self.__res(requests.get(url=f'{self.url}/board/{board_id}/turns'))

  def castle(self, board_id, side, spinoff=False):
    if side != 'KINGSIDE' and side != 'QUEENSIDE':
      raise Exception("Invalid side " + str(side))
    print(f"board_id{board_id} side{side} spinoff{spinoff}")
    return self.__res(requests.get(url=f'{self.url}/board/{board_id}/castle/{side}'))

  def __res(self, res):
    try:
      return res.json()
    except Exception as e:
      print(res.status_code, res.text)
      raise e

"""
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

