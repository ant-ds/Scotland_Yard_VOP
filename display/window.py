import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


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


class BoardWidget(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = QtGui.QImage()

    def image_data_slot(self, image_data):
        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()


class MainWidget(QtWidgets.QWidget):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.board_widget = BoardWidget()

        # TODO: set video port
        self.game_interaction = GameInteraction(game)

        image_data_slot = self.board_widget.image_data_slot
        self.game_interaction.game_data.connect(image_data_slot)
        self.game_interaction.start_timer(500)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.board_widget)
        """self.update_button = QtWidgets.QPushButton('Refresh')
        layout.addWidget(self.update_button)
        self.update_button.clicked.connect(self.game_interaction.update)"""

        self.setLayout(layout)
    
    def getGameInteraction(self):
        return self.game_interaction
