from random import randint

from players import Player


class FakeUser(Player):
    def __init__(self, board):
        super().__init__(board, 'U')
        
    def play(self):
        empty_squares = self._board.empty_squares()
        index = randint(0, len(empty_squares) - 1)
        self._board.play(empty_squares[index], self)
        print()

class FakePlayerSquareAlreadyInUse(Player):
    def __init__(self, board, name):
        super().__init__(board, name)

    def play(self):
        used_squares = self._board.used_squares()
        if len(used_squares) == 0:
            self._board.play(0, self)
        else:
            index = randint(0, len(used_squares) - 1)
            self._board.play(used_squares[index], self)
        print()

class FakeUserSquareAlreadyInUse(FakePlayerSquareAlreadyInUse):
    def __init__(self, board):
        super().__init__(board, 'U')

class FakeComputerSquareAlreadyInUse(FakePlayerSquareAlreadyInUse):
    def __init__(self, board):
        super().__init__(board, 'C')

class FakePlayerInvalidSquare(Player):
    def __init__(self, board, name):
        super().__init__(board, name)

    def play(self):
        self._board.play(10000, self)
        print()

class FakeUserInvalidSquare(FakePlayerInvalidSquare):
    def __init__(self, board):
        super().__init__(board, 'U')

class FakeComputerInvalidSquare(FakePlayerInvalidSquare):
    def __init__(self, board):
        super().__init__(board, 'C')
