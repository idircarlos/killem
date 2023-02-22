import pygame
from util.settings import *
from enemy import Enemy
from rand import Rand

class Spawn:
    def __init__(self,position,clock,rand):
        self.position = position
        self.clock = clock
        self.rand = rand
        self.cooldown = rand.randint(0,RESPAWN_COOLDOWN)
        self.ready = True if self.cooldown == 0 else False
        if self.position == LEFT:
            self.x = -ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER
            self.y = SCREEN_HEIGHT/2
        elif self.position == RIGHT:
            self.x = SCREEN_WIDTH + (ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER)
            self.y = SCREEN_HEIGHT/2
        elif self.position == TOP:
            self.x = SCREEN_WIDTH/2
            self.y = -ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER
        elif self.position == BOTTOM:
            self.x = SCREEN_WIDTH/2
            self.y = SCREEN_HEIGHT + (ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER)
        self.disp = True

        
    def try_spawn(self):
        #if not self.disp or self.position == TOP or self.position == BOTTOM or self.position == LEFT:
        #    return False 
        if not self.ready:
            self.cooldown += self.clock.get_time()
        if self.cooldown > RESPAWN_COOLDOWN:
            self.cooldown = 0
        if self.cooldown == 0 and self._rand_spawn():
            self.ready = False
            #self.disp = False
            return True
        elif self.cooldown == 0:
            self.ready = True
        return False
                
    def _rand_spawn(self):
        rand_n = self.rand.randint(0,100-(int(100*RESPAWN_PROB)))
        return rand_n == 0
        