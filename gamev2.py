import random
import pygame
import os
import sys
from pygame.locals import *


# Pendientes
# agregar nave como sprite para permitir colisiones y hacer respectivo if para que se depositen unidades
# hacer que el jugador vaya creadndo el mapa en el que pasa
# pasar esa inmformaciaon a traves de los demas jugadores
# ayudar a un jugador si la unidad pesa mas de 2 unidades y la lleven entre ellos
# NOTA: podria funcionar que en cuanto encuentren la nave comiejncen a hacer el aprendizaje de el mapa y asi comunicaarse ***Preguntar al profe si tienen que salir de la nave forzosamente

# aniadir valores a unidad y posteriormetente agregarlos en el juego
# Para comprobar el fin dle juego implementar: https://www.youtube.com/watch?v=G8VsEbVS3F8&list=PLjcN1EyupaQnHM1I9SmiXfbT6aG4ezUvu&index=6&ab_channel=CodingWithRuss
# Ordernar codigo
# musica https://www.youtube.com/watch?v=0HxZn6CzOIo&ab_channel=AdhesiveWombat


# dudas
# que paseria si en el camino a la nave se encuentra otra unidad
# que pasaria si todos los jugadores se encuetnran con una una unidad mayor de 2


pygame.init()

# Clock
clock = pygame.time.Clock()
fps = 60
score = 0
spaceship_units = 0
stop = 1
font_score = pygame.font.SysFont('Bauhaus 93', 30)
white = (0, 0, 0)
screen_width = 1000
screen_height = 1000
spaceship_x = 285
spaceship_y = 315
unitx = 0
unity = 0
# x = 285
# y = 315

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mars Mission')

# define game variables
tile_size = 30
menu = True
reactive = False
collaborative = False

