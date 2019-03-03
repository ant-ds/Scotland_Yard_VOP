import sys
from game.game import ScotlandYard

import game.constants as const

from PyQt5 import QtWidgets
from display.window import MainWidget


def main():
    game = ScotlandYard(visualize=True, verbose=True)

    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget(game)

    game.addGui(main_widget.getGameInteraction())

    main_window.setCentralWidget(main_widget)
    main_window.show()

    stop = False
    while not stop:
        stop, status = game.update()
        pass  # Visualization function calls could be added here
    
    print(f"Game ended with status {status}::  {const.GAME_END_MESSAGES[status]}")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
