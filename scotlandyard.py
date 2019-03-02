from game.game import ScotlandYard

import game.constants as const


def main():
    game = ScotlandYard(visualize=True, verbose=True)

    stop = False
    while not stop:
        stop, status = game.update()
        pass  # Visualization function calls could be added here
    
    print(f"Game ended with status {status}::  {const.GAME_END_MESSAGES[status]}")


if __name__ == '__main__':
    main()
