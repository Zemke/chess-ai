from engine import Engine

board_id = input()

eng = Engine(board_id)

print("Board ID", eng.board_id)


class Maximizer:
  def __init__(self, eng):
    self.eng = eng

  def move(self):
    board = eng.board()
    print(board)
    piece = None
    for d1 in board["grid"]:
      for p in d1:
        if p is None:
          continue
        if p['color'] == Engine.COLOR and p['name'] == 'Pawn':
          piece = p
    print('piece', piece)
    nxx = eng.next_turns(piece['id'])
    print(nxx)  #[{'file': 7, 'rank': 2}, {'file': 7, 'rank': 3}]
    eng.turn(piece['id'], nxx[0])
    #eng.turn(nxx[0])
    #self.minimax()
    pass

  def minimax(self):
    pass

maxim = Maximizer(eng)


while 1:
  print('enter to move')
  nex = input()
  maxim.move()

