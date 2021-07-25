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












pygame.init()

#Clock 
clock = pygame.time.Clock()
fps = 60
score = 0
spunits = 0
font_score = pygame.font.SysFont('Bauhaus 93', 30)
white = (0, 0, 0)
screen_width = 1000
screen_height = 1000

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
        
    def update(self):
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
           
            if selec == 1 and self.rect.y < 488: #limites
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
        
        # if(Player.hasunit == True):
        #     dx = 0
        #     dy = 0
        #     for dx in range(285):
                
                
            
                 
                    
                
        

            # update player coordinates
        self.rect.x += dx
        self.rect.y += dy
        # print(selec)
        print(self.rect.x)
        print(self.rect.y)

        # draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen,(255,255,255),self.rect,2) #draw margin of box for player

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
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1,1,1]
]


#Create random locations for units
# xlist = []
# ylist = []
# unitlist = []
# for i in range(20):
#     x = random.randint(24,534)
#     y = random.randint(30,488)
#     xlist.append(x)
#     ylist.append(y)
# unit1 = Unit(xlist[0],ylist[0])
# unit2 = Unit(xlist[1],ylist[1])
# unit3 = Unit(xlist[2],ylist[2])
# unit4 = Unit(xlist[3],ylist[3])
# unit5 = Unit(xlist[4],ylist[4])
# unit6 = Unit(xlist[5],ylist[5])
# unit7 = Unit(xlist[6],ylist[6])
# unit8 = Unit(xlist[7],ylist[7])
# unit9 = Unit(xlist[8],ylist[8])
# unit10 = Unit(xlist[9],ylist[9])
# unit11 = Unit(xlist[10],ylist[10])
# unit12 = Unit(xlist[11],ylist[11])
# unit13 = Unit(xlist[12],ylist[12])
# unit14 = Unit(xlist[13],ylist[13])
# unit15 = Unit(xlist[14],ylist[14])
# unit16 = Unit(xlist[15],ylist[15])
# unit17 = Unit(xlist[16],ylist[16])
# unit18 = Unit(xlist[17],ylist[17])
# unit19 = Unit(xlist[18],ylist[18])
# unit20= Unit(xlist[19],ylist[19])
# unitlist.extend((unit1,unit2,unit3,unit4,unit5,unit6,unit7,unit8,unit9,unit10,unit11,unit12,unit13,unit14,unit15,unit16,unit17,unit18,unit19,unit20))

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
    # clock.tick(fps)

    screen.blit(bg_img, (0, 0))

    
    
    
    
    
    # for i in range(len(unitlist)):
    #     unitlist[i].draw()
        
  
    
    

    

    world.draw()
    #Fatla agregar cuando valdara cada unidad  de 1 a 4 unidades
    #Idea1 : que chouqe, se pare su velocidad dx y dy y despues de eso obtenga cordenadas y llegue otro dude
    #Nota: tienen que ir a la nave al tener la unidad
    if pygame.sprite.spritecollide(player1, unit_group, True):  #If player collides with unit 
        score += 1
        player1.carrryingunit += 1
        player1.hasunit = True
    draw_text(' Player1 carrying X ' + str(player1.carrryingunit), font_score, white, tile_size + 700, 400) #que se reinicie cuando esta en la nave y seguir con player 2 
    
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
    
    
    if pygame.sprite.spritecollide(player1, spaceship_group, False): #implementar para los otros jugadores 
        if player1.hasunit == True:
            spunits += player1.carrryingunit
            player1.hasunit = False
            player1.carrryingunit = 0
    draw_text('Spaceship units' +str(spunits), font_score, white, tile_size + 700, 500)
    
    
    spaceship_group.draw(screen)
    unit_group.draw(screen)
    
    # unit1.update()
    # unit2.update()
    # unit3.update()
    # unit4.update()
    # unit5.update()
    # unit6.update()
    # unit7.update()
    # unit8.update()
    # unit9.update()
    # unit10.update()
    # unit11.update()
    # unit12.update()
    # unit13.update()
    # unit14.update()
    # unit15.update()
    # unit16.update()
    # unit17.update()
    # unit18.update()
    # unit19.update()
    # unit20.update()
    
    player1.update()
    # player2.update()
    # player3.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
