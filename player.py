from util.util import *
from util.settings import *
from bullet import Bullet
from entity import Entity
from skill import Skill
from mixer import Sound

NONE = 0
BLOCK_LEFT = 1
BLOCK_RIGHT = 2
FLIP_RIGHT = 3
FLIP_LEFT = 4
ROTATE = 5
SHOOT = 6
BLOCK = 7

class Player(Entity):
    def __init__(self,assets):
        super().__init__(PLAYER_CENTER,PLAYER_HITBOX,assets)
        self.skills = {ROTATE:Skill(ROTATE,ROTATE_COOLDOWN),SHOOT:Skill(SHOOT,SHOOT_COOLDOWN),BLOCK:Skill(BLOCK,BLOCK_COOLDOWN)}
        self.hitbox = pygame.Rect(self.hitbox)
        
    def skill_ready(self,skill):
        return self.skills[skill].ready
        
    def use_skill(self,skill):
        return self.skills[skill].trigger()
    
    def attack(self):
        if not self.is_animating:
            self.animate("attack")
            return True
        return False
    
    def block(self):
        return True
    
    def flip(self,dir):
        if self.current_animation != "block":
            super().flip(dir)
            
    def get_cooldowns(self):
        cds = []
        for skill in self.skills.values():
            cds.append(skill.ready)
        return cds
        
    def update(self,dt):
        if self.is_animating == True or self.current_animation == "idle":
            self.current_sprite += 15*dt
            if self.current_sprite >= len(self.animations[self.current_animation]):
                self.current_sprite = 0
                if self.current_animation != "idle":
                    self.is_animating = False
                    self.current_animation = "idle"
            self.image = self.animations[self.current_animation][int(self.current_sprite)]
        for skill in self.skills.values():
            skill.update_cd()