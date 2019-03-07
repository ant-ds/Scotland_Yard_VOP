from PyQt5 import QtWidgets
import display.main as main

import display.constants as const


def createApp(*args, **kwargs):
    return QtWidgets.QApplication(*args, **kwargs)


def createGui(game):
    main_window = QtWidgets.QMainWindow()
    main_widget = main.MainWidget(game, speed=const.REFRESH_RATE)

    game.addGui(main_widget.getGameInteraction())

    main_window.setCentralWidget(main_widget)

    displayMode = int(game.config['DISPLAY']['display_mode'])
    displayMode = const.DISPLAY_MODE_OPTIONS[displayMode]
    if displayMode == "Fullscreen":
        main_window.showFullScreen()
    elif displayMode == "Maximized":
        main_window.showMaximized()
    else:
        main_window.show()

    return main_window


def createReplayGui(config):
    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("Scotland Yard Replays")
    main_widget = main.MainReplayWidget()
    main_window.setCentralWidget(main_widget)

    displayMode = int(config['DISPLAY']['display_mode'])
    displayMode = const.DISPLAY_MODE_OPTIONS[displayMode]
    if displayMode == "Fullscreen":
        main_window.showFullScreen()
    elif displayMode == "Maximized":
        main_window.showMaximized()
    else:
        main_window.show()

    return main_window
