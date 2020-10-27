from abc import ABCMeta, abstractmethod
from random import randint


class Player(object, metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self, board, name):
        self._board = board
        self._name = name
        
    @abstractmethod
    def play(self):
        return
        
    def won(self):
        return self._board.won(self)

    def __str__(self):
        return self._name

    def toJSON(self):
        return str(self)

class User(Player):
    def __init__(self, board):
        super().__init__(board, 'U')
        
    def play(self):
        while True:
            try:
                square = int(input('Please choose the square you are going to play on by entering a number between 0 and 8: '))
                self._board.play(square, self)
                break
            except ValueError as e:
                print(f'Invalid square!')
            except Exception as e:
                print(str(e),'\n')
        
class Computer(Player):
    def __init__(self, board, user):
        super().__init__(board, 'C')
        self._user = user

    def play(self):
        winning_square = self._board.get_winning_square(self)
        if winning_square != self._board.SQUARE_NOT_FOUND:
            self._board.play(winning_square, self)
        else:
            winning_square = self._board.get_winning_square(self._user)
            if winning_square != self._board.SQUARE_NOT_FOUND:
                self._board.play(winning_square, self)
            else:
                empty_squares = self._board.empty_squares()
                index = randint(0, len(empty_squares) - 1)
                self._board.play(empty_squares[index], self)
        print()

class NoBody(Player):
    def __init__(self, board):
        super().__init__(board, ' ')
        
    def play(self):
        pass
