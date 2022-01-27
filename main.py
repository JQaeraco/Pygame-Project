# Pygame STAY AWAY OGRE
# Author: Joshua
# 2022

# Game Idea: Stay away from angry ogre for as long as possible


import pygame

"VARIABLES SECTION"

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

"OBJECTS SECTION"

class Player(pygame.sprite.Sprite):
    """
    To spawn the player and make it functional
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
        """
        Makes the player succumb to gravity
        """
        if self.is_jumping:
            self.movey += 3.2

    def control(self, x, y):
        """
        To control player movement
        x: x direction
        y: y direction
        """
        self.movex += x

    def jump(self):
        """
        setup for player's jump
        """
        if self.is_jumping is False:
            self.is_falling = False
            self.is_jumping = True

    def hp_remaining(self) -> int:
        """Return the percent of health remaining"""
        return self.hp / 200

    def update(self):
        # implement animation for running
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

        # Take damage when in contact with enemy
        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in enemy_hit_list:
            self.hp -= 1
            print(self.hp)

        # Make player interact with ground
        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for g in ground_hit_list:
            self.movey = 0
            self.rect.bottom = g.rect.top
            self.is_jumping = False  # stop jumping


        # Prevent player from phasing through platforms
        plat_hit_list = pygame.sprite.spritecollide(self, plat_list, False)
        for p in plat_hit_list:
            self.is_jumping = False  # stop jumping
            self.movey = 0

            # approach from below
            if self.rect.bottom <= p.rect.bottom:
                self.rect.bottom = p.rect.top
            else:
                self.movey += 3.2

        # Allow player to jump
        if self.is_jumping and self.is_falling is False:
            self.is_falling = True
            self.movey -= 30

        self.rect.x += self.movex
        self.rect.y += self.movey

        # If player is too far to the left, stop him from moving off the screen
        if self.rect.left < 0:
            self.rect.x = 0

        # If player is too far to the right, stop him from moving off the screen
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

        # load and scale orc sprite
        img = pygame.image.load(f"./images/orc1.png").convert()
        img = pygame.transform.scale(img, (11 * 5, 15 * 5))

        # get rid of box around enemy
        img.convert_alpha()
        img.set_colorkey((0, 0 ,0))
        self.images.append(img)

        # Set idle stance
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Make enemy follow player
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
        """
        Params:
            x: x location
            y: y location
            imgw: image width
            imgh: image height
            img: image file
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/tile_aqua.png")
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def ground(gloc,tile_x,tile_y):
        """
        Params:
            tile_x: x location of tile
            tile_y: y location of tile

        """
        ground_list = pygame.sprite.Group()
        i=0

        while i < len(gloc):
            ground = Platform(gloc[i], SCREEN_HEIGHT - tile_y, tile_x, tile_y, './images/tile_aqua.png')
            ground_list.add(ground)
            i=i+1

        return ground_list

    def platform(tile_x, tile_y):
        plat_list = pygame.sprite.Group()
        ploc = []
        i = 0
        # create platforms
        ploc.append((200, SCREEN_HEIGHT - tile_y - 150, 3))
        ploc.append((300, SCREEN_HEIGHT - tile_y - 300, 3))
        ploc.append((550, SCREEN_HEIGHT - tile_y - 150, 3))
        while i < len(ploc):
            j = 0
            while j <= ploc[i][2]:
                plat = Platform((ploc[i][0] + (j * tile_x)), ploc[i][1], tile_x, tile_y, './images/tile_aqua.png')
                plat_list.add(plat)
                j = j + 1
            print('run' + str(i) + str(ploc[i]))
            i = i + 1

        return plat_list

"SETUP SECTION"

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

world = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
time_score_seconds = 0

# Read highscore
with open("./data/highscore.txt") as f:
    high_score = int(f.readline().strip())

font = pygame.font.SysFont("Arial", 25)

i = 0
while i <= (SCREEN_WIDTH / tile_x)+tile_x:
    gloc.append(i * tile_x)
    i = i + 1

ground_list = Platform.ground(gloc, tile_x, tile_y )
plat_list = Platform.platform(tile_x, tile_y)

"MAIN LOOP SECTION"
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

    # Lose condition
    if player.hp_remaining() <= 0:
        main = False

    # Timer, record time
    time_score_seconds = fps_count // fps
    minutes = time_score_seconds // 60
    seconds = time_score_seconds % 60

    output_string = "{0:02}:{1:02}".format(minutes, seconds)

    # update background
    world.blit(background, background_parims)

    # Draw everything
    player.update()
    player.gravity()
    player_list.draw(world)
    enemy_list.draw(world)
    ground_list.draw(world)
    plat_list.draw(world)
    enemy.update()

    # Draw health bar
    pygame.draw.rect(world, BLUE, [700, 5, 215, 20])
    life_remaining = 215 - int(215 * player.hp_remaining())
    pygame.draw.rect(world, RED, [700, 5, life_remaining, 20])

    # Draw the current time with minutes and seconds
    world.blit(
        font.render(f"Current Time: {output_string}", True, WHITE),
        (5, 5)
    )
    # Draw the high score
    world.blit(
        font.render(f"High Score (seconds): {high_score}", True, WHITE),
        (5, 70)
    )
    # Draw the current time in seconds
    world.blit(
        font.render(f"Current time (seconds): {time_score_seconds}", True, WHITE),
        (5, 40)
    )

    # update the timer
    fps_count += 1

    # Update the screen
    pygame.display.flip()

    # ----------- CLOCK TICK
    clock.tick(fps)

    # Record score if it was greater than the previous high score
    with open("./data/highscore.txt", "w") as f:
        if time_score_seconds > high_score:
            f.write(str(time_score_seconds))
        else:
            f.write(str(high_score))

