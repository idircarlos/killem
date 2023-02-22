import pygame

class EnemiesStrong(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     
        self.original_image = pygame.image.load("resources/sprites/player/idle/idle_1.png").convert_alpha()
        self.image = self.original_image        
        self.rect = self.image.get_rect()  
        self.angle = 0

    def initLoc(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def update(self):
        center = pygame.math.Vector2(self.pos) + pygame.math.Vector2(0, -self.radius).rotate(-self.angle) 
        #self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = (round(center.x), round(center.y)))            

    def turnLeft(self):
        self.angle = (self.angle - 1) % 360
   
pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

enemy_s = EnemiesStrong()
enemy_s.initLoc(window.get_rect().center, 100)
all_sprites = pygame.sprite.Group(enemy_s)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    enemy_s.turnLeft()
    all_sprites.update()

    window.fill(0)
    pygame.draw.circle(window, (127, 127, 127), window.get_rect().center, 100, 1)
    all_sprites.draw(window)
    pygame.display.flip()

pygame.quit()
exit()