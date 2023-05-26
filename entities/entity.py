import pygame
from util.util import *
from util.settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self,center,hitbox,assets,orientation=RIGHT,current_animation="idle"):
        super().__init__()
        self.orientation = None
        self.is_animating = False
        self.current_animation = current_animation
        self.current_sprite = 0
        self.animations = {}
        self._deep_copy_assets(assets)
        self.image = self.animations[self.current_animation][self.current_sprite]
        self.rect = self.image.get_rect(center = center)
        self.hitbox = (self.rect[0]+hitbox[0],self.rect[1]+hitbox[1],self.rect[2]+hitbox[2],self.rect[3]+hitbox[3])
        if orientation is LEFT:
            self.flip(orientation)
        self.orientation = orientation
        
    def animate(self,animation):
        if not self.is_animating:
            self.current_animation = animation
            self.is_animating = True
            self.current_sprite = 0
    
    def _deep_copy_assets(self,assets: dict):
        for asset_key in assets.keys():
            self.animations[asset_key] = list(assets[asset_key])
    
        
    def flip(self,dir):
        if dir != self.orientation:
            self.orientation = dir 
            for animation in self.animations.keys():
                for i in range(len(self.animations[animation])):
                    self.animations[animation][i] = pygame.transform.flip(self.animations[animation][i], True, False)
    