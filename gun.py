from setup import *
from player import *
from spike import *
from ground import *


class Bullet:
    color = (0,0,0)
    width = 5
    factor = 5
    
    def __init__(self, start, direction):
        self.d = pygame.Vector2(start.x, start.y)
        self.r = pygame.Rect(start.x - self.width/2, start.y - self.width/2, self.width * self.factor, self.width * self.factor)
        self.v = pygame.Vector2(0.8, 0.8)
        self.a = pygame.Vector2(0.005, 0.005)
        self.dir = direction
        self.endpoint = pygame.Vector2(0,0)

    def check_collision(self, s_width, s_height, dt):    
        ex = abs(self.v.x) * dt
        ey = abs(self.v.y) * dt
        
        #screen border collision
        if self.r.right < 0 or self.r.left > s_width or self.r.bottom < 0 or self.r.top > s_height:
            return True

        for tile in GroundManager.tiles:
            tile_left = tile.d.x
            tile_right = tile.d.x + tile.width
            if self.r.left < tile_right and self.r.right > tile_left and self.r.bottom > Ground.level + Ground.grassH/2:
                return True

            if self.r.bottom > Ground.level + Ground.grassH/2 and (self.r.left < tile_right or self.r.right < tile_left):
                if abs(self.r.left - tile_right) < ex or abs(self.r.right > tile_left) < ex:
                    return True

        for spike in SpikeManager.spikes:
            right = self.d.x + self.r.width
            left = self.d.x
            top = self.d.y
            bottom = self.d.y + self.r.height

            sleft = spike.d.x
            sright = spike.d.x + spike.r.width
            stop = spike.d.y
            sbottom = spike.d.y + spike.r.height
            
            #if abs(right - sleft) < ex or abs(left - sright) < ex or abs(top - sbottom) < ey or abs(bottom - stop) < ey:
            if self.r.colliderect(spike.r):
                SpikeManager.delete(SpikeManager, spike)
                return True
            
        return False
        
    def update(self, dt):
        self.d.x += self.v.x * math.cos(math.radians(self.dir)) * dt
        self.d.y += -self.v.y * math.sin(math.radians(self.dir)) * dt
        self.v += self.a * dt

        self.r.center = self.d

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.d, self.width)
        #pygame.draw.rect(screen, (255,255,0), self.r)
        
        


