from engine import Engine
from math import inf
from time import time


class Maximizer:
  C = 'BLACK'

  def __init__(self, eng, board_id):
    self.eng = eng
    self.board_id = board_id

  def move(self):
    board = State.from_engine(eng.board(self.board_id))
    v, t = self.minimax(3, board, True, -inf, +inf)
    if t.castling:
      self.eng.castle(self.board_id, t.castling)
    else:
      self.eng.turn(self.board_id, t.piece, t.target)
    return v

  def heuristic(self, state):
    pieces_v = { 'q': 100, 'r': 50, 'b': 50, 'k': 50, 'p': 20, 'x': 0 }
    maxim = state.pieces(True)
    minim = state.pieces(False)
    v = 0
    for p in maxim:
      v += pieces_v[p]
    for p in minim:
      v -= pieces_v[p.lower()]
    return v

  def minimax(self, la, state, maxim, a, b, rett=True):
    if state.checkmated:
      return -inf if maxim else +inf
    elif la == 0:
      # TODO a heuristic may also be a neural network
      return self.heuristic(state)
    if maxim:
      v = -inf
      for t, s in self.__spinoff_boards(state, True):
        mx = self.minimax(la-1, s, False, a, b, False)
        # our goal is to maximize
        if mx > v:
          v = mx
          v_t = t
        a = max(a, v)
        if b <= a:
          break
    else:
      v = +inf
      for t, s in self.__spinoff_boards(state, False):
        v = min(v, self.minimax(la-1, s, True, a, b, False))
        b = min(b, v)
        if b <= a:
          break
    return (v, v_t) if rett else v

  def __spinoff_boards(self, state, maxim):
    res = []
    for side in state.castling:
      s = State.from_engine(self.eng.castle(state.board_id, side, True))
      res.append((self.heuristic(s), Move.castling(side), s))
    for turn in self.eng.turns(state.board_id):
      for target in turn['targets']:
        piece = turn['piece']['id']
        s = State.from_engine(
          self.eng.turn(state.board_id, piece, target, True))
        res.append((self.heuristic(s), Move.turn(piece, target), s))
    res.sort(key=lambda x: x[0], reverse=maxim)
    for r in res:
      yield [r[1], r[2]]


class Move:
  def __init__(self, piece=None, target=None, castling=False):
    self.piece = piece
    self.target = target
    self.castling = castling  # QUEENSIDE, KINGSIDE

  @staticmethod
  def castling(side):
    return Move(castling=side)

  @staticmethod
  def turn(piece, target):
    return Move(piece=piece, target=target)


class State:
  def __init__(self, board_id, grid, next_turn, checkmated, castling):
    self.board_id = board_id
    self.grid = grid
    self.next_turn = next_turn
    self.checkmated = checkmated
    self.castling = castling

  def pieces(self, black):
    pp = []
    for rank in self.grid:
      for p in rank:
        if p is None:
          continue
        elif black and p.islower():
          pp.append(p)
        elif not black and p.isupper():
          pp.append(p)
    return pp

  @staticmethod
  def from_engine(json):
    g = json['grid']
    r = [[None for k in range(8)] for i in range(8)]
    for ri in range(8):
      for ci in range(8):
        p = g[ri][ci]
        if p is not None:
          n = 'x' if p['name'] == 'King' else p['name'][0]
          n = n.lower() if p['color'] == Maximizer.C else n.upper()
          r[ri][ci] = n
    return State(board_id=json['id'],
                 grid=r,
                 next_turn=json['nextTurn'],
                 checkmated=json['checkmated'],
                 castling=json['castlingAllowed'])


eng = Engine()
maxim = Maximizer(eng, input())

while 1:
  print('enter to move')
  nex = input()
  print('thinking...')
  t = time()
  v = maxim.move()
  print(f'took me {time()-t:.2f}s for v={v}')

