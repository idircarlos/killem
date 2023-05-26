from util.settings import *

class Spawn:
    def __init__(self,clock,rand,cd):
        self.clock = clock
        self.rand = rand
        self.cooldown = cd
        self.current_cooldown = rand.randint(0,cd)
        self.ready = True if self.current_cooldown == 0 else False
        
    def try_spawn(self):
        #if not self.disp or self.position == TOP or self.position == BOTTOM or self.position == LEFT:
        #return False 
        if not self.ready:
            self.current_cooldown += self.clock.get_time()
        if self.current_cooldown > self.cooldown:
            self.current_cooldown = 0
        if self.current_cooldown == 0 and self._rand_spawn():
            self.ready = False
        #    self.disp = False
            return True
        elif self.current_cooldown == 0:
            self.ready = True
        return False
                
    def _rand_spawn(self):
        rand_n = self.rand.randint(0,100-(int(100*RESPAWN_PROB)))
        return rand_n == 0
        