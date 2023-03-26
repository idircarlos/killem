import pygame
from util.util import *
from util.settings import *
import random as rand
import math

class Shoot(pygame.sprite.Sprite):
    def __init__(self,coords,orientation,assets):
        super().__init__()
        self.orientation = orientation
        self.animations = {}
        self._deep_copy_assets(assets)
        self.current_animation = self.select_random_assets(assets)
        self.current_sprite = 0
        self.image = self.animations[self.current_animation][self.current_sprite]
        self.dir = -1 if self.orientation is LEFT else 1
        x = round(coords[0])
        y = round(coords[1])
        self.angle = math.atan2(BATTLE_SCREEN_HEIGHT/2 - y, BATTLE_SCREEN_WIDTH/2 - x)
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
        self.rect = self.image.get_rect(center = (x,y))
        self.timer = 0
        self.rotate(-int(self.angle*180/math.pi))

    def move(self):
        x = self.rect.centerx
        y = self.rect.centery
        self.angle = math.atan2(BATTLE_SCREEN_WIDTH/2 - y, BATTLE_SCREEN_HEIGHT/2 - x)
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
    
    def update(self,dt):
        if self.orientation == RIGHT and self.rect.x + self.rect.width > BATTLE_SCREEN_WIDTH/2:
            self.kill()
            print("321")
        elif self.orientation == LEFT and self.rect.x < BATTLE_SCREEN_HEIGHT/2:
            self.kill()
            print("123")
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
    
    def flip(self):
        for animation in self.animations.keys():
            for i in range(len(self.animations[animation])):
                self.animations[animation][i] = pygame.transform.flip(self.animations[animation][i], True, False)
    
    def select_random_assets(self,assets):
        return rand.choice(list(assets))
        
    def rotate(self,angle):
        for animation in self.animations.keys():
            for i in range(len(self.animations[animation])):
                self.animations[animation][i] = pygame.transform.rotate(self.animations[animation][i], angle)