import numpy as np

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from display.board import BoardWidget
from display.game import GameInteraction

import display.util as util

from game.game import ScotlandYard


class MainWidget(QtWidgets.QWidget):
    def __init__(self, game, speed=500):
        super().__init__()
        self.board_widget = BoardWidget()

        # Set window background color
        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.gray)
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
            self.run_button.clicked.connect(self.start_pressed)
            layout.addWidget(self.run_button)

        self.setLayout(layout)

    def start_pressed(self):
        self.game_interaction.start_game_thread()
        self.run_button.deleteLater()
    
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

            hboxLayout = QtWidgets.QHBoxLayout()
            self.horizontalButtonBox = QtWidgets.QGroupBox("Controls")
            self.horizontalButtonBox.setLayout(hboxLayout)

            self.back_button = QtWidgets.QPushButton('<- go back')
            self.back_button.clicked.connect(self.back)
            hboxLayout.addWidget(self.back_button)

            self.next_button = QtWidgets.QPushButton('next ->')
            self.next_button.clicked.connect(self.next)
            hboxLayout.addWidget(self.next_button)

            self.mrx_toggle_button = QtWidgets.QCheckBox("Secret Mister X")
            self.drawMrx = True
            self.mrx_toggle_button.stateChanged.connect(self.toggle_misterx)
            hboxLayout.addWidget(self.mrx_toggle_button)

            self.mrx_possible_toggle_button = QtWidgets.QCheckBox("Mister X Possible Positions")
            self.drawPossibleMrxPos = False
            self.mrx_possible_toggle_button.stateChanged.connect(self.toggle_misterx_possible)
            hboxLayout.addWidget(self.mrx_possible_toggle_button)

            hboxLayout.addStretch()

            self.exit_button = QtWidgets.QPushButton("<Exit>")
            self.exit_button.clicked.connect(self.exit)
            hboxLayout.addWidget(self.exit_button)

            self.refresh_button = QtWidgets.QPushButton("Refresh")
            self.refresh_button.clicked.connect(self.update)
            hboxLayout.addWidget(self.refresh_button)
            
            self.layout().addWidget(self.horizontalButtonBox)
            
            self.board_widget.hide()
            self.horizontalButtonBox.hide()

        self.parseData()  
            
    def showBoard(self):
        # Remove old widgets
        self.onFileSuccess.deleteLater()
        self.start_replay_button.deleteLater()

        # Show new widgets
        self.board_widget.show()
        self.horizontalButtonBox.show()

        self.parseData()            
        self.update()
    
    def parseData(self):
        data = self.data

        self.numDetectives = len(data[2])
        self.startPositions = [data[1][0][0][0]] + [det[0][0] for det in data[2]]
        self.positions = self.startPositions
        self.createTurns(data)
        self.idx = -1  # Index of turn currently showing, -1 for startpositions
    
    def createTurns(self, data):
        self.turns = []
        self.totalHistory = [[] for _ in range(self.numDetectives + 1)]  # One list for mrx and one per detective
        self.indices = [-1 for _ in range(self.numDetectives + 1)]  # One list for mrx and one per detective
        xindex = 0
        dindices = [0] * self.numDetectives
        allDone = False
        while not allDone:
            allDone = True
            if xindex < len(data[1][0]):
                allDone = False
                self.totalHistory[0].append(data[1][0][xindex])
                self.turns.append(0)
                if xindex in data[1][1]:
                    # overwrite because double so put both moves together
                    self.totalHistory[0][-1] = [data[1][0][xindex], data[1][0][xindex + 1]]
                    xindex += 1
                xindex += 1
            for i, idx in enumerate(dindices):
                if idx < len(data[2][i]):
                    allDone = False
                    self.totalHistory[i + 1].append(data[2][i][idx])
                    self.turns.append(i + 1)
                    dindices[i] += 1
    
    def update(self):
        dpos = self.positions[1:]
        # Only draw Mrx's position if asked
        if self.drawMrx:
            mrx = self.positions[0]
            img = util.drawReplay(dpos, mrx)
        else:
            img = util.drawReplay(dpos)
        
        # Draw registered possible mrx locations
        if self.drawPossibleMrxPos:
            self.updatePossibleMrxPositions()
            for pos in self.possibleMrxPos:
                img = util.drawCross(img, pos)
        
        self.board_widget.image_data_slot(img)
    
    def next(self):
        if self.idx + 1 >= len(self.turns):
            return self.update()
        self.idx += 1
        playerIndex = self.turns[self.idx]
        self.indices[playerIndex] += 1
        moveIndex = self.indices[playerIndex]
        move = self.totalHistory[playerIndex][moveIndex]

        if len(move) == 2:
            # Double move
            move = move[1]

        dest = move[-1]
        self.positions[playerIndex] = dest

        return self.update()
    
    def back(self):
        if self.idx == -1:
            return self.update()
        playerIndex = self.turns[self.idx]
        moveIndex = self.indices[playerIndex]
        move = self.totalHistory[playerIndex][moveIndex]

        if len(move) == 2:
            # Double move
            move = move[0]

        dest = move[0]
        self.positions[playerIndex] = dest
        
        self.idx -= 1
        self.indices[playerIndex] -= 1
        return self.update()
        
    def toggle_misterx(self):
        self.drawMrx = not self.drawMrx
        self.update()
    
    def updatePossibleMrxPositions(self):
        game = ScotlandYard(numDetectives=self.numDetectives)
        game.misterx.position = self.positions[0]
        numMovesDone = self.indices[0]
        hist = []
        for i in range(numMovesDone + 1):
            move = self.totalHistory[0][i]
            if len(move) == 2:
                # Double move
                for i in range(2):
                    hist.append(move[i])
            else:
                hist.append(move)
        game.misterx.history = hist
        for i, d in enumerate(game.detectives):
            d.position = self.positions[i + 1]
        
        self.possibleMrxPos = game.board.possibleMisterXPositions()
        print(f"After the following moves: {game.misterx.history}; We have a chance to find Mr. X at the following locations {self.possibleMrxPos}")

    def toggle_misterx_possible(self):
        self.drawPossibleMrxPos = not self.drawPossibleMrxPos
        self.update()

    def exit(self):
        QtCore.QCoreApplication.quit()
