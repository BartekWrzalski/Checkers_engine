import time

import pygame
from checkers.constants import WIDTH, HEIGHT, INFO_WIDTH
from checkers.game import Game


FPS = 60
GAMES = 10
WIN = pygame.display.set_mode((WIDTH + INFO_WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def main():
    game = Game(WIN, mode='ivi')

    for i in range(GAMES):
        game.start_game()
        time.sleep(3)
    pygame.quit()


if __name__ == '__main__':
    main()
