from util.util import *
from util.settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self,center,hitbox,orientation):
        super().__init__(center,hitbox,orientation)
        self.dir = 1 if orientation is RIGHT else -1
        self.precision_pos = 0
        self.current_animation = "walk"
        self.alive = True
        
    def attack(self):
        if not self.is_animating:
            self.animate("attack")
            
    def update(self):
        if not self.alive:
            self.precision_pos = 0
        if self.precision_pos >= 1:
            self.rect.x += self.dir*int(self.precision_pos)
            self.precision_pos = 0
        self.precision_pos += ENEMY_VELOCITY
        if self.is_animating == True or self.current_animation == "walk":
            self.current_sprite += 0.07
            if self.current_sprite >= len(self.animations[self.current_animation]):
                self.current_sprite = 0
                if self.current_animation == 'dead':
                    self.kill()
                if self.current_animation != "walk":
                    self.is_animating = False
                    self.current_animation = "walk"
            self.image = self.animations[self.current_animation][int(self.current_sprite)]
        
    def import_entity_assets(self):
        self.animations = {'idle':[],'walk':[],'dead':[]}
        for animation in self.animations.keys():
            full_path = SPRITES_PATH + "enemy/" +  animation
            self.animations[animation] = import_folder(full_path,(ENEMY_SPRTE_SIZE_X*ENEMY_SPRITE_MULTIPLIER,ENEMY_SPRTE_SIZE_Y*ENEMY_SPRITE_MULTIPLIER))
        