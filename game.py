import json

from board.board import Board
from constants import Options
from logger.logger import Console
from players import Computer, User


class TicTacToe:
    WON = 'You have won the game!'
    LOST = 'The computer has won the game!'
    TIE = 'The game is a tie!'
    
    def __init__(self, fn = 'games.json'):
        try:
            with open(fn) as fh:
                self._games = json.load(fh)
        except FileNotFoundError:
            self._games = []
        self._logger = Console()         
        self._board = Board()
        self._user = User(self._board)
        self._computer = Computer(self._board, self._user )
        self._first = None
        self._game_over = False
        self._games_file = fn

    def help(self):
        msg = '\nWelcome to the Tic Tac Toe game!\n'
        msg = msg + 'The computer will play with the letter C and you will play with the letter U. At the end of every game the winner and the state of the grid will be saved to the disk. When ask you to play enter a number between 0 and 8 representing the square on which you want to play as indicated by the following diagram:\n'
        self._logger.log(msg)
        self.diagram()
        
    def diagram(self):
        msg = ''
        msg = msg + '   |   |   ' + '\n'
        msg = msg + ' 0 | 1 | 2 ' + '\n'
        msg = msg + '   |   |   ' + '\n'
        msg = msg + '-----------' + '\n'
        msg = msg + '   |   |   ' + '\n'
        msg = msg + ' 3 | 4 | 5 ' + '\n'
        msg = msg + '   |   |   ' + '\n'
        msg = msg + '-----------' + '\n'
        msg = msg + '   |   |   ' + '\n'
        msg = msg + ' 6 | 7 | 8 ' + '\n'
        msg = msg + '   |   |   ' + '\n\n'
        self._logger.log(msg)

    def menu(self):
        msg = 'Menu:\n'
        msg = msg + '  Press 1 to start a new game.' + '\n'
        msg = msg + '  Press 2 to see a list of past games and their results.' + '\n'
        msg = msg + '  Press 3 to exit.' + '\n\n'
        self._logger.log(msg)

    def user_choice(self):
        self.menu()
        try:
            choice = int(input('Enter your choice: ').lower())
            if choice not in list(map(int, Options)):
                self._logger.log(f'\nInvalid number {choice}\n')
            return choice
        except ValueError:
            self._logger.log('\nInvalid number.\n')
            raise ValueError

    def begin(self):
        self.reset()
        self.first()
        self.play()
        self.results()
        self.append()
        self.save()
        
    def reset(self):
        self._board.reset()
        self._game_over = False
        self._first = None
        
    def first(self):
        user_answer = input('\nWould you like to go first?(y/n): ').lower()
        while user_answer != 'y' and user_answer != 'n':
            self._logger.log('Please enter y or n.')
            user_answer = input('\nWould you like to go first?(y/n): ').lower()
        self._logger.log('\n')
        self._first = self._user if user_answer == 'y' else self._computer

    def play(self):
        player = self._user if self._first == None else self._first
        while not self._board.is_full() and not self._user.won() and not self._computer.won():
            player.play()
            if player == self._computer:
                self._logger.log(str(self._board))
            player = self._computer if player == self._user else self._user
        if self._user.won() or (not self._computer.won() and self._first == self._user):
            self._logger.log(str(self._board))
        self._game_over = True
            
    def results(self):
        if self._game_over:
            if self._user.won():
                message = TicTacToe.WON
            elif self._computer.won():
                message = TicTacToe.LOST
            else:
                message = TicTacToe.TIE
            self._logger.log(message)
        else:
            self._logger.log("In order to see the results of a game you have to play it until the very end.")
        self._logger.log('\n')

    def append(self):
        if self._game_over:
            if self._user.won():
                result = str(self._user)
            elif self._computer.won():
                result = str(self._computer)
            else:
                result = "T"
            self._games.append({"result": result, "board": self._board.to_json()})
        else:
            self._logger.log("In order to append a game you have to play it until the very end.")

    def save(self):
        if self._game_over:
            try:
                with open(self._games_file, 'w') as fh:
                    json.dump(self._games, fh)
            except Exception as e:
                self._logger.log('\n')
                self._logger.log(str(e) + '\n')	
        else:
            self._logger.log("In order to save a game you have to play it until the very end.")

    def history(self):
        if len(self._games) > 0:
            self._logger.log('\n******** List of past games: ********\n')
            i = 1
            for game in self._games:
                if game['result'] == 'U':
                    result = TicTacToe.WON
                elif game['result'] == 'C':
                    result = TicTacToe.LOST
                else:
                    result = TicTacToe.TIE
                self._logger.log(f'Game #{i}: {result}')
                board = self._board.from_json(game['board'])
                self._logger.log(str(board))
                del(board)
                i += 1
        else:
            self._logger.log('There is no record of past games yet. Play some games and comeback later.\n')
