from board.exceptions import BoardSquareError
from constants import Options
from game import TicTacToe

game = TicTacToe()
game.help()

while True:
    try:
        choice = game.user_choice()
        if choice == Options.NEWGAME:
            game.begin()
        elif choice == Options.PASTGAMES:
            game.history()
        elif choice == Options.EXIT:
            break
        else:
            continue      
    except ValueError:
        continue
    except BoardSquareError as e:
        print(str(e))
