from engine import Engine
from math import inf
from time import time


class Maximizer:
  C = 'BLACK'
  __DP = {}

  def __init__(self, eng, board_id):
    self.eng = eng
    self.board_id = board_id

  def move(self):
    board = State.from_engine(eng.board(self.board_id))
    tt = self.minimax(3, board, True, -inf, +inf)
    tt.sort(key=lambda x: x[0], reverse=True)
    v, m = tt[0]
    if m.castling:
      self.eng.castle(self.board_id, m.castling)
    else:
      self.eng.turn(self.board_id, m.piece, m.target)
    return v

  def heuristic(self, state):
    pieces_v = { 'q': 4, 'r': 2, 'b': 2, 'k': 2, 'p': 1, 'x': 0 }
    maxim = state.pieces(True)
    minim = state.pieces(False)
    v = 0
    for p in maxim:
      v += pieces_v[p]
    for p in minim:
      v -= pieces_v[p.lower()]
    return v

  def minimax(self, la, state, maxim, a, b, rett=True):
    if rett:
      tt = []
    if state.checkmated:
      return -inf if maxim else +inf
    elif la == 0:
      # TODO a heuristic may also be a neural network
      return self.heuristic(state)
    spb = self.__spinoff_boards(state, maxim)
    if la <= 1:
      spb = spb[:10]
    v = -inf if maxim else +inf
    for t, s in spb:
      if s in self.__DP:
        mx = self.__DP[s]
      else:
        mx = self.minimax(la-1, s, not maxim, a, b, False)
        self.__DP[s] = mx
      if rett:
        tt.append((mx, t))
      if maxim:
        v = max(v, mx)
        a = max(a, v)
      else:
        v = min(v, mx)
        b = min(b, v)
      if b <= a:
        break
    return tt if rett else v

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
    return [[r[1], r[2]] for r in res]


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

  def __repr__(self):
    if self.castling:
      return str(self.castling)
    return str((self.piece, self.target))


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

  def __repr__(self):
    s = ''
    for row in self.grid:
      s += ' '.join([i if i is not None else ' ' for i in row])
      s += '\n'
    return s

  def __eq__(self, o):
    if not isinstance(o, State):
      return False
    return (self.grid == o.grid
        and self.next_turn == o.next_turn
        and self.checkmated == o.checkmated
        and self.castling == o.castling)

  def __hash__(self):
    return hash(
      (tuple([tuple(i) for i in self.grid]),
      self.next_turn,
      self.checkmated,
      tuple(self.castling)))


eng = Engine()
maxim = Maximizer(eng, input())

while 1:
  print('enter to move')
  nex = input()
  print('thinking...')
  t = time()
  v = maxim.move()
  print(f'took me {time()-t:.2f}s for v={v}')

