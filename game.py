import pygame
import glob



map ="""                             
                             
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                      S                         w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
w                                                w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"""




def init_display():
    global screen, tile, spaceship
    screen = pygame.display.set_mode((800, 440))
    #462, 256 normal
    tile = pygame.image.load("C:\\Users\\alexd\\Documents\\Python\\Mars\\imgs\\wall.png")
    spaceship = pygame.image.load("C:\\Users\\alexd\\Documents\\Python\\Mars\\imgs\\spaceship.png")
    
class Robot():
    def __init__(self, x, y):
        img = pygame.image.load("C:\\Users\\alexd\\Documents\\Python\\Mars\\imgs\\robot.png")
        self.image = pygame.transform.scale(img, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
    
def tiles(map):
    global tile
    for y, line in enumerate(map):
        for x, c in enumerate(line):
            if c == "w":
                screen.blit(tile, (x * 16, y * 16))
            if c == "S":
                screen.blit(spaceship,(x*16, y *16))


map = map.splitlines()
pygame.init()
init_display()
loop = 1
while loop:

    #screen.fill((0, 0, 0))
    tiles(map)
    for event in pygame.event.get():
        if event.type == quit:
            loop = 0

    pygame.display.update()
pygame.quit()
