from PyQt5 import QtWidgets
from PyQt5 import QtCore

from display.board import BoardWidget
from display.game import GameInteraction


class MainWidget(QtWidgets.QWidget):
    def __init__(self, game, refreshSpeed, **kwargs):
        super().__init__(**kwargs)
        self.board_widget = BoardWidget()

        # Set window background color
        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(p)

        self.game_interaction = GameInteraction(game)

        image_data_slot = self.board_widget.image_data_slot
        self.game_interaction.game_data.connect(image_data_slot)
        self.game_interaction.start_timer(refreshSpeed)

        self.run_button = QtWidgets.QPushButton('Start')
        self.run_button.clicked.connect(self.game_interaction.start_game_thread)

        self.game_interaction.game_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.board_widget)
        layout.addWidget(self.run_button)

        self.setLayout(layout)
    
    def getGameInteraction(self):
        return self.game_interaction
