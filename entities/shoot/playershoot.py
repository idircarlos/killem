from util.util import *
from util.settings import *
from entities.shoot.shoot import Shoot

class PlayerShoot(Shoot):
    def __init__(self,player_rect,orientation,assets):
        x = player_rect[0] + player_rect[2] if orientation is RIGHT else player_rect[0]
        y = ((player_rect[1] + player_rect[3]) - player_rect[1])/2 + player_rect[1] + 0
        super().__init__(x,y,orientation,assets,"icicle_start")
        self.timer = 0
        
    def update(self,dt):
        if self.rect[0] <= 0 - self.rect[2] or self.rect[0] >= BATTLE_SCREEN_WIDTH:
            self.kill()
            #print(str(round(self.timer,5)))
        self.rect.x += self.dir*round(BULLET_VELOCITY*dt*TARGET_FPS)
        self.current_sprite += 20*dt
        if self.current_sprite >= len(self.animations[self.current_animation]):
            self.current_sprite = 0
            if self.current_animation == "icicle_start":
                self.current_animation = "icicle"
        self.image = self.animations[self.current_animation][int(self.current_sprite)]
        self.timer += dt
        
    def _deep_copy_assets(self,assets: dict):
        for asset_key in assets.keys():
            self.animations[asset_key] = list(assets[asset_key])
    