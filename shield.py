import pygame
from util.util import *
from util.settings import *

class Shield(pygame.sprite.Sprite):
    def __init__(self,orientation,assets):
        super().__init__()
        self.orientation = orientation
        self.animations = {}
        self._deep_copy_assets(assets)
        self.current_animation = "block"
        self.current_sprite = 0
        self.image = self.animations[self.current_animation][self.current_sprite]
        self.dir = -1 if self.orientation is LEFT else 1
        self.rect = self.image.get_rect(center = SHIELD_CENTER_RIGHT if self.orientation is RIGHT else SHIELD_CENTER_LEFT)
        if self.orientation == LEFT:
            self.flip()
        hitbox = SHIELD_HITBOX_RIGHT if self.orientation is RIGHT else SHIELD_HITBOX_LEFT
        hitbox = (self.rect[0]+hitbox[0],self.rect[1]+hitbox[1],self.rect[2]+hitbox[2],self.rect[3]+hitbox[3])
        self.hitbox = pygame.Rect(hitbox)
        self.timer = 0
        self.blocked = False
        
    def update(self,dt):
        self.current_sprite += 20*dt
        if self.current_sprite >= len(self.animations[self.current_animation]):
            self.kill()
            return
        self.image = self.animations[self.current_animation][int(self.current_sprite)]
        self.timer += dt
        
    def _deep_copy_assets(self,assets: dict):
        for asset_key in assets.keys():
            self.animations[asset_key] = list(assets[asset_key])
    
    def flip(self):
        for animation in self.animations.keys():
            for i in range(len(self.animations[animation])):
                self.animations[animation][i] = pygame.transform.flip(self.animations[animation][i], True, False)