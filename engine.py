import requests
import chess


class State:
  pieces_v = { 'q': 4, 'r': 2, 'b': 2, 'n': 2, 'p': 1, 'k': 0 }

  def __init__(self, board):
    self.board = board
    self.v = self.heuristic()
    self.key = ' '.join(self.board.fen().split(' ')[:2])

  def pieces(self, black):
    res = []
    c = chess.BLACK if black else chess.WHITE
    for p in self.board.piece_map().values():
      if p.color == c:
        res.append(p.symbol())
    return res

  def heuristic(self):
    maxim = self.pieces(True)
    minim = self.pieces(False)
    v = 0
    lmf = .01 * self.board.legal_moves.count()
    for p in maxim:
      v += self.pieces_v[p]
      v += lmf
    for p in minim:
      v -= self.pieces_v[p.lower()]
      v -= lmf
    return v

  @staticmethod
  def from_uci(uci):
    return chess.Move.from_uci(uci)

  @staticmethod
  def square_rank(sq):
    return chess.square_rank(sq)

  @staticmethod
  def square_file(sq):
    return chess.square_file(sq)

  @staticmethod
  def from_engine(json):
    g = json['grid']
    fen = ''
    for ri in range(8):
      empc = 0
      for ci in range(8):
        p = g[ri][ci]
        if p is None:
          empc += 1
        else:
          if empc != 0:
            fen += str(empc)
            empc = 0
          n = 'n' if p['name'] == 'Knight' else p['name'][0]
          n = n.lower() if p['color'] == 'BLACK' else n.upper()
          fen += n
      if empc != 0:
        fen += str(empc)
        empc = 0
      if ri != 7:
        fen += '/'
    fen += ' '
    fen += 'b' if json['nextTurn'] == 'BLACK' else 'w'
    fen += ' '
    cstl = ''.join(list(map(lambda s: s[0], json['castlingAllowed'])))
    if len(cstl) > 0:
      fen += cstl.upper() if json['nextTurn'] == 'BLACK' else cstl.lower()
    else:
      fen += '-'
    fen += ' - 0 0'
    return State(chess.Board(fen))


class Engine:

  def __init__(self, board_id):
    self.url = "http://localhost:9999/api"
    self.board_id = board_id
    self.refresh()

  def refresh(self):
    self.board = \
      self.__res(requests.get(url = f'{self.url}/board/{self.board_id}'))
    if self.board_id != self.board['id']:
      raise Exception(f"{self.board_id} != {self.board['id']}")

  def turn(self, m):
    target = {
      "rank": 7-State.square_rank(m.to_square),
      "file": State.square_file(m.to_square)
    }
    f = (7-State.square_rank(m.from_square), State.square_file(m.from_square))
    piece = self.board['grid'][f[0]][f[1]]
    #print(f'from {f} to {target} via {m} piece {piece}')
    pl = {"piece": piece['id'], "target": target}
    if target['rank'] == 0 or target['rank'] == 7:
      pl['promotion'] = 'queen'
    return self.__res(
      requests.post(url=f'{self.url}/board/{self.board_id}/turn', json=pl))

  def castle(self, side, spinoff=False):
    if side != 'KINGSIDE' and side != 'QUEENSIDE':
      raise Exception("Invalid side " + str(side))
    return self.__res(requests.post(url=f'{self.url}/board/{self.board_id}/castle/{side}'))

  def __res(self, res):
    try:
      return res.json()
    except Exception as e:
      print(res.status_code, res.text)
      raise e

