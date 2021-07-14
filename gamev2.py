import random
import pygame
import os
from pygame.locals import *



#Pendientes
# Aumentar margen izq en x
# Blit solo permite dos?













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
bg_img = pygame.image.load("imgs\\background.png")


class Player():
    def __init__(self, x, y):
        img = pygame.image.load("imgs\\robot.png")
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
        elif key[pygame.K_a] and self.rect.x > 20:
            dx -= 2
        elif key[pygame.K_d] and self.rect.x < 542:
            dx += 2
        else:
            # Speed 
            clock.tick(0)
            if selec == 1 and self.rect.y < 488: #limites
                dy += 10
            elif selec == 2 and self.rect.y > 30:
                dy -= 10
            elif selec == 3 and self.rect.x < 540:
                dx += 10
            elif selec == 4 and self.rect.x > 24:
                dx -= 10
            

            # check for collision
        

            # update player coordinates
        self.rect.x += dx
        self.rect.y += dy
        # print(selec)
        # print(self.rect.y)

        # draw player onto screen
        screen.blit(self.image, self.rect)

class Unit():
    def __init__(self,x, y):
        img = pygame.image.load("imgs\\unit.png")
        self.image = pygame.transform.scale(img, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    
    def draw(self):
        screen.blit(self.image, self.rect)



class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        wall = pygame.image.load("imgs\\wall.png")
        spaceship = pygame.image.load("imgs\\spaceship.png")
        stone = pygame.image.load('imgs\\stone.png')

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
                    img = pygame.transform.scale(spaceship, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 5:
                    img = pygame.transform.scale(stone, (tile_size, tile_size))
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
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
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


#Create random locations for units
xlist = []
ylist = []
unitlist = []
for i in range(20):
    x = random.randint(24,534)
    y = random.randint(30,488)
    xlist.append(x)
    ylist.append(y)
unit1 = Unit(xlist[0],ylist[0])
unit2 = Unit(xlist[1],ylist[1])
unit3 = Unit(xlist[2],ylist[2])
unit4 = Unit(xlist[3],ylist[3])
unit5 = Unit(xlist[4],ylist[4])
unit6 = Unit(xlist[5],ylist[5])
unit7 = Unit(xlist[6],ylist[6])
unit8 = Unit(xlist[7],ylist[7])
unit9 = Unit(xlist[8],ylist[8])
unit10 = Unit(xlist[9],ylist[9])
unit11 = Unit(xlist[10],ylist[10])
unit12 = Unit(xlist[11],ylist[11])
unit13 = Unit(xlist[12],ylist[12])
unit14 = Unit(xlist[13],ylist[13])
unit15 = Unit(xlist[14],ylist[14])
unit16 = Unit(xlist[15],ylist[15])
unit17 = Unit(xlist[16],ylist[16])
unit18 = Unit(xlist[17],ylist[17])
unit19 = Unit(xlist[18],ylist[18])
unit20= Unit(xlist[19],ylist[19])
unitlist.extend((unit1,unit2,unit3,unit4,unit5,unit6,unit7,unit8,unit9,unit10,unit11,unit12,unit13,unit14,unit15,unit16,unit17,unit18,unit19,unit20))

#Create player (spawn player)
player1 = Player(100, screen_height - 500)
# player2 = Player(100, screen_height - 100)
# player3 = Player(100, screen_height - 800)
world = World(world_data)

run = True
while run:

    screen.blit(bg_img, (0, 0))
    # screen.blit(sun_img, (100, 100))
    
    
    
    
    
    for i in range(len(unitlist)):
        unitlist[i].draw()
    
    

  

    world.draw()
   

    player1.update()
    # player2.update()
    # player3.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
