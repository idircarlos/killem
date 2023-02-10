import pygame
from util.util import *
from util.settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player_rect,orientation):
        super().__init__()
        self.orientation = orientation
        self.import_bullet_assets()
        self.current_animation = "icicle_start"
        self.current_sprite = 0
        self.image = self.animations[self.current_animation][self.current_sprite]
        self.dir = -1 if self.orientation is LEFT else 1
        x = player_rect[0] + player_rect[2] if orientation is RIGHT else player_rect[0]
        print(player_rect)
        y = ((player_rect[1] + player_rect[3]) - player_rect[1])/2 + player_rect[1] + 0
        print(y)
        self.rect = self.image.get_rect(center = (x,y))
        
    def update(self):
        if self.rect[0] <= 0 - self.rect[2] or self.rect[0] >= SCREEN_WIDTH:
            self.kill()
        self.rect.x += self.dir*2
        self.current_sprite += 0.15
        if self.current_sprite >= len(self.animations[self.current_animation]):
            self.current_sprite = 0
            if self.current_animation == "icicle_start":
                self.current_animation = "icicle"
        self.image = self.animations[self.current_animation][int(self.current_sprite)]
        
    def import_bullet_assets(self):
        self.animations = {'icicle_start':[],'icicle':[]}
        for animation in self.animations.keys():
            full_path = SPRITES_PATH + "bullet/" +  animation
            self.animations[animation] = import_folder(full_path, (BULLET_SPRITE_SIZE_X,BULLET_SPRITE_SIZE_Y),self.orientation)