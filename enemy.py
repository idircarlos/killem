from util.util import *
from util.settings import *
from entity import Entity
from math import sqrt

class Enemy(Entity):
    def __init__(self,center,hitbox,spawn):
        self.spawn = spawn
        if spawn == LEFT or spawn == BOTTOM:
            self.orientation = RIGHT
        elif spawn == RIGHT or spawn == TOP:
            self.orientation = LEFT
        super().__init__(center,hitbox,self.orientation)
        self.dir = 1 if self.spawn == LEFT or self.spawn == BOTTOM else -1
        self.precision_pos = 0
        self.current_animation = "walk"
        self.alive = True
        self.rotating = False
        if self.spawn == TOP:
            self.angle = 180
        elif self.spawn == RIGHT:
            self.angle = 270
        elif self.spawn == BOTTOM:
            self.angle = 360
        elif self.spawn == LEFT:
            self.angle = 90
        self.pos = (self.rect.x,self.rect.y)
        self.radius = 0
        self.angle_animation = 0
        
    def attack(self):
        if not self.is_animating:
            self.animate("attack")
            
    def update(self,dt):
        if self.rotating:
            self.angle_animation += 2
            self.angle = (self.angle - 2) % 360
            center = pygame.math.Vector2((CENTER_X,CENTER_Y)) + pygame.math.Vector2(0, -self.radius).rotate(-self.angle) 
            self.rect = self.image.get_rect(center = (round(center.x), round(center.y)))      
            if self.angle_animation == 90:
                self._update_sprite_directions()
                self.rotating = False
                self.angle_animation = 0 
            return
        self.pos = (self.rect.x,self.rect.y)
        if not self.alive:
            self.precision_pos = 0
        if self.precision_pos >= 1:
            if self.spawn == LEFT or self.spawn == RIGHT:
                self.rect.x += self.dir*int(self.precision_pos)
            elif self.spawn == TOP or self.spawn == BOTTOM:
                 self.rect.y += self.dir*int(self.precision_pos)
            self.precision_pos = 0
        self.precision_pos += ENEMY_VELOCITY*dt
        if self.is_animating == True or self.current_animation == "walk":
            self.current_sprite += 13.5*dt
            if self.current_sprite >= len(self.animations[self.current_animation]):
                self.current_sprite = 0
                if self.current_animation == 'dead':
                    self.kill()
                if self.current_animation != "walk":
                    self.is_animating = False
                    self.current_animation = "walk"
            self.image = self.animations[self.current_animation][int(self.current_sprite)]
        
    def import_entity_assets(self):
        self.animations = {'idle':[],'walk':[],'dead':[]}
        for animation in self.animations.keys():
            full_path = SPRITES_PATH + "enemy/" +  animation
            self.animations[animation] = import_folder(full_path,(ENEMY_SPRTE_SIZE_X*ENEMY_SPRITE_MULTIPLIER,ENEMY_SPRTE_SIZE_Y*ENEMY_SPRITE_MULTIPLIER))

    def _update_sprite_directions(self):
        if self.spawn == TOP:
            self.spawn = RIGHT
            orientation = LEFT
            self.dir = -1
        elif self.spawn == RIGHT:
            self.spawn = BOTTOM
            orientation = LEFT
            self.dir = -1
        elif self.spawn == BOTTOM:
            self.spawn = LEFT
            orientation = RIGHT
            self.dir = 1
        elif self.spawn == LEFT:
            self.spawn = TOP
            orientation = RIGHT
            self.dir = 1
        self.flip(orientation)