# load images
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
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.carrryingunit = 0
        self.unitsleft = 0
        self.isreturning = False
        self.hasunit = False
        self.poshistory = []
        # self.speed = 0
        self.nturns = 0

    def update(self, stop):
        selec = random.randint(1, 4)
        unitsize = random.randint(1, 4)
        dx = 0
        dy = 0
        global spaceship_units
        global score
        if stop == 1:
            selec = random.randint(1, 4)
            dx = 0
            dy = 0
            clock.tick(fps)  # Speed of update
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
                # limites (ya no se deberia de salir con funcion  de abajo, pero manteniendo)
                if selec == 1 and self.rect.y < 488:
                    dy += 10
                elif selec == 2 and self.rect.y > 30:
                    dy -= 10
                elif selec == 3 and self.rect.x < 540:
                    dx += 10
                elif selec == 4 and self.rect.x > 24:
                    dx -= 10

                # Speed
                # clock.tick(60)
                # if selec == 1 and self.rect.y < 488: #limites
                #     dy += 10
                # elif selec == 2 and self.rect.y > 30:
                #     dy -= 10
                # elif selec == 3 and self.rect.x < 540:
                #     dx += 10
                # elif selec == 4 and self.rect.x > 24:
                #     dx -= 10

                # check for unit

                # check for collisions
                for tile in world.tile_list:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        dy = 0
                # Check for player collision with unit
                unitsize = 1
                if self.hasunit == False:
                    # If player collides with unit
                    if pygame.sprite.spritecollide(self, unit_group, True):
                        if unitsize < 2:
                            self.carrryingunit += unitsize
                            self.hasunit = True
                            stop = 1
                        else:
                            self.carrryingunit += unitsize
                            self.hasunit = True
                            stop = 0
                else:
                    if self.rect.x > spaceship_x:
                        dx -= 1
                    else:
                        dx += 1
                    if self.rect.y < spaceship_y:
                        dy += 1
                    else:
                        dy -= 1
                    if pygame.sprite.spritecollide(self, spaceship_group, False):
                        score += self.carrryingunit
                        spaceship_units += self.carrryingunit
                        self.hasunit = False
                        self.carrryingunit = 0

                # update player coordinates
                self.rect.x += dx
                self.rect.y += dy
                self.poshistory = [self.rect.x, self.rect.y]
            # print(selec)
            # print(self.rect.x)
            # print(self.rect.y)
            print(stop, self.carrryingunit, self.rect.x,
                  self.rect.y, self.poshistory)

            # draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect,
                         2)  # draw margin of box for player
        draw_text('carrying X' + str(self.carrryingunit),
                  font_score, white, tile_size + 700, 400)
        return stop



    def updatee(self):
        selec = random.randint(1, 4)
        unitsize = random.randint(1, 4)
        dx = 0
        dy = 0
        global spaceship_units
        global score
        global unitx
        global unity
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            dy -= 5
        elif key[pygame.K_a]:
            dx -= 5
        elif key[pygame.K_s]:
            dy += 5
        elif key[pygame.K_d]:
            dx += 10
        if selec == 1 and self.rect.y < 488:
            dy += 1
        elif selec == 2 and self.rect.y > 30:
            dy -= 1
        elif selec == 3 and self.rect.x < 540:
            dx += 1
        elif selec == 4 and self.rect.x > 24:
            dx -= 1

        # check for collisions
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0
        # Check for player collision with unit
        unitsize = 2

        # Robot is free for navigating
        if self.hasunit == False and self.isreturning == False:
            # If player collides with unit
            if pygame.sprite.spritecollide(self, unit_group, False):
                # OBTENER COORDENADAS DE X Y Y DE LA UNIDAD
                unitx = self.rect.x
                unity = self.rect.y
                # SI LA UNIDAD ES UNA
                if unitsize == 1:
                    self.carrryingunit += unitsize
                    self.hasunit = True
                    self.isreturning = False
                # SI LA UNIDAD ES MAS GRANDE QUE UNA
                elif unitsize > 1:
                    self.unitsleft = unitsize
                    self.hasunit = True
                    self.isreturning = True

        # CUANDO UNIDAD SEA UNA
        elif self.hasunit == True and self.isreturning == False:
            # BUSCA COORDENADAS DE LA NAVE
            if (self.rect.x > spaceship_x):
                dx -= 1
            else:
                dx += 1
            if (self.rect.y < spaceship_y):
                dy += 1
            else:
                dy -= 1
            # UNA VEZ ENCONTRADA Y HECHO COLISION CON LA NAVE NO TENDRA UNIDADES POR LO QUE VOLVERA A FALSE FALSE Y NO ESTARA CARGANDO U'S
            if pygame.sprite.spritecollide(self, spaceship_group, False):
                score += self.carrryingunit
                spaceship_units += self.carrryingunit
                self.hasunit = False
                self.isreturning = False
                self.carrryingunit = 0

        # SI LA UNIDAD ES MAS GRANDE DE 1
        #UNIT IS BIGGER THAN ONE SO IT HAS UNIT AND ITS GOING TO RETURN
        elif self.hasunit == True and self.isreturning == True:
            #EXAMPLE 2 UNITSLEFT WOULD HAVE TO GO FIRST TO SPACESHIP, ONCE COLLIDED WITH SPACESHIP, GO TO UNITX AND UNITY AND THEN TO SPACESHIP AGAIN
            if unitsize > 0:
                if self.rect.x > spaceship_x:
                    dx -= 1
                else:
                    dx += 1
                if (self.rect.y < spaceship_y):
                    dy += 1
                else:
                    dy -= 1
                if self.rect.x == spaceship_x and self.rect.y == spaceship_y:
                    if (self.rect.x > unitx):
                        dx -= 1
                    else:
                        dx += 1
                    if (self.rect.y < unity):
                        dy += 1
                    else:
                        dy -= 1

                    if pygame.sprite.spritecollide(self, unit_group, False):
                        if (self.rect.x > spaceship_x):
                            dx -= 1
                        else:
                            dx += 1
                        if (self.rect.y < spaceship_y):
                            dy += 1
                        else:
                            dy -= 1

                        unitsize -= 1
                    else:
                        if (self.rect.x > unitx):
                            dx -= 1
                        else:
                            dx += 1
                        if (self.rect.y < unity):
                            dy += 1
                        else:
                            dy -= 1

            else:
                self.isreturning = False
                self.hasunit = False





                # UNA VEZ TERMINADO EL FOR SE QUEDA LIBRE
           # self.hasunit = False
            #self.isreturning = False
            #self.carrryingunit = 0

            # #MIENTRAS QUE LAS UNIDADES RESTANTES SEAN MAYORES O IGUALES AL NUMERO DE VUELTAS 

            # while self.unitsleft > self.nturns:
            #     #BUSCARA LA NAVE 
            #     if(self.rect.x > spaceship_x):
            #         dx -= 5
            #     else:
            #         dx += 5
            #     if(self.rect.y < spaceship_y):
            #         dy += 5
            #     else:
            #         dy -= 5
            #     #UNA VEZ HECHA COLISION CON LA NAVE 
            #     if pygame.sprite.spritecollide(self, spaceship_group, False):
            #         score += 1 
            #         spaceship_units += 1
            #         self.carrryingunit = 0
            #         self.nturns += 1
            #         #BUSCARA LA UNIDAD    
            #         if(self.rect.x > unitx):
            #             dx -= 10
            #         else:
            #             dx += 10
            #         if(self.rect.y < unity):
            #             dy += 10
            #         else:
            #             dy -= 10
            #         if pygame.sprite.spritecollide(self,unit_group,False):
            #           self.carrryingunit +=1
            #     self.hasunit = False
            #     self.isreturning = False

            # else:
            #     self.hasunit = False
            #     self.isreturning = False

        # elif self.hasunit == False and self.isreturning == True:

        #     if(self.rect.x > unitx):
        #      dx -= 10
        #     else:
        #      dx += 10
        #     if(self.rect.y < unity):
        #      dy += 10
        #     else:
        #      dy -= 10
        #     if pygame.sprite.spritecollide(self, unit_group, False):
        #         self.carrryingunit += self.unitsleft
        #         self.hasunit = True
        #         self.isreturning = True 

        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy
        # print(selec)
        # print(self.rect.x)
        # print(self.rect.y)
        # print(self.carrryingunit, self.rect.x,
        #           self.rect.y, unitsize, unitx, unity, self.unitsleft, self.hasunit, self.isreturning)
        print(self.rect.x, self.rect.y, unitx, unity, self.hasunit, self.isreturning, self.carrryingunit,
              self.unitsleft)


        # draw player onto screens
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect,
                         2)  # draw margin of box for player
        draw_text('carrying X' + str(self.carrryingunit),
                  font_score, white, tile_size + 700, 400)


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = spaceship_img
        self.image = pygame.transform.scale(
            img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        # self.rect.center = (x, y)
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)
        # x = 285
        # y = 315


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

        # load images
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
                    img = pygame.transform.scale(stone, (tile_size, tile_size))
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
            # draw rectangles for nubmer 1
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 7, 0, 0, 0, 0, 0, 2, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 7, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 5, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Create player (spawn player)
unit_group = pygame.sprite.Group()
spaceship_group = pygame.sprite.Group()
score_coin = Unit(700, 200)
unit_group.add(score_coin)
# spaceship = Spaceship(285, 315)  # Coordenadas x y predeterminadas en lista
player1 = Player(285, 315)
# player2 = Player(100, screen_height - 100)
# player3 = Player(100, screen_height - 800)
reactive_button = Button(400, 500, reactive_img)
collaborative_button = Button(600, 500, collaborative_img)
exit_button = Button(800, 500, exit_img)
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

        spaceship_group.draw(screen)
        unit_group.draw(screen)
        stop = player1.update(stop)
        draw_text('carrying X' + str(player1.carrryingunit),
                  font_score, white, tile_size + 700, 400)
        draw_text('units' + str(spaceship_units),
                  font_score, white, tile_size + 700, 500)

    elif reactive == True:
        world.draw()
        spaceship_group.draw(screen)
        unit_group.draw(screen)
        player1.updatee()
        draw_text('carrying X' + str(player1.carrryingunit),
                  font_score, white, tile_size + 700, 400)
        draw_text('units' + str(spaceship_units),
                  font_score, white, tile_size + 700, 500)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
