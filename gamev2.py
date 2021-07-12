import random
import pygame
from pygame.locals import *

pygame.init()

#Clock 
clock = pygame.time.Clock()

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mars')

# define game variables
tile_size = 30


# load images
# sun_img = pygame.image.load('imgs/robot.png')
bg_img = pygame.image.load(
    "C:\\Users\\alexd\\Documents\\Python\\Mars\\imgs\\background.png")


class Player():
    def __init__(self, x, y):
        img = pygame.image.load(
            "C:\\Users\\alexd\\Documents\\Python\\Mars\\imgs\\robot.png")
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        selec = random.randint(1,4)
        dx = 0
        dy = 0

        # get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_s]:
            dy += 2
        elif key[pygame.K_w]:
            dy -= 2
        elif key[pygame.K_a]:
            dx -= 2
        elif key[pygame.K_d]:
            dx += 2
        else:
            #Speed 
            clock.tick(200)
            if selec == 1:
                dy += 10
            elif selec == 2:
                dy -= 10
            elif selec == 3:
                dx += 10
            elif selec == 4:
                dx -= 10
            

            # check for collision

            # update player coordinates
        self.rect.x += dx
        self.rect.y += dy
        print(selec)        

        # draw player onto screen

        screen.blit(self.image, self.rect)


class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        wall = pygame.image.load(
            "C:\\Users\\alexd\\Documents\\Python\\Mars\\imgs\\wall.png")
        spaceship = pygame.image.load(
            "C:\\Users\\alexd\\Documents\\Python\\Mars\\imgs\\spaceship.png")
        # grass_img = pygame.image.load('imgs/wall.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(wall, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(
                        spaceship, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


#Spawn player with location in ()
player1 = Player(100, screen_height - 500)
# player2 = Player(100, screen_height - 100)
# player3 = Player(100, screen_height - 800)
world = World(world_data)

run = True
while run:

    screen.blit(bg_img, (0, 0))
    # screen.blit(sun_img, (100, 100))

    world.draw()

    player1.update()
    # player2.update()
    # player3.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
