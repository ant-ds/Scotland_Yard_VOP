import numpy as np

from PyQt5 import QtCore


class GameInteraction(QtCore.QObject):
    game_data = QtCore.pyqtSignal(np.ndarray)

    lastDrawn = None  # Last drawn image of the game

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.timer = QtCore.QBasicTimer()
        self.game = game
        game.guiInteraction = self

    def start_timer(self, ms):
        self.timer.start(ms, self)  # Update every x ms

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        self.update()
    
    def update(self):
        data = self.game.getDrawData()
        
        self.lastDrawn = data
        self.game_data.emit(data)
