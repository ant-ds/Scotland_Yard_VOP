from game.game import ScotlandYard
from game.board import Board

def main():
    game = ScotlandYard(21)

    while game.update():
        pass  # Visualization function calls could be added here
    
    print("Game ended.")

if __name__ == '__main__':
    main()
