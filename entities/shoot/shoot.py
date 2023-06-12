import pygame
from util.util import *
from util.settings import *
import random as rand
import math
from entities.entity import Entity

class Shoot(Entity):
    def __init__(self,x,y,orientation,assets,current_animation):
        center = (x,y)
        super().__init__(center,[0,0,0,0],assets,orientation,current_animation=current_animation)
        self.dir = -1 if self.orientation is LEFT else 1
        
    def move(self):
        x = self.rect.centerx
        y = self.rect.centery
        self.angle = math.atan2(BATTLE_SCREEN_HEIGHT/2 - y, BATTLE_SCREEN_WIDTH/2 - x)
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
    
    def update(self,dt):
        if self.orientation == RIGHT and self.rect.x + self.rect.width > BATTLE_SCREEN_WIDTH/2:
            self.kill()
        elif self.orientation == LEFT and self.rect.x < BATTLE_SCREEN_HEIGHT/2:
            self.kill()
        self.move()
        self.rect.x += round(self.dx*BULLET_VELOCITY*dt*TARGET_FPS)
        self.rect.y += round(self.dy*BULLET_VELOCITY*dt*TARGET_FPS)
        self.current_sprite += 20*dt
        if self.current_sprite >= len(self.animations[self.current_animation]):
            self.current_sprite = 0
        self.image = self.animations[self.current_animation][int(self.current_sprite)]
        self.timer += dt
        
    def _deep_copy_assets(self,assets: dict):
        for asset_key in assets.keys():
            self.animations[asset_key] = list(assets[asset_key])
    
    def select_random_assets(self,assets):
        return rand.choice(list(assets))
        
    def rotate(self,angle):
        for animation in self.animations.keys():
            for i in range(len(self.animations[animation])):
                self.animations[animation][i] = pygame.transform.rotate(self.animations[animation][i], angle)