class Gun:
    firerate = 30
    max_ammo = 8
    mflash = pygame.transform.scale(pygame.image.load("assets/guns/flash.png"), (44,24))
    shooting = False
    flashing = False
    bullets = []
    

    def __init__(self, x, y, gun):
        self.d = pygame.Vector2(x, y)
        self.dir = 0
        self.d2 = pygame.Vector2(self.d)
        
        self.b = pygame.Vector2(self.d2.x, self.d2.y) #barrel coordinate for where the bullet will shoot from

        #player gun model
        self.display = pygame.image.load("assets/guns/" + gun + "/model.png")
        self.image = self.display#pygame.transform.scale(self.display, (42, self.display.get_height()))
        self.hit = pygame.image.load("assets/guns/" + gun + "/hitbox.png")
        self.hit = pygame.transform.scale(self.hit, (42, self.hit.get_height()))
        self.dimensions = (self.hit.get_width(), self.hit.get_height()) #gun dimensions
        self.copy = self.image
        self.r = self.copy.get_rect()

        #muzzle flash
        self.mcopy = self.mflash 
        self.mr = self.mcopy.get_rect()
        
        self.offset = 0
        self.facing = ["right", "up"]
        self.ammo = self.max_ammo


    def fix_angle(self, angle):
        x = angle
        if x >= 360:
            x -= 360
        if x < 0:
            x += 360

        return x

    def shoot(self):
        self.ammo -= 1
        bullet = Bullet(self.b, self.dir)
        self.bullets.append(bullet)

    def reload(self, amount):
        self.ammo += amount

    def update(self, x, y, dead, s_width, s_height, dt):
        self.d.x = x
        self.d.y = y

        mx, my = pygame.mouse.get_pos()
        distance = math.dist((mx, my), self.d)

        if not dead:
            if mx < self.d.x:
                if self.facing[0] == "right":#only if facing right prev frame
                    self.image = pygame.transform.flip(self.image, False, True)
                    self.mflash = pygame.transform.flip(self.mflash, False, True)
                self.facing[0] = "left"
            else:
                if self.facing[0] == "left":
                    self.image = pygame.transform.flip(self.image, False, True)
                    self.mflash = pygame.transform.flip(self.mflash, False, True)
                self.facing[0] = "right"
            if my < self.d.y:
                self.facing[1] = "up"
            else:
                self.facing[1] = "down"

            angle = math.acos((mx-self.d.x)/distance)
            
            if my >= self.d.y:
                angle *= -1
            self.dir = self.fix_angle(math.degrees(angle))
        
        self.copy = pygame.transform.rotate(self.image, self.dir)
        self.mcopy = pygame.transform.rotate(self.mflash, self.dir)
            
        
        self.r = self.copy.get_rect()
        self.mr = self.mcopy.get_rect()

        self.d2.x = self.d.x + self.image.get_width() * math.cos(math.radians(self.dir))
        self.d2.y = self.d.y - self.image.get_width() * math.sin(math.radians(self.dir))

        self.offset = 0
        if self.facing[0] == "left":
            self.offset = self.copy.get_width()
            self.d2.x += self.offset * math.sin(math.radians(self.dir))

        
        self.r.topleft = (self.d.x - self.offset, (self.d2.y + self.d.y)/2 - self.copy.get_height()/2)

        if self.facing == ["right", "up"]:
            self.b.x = self.d.x + self.dimensions[0] * math.cos(math.radians(self.dir))
            vertical = self.dimensions[1] * math.cos(math.radians(self.dir))
            difference = (self.r.y + self.r.height) - self.d.y #difference in gun bottom and player middle since gun is lower on screen
            self.b.y = self.d.y - vertical + difference - self.dimensions[0] * math.sin(math.radians(self.dir))

        if self.facing == ["right", "down"]:
            self.b.x = self.d.x - self.dimensions[1] * math.sin(math.radians(self.dir)) + self.dimensions[0] * math.cos(math.radians(self.dir))
            vertical = self.dimensions[1] * math.cos(math.radians(self.dir))
            difference = self.d.y - self.r.y #difference in player middle and gun bottom since gun is higher on screen
            self.b.y = self.d.y - vertical + difference - self.dimensions[0] * math.sin(math.radians(self.dir))

        if self.facing == ["left", "up"]:
            self.b.x = self.d.x + self.dimensions[0] * math.cos(math.radians(self.dir))
            vertical = self.dimensions[1] * math.cos(math.radians(self.dir))
            difference = (self.r.y + self.r.height) - self.d.y
            self.b.y = self.d.y + vertical + difference - self.dimensions[0] * math.sin(math.radians(self.dir))

        if self.facing == ["left", "down"]:
            self.b.x = self.d.x + self.dimensions[1] * math.sin(math.radians(self.dir)) + self.dimensions[0] * math.cos(math.radians(self.dir))
            vertical = self.dimensions[1] * math.cos(math.radians(self.dir))
            difference = self.d.y - self.r.y
            self.b.y = self.d.y + vertical + difference - self.dimensions[0] * math.sin(math.radians(self.dir))

        self.mr.center = self.b
        
        if self.shooting:
            self.shoot()

        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.check_collision(s_width, s_height, dt):
                self.bullets.remove(bullet)

        
    def draw(self, screen):
        screen.blit(self.copy, (self.r.topleft))

        for bullet in self.bullets:
            bullet.draw(screen)
        #pygame.draw.circle(screen, (255,0,0), self.b, 4)
        


#class GunManager:

    #def __init__(self,
        
        
    
        
        

        
    
