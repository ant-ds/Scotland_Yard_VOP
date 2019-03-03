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

    displayMode = const.DISPLAY_MODE
    displayMode = const.DISPLAY_MODE_OPTIONS[displayMode]
    if displayMode == "Fullscreen":
        main_window.showFullScreen()
    elif displayMode == "Maximized":
        main_window.showMaximized()
    else:
        main_window.show()

    return main_window
