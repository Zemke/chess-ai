from engine import Engine, State
from math import inf
from time import time


class Maximizer:
  C = 'BLACK'
  S = {}

  def __init__(self, engine):
    self.engine = engine

  def move(self):
    self.engine.refresh()
    s = State.from_engine(self.engine.board)
    S_before = len(self.S)
    mm = self.minimax(5, s, True, -inf, +inf)
    mm.sort(key=lambda x: x[0], reverse=True)
    v, m = mm[0]
    self.engine.turn(m)
    return v, len(self.S)-S_before

  def minimax(self, la, s, maxim, a, b, ret=True):
    if ret:
      vm = []
    if s.board.is_checkmate():
      return -inf if maxim else +inf
    elif s.board.is_stalemate():
      return 0
    elif la == 0:
      # a heuristic may also be a neural network
      return s.v

    opts = []
    for m in s.board.legal_moves:
      cp = s.board.copy(stack=False)
      cp.push(m)
      ns = State(cp)
      opts.append((m, ns))
    opts.sort(key=lambda o: o[1].v, reverse=maxim)

    # beam
    if la <= 2:
      opts = opts[:10]

    v = -inf if maxim else +inf
    for m, s in opts:
      if s.key not in self.S:
        # TODO prune S
        self.S[s.key] = self.minimax(la-1, s, not maxim, a, b, False)
      if ret:
        vm.append((self.S[s.key], m))
      if maxim:
        v = max(v, self.S[s.key])
        a = max(a, v)
      else:
        v = min(v, self.S[s.key])
        b = min(b, v)
      if b <= a:
        break # alpha-beta cutoff

    return vm if ret else v


# TODO castling

print("paste game uuid")
maxim = Maximizer(Engine(input()))

while 1:
  print('enter to move')
  tw = time()
  nex = input()
  print(f'waited for {time()-tw:.2f}s')
  print('thinking...')
  t = time()
  v, vis = maxim.move()
  print(f'took me {time()-t:.2f}s v{v} {vis} new opts')

