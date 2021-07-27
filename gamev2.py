import random
import pygame
from pygame.locals import *



#Pendientes
#agregar nave como sprite para permitir colisiones y hacer respectivo if para que se depositen unidades
#hacer que el jugador vaya creadndo el mapa en el que pasa 
#pasar esa inmformaciaon a traves de los demas jugadores
# ayudar a un jugador si la unidad pesa mas de 2 unidades y la lleven entre ellos 
# NOTA: podria funcionar que en cuanto encuentren la nave comiejncen a hacer el aprendizaje de el mapa y asi comunicaarse ***Preguntar al profe si tienen que salir de la nave forzosamente

# aniadir valores a unidad y posteriormetente agregarlos en el juego
# Para comprobar el fin dle juego implementar: https://www.youtube.com/watch?v=G8VsEbVS3F8&list=PLjcN1EyupaQnHM1I9SmiXfbT6aG4ezUvu&index=6&ab_channel=CodingWithRuss 
#Ordernar codigo
#musica https://www.youtube.com/watch?v=0HxZn6CzOIo&ab_channel=AdhesiveWombat


#dudas
# que paseria si en el camino a la nave se encuentra otra unidad 
# que pasaria si todos los jugadores se encuetnran con una una unidad mayor de 2 








pygame.init()

#Clock 
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
# x = 285
# y = 315

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mars')

# define game variables
tile_size = 30


# load images
# sun_img = pygame.image.load('imgs/robot.png')
bg = pygame.image.load('C:\\Users\\alexd\\Documents\\GitHub\\Mars\\imgs\\background.png')
bg_img =pygame.transform.scale(bg, (1000, 600))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    img.set_alpha(127)
    screen.blit(img, (x, y)) 
 

class Player():
    def __init__(self, x, y):
       
        img = pygame.image.load("C:\\Users\\alexd\\Documents\\GitHub\\Mars\\imgs\\robot.png")
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hasunit = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.carrryingunit = 0
        # self.speed = 0
        
    def update(self, stop):
        selec = random.randint(1,4)
        unitsize = random.randint(1,4)
        dx = 0
        dy = 0
        global spaceship_units
        global score
        if stop == 1:
            selec = random.randint(1,4)
            dx = 0
            dy = 0
            clock.tick(fps) #Speed of update 
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
                if selec == 1 and self.rect.y < 488: #limites (ya no se deberia de salir con funcion  de abajo, pero manteniendo)
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
            
                #check for collisions
                for tile in world.tile_list:
                    if tile[1].colliderect(self.rect.x +dx, self.rect.y, self.width, self.height):
                        dx = 0
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        dy = 0
                #Check for player collision with unit
                unitsize = 1
                if self.hasunit == False:
                    if pygame.sprite.spritecollide(self, unit_group, True):  #If player collides with unit 
                        if unitsize < 2:
                            self.carrryingunit += unitsize
                            self.hasunit = True
                            stop = 1
                        else:
                            self.carrryingunit += unitsize
                            self.hasunit = True
                            stop = 0
                else:
                    if(self.rect.x > spaceship_x):
                        dx -= 1
                    else:
                        dx +=1
                    if(self.rect.y < spaceship_y):
                        dy += 1
                    else:
                        dy -=1
                    if pygame.sprite.spritecollide(self, spaceship_group, False): #implementar para los otros jugadores 
                        score += self.carrryingunit
                        spaceship_units += self.carrryingunit
                        self.hasunit = False
                        self.carrryingunit = 0
                        
                        
                        
                
                        
                    
            # update player coordinates
                self.rect.x += dx
                self.rect.y += dy
            # print(selec)
            # print(self.rect.x)
            # print(self.rect.y)
            print (stop,self.carrryingunit,self.rect.x, self.rect.y)
            

            # draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen,(255,255,255),self.rect,2) #draw margin of box for player
        draw_text('carrying X' + str(self.carrryingunit), font_score, white, tile_size + 700, 400)
        return stop

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('C:\\Users\\alexd\\Documents\\GitHub\\Mars\\imgs\\spaceship.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        # self.rect.center = (x, y)
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image,self.rect)
        # x = 285
        # y = 315
       
        
        


