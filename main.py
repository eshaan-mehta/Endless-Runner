from setup import * 
from ground import *
from spike import *
from player import *
from game import *

#flags = FULLSCREEN | DOUBLEBUF
#screen = pygame.display.set_mode((s_width, s_height), flags, 16)
screen = pygame.display.set_mode((s_width, s_height))

isRunning = True

game = Runner(s_width, s_height)

pt = pygame.time.get_ticks()
pygame.mouse.set_pos(s_width/2, s_height/2)

while isRunning:
    #delta time calculation
    #print(game.player.d.y)
    ct = pygame.time.get_ticks()
    dt = ct - pt
    pt = ct

    screen.fill((129,203,248)) #background
    

    #update and draw game to screen
    game.update(s_width, s_height, dt)
    game.draw(screen, s_width, s_height)

    if not game.dead:
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        crosshair = pygame.image.load("assets/crosshair.png").convert_alpha()
        screen.blit(crosshair, (pygame.mouse.get_pos()[0] - crosshair.get_width()/2, pygame.mouse.get_pos()[1] - crosshair.get_height()/2))
    else:
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)    
    
    #check to see if manually exited out of window
    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
                isRunning = False
        

    pygame.display.update() #update display
    
pygame.quit() #quit 
