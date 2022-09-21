from pickle import FALSE
from setup import *
from player import *
from spike import *
from ground import *
from gun import * 

class Runner:
    home_color = (50,50,50)
    
    
    def __init__(self, s_width, s_height):
        self.dead = False
        self.home = True
        self.pressing = False
        
        self.time_diff = 0
        self.score = 0
        self.high_score = 0
        self.et = 0
        
        #create player and ground
        self.Gmanager = GroundManager()
        self.lava = pygame.Rect(0, 680, s_width, s_height - 680)
        self.lava2 = pygame.Rect(0, 690, s_width, s_height - 690)
        self.player = Player(s_width/2, s_height/2)
        self.gun = Gun(self.player.d.x + self.player.width/2, self.player.d.y + self.player.height/2, "shotgun")
        self.Smanager = SpikeManager(s_width, self.score)

        self.menupos = pygame.Vector2(0, s_height + 3)
        self.menuvelo = pygame.Vector2(0, 0)
        self.menuaccel = pygame.Vector2(0, -0.0012)
        self.menu = pygame.Rect(self.menupos.x, self.menupos.y, s_width, s_height)
        self.image = pygame.transform.scale(pygame.image.load("assets/dark.png"), (s_width, s_height)).convert()

        self.font = pygame.font.Font('fonts/SourceSansPro-Bold.ttf', 180)
        self.font2 = pygame.font.Font('fonts/SourceSansPro-Regular.ttf', 60)
        self.font3 = pygame.font.Font('fonts/SourceSansPro-Light.ttf', 42)

    def home_screen(self, screen, width, height, dt):
        pygame.draw.rect(screen, self.home_color, pygame.Rect(0,0, width, height))
        msg = self.font.render("Press Space to Play", True, (0,0,0))

    def death_screen_animation(self, dt):
        self.menupos += self.menuvelo * dt
        self.menuvelo += self.menuaccel * dt
        if self.menupos.y < 0:
            self.menupos.y = 0

        self.menu.x = self.menupos.x
        self.menu.y = self.menupos.y
    

    def update(self, s_width, s_height, dt):
        self.dead, add = self.player.check_collision(self.Gmanager.tiles, self.Smanager.spikes, s_width, self.dead, dt) #check player collision

        if add > 0 and self.gun.ammo < self.gun.max_ammo:
            self.gun.reload(add)
        
        tt = int(pygame.time.get_ticks()/1000)
        self.ingamescore = self.font.render(str(self.score), True, (255,255,255))
        self.roundscore = self.font2.render('Score: %s' %(self.score), True, (255,255,255))
        self.ammo_count = self.font3.render(str(self.gun.ammo), True, (0,0,0))

        self.display_img = self.gun.display

        if not self.dead:
            self.score = tt - self.time_diff
            self.Smanager.update(self.Gmanager.tiles, dt, self.score)
            self.Gmanager.update(dt, s_width, self.score) #update ground tiles
        else:
            if self.score > self.high_score:
                self.high_score = self.score
                
            self.hiscore = self.font2.render('High Score: %s' %(self.high_score), True, (255,255,255))
                                                                
            self.Smanager.amount = 5
            if self.menupos.y != 0:
                self.death_screen_animation(dt)
            self.Smanager.clear()
        
        pressed = pygame.key.get_pressed()
        if (pressed[pygame.K_LEFT] or pressed[K_a]) and not self.player.movingR and not self.dead: #player right input
            self.player.move_left()
            self.player.movingL = True
        else:
            self.player.movingL = False
            
        if (pressed[pygame.K_RIGHT] or pressed[K_d]) and not self.player.movingL and not self.dead: #player left input
            self.player.move_right() 
            self.player.movingR = True
        else:
            self.player.movingR = False
            
        if (pressed[pygame.K_UP] or pressed[K_w] or pressed[K_SPACE]) and self.player.grounded and not self.player.crouching and not self.dead and self.score > 0: #jumping input
            self.player.jump()
            self.player.crouching = False

        if not self.dead and pygame.mouse.get_pressed()[0] and self.et == 0 and self.gun.b.y < Ground.level and self.gun.ammo > 0 and not self.pressing:
            self.gun.shooting = True
            self.gun.flashing = True
            self.pressing = True
            self.et = self.gun.firerate
        elif self.et < self.gun.firerate:
            if self.et < self.gun.firerate - 2:
                self.gun.flashing = False
            self.gun.shooting = False

        if not pygame.mouse.get_pressed()[0] and not pressed[K_SPACE]:
            self.pressing = False

        if self.menupos.y == 0 and (pressed[K_SPACE] or pygame.mouse.get_pressed()[0]):
            self.dead = False
            self.et = 17
            self.Gmanager.clear()
            self.time_diff = tt
            self.player.a.y = self.player.gravity
            self.player.kill()
            self.gun.ammo = self.gun.max_ammo
            self.menupos.y = s_height + 3
            self.menuvelo.y = 0
            self.menu.y = self.menupos.y
            
        if (pressed[pygame.K_DOWN] or pressed[K_s] or pressed[K_LSHIFT]) and not self.dead:# and self.player.grounded: #crouching input
            self.player.crouching = True
        else:
            self.player.crouching = False

        
        self.player.update(dt)
        self.gun.update(self.player.d.x + self.player.width/2, self.player.d.y + self.player.height/2, self.dead, s_width, s_height, dt)

        if self.et > 0:
            self.et -= 1

    def draw(self, screen, s_width, s_height):
        
        if not self.dead:
            screen.blit(self.ingamescore,(s_width/2 - self.ingamescore.get_width()/2, s_height/2 - self.ingamescore.get_height()/2))     
           
        pygame.draw.rect(screen, (173, 55, 9), self.lava) #lava
        
        #draw player and ground to screen  
        self.player.draw(screen, self.dead)

        pygame.draw.rect(screen, (173, 55, 9), self.lava2) #lava2 
        self.Smanager.draw(screen)
        self.Gmanager.draw(screen, s_width)
        
        self.gun.draw(screen)
        
        screen.blit(self.ammo_count, (s_width - self.ammo_count.get_width() - 30, 8))

        screen.blit(self.display_img, (s_width - self.ammo_count.get_width() - 43 - self.display_img.get_width(), 12 + self.ammo_count.get_height()/2 - self.display_img.get_height()/2))
            
        if self.dead:
            screen.blit(self.image, (self.menupos))
            screen.blit(self.roundscore, ((self.menupos.x + self.menu.width)/2 - self.roundscore.get_width()/2, (self.menupos.y + self.menu.height)/2 + self.roundscore.get_height()/2))
            screen.blit(self.hiscore, ((self.menupos.x + self.menu.width)/2 - self.hiscore.get_width()/2, (self.menupos.y + self.menu.height)/2 - self.hiscore.get_height() - 0))