class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('C:\\Users\\alexd\\Documents\\GitHub\\Mars\\imgs\\unit.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        

class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        wall = pygame.image.load("C:\\Users\\alexd\\Documents\\GitHub\\Mars\\imgs\\wall.png")
        spaceship = pygame.image.load("C:\\Users\\alexd\\Documents\\GitHub\\Mars\\imgs\\spaceship.png")
        stone = pygame.image.load('C:\\Users\\alexd\\Documents\\GitHub\\Mars\\imgs\\stone.png')

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
                    spaceship = Spaceship(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    spaceship_group.add(spaceship)
                if tile == 5:
                    img = pygame.transform.scale(stone, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 7:
                    unit = Unit(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    unit_group.add(unit)
                
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen,(255,255,255),tile[1], 2) #draw rectangles for nubmer 1 



           
            
           


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1,1,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 7, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1,1,1]
]

#Create player (spawn player)
unit_group = pygame.sprite.Group()
spaceship_group = pygame.sprite.Group()
score_coin = Unit(700, 200)
unit_group.add(score_coin)
spaceship = Spaceship(285,315) #Coordenadas x y predeterminadas en lista 
player1 = Player(100, screen_height - 500)
# player2 = Player(100, screen_height - 100)
# player3 = Player(100, screen_height - 800)
world = World(world_data)

run = True
while run:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))
    world.draw()
    
    spaceship_group.draw(screen)
    unit_group.draw(screen)
    stop = player1.update(stop)
    draw_text('carrying X' + str(player1.carrryingunit), font_score, white, tile_size + 700, 400)
    draw_text('units' +str(spaceship_units), font_score, white, tile_size + 700, 500)
    # print (player1.rect.x, player1.rect.y, selec)
    # if pygame.sprite.spritecollide(player1, unit_group, True):  #If player collides with unit 
    #     if selec > 1:
    #         player1.carrryingunit += selec
    #         player1.dx = 0
    #         player1.dy = 0
    #         # player1.rect.x = player1.rect.x
    #         # player1.rect.y = player1.rect.y
    #         player1.hasunit = True
    # draw_text('Player 1 carrying X ' + str(player1.carrryingunit), font_score, white, tile_size + 700, 400) #que se reinicie cuando esta en la nave y seguir con player 2 
    #Fatla agregar cuando valdara cada unidad  de 1 a 4 unidades
    #Idea1 : que chouqe, se pare su velocidad dx y dy y despues de eso obtenga cordenadas y llegue otro dude
    #Nota: tienen que ir a la nave al tener la unidad
    # if pygame.sprite.spritecollide(player1, unit_group, True):  #If player collides with unit 
    #     score += 1
    #     player1.carrryingunit += 1
    #     player1.hasunit = True
    # draw_text(' Player1 carrying X ' + str(player1.carrryingunit), font_score, white, tile_size + 700, 400) #que se reinicie cuando esta en la nave y seguir con player 2 
    
    # if player1.hasunit == True:
    #     player1.rect.x 
        
    
    
    # if pygame.sprite.spritecollide(player2, unit_group, True):  #If player collides with unit 
    #     score += 1
    #     player2.carrryingunit += 1
    #     player2.hasunit = True
    # draw_text(' Player1 carrying X ' + str(score), font_score, white, tile_size + 600, 400)
    # if pygame.sprite.spritecollide(player3, unit_group, True):  #If player collides with unit 
    #     score += 1
    #     player3.carrryingunit += 1
    #     player3.hasunit = True
    # draw_text(' Player1 carrying X ' + str(score), font_score, white, tile_size + 600, 400)
    # draw_text(s, font_score,white, tile_size + 900, 900)
    
    
    # if pygame.sprite.spritecollide(player1, spaceship_group, False): #implementar para los otros jugadores 
        
    #     spunits += self.carrryingunit
    #     self.hasunit = False
    #     self.carrryingunit = 0
    # # draw_text('Spaceship units' +str(spunits), font_score, white, tile_size + 700, 500)
  
    # player1.update()
    # player2.update()
    # player3.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
