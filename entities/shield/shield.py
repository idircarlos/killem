import pygame
from util.util import *
from util.settings import *
from entities.entity import Entity

class Shield(Entity):
    def __init__(self,orientation,assets):
        center = SHIELD_CENTER_RIGHT if orientation is RIGHT else SHIELD_CENTER_LEFT
        hitbox = SHIELD_HITBOX_RIGHT if orientation is RIGHT else SHIELD_HITBOX_LEFT
        super().__init__(center,hitbox,assets,orientation,current_animation="block")
        self.dir = -1 if self.orientation is LEFT else 1
        self.hitbox = pygame.Rect(self.hitbox)
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
    