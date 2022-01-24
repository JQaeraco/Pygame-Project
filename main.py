# Pygame Boilerplate
# Author: Joshua
# 2022

# Game Idea: fruit ninja type game


# import pygame
# import random
#
# pygame.init()
#
# WHITE = (255, 255, 255)
# BLACK = (  0,   0,   0)
# RED   = (255,   0,   0)
# GREEN = (  0, 255,   0)
# BLUE  = (  0,   0, 255)
# BGCOLOUR = (100, 100, 255)
#
# lives = 3
# score = 0
# SCREEN_WIDTH  = 800
# SCREEN_HEIGHT = 600
# SCREEN_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT)
# WINDOW_TITLE  = "<<Not Fruit Ninja>>"
#
# # Create a movable player
# class Player:
#     def __init__(self):
#         pos = pygame.mouse.get_pos()
#         self.x = pos[0]
#         self.y = pos[1]
#         self.width = 5
#         self.height = 5
#
#
# class Fruit:
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.image.load("./images/Apple.jpg")
#         self.width = 160
#         self.height = 160
#         self.rect.x, self.rect.y = (
#             random.randrange(SCREEN_WIDTH),
#             650
#         )
#     def update(self):
#
#
#
# def main() -> None:
#     """Driver of the Python script"""
#     # Create the screen
#     screen = pygame.display.set_mode(SCREEN_SIZE)
#     pygame.display.set_caption(WINDOW_TITLE)
#
#     # Create some local variables that describe the environment
#     done = False
#     clock = pygame.time.Clock()
#     all_sprites = pygame.sprite.Group()
#     enemy_sprites = pygame.sprite.Group()
#     # ----------- MAIN LOOP
#     while not done:
#         # ----------- EVENT LISTENER
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 done = True
#
#         # ----------- CHANGE ENVIRONMENT
#
#         # ----------- DRAW THE ENVIRONMENT
#         screen.fill(BGCOLOUR)      # fill with bgcolor
#
#         # Update the screen
#         pygame.display.flip()
#
#         # ----------- CLOCK TICK
#         clock.tick(75)
#
#
# if __name__ == "__main__":
#     main()

import random
import time
import pygame
import sys
import os
from PIL import Image


# Variables Section

# Colours
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
VIRIDIAN_GREEN = (14, 149, 148)
ORANGE_SODA = (242, 84, 45)
WHEAT = (245, 223, 187)
BGCOLOUR = (100, 100, 255)
ALPHA = (157, 142, 135)
AlPHA2 = (3, 9, 18)
direction = 0
# Screen dimensions
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# frames
fps = 60
ani = 4 # for animating
main = True
world = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Objects Section

class Player(pygame.sprite.Sprite):
    """
    To spawn the player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.hp = 10
        self.images = []
        # load all images of walk cycle
        for i in range(1, 5):
            # load and scale the images
            img = pygame.image.load(f"./images/hero{i}.png").convert()
            img = pygame.transform.scale(img, (11 * 5, 15 * 5))
            # Get rid of coloured box around the image
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            # Set idle stance
            self.image = self.images[0]
            self.rect = self.image.get_rect()


    def control(self, x, y):
        """
        To control player movement
        :param x: x direction
        :param y: y direction
        """
        self.movex += x
        self.movey += y

    def update(self):
        """
        :return:
        """
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        if self.movex < 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        if self.movex > 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = self.images[self.frame//ani]
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.hp -= 1
            print(self.hp)

class Enemy(pygame.sprite.Sprite):
    """
    Spawn Enemy
    """
    def __init__(self, x, y, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.frame = 0
        self.images = []
        for i in range(1, 6):
            # load and scale the images
            img = pygame.image.load(f"./images/orc{i}.png").convert()
            img = pygame.transform.scale(img, (11 * 5, 15 * 5))
            img.convert_alpha()
            img.set_colorkey((0, 0 ,0))
            self.images.append(img)
            # Set idle stance
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        self.counter = 0
    def move(self, Player):
        """
        movement
        :return:
        """


        # speed = 5
        # if self.rect.x > Player.movex:
        #     self.rect.x -= speed
        # elif self.rect.x < Player.movex:
        #     self.rect.x += speed
        #     # Movement along y direction
        # if self.rect.y < Player.movey:
        #     self.rect.y += speed
        # elif self.rect.y > Player.movey:
        #     self.rect.y -= speed
        #
        # self.counter += 1

    def update(self):
        if self.player.rect.x > self.rect.x:
            self.rect.x += 5
        if self.player.rect.x < self.rect.x:
            self.rect.x -= 5
        if self.player.rect.y > self.rect.y:
            self.rect.y += 5
        if self.player.rect.y < self.rect.y:
            self.rect.y -= 5

# Setup Section
clock = pygame.time.Clock()
pygame.init()
background = pygame.image.load("./images/bachground.jpg")
background_parims = world.get_rect()
player = Player()
player.rect.x = 0
player.rect.y = 400
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 7

enemy = Enemy(300, 400, player)
enemy_list = pygame.sprite.Group()
enemy_list.add(enemy)
# Main Loop Section
while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Press Q to Quit game
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                main = False

        # Player movement
            if event.key == pygame.K_a:
                player.control(-steps, 0)
            if event.key == pygame.K_d:
                player.control(steps, 0)
            if event.key == pygame.K_w:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.control(steps, 0)
            if event.key == pygame.K_d:
                player.control(-steps, 0)


    # update background
    world.blit(background, background_parims)

    # draw player into the world
    player.update()
    player_list.draw(world)
    enemy_list.draw(world)
    enemy.update()
    # Update the screen
    pygame.display.flip()

    # ----------- CLOCK TICK
    clock.tick(fps)
