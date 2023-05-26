from util.util import *
from util.settings import *
from entities.entity import Entity
from math import sqrt
from mixer.mixer import Sound

class Enemy(Entity):
    def __init__(self,center,hitbox,assets,spawn):
        self.spawn = spawn
        if spawn == LEFT or spawn == BOTTOM:
            self.orientation = RIGHT
        elif spawn == RIGHT or spawn == TOP:
            self.orientation = LEFT
        super().__init__(center,hitbox,assets,self.orientation,current_animation="walk")
        self.dir = 1 if self.spawn == LEFT or self.spawn == BOTTOM else -1
        self.precision_pos = 0
        self.current_animation = "walk"
        self.alive = True
        self.rotating = False
        if self.spawn == TOP:
            self.start_angle = 180
        elif self.spawn == RIGHT:
            self.start_angle = 270
        elif self.spawn == BOTTOM:
            self.start_angle = 360
        elif self.spawn == LEFT:
            self.start_angle = 90
        self.angle = self.start_angle
        self.pos = (self.rect.x,self.rect.y)
        self.radius = 0
        self.angle_animation = 0
        self.timer = 0
        
    def rotate(self):
        self.radius = int(sqrt(pow(abs(CENTER_X - (self.rect.x + self.rect.width/2)),2) + pow(abs(CENTER_Y - (self.rect.y + self.rect.height/2)),2)))
        self.rotating = True
        self.timer = 0
        
    def attack(self):
        if not self.is_animating:
            self.animate("attack")
            
    def update(self,dt):
        if self.rotating:
            self.angle = ((self.angle - (ROTATE_VELOCITY * dt * TARGET_FPS)) % 360)
            center = pygame.math.Vector2((CENTER_X,CENTER_Y)) + pygame.math.Vector2(0, -self.radius).rotate(-self.angle)
            self.rect = self.image.get_rect(center = (round(center.x), round(center.y)))
            self.timer += dt
            if (self.angle + 90) % 360 <= self.start_angle and self.start_angle != 0:
                self._update_sprite_directions()
                self.rotating = False
                self.angle_animation = 0
                self.start_angle = (self.start_angle - 90) % 360
                self.angle = self.start_angle
                center = pygame.math.Vector2((CENTER_X,CENTER_Y)) + pygame.math.Vector2(0, -self.radius).rotate(-self.angle)
                self.rect = self.image.get_rect(center = (round(center.x), round(center.y)))
            elif self.start_angle == 0 and self.angle <= 270:
                self._update_sprite_directions()
                self.rotating = False
                self.angle_animation = 0
                self.start_angle = 270
                self.angle = self.start_angle
                center = pygame.math.Vector2((CENTER_X,CENTER_Y)) + pygame.math.Vector2(0, -self.radius).rotate(-self.angle)
                self.rect = self.image.get_rect(center = (round(center.x), round(center.y)))
            return
        self.pos = (self.rect.x,self.rect.y)
        if not self.alive:
            self.precision_pos = 0
        if self.precision_pos >= 1:
            if self.spawn == LEFT or self.spawn == RIGHT:
                self.rect.x += self.dir*self.precision_pos
            elif self.spawn == TOP or self.spawn == BOTTOM:
                 self.rect.y += self.dir*self.precision_pos
            self.precision_pos = 0
        self.precision_pos += round(ENEMY_VELOCITY*dt*TARGET_FPS)
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
