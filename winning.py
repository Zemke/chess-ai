from engine import Engine
from math import inf

# TODO En passant and castle

board_id = input()
print("Board ID:", eng.board_id)
eng = Engine(board_id)

class Maximizer:
  C = 'BLACK'

  def __init__(self, eng):
    self.eng = eng

  def move(self):
    board = eng.board()
    print(board)

    # TODO for now just taking the first turn, but be clever
    piece = None
    for d1 in board["grid"]:
      for p in d1:
        if p is None:
          continue
        if p['color'] == self.C and p['name'] == 'Pawn':
          piece = p
    print('piece', piece)
    nxx = eng.next_turns(piece['id'])
    print(nxx)  #[{'file': 7, 'rank': 2}, {'file': 7, 'rank': 3}]
    eng.turn(piece['id'], nxx[0])

    # here's smartness
    minimax(1, State.from_engine(board), True)

  def heuristic(self, state):
    pieces_v = { 'q': 5, 'r': 4, 'b': 3, 'k': 2, 'p': 1 }
    maxim = state.pieces(True)
    minim = state.pieces(False)
    v_maxim = 0
    for p in maxim:
      v_maxim += self.pieces_v[p]
    v_minim = 0
    for p in minim:
      v_maxim -= self.pieces_v[p.lower()]
    return v_maxim

  def minimax(self, look_ahead, state, maxim):
    terminal = eng.terminal(state)
    if terminal:
      return -inf if maxim else +inf
    elif look_ahead == 0:
      # TODO a heuristic may also be a neural network
      return self.heuristic(state)
    # TODO prune node if a max/min has been reached for a node
    #  that exceeds what cannot be rehabilitated from
    # TODO for testing moves engine requires state changes
    #  without mutating the original board
    if maxim:
      v = -inf
      for t in self.eng.next_turns():
        turn = t  # TODO move after turn
        v = max(v, minimax(t, look_ahead-1, False))
    else:
      v = +inf
      for t in self.eng.next_turns():
        turn = t  # TODO move after turn
        v = max(v, minimax(t, look_ahead-1, True))
    return v

class State:
  def __init__(self, grid, next_turn):
    self.grid = grid
    self.next_turn = next_turn

  def pieces(self, black):
    pp = []
    for rank in self.grid:
      for p in rank:
        if p is None:
          continue
        elif black and p.islower()
          pp.append(p)
        elif not black and p.isupper():
          pp.append(p)
    return pp

  @staticmethod
  def from_engine(self, json):
    g = json['grid']
    r = [[[] for i in range(9)]]
    for row in g:
      for p in g:
        if p is None:
          n = None
        else:
          n = 'x' if p['name'] == 'King' else p['name'][0]
          n = n.lower() if p['color'] == Maxmimizer.C else n.upper()
        r[p['position']['rank']][p['position']['file']] = n
    return State(grid=r, next_turn=json['nextTurn'])


maxim = Maximizer(eng)

while 1:
  print('enter to move')
  nex = input()
  maxim.move()

