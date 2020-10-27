from abc import ABCMeta, abstractmethod


class BoardSquareError(Exception, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, square):
        self._square = square

    @abstractmethod
    def __str__(self):
        return

class BoardInvalidSquareError(BoardSquareError):
    def __init__(self, this, square):
        super().__init__(square)
        self._max = this.MAX - 1

    def __str__(self):
        return 	f'The square {self._square} does not exist. Squares range from 0 to {self._max}.'

class BoardAlreadyInUseSquareError(BoardSquareError):
    def __init__(self, this, square, player):
        super().__init__(square)
        self._player = player
        self._availables = this.empty_squares()

    def __str__(self):
        return f'\n"{str(self._player)}", the square {self._square} is already in use. The squares available to play on are : {self._availables}\n'
