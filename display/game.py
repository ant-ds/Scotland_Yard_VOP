import numpy as np
import threading

from PyQt5 import QtCore


class GameInteraction(QtCore.QObject):
    game_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.timer = QtCore.QBasicTimer()
        self.game = game
        game.guiInteraction = self
        self.game_running = False

    def start_timer(self, ms):
        self.timer.start(ms, self)  # Update every x ms

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        self.update()
    
    def update(self):
        data = self.game.getDrawData()
        self.game_data.emit(data)
    
    def start_game_thread(self):
        if not self.game_running:
            t = threading.Thread(target=self.game.loop)
            t.start()
            self.game_running = True
