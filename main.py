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
fps_count = 0
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
        self.hp = 200
        self.is_jumping = True
        self.is_falling = False
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

    def gravity(self):
        if self.is_jumping:
            self.movey += 3.2

    def control(self, x, y):
        """
        To control player movement
        :param x: x direction
        :param y: y direction
        """
        self.movex += x

    def jump(self):
        if self.is_jumping is False:
            self.is_falling = False
            self.is_jumping = True

    def hp_remaining(self) -> int:
        """Return the percent of health remaining"""
        return self.hp / 200

    def update(self):
        """
        :return:
        """
        if self.movex < 0:
            self.is_jumping = True
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        if self.movex > 0:
            self.is_jumping = True
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = self.images[self.frame//ani]
        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in enemy_hit_list:
            self.hp -= 1
            print(self.hp)

        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for g in ground_hit_list:
            self.movey = 0
            self.rect.bottom = g.rect.top
            self.is_jumping = False  # stop jumping

        # fall off the world
        if self.rect.y > SCREEN_HEIGHT:
            self.hp -= 1
            print(self.hp)
            self.rect.x = tile_x
            self.rect.y = tile_y

        plat_hit_list = pygame.sprite.spritecollide(self, plat_list, False)
        for p in plat_hit_list:
            self.is_jumping = False  # stop jumping
            self.movey = 0
            # approach from below
            if self.rect.bottom <= p.rect.bottom:
                self.rect.bottom = p.rect.top
            else:
                self.movey += 3.2

        if self.is_jumping and self.is_falling is False:
            self.is_falling = True
            self.movey -= 30

        self.rect.x += self.movex
        self.rect.y += self.movey

        # If player is too far to the left
        if self.rect.left < 0:
            self.rect.x = 0

        # If player is too far to the right
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH








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

    def update(self):
        speed = 3
        if self.player.rect.x + 20> self.rect.x:
            self.rect.x += speed
        if self.player.rect.x -20 < self.rect.x:
            self.rect.x -= speed
        if self.player.rect.y + 20 > self.rect.y:
            self.rect.y += speed - 1
        if self.player.rect.y - 20 < self.rect.y:
            self.rect.y -= speed - 1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, imgw, imgh, img):
        """Params:
        x: x location
        y: y location
        imgw: image width
        imgh: image height
        img: image file"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/tile_aqua.png")
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def ground(gloc,tile_x,tile_y):
        ground_list = pygame.sprite.Group()
        i=0

        while i < len(gloc):
            ground = Platform(gloc[i], SCREEN_HEIGHT - tile_y, tile_x, tile_y, './images/tile_aqua.png')
            ground_list.add(ground)
            i=i+1

        return ground_list

    def platform(tx, ty):
        plat_list = pygame.sprite.Group()
        ploc = []
        i = 0

        ploc.append((200, SCREEN_HEIGHT - ty - 150, 3))
        ploc.append((300, SCREEN_HEIGHT - ty - 300, 3))
        ploc.append((550, SCREEN_HEIGHT - ty - 150, 3))
        while i < len(ploc):
            j = 0
            while j <= ploc[i][2]:
                plat = Platform((ploc[i][0] + (j * tx)), ploc[i][1], tx, ty, './images/tile_aqua.png')
                plat_list.add(plat)
                j = j + 1
            print('run' + str(i) + str(ploc[i]))
            i = i + 1

        return plat_list



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

gloc = []
tile_x = 64
tile_y = 64

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
time_score_seconds = 0

with open("./data/highscore.txt") as f:
    high_score = int(f.readline().strip())

font = pygame.font.SysFont("Arial", 25)

i = 0
while i <= (SCREEN_WIDTH / tile_x)+tile_x:
    gloc.append(i * tile_x)
    i = i + 1

ground_list = Platform.ground(gloc, tile_x, tile_y )
plat_list = Platform.platform(tile_x, tile_y)
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
            if event.key == pygame.K_SPACE:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.control(steps, 0)
            if event.key == pygame.K_d:
                player.control(-steps, 0)

    if player.hp_remaining() <= 0:
        main = False

    time_score_seconds = fps_count // fps
    time_score_minutes = time_score_seconds // 60
    seconds = time_score_seconds % 60

    output_string = "{0:02}:{1:02}".format(time_score_minutes, seconds)

    # update background
    world.blit(background, background_parims)

    # draw player into the world
    player.update()
    player.gravity()
    player_list.draw(world)
    enemy_list.draw(world)
    ground_list.draw(world)
    plat_list.draw(world)
    enemy.update()
    pygame.draw.rect(screen, BLUE, [580, 5, 215, 20])
    # Draw the foreground rectangle which is the remaining health
    life_remaining = 215 - int(215 * player.hp_remaining())
    pygame.draw.rect(screen, RED, [580, 5, life_remaining, 20])

    screen.blit(
        font.render(f"Current Time: {output_string}", True, WHITE),
        (5, 5)
    )
    screen.blit(
        font.render(f"High Score (seconds): {high_score}", True, WHITE),
        (5, 70)
    )
    screen.blit(
        font.render(f"Current time (seconds): {time_score_seconds}", True, WHITE),
        (5, 40)
    )
    fps_count += 1
    # Update the screen
    pygame.display.flip()

    # ----------- CLOCK TICK
    clock.tick(fps)

    with open("./data/highscore.txt", "w") as f:
        if time_score_seconds > high_score:
            f.write(str(time_score_seconds))
        else:
            f.write(str(high_score))

