import os
import pygame
import random
import sys
from pygame import mixer

from pygame.locals import *

pygame.mixer.pre_init(44100, -16,2,512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 30
score = 0
spaceship_units = 0
stop = 1
font_score = pygame.font.SysFont('Bauhaus 93', 30)
white = (0, 0, 0)
screen_width = 750
screen_height = 800
spaceship_x = 285
spaceship_y = 315
unitx = 0
unity = 0
game_over = 0
stop = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mars Mission')

tile_size = 30
menu = True
reactive = False
collaborative = False

bg = pygame.image.load('imgs/background.png')
bg_img = pygame.transform.scale(bg, (1000, 600))
player_img = pygame.image.load(
    "imgs/robot.png")
spaceship_img = pygame.image.load(
    'imgs/spaceship.png')
reactive_img = pygame.image.load(
    "imgs/reactive_btn.png")
collaborative_img = pygame.image.load(
    "imgs/collaborative_btn.png")
exit_img = pygame.image.load(
    "imgs/exit_btn.png")
unit_img = pygame.image.load(
    'imgs/unit.png')
wall_img = pygame.image.load(
    "imgs/wall.png")
stone_img = pygame.image.load(
    'imgs/stone.png')
pygame.mixer.music.load('music/music1.mp3')
pygame.mixer.music.play(-1,0.0,5000)



def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    img.set_alpha(127)
    screen.blit(img, (x, y))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action


class Player():
    def __init__(self, x, y):

        img = player_img
        self.image = pygame.transform.scale(img, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.waitingx = 0
        self.waitingy = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.carrryingunit = 0
        self.unitsleft = 0
        self.isreturning = False
        self.hasunit = False
        self.iswaiting = False
        self.canhelp = True
        self.canpickup = True
        self.needshelp = False
        self.poshistory = []
        self.goingback = False
        self.isalone = False

    def update(self, stop):

        selec = random.randint(1, 4)
        unitsize = random.randint(1, 4)
        dx = 0
        dy = 0
        global spaceship_units
        global score
        score = spaceship_units
        global unitx
        global unity
        action = 0

        if stop == 0:

            if selec == 1 and self.rect.y < 488:
                dy += 2
            elif selec == 2 and self.rect.y > 30:
                dy -= 2
            elif selec == 3 and self.rect.x < 540:
                dx += 2
            elif selec == 4 and self.rect.x > 24:
                dx -= 2

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    dy = 0

            if self.iswaiting:
                action = 5

            elif self.canpickup == False:
                if pygame.sprite.spritecollide(self, unit_group, False):
                    action = 0
                    self.isreturning = True

            elif self.isreturning == True:
                action = 2
                if pygame.sprite.spritecollide(self, spaceship_group, False):
                    action = 0
                    self.isreturning = False
                    self.canpickup = True

            elif self.hasunit == True:
                action = 2
                if pygame.sprite.spritecollide(self, spaceship_group, False):
                    spaceship_units += self.unitsleft
                    self.unitsleft = 0
                    self.isreturning = False
                    self.hasunit = False



            elif self.canpickup == True and self.isreturning == False:

                if pygame.sprite.spritecollide(self, unit_group, True):

                    unitx = self.rect.x
                    unity = self.rect.y

                    if unitsize == 1:
                        self.unitsleft = 1
                        self.hasunit = True

                    elif unitsize > 1:
                        self.unitsleft = unitsize

                        self.iswaiting = True

                else:
                    action = 0

            if action == 0:
                if selec == 1 and self.rect.y < 488:
                    dy += 2
                elif selec == 2 and self.rect.y > 30:
                    dy -= 2
                elif selec == 3 and self.rect.x < 540:
                    dx += 2
                elif selec == 4 and self.rect.x > 24:
                    dx -= 2

            elif action == 1:
                if self.rect.x > unitx:
                    dx -= 2
                else:
                    dx += 2
                if self.rect.y < unity:
                    dy += 2
                else:
                    dy -= 2

            elif action == 2:
                if self.rect.x > spaceship_x:
                    dx -= 2
                else:
                    dx += 2
                if self.rect.y < spaceship_y:
                    dy += 2
                else:
                    dy -= 2

            elif action == 3:
                pass


            elif action == 4:
                pass


            elif action == 5:
                dx = 0
                dy = 0
            for tile in world.tile_list:

                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx *= -4
                    dy *= -4

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    dy *= -4
                    dx *= -4

            self.rect.x += dx
            self.rect.y += dy
            self.poshistory = [self.rect.x, self.rect.y]

            screen.blit(self.image, self.rect)

            draw_text('SCORE X' + str(spaceship_units),
                      font_score, white, tile_size + 600, 300, )
            return stop

    def updatee(self, stop):
        selec = random.randint(1, 4)
        unitsize = random.randint(1, 4)
        dx = 0
        dy = 0
        global spaceship_units
        global score
        score = spaceship_units
        global unitx
        global unity
        if stop == 0:

            if selec == 1 and self.rect.y < 488:
                dy += 2
            elif selec == 2 and self.rect.y > 30:
                dy -= 2
            elif selec == 3 and self.rect.x < 540:
                dx += 2
            elif selec == 4 and self.rect.x > 24:
                dx -= 2

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    dy = 0

            if self.hasunit == False and self.isreturning == False:

                if pygame.sprite.spritecollide(self, unit_group, False):

                    unitx = self.rect.x
                    unity = self.rect.y

                    if unitsize == 1:
                        self.unitsleft = unitsize
                        self.hasunit = True
                        self.isreturning = False

                    elif unitsize > 1:
                        self.unitsleft = unitsize
                        self.hasunit = True
                        self.isreturning = True

            elif self.hasunit == True and self.isreturning == False:

                if self.rect.x > spaceship_x:
                    dx -= 2
                else:
                    dx += 2
                if self.rect.y < spaceship_y:
                    dy += 2
                else:
                    dy -= 2

                if pygame.sprite.spritecollide(self, spaceship_group, False):
                    spaceship_units += 1
                    self.hasunit = False
                    self.isreturning = True
                    self.unitsleft = 5

            elif self.hasunit == True and self.isreturning == True:

                if self.unitsleft > 0:
                    if self.rect.x > spaceship_x:
                        dx -= 2
                    else:
                        dx += 2
                    if self.rect.y < spaceship_y:
                        dy += 2
                    else:
                        dy -= 2
                    if pygame.sprite.spritecollide(self, spaceship_group, False):
                        self.hasunit = False
                        self.isreturning = True
                        self.unitsleft -= 1
                        spaceship_units += 1
                else:
                    self.hasunit = False
                    self.isreturning = False


            elif self.hasunit == False and self.isreturning == True:
                if self.unitsleft == 1:
                    if self.rect.x > unitx:
                        dx -= 2
                    else:
                        dx += 2
                    if self.rect.y < unity:
                        dy += 2
                    else:
                        dy -= 2
                    if pygame.sprite.spritecollide(self, unit_group, True):
                        self.hasunit = True
                        self.isreturning = True
                elif self.unitsleft == 5:
                    if self.rect.x > unitx:
                        dx -= 2
                    else:
                        dx += 2
                    if self.rect.y < unity:
                        dy += 2
                    else:
                        dy -= 2
                    if pygame.sprite.spritecollide(self, unit_group, True):
                        self.hasunit = False
                        self.isreturning = False
                        self.unitsleft = 0


                elif self.unitsleft > 0:
                    if self.rect.x > unitx:
                        dx -= 2
                    else:
                        dx += 2
                    if self.rect.y < unity:
                        dy += 2
                    else:
                        dy -= 2
                    if pygame.sprite.spritecollide(self, unit_group, False):
                        self.hasunit = True
                        self.isreturning = True

                else:

                    self.hasunit = False
                    self.isreturning = False

            for tile in world.tile_list:

                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx *= -4
                    dy *= -4

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    dy *= -4
                    dx *= -4

            self.rect.x += dx
            self.rect.y += dy

            screen.blit(self.image, self.rect)

            draw_text('SCORE X' + str(spaceship_units), font_score, white, tile_size + 600, 100)
        return stop


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = spaceship_img
        self.image = pygame.transform.scale(
            img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)


class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = unit_img
        self.image = pygame.transform.scale(
            img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class World():
    def __init__(self, data):
        self.tile_list = []

        wall = wall_img
        spaceship = spaceship_img
        stone = stone_img

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
                    spaceship = Spaceship(
                        col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    spaceship_group.add(spaceship)
                if tile == 5:
                    img = pygame.transform.scale(stone, (tile_size // 2, tile_size // 2))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 7:
                    unit = Unit(col_count * tile_size + (tile_size // 2),
                                row_count * tile_size + (tile_size // 2))
                    unit_group.add(unit)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 5, 0, 0, 0, 0, 5, 7, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 7, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 7, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 5, 7, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 5, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

unit_group = pygame.sprite.Group()
spaceship_group = pygame.sprite.Group()
player1 = Player(285, 315)
player2 = Player(285, 314)
player3 = Player(285, 316)
reactive_button = Button(120, 120, reactive_img)
collaborative_button = Button(240, 240, collaborative_img)
exit_button = Button(360, 360, exit_img)
world = World(world_data)

run = True
while run:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))

    if menu == True:
        if exit_button.draw():
            run = False

        if reactive_button.draw() == True:
            menu = False
            reactive = True
            collaborative = False
        if collaborative_button.draw() == True:
            menu = False
            reactive = False
            collaborative = True

    elif collaborative == True:

        world.draw()
        if stop == 0:
            spaceship_group.draw(screen)
            unit_group.draw(screen)

            if player1.iswaiting:
                player2.canpickup = False
            if player2.iswaiting:
                player1.canpickup = False

            if player1.iswaiting and player2.canhelp:
                if player2.rect.x > player1.rect.x:
                    player2.rect.x -= 1
                else:
                    player2.rect.x += 1

                if player2.rect.y < player1.rect.y:
                    player2.rect.y += 1
                else:
                    player2.rect.y -= 1

            if player2.iswaiting and player1.canhelp:
                if player1.rect.x > player2.rect.x:
                    player1.rect.x -= 1
                else:
                    player1.rect.x += 1

                if player1.rect.y < player2.rect.y:
                    player1.rect.y += 1
                else:
                    player1.rect.y -= 1

            if (player1.rect.x == player2.rect.x or player1.rect.y == player2.rect.y):
                if player1.rect.x > spaceship_x and player2.rect.x > spaceship_x:
                    player1.rect.x -= 1
                    player2.rect.x -= 1
                else:
                    player1.rect.x += 1
                    player2.rect.x += 1

                if player1.rect.y < spaceship_y and player2.rect.y < spaceship_y:
                    player1.rect.y += 1
                    player2.rect.y += 1
                else:
                    player1.rect.y -= 1
                    player2.rect.y -= 1

                if pygame.sprite.spritecollide(player1, spaceship_group, False):
                    player2.isreturning = False
                    player1.isreturning = False
                    player1.canpickup = True
                    player2.canpickup = True
                    spaceship_units += player1.unitsleft
                    spaceship_units += player2.unitsleft
                    player1.unitsleft = 0
                    player2.unitsleft = 0
                    player1.iswaiting = False
                    player2.iswaiting = False

                if player1.iswaiting == False and player2.canpickup == True and player3.iswaiting == True:
                    player3.isalone = True
                    player3.iswaiting = False
                    player3.canpickup = False

                if player1.iswaiting == True and player2.canpickup == False and player3.iswaiting == True:
                    player3.isalone = True
                    player3.iswaiting = False
                    player3.canpickup = False

                if player3.isalone == True:
                    if player3.rect.x > spaceship_x:
                        player3.rect.x -= 2
                    else:
                        player3.rect.x += 2
                    if player3.rect.y < spaceship_y:
                        player3.rect.y += 2
                    else:
                        player3.rect.y -= 2
                    if pygame.sprite.spritecollide(player3, spaceship_group, False):
                        spaceship_units += player3.unitsleft
                        player3.unitsleft = 0
                        player3.isalone = False
                        player3.goingback = True
                        player3.canpickup = True
                        player3.isreturning = False

                if spaceship_units >= 20:
                    player1.rect.x = spaceship_x
                    player2.rect.x = spaceship_x
                    player3.rect.x = spaceship_x
                    player1.rect.x = spaceship_y
                    player2.rect.x = spaceship_y
                    player3.rect.x = spaceship_y

                    stop = 1

            stop = player1.update(stop)
            stop = player2.update(stop)
            stop = player3.update(stop)


        else:
            draw_text("GAME OVER", font_score, white, 600, 300)


    elif reactive == True:
        world.draw()
        if stop == 0:
            spaceship_group.draw(screen)
            unit_group.draw(screen)

            if spaceship_units >= 20:
                player1.rect.x = spaceship_x
                player2.rect.x = spaceship_x
                player3.rect.x = spaceship_x
                player1.rect.x = spaceship_y
                player2.rect.x = spaceship_y
                player3.rect.x = spaceship_y

                stop = 1
            stop = player1.updatee(stop)
            stop = player2.updatee(stop)
            stop = player3.updatee(stop)
        else:
            draw_text("GAME OVER", font_score, white, 600, 300)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
