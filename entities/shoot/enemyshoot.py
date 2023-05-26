import pygame
from util.util import *
from util.settings import *
import random as rand
import math
from entities.shoot.shoot import Shoot

class EnemyShoot(Shoot):
    def __init__(self,coords,orientation,assets):
        x = round(coords[0])
        y = round(coords[1])
        random_animation = self.select_random_assets(assets)
        super().__init__(x,y,orientation,assets,random_animation)

        self.angle = math.atan2(BATTLE_SCREEN_HEIGHT/2 - y, BATTLE_SCREEN_WIDTH/2 - x)
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
        self.timer = 0
        if self.orientation == RIGHT:
            self.rotate(-int(self.angle*180/math.pi))
        else:
            self.rotate(-int(self.angle*180/math.pi) + 180) # flip
        
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
        self.rect.x += round(self.dx*SHOOT_VELOCITY*dt*TARGET_FPS)
        self.rect.y += round(self.dy*SHOOT_VELOCITY*dt*TARGET_FPS)
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