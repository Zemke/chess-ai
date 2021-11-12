from engine import Engine
from math import inf

# TODO En passant and castle


class Maximizer:
  C = 'BLACK'

  def __init__(self, eng, board_id):
    self.eng = eng
    self.board_id = board_id

  def move(self):
    board = eng.board(self.board_id)

    # TODO for now just taking the first turn, but be clever
    #piece = None
    #for d1 in board["grid"]:
    #  for p in d1:
    #    if p is None:
    #      continue
    #    if p['color'] == self.C and p['name'] == 'Pawn':
    #      piece = p
    #print('piece', piece)
    #nxx = eng.next_turns(piece['id'])
    #print(nxx)  #[{'file': 7, 'rank': 2}, {'file': 7, 'rank': 3}]
    #eng.turn(piece['id'], nxx[0])

    # here's smartness
    look_ahead = 2
    acc = [[] for i in range(look_ahead+1)]
    mx = self.minimax(look_ahead, State.from_engine(board), None, True, acc)
    print(acc)
    v, b, [piece, target] = sorted(acc[look_ahead-1], key=lambda x: x[0])[-1]
    self.eng.turn(self.board_id, piece, target)

  def heuristic(self, state):
    pieces_v = { 'q': 5, 'r': 4, 'b': 3, 'k': 2, 'p': 1, 'x': 0 }
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
      for turn, b in self.__spinoff_boards(state.board_id):
        v = max(v, self.minimax(look_ahead-1, b, turn, False, acc))
    else:
      v = +inf
      for turn, b in self.__spinoff_boards(state.board_id):
        v = min(v, self.minimax(look_ahead-1, b, turn, True, acc))
    acc[look_ahead].append([v, state, by_turn])
    return v

  def __spinoff_boards(self, board_id):
    for turn in self.eng.turns(board_id):
      for target in turn['targets']:
        yield ((turn['piece']['id'], target),
                State.from_engine(
                  self.eng.turn(board_id, turn['piece']['id'], target, True)))

class State:
  def __init__(self, board_id, grid, next_turn, checkmated):
    self.board_id = board_id
    self.grid = grid
    self.next_turn = next_turn
    self.checkmated = checkmated

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
                 checkmated=json['checkmated'])


eng = Engine()
maxim = Maximizer(eng, input())

while 1:
  print('enter to move')
  nex = input()
  maxim.move()

