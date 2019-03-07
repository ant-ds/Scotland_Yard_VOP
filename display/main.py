import numpy as np

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from display.board import BoardWidget
from display.game import GameInteraction

import display.util as util


class MainWidget(QtWidgets.QWidget):
    def __init__(self, game, speed=500):
        super().__init__()
        self.board_widget = BoardWidget()

        # Set window background color
        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(p)

        self.game_interaction = GameInteraction(game)

        image_data_slot = self.board_widget.image_data_slot
        self.game_interaction.game_data.connect(image_data_slot)
        self.game_interaction.start_timer(speed)

        self.game_interaction.game_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.board_widget)

        if game.config['DISPLAY'].getboolean('multithreaded_drawing'):
            self.run_button = QtWidgets.QPushButton('Start')
            self.run_button.clicked.connect(self.game_interaction.start_game_thread)
            layout.addWidget(self.run_button)

        self.setLayout(layout)
    
    def getGameInteraction(self):
        return self.game_interaction


class MainReplayWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set window background color
        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.gray)
        self.setPalette(p)

        layout = QtWidgets.QVBoxLayout()

        self.openfile_button = QtWidgets.QPushButton('Open Replay File')
        self.openfile_button.clicked.connect(self.openFile)
        layout.addWidget(self.openfile_button)

        self.setLayout(layout)

    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Scotland Yard File Selector",
            "",
            "Numpy Files (*.npy);;All Files (*)",
            options=options
        )
        if filepath:
            self.data = np.load(filepath)

            self.openfile_button.deleteLater()

            self.onFileSuccess = QtWidgets.QLabel(f"Successfully loaded {filepath}")
            self.layout().addWidget(self.onFileSuccess)

            self.start_replay_button = QtWidgets.QPushButton('Start replay')
            self.start_replay_button.clicked.connect(self.showBoard)
            self.layout().addWidget(self.start_replay_button)

            self.board_widget = BoardWidget()
            self.layout().addWidget(self.board_widget)

            self.back_button = QtWidgets.QPushButton('<- go back')
            self.next_button = QtWidgets.QPushButton('next ->')

            self.back_button.clicked.connect(self.back)
            self.next_button.clicked.connect(self.next)

            self.layout().addWidget(self.back_button)
            self.layout().addWidget(self.next_button)
            
            self.board_widget.hide()
            self.back_button.hide()
            self.next_button.hide()

        self.parseData()  
            
    def showBoard(self):
        # Remove old widgets
        self.onFileSuccess.deleteLater()
        self.start_replay_button.deleteLater()

        # Show new widgets
        self.board_widget.show()
        self.back_button.show()
        self.next_button.show()

        self.parseData()            
        self.update()
    
    def parseData(self):
        data = self.data

        self.numDetectives = len(data[2])
        self.startPositions = {
            'detectives': [det[0][0] for det in data[2]],
            'mrx': data[1][0][0][0],
        }
        self.turns = self.createTurns(data)
        self.positions = {
            'detectives': self.startPositions['detectives'],
            'mrx': self.startPositions['mrx'],
        }
        self.idx = -1  # Index of turn currently showing, -1 for startpositions
    
    def swapStartDest(self, start, dest):
        if self.positions['mrx'] == start:
            self.positions['mrx'] = dest
        else:
            for i in range(self.numDetectives):
                if self.positions['detectives'][i] == start:
                    self.positions['detectives'][i] = dest
        
    def back(self):
        if self.idx is None:
            return self.update()
        if self.idx == 0:
            self.positions = {
                'detectives': self.startPositions['detectives'],
                'mrx': self.startPositions['mrx'],
            }
            self.idx = -1
            return self.update()
        # default scenario
        self.idx -= 1
        move = self.turns[self.idx]
        if len(move) == 2:
            # double move
            for i in range(2):
                dest, _, start = move[i]
                self.swapStartDest(start, dest)
        else:
            dest, _, start = move
            self.swapStartDest(start, dest)
        return self.update()    

    def next(self):
        if self.idx == len(self.turns) - 1:
            return self.update()
        self.idx += 1
        move = self.turns[self.idx]
        if len(move) == 2:
            # double move
            for i in range(2):
                start, _, dest = move[i]
                self.swapStartDest(start, dest)
        else:
            start, _, dest = move
            self.swapStartDest(start, dest)
        return self.update()        

    def createTurns(self, data):
        turns = []
        xindex = 0
        dindices = [0] * len(data[2])
        allDone = False
        while not allDone:
            allDone = True
            if xindex < len(data[1][0]):
                allDone = False
                turns.append(data[1][0][xindex])
                if xindex in data[1][1]:
                    # overwrite because double so put together
                    turns[-1] = [data[1][0][xindex], data[1][0][xindex + 1]]
                    xindex += 1
                xindex += 1
            for i, idx in enumerate(dindices):
                if idx < len(data[2][i]):
                    allDone = False
                    turns.append(data[2][i][idx])
                    dindices[i] += 1
        return turns

    def update(self):
        dpos = self.positions['detectives']
        mrx = self.positions['mrx']
        img = util.drawReplay(dpos, mrx)
        self.board_widget.image_data_slot(img)
