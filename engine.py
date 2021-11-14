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
    return self.__res(requests.post(url=f'{self.url}/board/{board_id}/castle/{side}'))

  def __res(self, res):
    try:
      return res.json()
    except Exception as e:
      print(res.status_code, res.text)
      raise e

