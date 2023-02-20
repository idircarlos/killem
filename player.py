from util.util import *
from util.settings import *
from bullet import Bullet
from entity import Entity

class Player(Entity):
    def __init__(self):
        super().__init__(PLAYER_CENTER,PLAYER_HITBOX)
    
    def attack(self):
        if not self.is_animating:
            self.animate("attack")
            return True
        return False
    
    def block(self):
        if not self.is_animating:
            self.animate("block")
            return True
        return False
    
    def flip(self,dir):
        if self.current_animation != "block":
            super().flip(dir)
        
    def update(self,dt):
        if self.is_animating == True or self.current_animation == "idle":
            self.current_sprite += 20*dt
            if self.current_sprite >= len(self.animations[self.current_animation]):
                self.current_sprite = 0
                if self.current_animation != "idle":
                    self.is_animating = False
                    self.current_animation = "idle"
            self.image = self.animations[self.current_animation][int(self.current_sprite)]
        
    def import_entity_assets(self):
        self.animations = {'idle':[],'attack':[],'block':[]}
        for animation in self.animations.keys():
            full_path = SPRITES_PATH + "player/" +  animation
            self.animations[animation] = import_folder(full_path,(PLAYER_SPRITE_SIZE_X*2,PLAYER_SPRITE_SIZE_Y*2))