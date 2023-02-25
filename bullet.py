import pygame
from util.util import *
from util.settings import *
import time

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player_rect,orientation,assets):
        super().__init__()
        self.orientation = orientation
        self.animations = {}
        self._deep_copy_assets(assets)
        self.current_animation = "icicle_start"
        self.current_sprite = 0
        self.image = self.animations[self.current_animation][self.current_sprite]
        self.dir = -1 if self.orientation is LEFT else 1
        x = player_rect[0] + player_rect[2] if orientation is RIGHT else player_rect[0]
        y = ((player_rect[1] + player_rect[3]) - player_rect[1])/2 + player_rect[1] + 0
        self.rect = self.image.get_rect(center = (x,y))
        if self.orientation == LEFT:
            self.flip()
        self.timer = 0
        
    def update(self,dt):
        if self.rect[0] <= 0 - self.rect[2] or self.rect[0] >= SCREEN_WIDTH:
            self.kill()
            #print(str(round(self.timer,5)))
        self.rect.x += self.dir*round(BULLET_VELOCITY*dt*TARGET_FPS)
        self.current_sprite += 20*dt
        if self.current_sprite >= len(self.animations[self.current_animation]):
            self.current_sprite = 0
            if self.current_animation == "icicle_start":
                self.current_animation = "icicle"
        self.image = self.animations[self.current_animation][int(self.current_sprite)]
        self.timer += dt
        
    def _deep_copy_assets(self,assets: dict):
        for asset_key in assets.keys():
            self.animations[asset_key] = list(assets[asset_key])
    
    def flip(self):
        for animation in self.animations.keys():
            for i in range(len(self.animations[animation])):
                self.animations[animation][i] = pygame.transform.flip(self.animations[animation][i], True, False)