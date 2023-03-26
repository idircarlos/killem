from util.settings import *
from shoot import *

class ShootRespawn:
    def __init__(self,clock,rand):
        self.clock = clock
        self.rand = rand
        self.cooldown = rand.randint(0,SHOOT_RESPAWN_COOLDOWN)
        self.ready = True if self.cooldown == 0 else False
        self.right_x = BATTLE_SCREEN_WIDTH + (ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER)
        self.left_x  = -ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER
        self.list_x = [self.left_x,self.right_x] #list with 2 possible values for x
        
    def try_spawn(self):
        #if not self.disp or self.position == TOP or self.position == BOTTOM or self.position == LEFT:
        #return False
        #if not self.disp:
        #    return False
        if not self.ready:
            self.cooldown += self.clock.get_time()
        if self.cooldown > RESPAWN_COOLDOWN:
            self.cooldown = 0
        if self.cooldown == 0 and self._rand_spawn():
            self.ready = False
            self.disp = False
            return True
        elif self.cooldown == 0:
            self.ready = True
        return False
    
    def generate_shoot_pos(self):
        
        x = self.rand.choice(self.list_x)
        y = self.rand.random_of_ranges([(0,int(BATTLE_SCREEN_HEIGHT/2) - 300),(int(BATTLE_SCREEN_HEIGHT/2 + 300),BATTLE_SCREEN_HEIGHT)])
        return {"coords":(x,y),"orientation":self.list_x.index(x)} # if the choice is the first item, then index is 0 -> orientation is RIGHT because the position is LEFT
                
    def _rand_spawn(self):
        rand_n = self.rand.randint(0,100-(int(100*RESPAWN_PROB)))
        return rand_n == 0
        