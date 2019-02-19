from game.game import ScotlandYard
from game.board import Board

def main():
    board = Board(10)  # TODO: correct initalization for board, and include in default init for game
    game = ScotlandYard(board=board)

    while game.update():
        pass  # Visualization function calls could be added here
        board.draw()  # TODO: draw without interrupting?
    
    print("Game ended.")

if __name__ == '__main__':
    main()
