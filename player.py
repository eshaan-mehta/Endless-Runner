from setup import *
from ground import *
from spike import *
from gun import * 

class Player:
    width, height = 25, 60
    color = (66, 28, 2)
    gravity = 0.0015
    acceleration = 0.002
    jump_power = 0.65
    resistance = 0.005
    movingL = False
    movingR = False
    grounded = False
    jumping = False
    crouching = False
    prev = False
    
    def __init__(self, x, y):
        self.d = pygame.Vector2(x, y)
        self.v = pygame.Vector2(0, 0)
        self.a = pygame.Vector2(0, self.gravity)
        self.r = pygame.Rect(self.d.x, self.d.y, self.width, self.height)

    def kill(self):
        #self.crouching = False
        
        if self.d.y + self.height < Ground.level + Ground.grassH:
            self.__init__(self.d.x, self.d.y)
        else:
            self.__init__(self.d.x, Ground.level - self.height - 2)
    def jump(self):
        #if jumping, then make the velocity = jump power
        self.v.y = -self.jump_power

    def crouch(self):
        self.height = 30
        self.r.height = 30
        self.acceleration = 0.002/3
        #self.d.y -= 30

    def move_right(self):
        #icrease acceleration on right movement
        self.a.x += self.acceleration

    def move_left(self):
        #decrease acceleration on left movement
        self.a.x -= self.acceleration

    def check_collision(self, tiles, spikes, s_width, dead, dt):
        ey = abs(self.v.y) * dt #epsilon is the margin of error for vertical collision detection
        ex = abs(self.v.x) * dt
        
        player_left = self.d.x
        player_right = self.d.x + self.width
        
        if self.d.x < 0: #to prevent player going off left side of screen
            self.d.x = 0
            self.v.x = 0
        if self.d.x + self.width > s_width: #to prevent player going off right side of screen
            self.d.x = s_width - self.width
            self.v.x = 0
        if self.d.y > s_height: #to prevent player from going off bottom of screen
            self.v = pygame.Vector2(0, 0)
            self.a = pygame.Vector2(0, 0)
        
        if abs((self.d.y + self.height) - (s_height - 20)) < ey: #if player falls in lava, kill them
            dead = True
            
        #to check collision for each tile
        for tile in tiles:
            tile_left = tile.d.x
            tile_right = tile.d.x + tile.width
            if player_left < tile_right and player_right > tile_left: #allow player to be half off the tile and still collide
                if abs((self.d.y + self.height) - tile.d.y) < ey: #to check if on top of tile
                    self.d.y = tile.d.y - self.height
                    self.grounded = True #grounded controls abilty to jump
                else:
                    self.grounded = False
                    
            if self.d.y + self.height > tile.d.y + Ground.grassH + Ground.dirtH/4: #if player is below the tile surface (ie. falling into lava), to prevent player from going inside the ground tile
                if abs(player_left - tile_right) < ex or abs(player_right - tile_left) < ex:
                    self.v.x = 0

        if self.grounded and not self.jumping: #if player is grounded and not currently jumping, (ie. standing on ground), set vertical velocity to zero
            self.v.y = 0

        add = 0
        for spike in spikes:
            if self.r.colliderect(spike.r):
                if spike.type == "spike":
                    dead = True
                    self.v = pygame.Vector2(0, 0)
                    self.a = pygame.Vector2(0, 0)
                else:
                    add = 1
                    SpikeManager.delete(SpikeManager, spike)
                    

        return dead, add
        
    def update(self, dt):
        self.d += self.v * dt
        self.r.x = self.d.x
        self.r.y = self.d.y
        self.v += self.a * dt
        self.v.x *= max(0, 1 - (dt * self.resistance))

        #print(self.r.topleft)

        #to see if player is currently jumping
        if self.v.y < 0: 
            self.jumping = True
        else:
            self.jumping = False

        #reset horizontal acceleration and grouded state
        self.a.x = 0
        self.grounded = False
        
        if self.crouching:
            if not self.prev:
                self.d.y += 30
            self.crouch()
        else:
            self.height = 60
            self.r.height = 60
            self.acceleration = 0.002
            if self.prev:
                self.d.y -= 30
        self.prev = self.crouching



    def draw(self, screen, dead):
        #draw player

        #if dead:
            #pygame.draw.rect(screen, (255,255,255), pygame.Rect(self.d.x - 2, self.d.y - 2, self.width + 4, self.height + 4))
        
        pygame.draw.rect(screen, self.color, self.r)

