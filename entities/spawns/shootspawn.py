from util.settings import *
from entities.spawns.spawn import Spawn

class ShootSpawn(Spawn):
    def __init__(self,clock,rand):
        super().__init__(clock,rand,SHOOT_RESPAWN_COOLDOWN)
        self.right_x = BATTLE_SCREEN_WIDTH + (ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER)
        self.left_x  = -ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER
        self.list_x = [self.left_x,self.right_x] #list with 2 possible values for x
    
    def generate_shoot_pos(self):
        x = self.rand.choice(self.list_x)
        y = self.rand.random_range((0,int(BATTLE_SCREEN_HEIGHT/4)))
        return {"coords":(x,y),"orientation":self.list_x.index(x)} # if the choice is the first item, then index is 0 -> orientation is RIGHT because the position is LEFT
                
       