# Pygame Boilerplate
# Author: Joshua
# 2022

# Game Idea: fruit ninja type game


import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BGCOLOUR = (100, 100, 255)

lives = 3
score = 0
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE  = "<<Not Fruit Ninja>>"

# Create a movable player
class Player:
    def __init__(self):
        pos = pygame.mouse.get_pos()
        self.x = pos[0]
        self.y = pos[1]
        self.width = 5
        self.height = 5


class Fruit:
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./sprites/Apple.jpg")
        self.width = 160
        self.height = 160
        self.rect.x, self.rect.y = (
            random.randrange(SCREEN_WIDTH),
            650
        )
    def update(self):



def main() -> None:
    """Driver of the Python script"""
    # Create the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)

    # Create some local variables that describe the environment
    done = False
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    # ----------- MAIN LOOP
    while not done:
        # ----------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----------- CHANGE ENVIRONMENT

        # ----------- DRAW THE ENVIRONMENT
        screen.fill(BGCOLOUR)      # fill with bgcolor

        # Update the screen
        pygame.display.flip()

        # ----------- CLOCK TICK
        clock.tick(75)


if __name__ == "__main__":
    main()
