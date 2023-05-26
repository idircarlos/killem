from util.settings import *
from entities.spawns.spawn import Spawn

class EnemySpawn(Spawn):
    def __init__(self,position,clock,rand):
        super().__init__(clock,rand,RESPAWN_COOLDOWN)
        self.position = position
        if self.position == LEFT:
            self.x = -ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER
            self.y = BATTLE_SCREEN_HEIGHT/2
        elif self.position == RIGHT:
            self.x = BATTLE_SCREEN_WIDTH + (ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER)
            self.y = BATTLE_SCREEN_HEIGHT/2
        elif self.position == TOP:
            self.x = BATTLE_SCREEN_WIDTH/2
            self.y = -ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER
        elif self.position == BOTTOM:
            self.x = BATTLE_SCREEN_WIDTH/2
            self.y = BATTLE_SCREEN_HEIGHT + (ENEMY_SPRTE_SIZE_X * ENEMY_SPRITE_MULTIPLIER)
