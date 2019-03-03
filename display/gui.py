from PyQt5 import QtWidgets
from display.main import MainWidget

import display.constants as const


def createApp(*args, **kwargs):
    return QtWidgets.QApplication(*args, **kwargs)


def createGui(game):
    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget(game, const.REFRESH_RATE)

    game.addGui(main_widget.getGameInteraction())

    main_window.setCentralWidget(main_widget)
    main_window.show()

    return main_window
