import builtins

import mock
import pytest

from board.board import Board
from board.exceptions import (BoardAlreadyInUseSquareError,
                              BoardInvalidSquareError)
from constants import Options
from game import TicTacToe
from players import Computer, Player, User
from tests.fake_players import (FakeComputerInvalidSquare,
                                FakeComputerSquareAlreadyInUse, FakeUser,
                                FakeUserInvalidSquare,
                                FakeUserSquareAlreadyInUse)


class TestTicTacToe:
    new_json_file = './tests/test_new_games.json'
    old_json_file = './tests/test_old_games.json'

    def setup_method(self):
        self._game = TicTacToe(TestTicTacToe.old_json_file)

    def test_init_new_json(self):
        self._game = TicTacToe(TestTicTacToe.new_json_file)
        assert self._game._games == []

    def test_init_old_json(self):
        assert len(self._game._games) == 1
   
    def test_init_instance(self):
        assert isinstance(self._game, TicTacToe)

    def test_init_instance_attributes(self):
        assert isinstance(self._game._board, Board)
        assert isinstance(self._game._user, User)
        assert isinstance(self._game._computer, Computer)
        assert self._game._first == None
        assert self._game._game_over == False

    def test_user_choice_is_valid(self):
        with mock.patch.object(builtins, 'input', lambda _: '3'):
            assert self._game.user_choice() == Options.EXIT

    def test_user_choice_is_invalid(self):
        with mock.patch.object(builtins, 'input', lambda _: '4'):
            choice = self._game.user_choice()
            assert choice not in list(map(int, Options))

    def test_user_choice_error(self):
        with mock.patch.object(builtins, 'input', lambda _: 'Livan'):
            with pytest.raises(ValueError):
                self._game.user_choice()

    def test_reset(self):
        self._game.reset()
        assert self._game._game_over == False
        assert self._game._first == None

    def test_user_goes_first(self):
        with mock.patch.object(builtins, 'input', lambda _: 'y'):
            self._game.first()
            assert self._game._first == self._game._user

    def test_user_does_not_go_first(self):
        with mock.patch.object(builtins, 'input', lambda _: 'n'):
            self._game.first()
            assert self._game._first != self._game._user
            assert self._game._first == self._game._computer

    def test_user_played_square_already_in_use(self):
        self._game._user = FakeUserSquareAlreadyInUse(self._game._board)
        with pytest.raises(BoardAlreadyInUseSquareError):
          self._game.play()

    def test_user_played_invalid_square(self):
        self._game._user = FakeUserInvalidSquare(self._game._board)
        with pytest.raises(BoardInvalidSquareError):
          self._game.play()

    def test_computer_played_square_already_in_use(self):
        self._game._user = FakeUser(self._game._board)
        self._game._computer = FakeComputerSquareAlreadyInUse(self._game._board)
        with pytest.raises(BoardAlreadyInUseSquareError):
          self._game.play()

    def test_computer_played_invalid_square(self):
        self._game._user = FakeUser(self._game._board)
        self._game._computer = FakeComputerInvalidSquare(self._game._board)
        with pytest.raises(BoardInvalidSquareError):
          self._game.play()

    def test_game_play(self):
        self._game._user = FakeUser(self._game._board)
        self._game.play()
        assert(self._game._game_over == True)
