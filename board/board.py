import json

from board.exceptions import (BoardAlreadyInUseSquareError,
                              BoardInvalidSquareError)
from players import Computer, NoBody, User


class Board:
    MAX = 9
    SQUARE_NOT_FOUND = -1

    def __init__(self):
        self._nobody = NoBody(self)
        self.reset()

    def reset(self):
        self._board = [self._nobody] * Board.MAX
        
    def is_full(self):
        return not any((player == self._nobody) for player in self._board)		
        
    def is_empty(self):
        return not any((player != self._nobody) for player in self._board)		
        
    def is_square_empty(self, square):
        try:
            return self[square] == self._nobody
        except IndexError:
            raise BoardInvalidSquareError(self, square)	

    def empty_squares(self):
        return [square for square in range(Board.MAX) if self.is_square_empty(square)]
    
    def used_squares(self):
        return [square for square in range(Board.MAX) if not self.is_square_empty(square)]

    def get_winning_square(self, player):
        squares = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

        for square0, square1, square2 in squares:
            if self[square0] == player and self[square1] == player and self[square2] == self._nobody:
              return square2
            if self[square0] == player and self[square1] == self._nobody and self[square2] == player:
              return square1
            if self[square0] == self._nobody and self[square1] == player and self[square2] == player:
              return square0
              
        return Board.SQUARE_NOT_FOUND

    def won(self, player):
        return (
           (self[0] == player and self[1] == player and self[2] == player) or 
           (self[3] == player and self[4] == player and self[5] == player) or 
           (self[6] == player and self[7] == player and self[8] == player) or
           (self[0] == player and self[3] == player and self[6] == player) or 
           (self[1] == player and self[4] == player and self[7] == player) or 
           (self[2] == player and self[5] == player and self[8] == player) or
           (self[2] == player and self[4] == player and self[6] == player) or 
           (self[0] == player and self[4] == player and self[8] == player)
        )

    def __str__(self):
        msg = ''
        msg = msg + '   |   |   ' + '\n'
        msg = msg + f' {self[0]} | {self[1]} | {self[2]} ' + '\n'
        msg = msg + '   |   |   ' + '\n'
        msg = msg + '-----------' + '\n'
        msg = msg + '   |   |   ' + '\n'
        msg = msg + f' {self[3]} | {self[4]} | {self[5]} ' + '\n'
        msg = msg + '   |   |   ' + '\n'
        msg = msg + '-----------' + '\n'
        msg = msg + '   |   |   ' + '\n'
        msg = msg + f' {self[6]} | {self[7]} | {self[8]} ' + '\n'
        msg = msg + '   |   |   ' + '\n'
        msg = msg + 'C : Computer' + '\n'
        msg = msg + 'U : User' + '\n'
        msg = msg + '\n'
        return msg

    def to_json(self):
        json = ''
        for square in range(Board.MAX):
            player_code = str(self[square])
            json = '"' + player_code + '"' if json == '' else json + ',"' + player_code + '"'
        return "[" + json + "]"

    @classmethod
    def from_json(cls, json_board):
        board = cls()
        board._board = json.loads(json_board)
        return board

    def play(self, square, player):
        self[square] = player

    def __getitem__(self, square):
        try:
            return self._board[square]
        except IndexError:
            raise BoardInvalidSquareError(self, square)
        
    def __setitem__(self, square, player):
        if not self.is_square_empty(square):
            raise BoardAlreadyInUseSquareError(self, square, player)

        self._board[square] = player
