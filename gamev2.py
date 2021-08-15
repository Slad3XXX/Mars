import random
import pygame
import os
import sys
from pygame.locals import *


# Pendientes
# FUNCIONA PERO TENEMOS UN PEQUE;O ERROR AL MOMENTO DE IR DE REGRESO A LA UNIDAD
# SI DA TIEMPO IMPLEMENTAR EL GAMEOVER Y MUSICA EN UPDATEEE
#REEMPLAZAR STOP A GAME_OVER


# Para comprobar el fin dle juego implementar: https://www.youtube.com/watch?v=G8VsEbVS3F8&list=PLjcN1EyupaQnHM1I9SmiXfbT6aG4ezUvu&index=6&ab_channel=CodingWithRuss
# Ordernar codigo
# musica https://www.youtube.com/watch?v=0HxZn6CzOIo&ab_channel=AdhesiveWombat


# dudas



pygame.init()

# Clock
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
        self.isalone = False



    def update(self, stop):


        #NEED TO MAKE ROBOTS MOVE RANDOMLY AND IF ONE FOUNDS A UNIT BIGGER THAN 1, ROBOT HAS TO WAIT FOR OTHER 2 ROBOTS AND IF ONE IS FREE, ONE SHOULD COME TO HELP THE ONE IS WAITNING AND THEN TOGETHER GRAB THE UNIT AND GO TO ROCKET
        #MOVEMENT SHOULD ME RANDOM (ABOVE CODED)
        #UNITSIZE SHOULD BE RANDOM BETWEEN 1 UP TO 4 MAX
        # IF ALL THE ROBOTS ARE BUSY AND NO OTHER CAN HELP HE HAS TO DELIVER UNIT ONE BY ONE
        # ONCE 20 SPACESHIP UNITS IS REACHED GAME WILL BE OVER
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
                key = pygame.key.get_pressed()
                #---------------------------------------- MOVEMENT SHOULD BE AUTOMATIC BUT KEYS HELP SO WE CAN FASTEN THE PROCESS OF CODING, ONCE FINISHED THIS WILL BE DELETED
                if key[pygame.K_w]:
                    dy -= 5
                elif key[pygame.K_a]:
                    dx -= 5
                elif key[pygame.K_s]:
                    dy += 5
                elif key[pygame.K_d]:
                    dx += 5
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



                    # ------------------------------------- HARDCOIDNG UNITSIZE FOR CODING PURPOSES, AFTER COMPLETED THIS WILL BE DELETED
                unitsize = 2



                if self.iswaiting:
                    action = 5
                elif self.isalone == True:
                    action = 3



                #------------------------------------ IS GOING TO HELP
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
                    # If player collides with unit
                    if pygame.sprite.spritecollide(self, unit_group, True):
                        # ------------------------------------GET X AND Y UNIT COORDINATES
                        unitx = self.rect.x
                        unity = self.rect.y
                        # SI LA UNIDAD ES UNA
                        if unitsize == 1:
                            self.unitsleft = 1
                            self.hasunit = True


                        # -------------------------------- IF UNIT IS BIGGER THAN ONE
                        elif unitsize > 1:
                            self.unitsleft = unitsize
                            # self.hasunit = True
                            # self.isreturning = True
                            self.iswaiting = True

                    else:
                        action = 0




                #________________________________ RANDOM MOVEMENT
                if action == 0:
                    if selec == 1 and self.rect.y < 488:
                        dy += 2
                    elif selec == 2 and self.rect.y > 30:
                        dy -= 2
                    elif selec == 3 and self.rect.x < 540:
                        dx += 2
                    elif selec == 4 and self.rect.x > 24:
                        dx -= 2
                #------------------------------------ GOING TOWARDS UNIT
                elif action == 1:
                    if self.rect.x > unitx:
                        dx -= 2
                    else:
                        dx += 2
                    if self.rect.y < unity:
                        dy += 2
                    else:
                        dy -= 2
                #----------------------------------- GOING TOWARDS SPACESHIP
                elif action == 2:
                    if self.rect.x > spaceship_x:
                        dx -= 2
                    else:
                        dx += 2
                    if self.rect.y < spaceship_y:
                        dy += 2
                    else:
                        dy -= 2
                #---------------------------------- ACTION TO TAKE IF NO PLAYER IS AVAILABLE (NOT IMPLEMENTED YET)
                elif action == 3:
                    self.carrryingunit = 1
                    if self.rect.x > spaceship_x:
                        dx -= 2
                    else:
                        dx += 2
                    if self.rect.y < spaceship_y:
                        dy += 2
                    else:
                        dy -= 2
                    if pygame.sprite.spritecollide(self, spaceship_group, False):
                        spaceship_units += self.carrryingunit
                        self.carrryingunit = 0



                #---------------------------------- EXTRA SPACE IF NEEDED FOR ANYTHING ELSE
                elif action == 4:
                    print("se esta haciendo")


                #----------------------------------- WAITING FOR OTHER PLAYER TO COME IF FREE
                elif action == 5:
                    dx = 0
                    dy = 0



                    
                #------------------------------------ UPDATE PLAYER COORDINATES
                self.rect.x += dx
                self.rect.y += dy
                self.poshistory = [self.rect.x, self.rect.y]
                # print(stop, self.carrryingunit, self.rect.x,
                #   self.rect.y, self.poshistory, action)


                 #-------------------------------------- DRAW PLAYER ONTO SCREEN
                screen.blit(self.image, self.rect)
                #--------------------------------------- DRAW MARGIN OF PLAYER
                pygame.draw.rect(screen, (255, 255, 255), self.rect,
                             2)
                draw_text('SCORE X' + str(spaceship_units),
                  font_score, white, tile_size + 600, 300,)
                return stop



    def updatee(self):
        selec = random.randint(1, 4)
        unitsize = random.randint(1, 4)
        dx = 0
        dy = 0
        global spaceship_units
        global score
        score = spaceship_units
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
            dx += 5
        if selec == 1 and self.rect.y < 488:
            dy += 2
        elif selec == 2 and self.rect.y > 30:
            dy -= 2
        elif selec == 3 and self.rect.x < 540:
            dx += 2
        elif selec == 4 and self.rect.x > 24:
            dx -= 2

        # ------------------------------------------------------CHECK FOR COLLISION WITH WALLS
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0
        # Check for player collision with unit

        #unitsize = 3

        # ---------------------------------------Robot is free for navigating
        if self.hasunit == False and self.isreturning == False:
            # If player collides with unit
            if pygame.sprite.spritecollide(self, unit_group, False):
                # ------------------------------------GET X AND Y UNIT COORDINATES
                unitx = self.rect.x
                unity = self.rect.y
                # SI LA UNIDAD ES UNA
                if unitsize == 1:
                    self.unitsleft = unitsize
                    self.hasunit = True
                    self.isreturning = False

                #-------------------------------- IF UNIT IS BIGGER THAN ONE
                elif unitsize > 1:
                    self.unitsleft = unitsize
                    self.hasunit = True
                    self.isreturning = True

        # ----------------------------------------ONLY ONE UNIT
        elif self.hasunit == True and self.isreturning == False:

            # BUSCA COORDENADAS DE LA NAVE
            if self.rect.x > spaceship_x:
                dx -= 2
            else:
                dx += 2
            if self.rect.y < spaceship_y:
                dy += 2
            else:
                dy -= 2
            # UNA VEZ ENCONTRADA Y HECHO COLISION CON LA NAVE NO TENDRA UNIDADES POR LO QUE VOLVERA A FALSE FALSE Y NO ESTARA CARGANDO U'S
            if pygame.sprite.spritecollide(self, spaceship_group, False):

                spaceship_units += 1
                self.hasunit = False
                self.isreturning = True
                self.unitsleft = 5


      #---------------------------------------------------------------UNIT BIGGER THAN ONE

        elif self.hasunit == True and self.isreturning == True:
            #
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

        #-------------------------------------------------------------- RETURN TO UNIT (IF ONE UNIT, RETURN TO IT TO DELTE IT AND KEEP GOING)
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

            #------------------------- COLISSION IN X
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx *= -4
                dy *= -4
            # ------------------ COLLISION IN Y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy *= -4
                dx *= -4




        # -----------------------------------------------------------------update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # draw player onto screens
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect,
                         #2)  # draw margin of box for player
        print(self.rect.x, self.rect.y)
        draw_text('SCORE X' + str(spaceship_units), font_score, white, tile_size + 600, 100)


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
                    img = pygame.transform.scale(stone, (tile_size//2, tile_size//2))
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
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [1, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1 ],
    [1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1 ],
    [1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 5, 0, 0, 0, 0, 5, 7, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [1, 0, 0, 7, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1 ],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [1, 0, 7, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 5, 7, 0, 0, 0, 1 ],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 5, 0, 0, 1 ],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Create player (spawn player)
unit_group = pygame.sprite.Group()
spaceship_group = pygame.sprite.Group()
# spaceship = Spaceship(285, 315)  # Coordenadas x y predeterminadas en lista
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


            ##########------------------------------------ TRYING TO CHECK IF ONE PLAYER IS FREE AND OTHER WAITING AND DO SOMETHING (HASNT BEEN COMPLETED YET, ITS JUST AN IDEA)


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
                    player2.rect.y  -= 1

            if player2.iswaiting and player1.canhelp:
                if player1.rect.x > player2.rect.x:
                    player1.rect.x -= 1
                else:
                    player1.rect.x += 1

                if player1.rect.y < player2.rect.y:
                    player1.rect.y += 1
                else:
                    player1.rect.y  -= 1

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

                if player1.iswaiting == True and player2.canpickup == False and player3.iswaiting == True:
                    player3.isalone = True
                    player3.iswaiting = False
















            # print (player1.rect.x, player1.rect.y, player2.rect.x, player2.rect.y)
            print(player1.iswaiting, player1.canpickup,player2.iswaiting, player2.canpickup, player3.isalone, player3.unitsleft)

            stop = player1.update(stop)
            stop = player2.update(stop)
            stop = player3.update(stop)







        else:
            draw_text("GAME OVER",font_score, white, 600, 300)





    elif reactive == True:
        world.draw()
        spaceship_group.draw(screen)
        unit_group.draw(screen)
        player1.updatee()
        #player2.updatee()
        #player3.updatee()
        if spaceship_units >= 20:
            run = False




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
