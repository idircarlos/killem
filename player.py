from util.util import *
from util.settings import *
from bullet import Bullet
from entity import Entity
from skill import Skill

NONE = 0
SHOOT = 1
FLIP_RIGHT = 2
FLIP_LEFT = 3
ROTATE = 4
BLOCK = 5

class Player(Entity):
    def __init__(self,assets):
        super().__init__(PLAYER_CENTER,PLAYER_HITBOX,assets)
        self.skills = {ROTATE:Skill(ROTATE,ROTATE_COOLDOWN),SHOOT:Skill(SHOOT,SHOOT_COOLDOWN)}
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
        if not self.is_animating:
            self.animate("block")
            return True
        return False
    
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