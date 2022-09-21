from setup import *

class Ground:
    width = 135
    level = 600
    grassH = 20
    dirtH = 100
    Gcolor = (0, 190, 0)
    Dcolor = (101, 67, 33)
    
    def __init__(self, x, speed):
        self.d = pygame.Vector2(x, self.level)
        self.v = pygame.Vector2(-speed, 0)

    def update(self, speed, dt):
        #updating tile position
        self.d += self.v * dt
        self.v.x = -speed

    def draw(self, screen, version):
        #drawing grass
        #g = pygame.Rect(self.d.x, self.d.y, self.width, self.grassH)
        grass = pygame.transform.scale(pygame.image.load("assets/ground/grass.png").convert(), (self.width, self.grassH))
        screen.blit(grass, self.d)
        #pygame.draw.rect(screen, self.Gcolor, g)

        #drawing dirt
        #d = pygame.Rect(self.d.x, self.d.y + self.grassH, self.width, self.dirtH)
        #pygame.draw.rect(screen, self.Dcolor, d)
        dirt = pygame.transform.scale(pygame.image.load("assets/ground/" + str(version) +  ".png").convert(), (self.width, self.dirtH))
        screen.blit(dirt, (self.d.x, self.d.y + self.grassH))


class GroundManager:
    upperbound = 2 #upperbound for range when picking random number
    max_consec_holes = 2 #max 2 holes in a row
    tiles = []
    increased = False
    
    
    def __init__(self):
        #list that will hold all the tiles currently displayed on the screen
        
        self.value = []
        self.speed = 0.06
        self.total = 0

        #7 tiles initially displayed on screen
        for i in range(7):
            #creating a tile and adding to tile list
            if i == 0:
                self.value.append("left")
            else:
                self.value.append("middle")
            tile = Ground(i*Ground.width, self.speed)
            self.tiles.append(tile)
            self.total += 1

    def more_new(self):
        pass
    
    def new(self):
        hole_count = 0 #current consecutive hole count

        #loop used to not have too many new hole times in a row
        while hole_count <= self.max_consec_holes: #loop ends when max number of consecutive holes are reached or when a ground tile is added
            if random.randint(1, self.upperbound) == 1 and self.total > 7:
                hole_count += 1 #increase current consecutive hole count
                if (self.value[-1] == "left" or self.value[-1] == "iso"):
                    self.value[-1] = "iso"
                else:
                    self.value[-1] = "right"
            else:
                #otherwise create a tile, add it to the tiles list and break from loop
                tile = Ground(self.tiles[-1].d.x + ((hole_count + 1) * Ground.width), self.speed)
                self.tiles.append(tile)
                
                if hole_count > 0:
                    self.value.append("left")
                else:
                    self.value.append("middle")
                    
                self.total += 1
                break


        # if random.random() < 1/self.upperbound:
        #     pass
        # else:
        #     tile = Ground(self.tiles[-1].d.x + ((hole_count + 1) * Ground.width), self.speed)


            
        
    def delete(self, tile):
        #remove the tile from the tile list
        self.tiles.remove(tile)
        self.value.remove(self.value[0])

    def clear(self):
        self.tiles.clear()
        self.value.clear()
            
        self.__init__()
    
    def update(self, dt, s_width, score):
        #tile each tile in list
        for tile in self.tiles:
            tile.update(self.speed, dt)
            spawnable = True #used to limit amount of new tiles created to 1
            if self.tiles[-1].d.x < s_width + abs(tile.v.x) * dt and spawnable: #if the right side of the rightmost tile is visible on screen, create 1 new tile 
                self.new()
                spawnable = False
            if tile.d.x + tile.width < 0: #if the right side of the leftmost tile is off the screen, remove that tile
                self.delete(tile)
        
        #increasing ground speed
        if score % 20 == 0 and score > 0 :
            if not self.increased:
                self.speed += 0.05
                self.increased = True
        else:
            self.increased = False

        if score > 55:
            self.max_consec_holes = 3

    def draw(self, screen, s_width):
        #draw each tile onto the screen
        i = 0
        for tile in self.tiles:
            if tile.d.x <= s_width + tile.width/2:
                tile.draw(screen, self.value[i])
            i += 1
            
