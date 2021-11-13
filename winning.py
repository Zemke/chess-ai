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
    pieces_v = { 'q': 3, 'r': 2, 'b': 2, 'k': 2, 'p': 1, 'x': 0 }
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
      for t, s in self.__spinoff_boards(state):
        mx = self.minimax(la-1, s, False, a, b, False)
        # our goal is to maximize
        if mx > v:
          v = mx
          v_t = t
        if v >= b:
          break
        a = max(a, v)
    else:
      v = +inf
      for t, s in self.__spinoff_boards(state):
        v = min(v, self.minimax(la-1, s, True, a, b, False))
        if v <= a:
          break
        b = min(b, v)
    return (v, v_t) if rett else v

  def __spinoff_boards(self, state):
    for side in state.castling:
      b = self.eng.castle(state.board_id, side, True)
      yield (Move.castling(side), State.from_engine(b))
    for turn in self.eng.turns(state.board_id):
      for target in turn['targets']:
        b = self.eng.turn(state.board_id, turn['piece']['id'], target, True)
        yield (Move.turn(turn['piece']['id'], target), State.from_engine(b))


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
    r = [[None for i in range(9)] for i in range(9)]
    for row in g:
      for p in row:
        if p is None:
          n = None
        else:
          n = 'x' if p['name'] == 'King' else p['name'][0]
          n = n.lower() if p['color'] == Maximizer.C else n.upper()
        if p is not None:
          r[p['position']['rank']][p['position']['file']] = n
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

