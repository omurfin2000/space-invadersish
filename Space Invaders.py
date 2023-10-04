import pygame
import time
import random


from pygame.locals import ( # easier access to keys
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)
'''
surf_center = (
    (SCREEN_WIDTH-surf.get_width())/2, # how to get the center of the sprite
    (SCREEN_HEIGHT-surf.get_height())/2
)
'''

pygame.init()

surf = pygame.Surface((50,50))

surf.fill((0,255,0))

rect = surf.get_rect()

SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1040
PLANE = 800
SPAWN = 100



enemySpawnClock = time.time()
clock = time.time()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, coord): 
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((8, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.x = ((coord[0]+surf.get_width()/2))
        self.rect.y = ((coord[1]+surf.get_height()/2))
    
    def update(self):
        self.rect.move_ip(0,-1)
        if self.rect.y < 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((60, 45))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = PLANE
    

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)
        if pressed_keys[K_SPACE]:
            return 1

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH - 50:
            self.rect.right = SCREEN_WIDTH - 50


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super(Alien, self).__init__()
        self.rect = pygame.Rect(0, 0, 60, 40)
        self.rect.x = random.randint(100, 1700)
        self.rect.y = SPAWN
        self.clock = time.time()
        self.image = pygame.image.load("C:/Users/jamie/Oliver Computer Work/Python/Pygame Portfolio/Space Invaders/images/alien.png")
    
    def update(self):
        if time.time() - self.clock < 0.1:
            pass
        else: 
            self.clock = time.time()
            r = random.randint(0,1)
            if r == 0:
                self.rect.move_ip(-20, 15)
            elif r == 1:
                self.rect.move_ip(20, 15)
        if self.rect.y >= PLANE:
            player.kill()
        if pygame.sprite.spritecollideany(self, projectiles):
            self.kill()
        


screen = pygame.display.set_mode([SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80])


projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
players.add(player)


running = True
while running:


    for event in pygame.event.get():
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    if player.update(pressed_keys):
        if time.time() - clock < 0.4:
            pass
        else: 
            clock = time.time()
            proj = Bullet((player.rect.x, player.rect.y))
            projectiles.add(proj)
            all_sprites.add(proj)

    if time.time() - enemySpawnClock < 2:
        for entity in enemies:
            entity.update()
            if entity.rect.y >= PLANE:
                print(entity.rect.y)
                player.kill()
    else:    
        enemySpawnClock = time.time()
        enemy = Alien()
        enemies.add(enemy)
        all_sprites.add(enemy)
 

    screen.fill((0, 0, 0))

    for p in projectiles:
        if p != None:        
            p.update()
            screen.blit(p.surf, p.rect)

    for e in enemies:
        screen.blit(e.image, e.rect)
        
    for p in players:
        screen.blit(player.surf, player.rect)
    
    
    

    pygame.display.flip() # flip updates the screen


pygame.quit()
