from engine import Engine
from math import inf


class Maximizer:
  C = 'BLACK'

  def __init__(self, eng, board_id):
    self.eng = eng
    self.board_id = board_id

  def move(self):
    board = eng.board(self.board_id)
    look_ahead = 2
    acc = [[] for i in range(look_ahead+1)]
    mx = self.minimax(look_ahead, State.from_engine(board), None, True, acc)
    print(acc)
    move = sorted(acc[look_ahead-1], key=lambda x: x[0])[-1][2]
    if move.castling:
      self.eng.castle(self.board_id, move.castling)
    else:
      self.eng.turn(self.board_id, move.piece, move.target)

  def heuristic(self, state):
    pieces_v = { 'q': 3, 'r': 2, 'b': 2, 'k': 2, 'p': 1, 'x': 0 }
    maxim = state.pieces(True)
    minim = state.pieces(False)
    v_maxim = 0
    for p in maxim:
      v_maxim += pieces_v[p]
    v_minim = 0
    for p in minim:
      v_maxim -= pieces_v[p.lower()]
    return v_maxim

  def minimax(self, look_ahead, state, by_turn, maxim, acc):
    if state.checkmated:
      v = -inf if maxim else +inf
      acc[look_ahead].append([v, state, by_turn])
      return v
    elif look_ahead == 0:
      # TODO a heuristic may also be a neural network
      v = self.heuristic(state)
      acc[look_ahead].append([v, state, by_turn])
      return v
    # TODO prune node if a max/min has been reached for a node
    #  that exceeds what cannot be rehabilitated from
    if maxim:
      v = -inf
      for turn, b in self.__spinoff_boards(state):
        v = max(v, self.minimax(look_ahead-1, b, turn, False, acc))
    else:
      v = +inf
      for turn, b in self.__spinoff_boards(state):
        v = min(v, self.minimax(look_ahead-1, b, turn, True, acc))
    acc[look_ahead].append([v, state, by_turn])
    return v

  def __spinoff_boards(self, state):
    for side in state.castling:
      b = self.eng.castle(Move.castling(side), True)
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
  maxim.move()

