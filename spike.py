from setup import *
from ground import *

class Spike:
    width = 10
    colliding = False
    speed = 0.25

    def __init__(self, s_width, _type):
        self.d = pygame.Vector2(random.randint(self.width, s_width - self.width), -1 * random.randint(self.width, 20 * self.width))
        self.v = pygame.Vector2(0, 0)
        self.a = pygame.Vector2(0, 0.001)
        if _type == "spike":
            factor = 2
        else:
            factor = 3
        self.r = pygame.Rect(self.d.x, self.d.y, factor * self.width, factor * self.width)
        self.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
        self.type = _type

    def check_collision(self, tiles, dt):
        epsilon = abs(self.v.y) * dt

        for tile in tiles:
            if self.d.x < tile.d.x + tile.width and self.d.x + 2 * self.width > tile.d.x: 
                if abs(self.d.y - tile.d.y) < epsilon:
                    self.colliding = True
            if self.d.y > 680:
                self.colliding = True

    def update(self, dt):
        self.d += self.v * dt
        if self.v.y < self.speed:
            self.v += self.a * dt
        else:
            self.v.y = self.speed
        self.r.x = self.d.x
        self.r.y = self.d.y

        

    def draw(self, screen):
        if self.d.y > -self.width:
            if self.type == "spike":
                left = self.d.x
                right = self.d.x + 2 * self.width
                middle = self.d.x + self.width
                top = self.d.y
                bottom = self.d.y + 2 * self.width

                pygame.draw.polygon(screen, (0,0,0), [(left - 3, top - 3), (right + 3, top - 3), (middle, bottom + 3)])
                pygame.draw.polygon(screen, self.color, [(left, top), (right, top), (middle, bottom)])
            else:
                screen.blit(pygame.transform.scale(pygame.image.load("assets/collectables/refill.png").convert_alpha(), (self.r.width, self.r.height)), self.d)

                
class SpikeManager:
    amount = 5
    increased = False
    spawn_delay = 3
    spikes = []

    def __init__(self, s_width, score):
        if score > self.spawn_delay:
            for i in range(self.amount):
                spike = Spike(s_width, "spike")
                self.spikes.append(spike)

    def new(self):
        _type = "spike"
        if random.randint(0, 25) == 0:
            _type = "ammo"
        
        spike = Spike(s_width, _type)
        self.spikes.append(spike)

    def delete(self, spike):
        self.spikes.remove(spike)

    def clear(self):
        for spike in self.spikes:
            self.delete(spike)

    def update(self, tiles, dt, score):
        for spike in self.spikes:
            spike.check_collision(tiles, dt)
            spike.update(dt)
            if spike.colliding == True:
                self.delete(spike)

        if score % 15 == 0 and score > 0 :
            if not self.increased:
                self.amount += 1
                self.increased = True
        else:
            self.increased = False
 
        if len(self.spikes) < self.amount and score > self.spawn_delay:
            self.new()
        #print(len(self.spikes))

    def draw(self, screen):
        for spike in self.spikes:
            spike.draw(screen)
