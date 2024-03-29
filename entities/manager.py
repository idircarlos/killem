import pygame
from entities.characters.player import *
from entities.characters.enemy  import *
from entities.shoot.playershoot import *
from entities.shield.shield import *
from entities.shoot.enemyshoot import *
from entities.spawns.enemyspawn import *
from entities.spawns.shootspawn import *
from util.rand import Rand
from util.debug import *
from mixer.mixer import GLOBAL_MIXER, SHOOT_SOUND, ENEMY_DEATH_SOUND, SHOOT_BLOCKED_SOUND

PLAYER_DEAD = 0
ENEMY_DEAD  = 1
SHOOT_BLOCKED = 2

class EntityManager:
    def __init__(self,paused,screen,clock,assets):
        self.paused = paused
        self.screen = screen
        self.rand = Rand()
        self.player = Player(assets["player"])
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.shield_group = pygame.sprite.Group()
        self.shoot_group = pygame.sprite.Group()
        self.left_respawn  = EnemySpawn(LEFT,clock,self.rand)
        self.right_respawn  = EnemySpawn(RIGHT,clock,self.rand)
        self.shoot_respawn = ShootSpawn(clock,self.rand)
        self.enemy_group = pygame.sprite.Group()
        self.clock = clock
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
        self.assets = assets
        
    def flip_axis(self):
        for enemy in self.enemy_group:
            enemy.rotate()
        
    def player_action(self,action_list):
        selected = max(action_list)
        action = action_list.index(selected)
        if action == SHOOT:
            if self.player.skill_ready(SHOOT):
                self.player.use_skill(SHOOT)
                self.player_attack()
        elif action == SHOOT_LEFT:
            if self.player.skill_ready(SHOOT):
                self.player_flip(LEFT)
                self.player.use_skill(SHOOT)
                self.player_attack()
        elif action == SHOOT_RIGHT:
            if self.player.skill_ready(SHOOT):
                self.player_flip(RIGHT)
                self.player.use_skill(SHOOT)
                self.player_attack()
        elif action == SHOOT_RIGHT:
            self.player_flip(RIGHT)
        elif action == ROTATE:
            if self.player.skill_ready(ROTATE):
                self.player.use_skill(ROTATE)
                self.flip_axis()
        elif action == BLOCK_LEFT:
            if self.player.skill_ready(BLOCK):
                self.player_flip(LEFT)
                self.player.use_skill(BLOCK)
                self.player_block(LEFT)
        elif action == BLOCK_RIGHT:
            if self.player.skill_ready(BLOCK):
                self.player_flip(RIGHT)
                self.player.use_skill(BLOCK)
                self.player_block(RIGHT)
        
    def player_attack(self):
        can_attack = self.player.attack()
        if can_attack:
            self.bullet_group.add(PlayerShoot(self.player.hitbox,self.player.orientation,self.assets["bullet"]))
            GLOBAL_MIXER.play(SHOOT_SOUND)
            
    def player_block(self,orientation):
        can_block = self.player.block()
        if can_block:
            self.shield_group.add(Shield(orientation,self.assets["block"]))
        
    def player_flip(self,dir):
        self.player.flip(dir)
            
    def try_spawn(self):
        enemy_assets = self.assets["enemy_skeleton"]
        if self.left_respawn.try_spawn():
            is_special_enemy = self.rand.decision(0.01)
            if is_special_enemy:
                enemy_assets = self.assets["enemy_undead"]
            self.enemy_group.add(Enemy((self.left_respawn.x,self.left_respawn.y),(0,0,0,0),enemy_assets,LEFT))
        if self.right_respawn.try_spawn():
            is_special_enemy = self.rand.decision(0.01)
            if is_special_enemy:
                enemy_assets = self.assets["enemy_undead"]
            self.enemy_group.add(Enemy((self.right_respawn.x,self.right_respawn.y),(0,0,0,0),enemy_assets,RIGHT))
            
        if self.shoot_respawn.try_spawn():
            data = self.shoot_respawn.generate_shoot_pos()
            self.shoot_group.add(EnemyShoot(data["coords"],data["orientation"],self.assets["shoot"]))

    
    def get_enemies_positions(self):
        left  = False
        right = False
        for enemy in self.enemy_group:
            if enemy.spawn == RIGHT and enemy.rect.x <= BATTLE_SCREEN_WIDTH - 1 and enemy.alive:
                right = True
            elif enemy.spawn == LEFT and enemy.rect.x + enemy.rect.width >= 1 and enemy.alive:
                left = True
        return left, right
            
    def get_bullets_positions(self):
        left  = False
        right = False
        for bullet in self.bullet_group:
            if bullet.orientation == RIGHT:
                right = True
            else:
                left = True
        return left, right
    
    def get_shoots_positions(self):
        left  = False
        right = False
        for shoot in self.shoot_group:
            if shoot.orientation == RIGHT:
                right = True
            else:
                left = True
        return left, right
    
    def check_positions(self):
        danger_zone_left = -1
        danger_zone_right = -1
        for enemy in self.enemy_group:
            if enemy.spawn == LEFT and enemy.alive:
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_0) and danger_zone_left < 0:
                    danger_zone_left = 0
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_1) and danger_zone_left < 1:
                    danger_zone_left = 1
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_2) and danger_zone_left < 2:
                    danger_zone_left = 2
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_3) and danger_zone_left < 3:
                    danger_zone_left = 3
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_4) and danger_zone_left < 4:
                    danger_zone_left = 4
            
            elif enemy.spawn == RIGHT and enemy.alive:
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_0) and danger_zone_right < 0:
                    danger_zone_right = 0
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_1) and danger_zone_right < 1:
                    danger_zone_right = 1
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_2) and danger_zone_right < 2:
                    danger_zone_right = 2
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_3) and danger_zone_right < 3:
                    danger_zone_right = 3
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_4) and danger_zone_right < 4:
                    danger_zone_right = 4
        return danger_zone_left, danger_zone_right                
            
    def check_collisions(self):
        for bullet in self.bullet_group:
            for enemy in self.enemy_group:
                if enemy.spawn == RIGHT:
                    if pygame.Rect.colliderect(bullet.rect,enemy.rect) and bullet.rect.x + bullet.rect.width >= enemy.rect.x + int(enemy.rect.width/2 + 25) and (enemy.spawn != TOP and enemy.spawn != BOTTOM) and enemy.alive:
                        danger_zone = 0
                        if self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_0):
                            danger_zone = DANGER_ZONE_RIGHT_0
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_1):
                            danger_zone = DANGER_ZONE_RIGHT_1
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_2):
                            danger_zone = DANGER_ZONE_RIGHT_2
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_3):
                            danger_zone = DANGER_ZONE_RIGHT_3
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_4):
                            danger_zone = DANGER_ZONE_RIGHT_4
                        enemy.alive = False
                        GLOBAL_MIXER.play(ENEMY_DEATH_SOUND)
                        enemy.animate("dead")
                        bullet.kill()
                        return ENEMY_DEAD, danger_zone
                else:
                    if pygame.Rect.colliderect(bullet.rect,enemy.rect) and bullet.rect.x <= enemy.rect.x + int(enemy.rect.width/2 - 25) and (enemy.spawn != TOP and enemy.spawn != BOTTOM) and enemy.alive:
                        danger_zone = 0
                        if self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_4):
                            danger_zone = DANGER_ZONE_LEFT_4
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_3):
                            danger_zone = DANGER_ZONE_LEFT_3
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_2):
                            danger_zone = DANGER_ZONE_LEFT_2
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_1):
                            danger_zone = DANGER_ZONE_LEFT_1
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_0):
                            danger_zone = DANGER_ZONE_LEFT_0
                        enemy.alive = False
                        GLOBAL_MIXER.play(ENEMY_DEATH_SOUND)
                        enemy.animate("dead")
                        bullet.kill()
                        return ENEMY_DEAD, danger_zone
        for enemy in self.enemy_group:
            if pygame.Rect.colliderect(self.player.hitbox,enemy.rect):                
                self.player.animate("dead")
                return PLAYER_DEAD, -1
        for shoot in self.shoot_group:
            if pygame.Rect.colliderect(self.player.hitbox,shoot.rect):   
                # hide shoot sprite, but detect collide to reproduce dead to player
                temp_image = pygame.Surface((24, 24), flags=pygame.SRCALPHA)
                temp_image.fill((0, 0, 0, 0)) #RGBA sequence
                shoot.image = temp_image
                self.player.animate("dead")
                return PLAYER_DEAD, -1
            for shield in self.shield_group:
                if pygame.Rect.colliderect(shield.hitbox,shoot.rect):
                    GLOBAL_MIXER.play(SHOOT_BLOCKED_SOUND)
                    shoot.kill()
                    return SHOOT_BLOCKED, -1
        return None, -1
            
    def enemy_in_danger_zone(self,enemy,danger_zone):
        spawn = enemy.spawn
        if spawn == RIGHT:
            if enemy.rect.x <= danger_zone:
                return True
        elif spawn == LEFT:
            if enemy.rect.x + enemy.rect.width >= danger_zone:
                return True
        return False
    
    def shoot_in_danger_zone(self,shoot,danger_zone):
        orientation = shoot.orientation
        if orientation == RIGHT:
            if shoot.rect.x + shoot.rect.width >= danger_zone:
                return True
        elif orientation == LEFT:
            if shoot.rect.x <= danger_zone:
                return True
        return False
    
    def player_shoot_danger_zone(self,shoot,danger_zone):
        orientation = shoot.orientation
        if orientation == RIGHT:
            if shoot.rect.x <= danger_zone:
                return True
        elif orientation == LEFT:
            if shoot.rect.x + shoot.rect.width >= danger_zone:
                return True
        return False
            
    def get_enemies_danger(self):
        danger_left  = {DANGER_ZONE_LEFT_0:False,DANGER_ZONE_LEFT_1:False,DANGER_ZONE_LEFT_2:False,DANGER_ZONE_LEFT_3:False,DANGER_ZONE_LEFT_4:False}
        danger_right = {DANGER_ZONE_RIGHT_0:False,DANGER_ZONE_RIGHT_1:False,DANGER_ZONE_RIGHT_2:False,DANGER_ZONE_RIGHT_3:False,DANGER_ZONE_RIGHT_4:False}
        for enemy in self.enemy_group:
            if enemy.spawn == RIGHT and enemy.alive:
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_4):
                    danger_right[DANGER_ZONE_RIGHT_4] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_3):
                    danger_right[DANGER_ZONE_RIGHT_3] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_2):
                    danger_right[DANGER_ZONE_RIGHT_2] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_1):
                    danger_right[DANGER_ZONE_RIGHT_1] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_0):
                    danger_right[DANGER_ZONE_RIGHT_0] = True
            elif enemy.spawn == LEFT and enemy.alive:
                if self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_4):
                    danger_left[DANGER_ZONE_LEFT_4] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_3):
                    danger_left[DANGER_ZONE_LEFT_3] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_2):
                    danger_left[DANGER_ZONE_LEFT_2] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_1):
                    danger_left[DANGER_ZONE_LEFT_1] = True
                elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_LEFT_0):
                    danger_left[DANGER_ZONE_LEFT_0] = True
        return danger_left, danger_right
    
    def get_shoots_danger(self):
        danger_left  = {DANGER_SHOOT_LEFT:False}
        danger_right = {DANGER_SHOOT_RIGHT:False}
        for shoot in self.shoot_group:
            if shoot.orientation == RIGHT:
                if self.shoot_in_danger_zone(shoot,DANGER_SHOOT_LEFT): # si la orientacion es la izquierda, la danger zones sera la derecha, ya que vendra del respawn derecho
                    danger_left[DANGER_SHOOT_LEFT] = True
            elif shoot.orientation == LEFT:
                if self.shoot_in_danger_zone(shoot,DANGER_SHOOT_RIGHT):
                    danger_right[DANGER_SHOOT_RIGHT] = True
        return danger_left, danger_right

    def get_player_shoots_sections(self):
        danger_left  = {DANGER_ZONE_LEFT_0:False,DANGER_ZONE_LEFT_1:False,DANGER_ZONE_LEFT_2:False,DANGER_ZONE_LEFT_3:False,DANGER_ZONE_LEFT_4:False}
        danger_right = {DANGER_ZONE_RIGHT_0:False,DANGER_ZONE_RIGHT_1:False,DANGER_ZONE_RIGHT_2:False,DANGER_ZONE_RIGHT_3:False,DANGER_ZONE_RIGHT_4:False}
        for bullet in self.bullet_group:
            if bullet.orientation == RIGHT:
                if self.player_shoot_danger_zone(bullet,DANGER_ZONE_RIGHT_4):
                    danger_right[DANGER_ZONE_RIGHT_4] = True
                elif self.player_shoot_danger_zone(bullet,DANGER_ZONE_RIGHT_3):
                    danger_right[DANGER_ZONE_RIGHT_3] = True
                elif self.player_shoot_danger_zone(bullet,DANGER_ZONE_RIGHT_2):
                    danger_right[DANGER_ZONE_RIGHT_2] = True
                elif self.player_shoot_danger_zone(bullet,DANGER_ZONE_RIGHT_1):
                    danger_right[DANGER_ZONE_RIGHT_1] = True
                elif self.player_shoot_danger_zone(bullet,DANGER_ZONE_RIGHT_0):
                    danger_right[DANGER_ZONE_RIGHT_0] = True
            elif bullet.orientation == LEFT:
                if self.player_shoot_danger_zone(bullet,DANGER_ZONE_LEFT_4):
                    danger_left[DANGER_ZONE_LEFT_4] = True
                elif self.player_shoot_danger_zone(bullet,DANGER_ZONE_LEFT_3):
                    danger_left[DANGER_ZONE_LEFT_3] = True
                elif self.player_shoot_danger_zone(bullet,DANGER_ZONE_LEFT_2):
                    danger_left[DANGER_ZONE_LEFT_2] = True
                elif self.player_shoot_danger_zone(bullet,DANGER_ZONE_LEFT_1):
                    danger_left[DANGER_ZONE_LEFT_1] = True
                elif self.player_shoot_danger_zone(bullet,DANGER_ZONE_LEFT_0):
                    danger_left[DANGER_ZONE_LEFT_0] = True
        return danger_left, danger_right
    
    
    def get_n_enemies(self):
        danger_left, danger_right = self.get_enemies_danger()
        left = 0
        right = 0
        for section in danger_left.values():
            if section == True:
                left += 1
        for section in danger_right.values():
            if section == True:
                right += 1
        return left, right

    def get_n_shoots(self):
        danger_left, danger_right = self.get_player_shoots_sections()
        left = 0
        right = 0
        for section in danger_left.values():
            if section == True:
                left += 1
        for section in danger_right.values():
            if section == True:
                right += 1
        return left, right
        
    def is_player_blocking(self):
        if len(self.shield_group) >= 1:
            for shield in self.shield_group:
                return shield.orientation == LEFT, shield.orientation == RIGHT 
        return False, False
    def update(self,dt,zone=GAME):
        if zone == MENU:
            self.player_group.draw(self.screen)
            self.player_group.update(dt)
            return
        self.check_collisions()
        self.player_group.draw(self.screen)

        self.enemy_group.draw(self.screen)

        self.bullet_group.draw(self.screen)
        
        self.shield_group.draw(self.screen)
        
        self.shoot_group.draw(self.screen)
        
        if zone == GAME or zone == GAME_OVER:
            self.player_group.update(dt)
        if zone == GAME:
            self.enemy_group.update(dt)
            self.bullet_group.update(dt)
            self.shield_group.update(dt)
            self.shoot_group.update(dt)
            self.try_spawn()
            
        if DEBUG_MODE:
            pygame.draw.rect(self.screen,(0,0,255),self.player.hitbox,1)
            pygame.draw.line(self.screen,(255,255,255),(DANGER_ZONE_LEFT_0,0),(DANGER_ZONE_LEFT_0,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(255,255,255),(DANGER_ZONE_RIGHT_0-1,0),(DANGER_ZONE_RIGHT_0-1,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(0,255,255),(DANGER_ZONE_RIGHT_1,0),(DANGER_ZONE_RIGHT_1,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(0,255,255),(DANGER_ZONE_LEFT_1,0),(DANGER_ZONE_LEFT_1,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(0,255,255),(DANGER_ZONE_RIGHT_1,0),(DANGER_ZONE_RIGHT_1,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(0,255,0),(DANGER_ZONE_LEFT_2,0),(DANGER_ZONE_LEFT_2,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(0,255,0),(DANGER_ZONE_RIGHT_2,0),(DANGER_ZONE_RIGHT_2,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(255,255,0),(DANGER_ZONE_LEFT_3,0),(DANGER_ZONE_LEFT_3,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(255,255,0),(DANGER_ZONE_RIGHT_3,0),(DANGER_ZONE_RIGHT_3,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(255,0,0),(DANGER_ZONE_LEFT_4,0),(DANGER_ZONE_LEFT_4,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(255,0,0),(DANGER_ZONE_RIGHT_4,0),(DANGER_ZONE_RIGHT_4,BATTLE_SCREEN_HEIGHT),1)
            
            pygame.draw.line(self.screen,(255,0,255),(DANGER_SHOOT_LEFT,0),(DANGER_SHOOT_LEFT,BATTLE_SCREEN_HEIGHT),1)
            pygame.draw.line(self.screen,(255,0,255),(DANGER_SHOOT_RIGHT,0),(DANGER_SHOOT_RIGHT,BATTLE_SCREEN_HEIGHT),1)
            for enemy in self.enemy_group:
                pygame.draw.rect(self.screen,(255,0,0),enemy.rect,1)
            for shield in self.shield_group:
                pygame.draw.rect(self.screen,(0,255,255),shield.hitbox,1)
            for bullet in self.bullet_group:
                pygame.draw.rect(self.screen,(82, 198, 227),bullet.rect,1)
            for shoot in self.shoot_group:
                pygame.draw.rect(self.screen,(255,128,0),shoot.rect,1)

            pygame.draw.circle(self.screen,(255,0,255),(BATTLE_SCREEN_WIDTH/2,BATTLE_SCREEN_HEIGHT/2),5,50)
        
    def free(self):
        for sprite in self.player_group:
            sprite.kill()
        for sprite in self.enemy_group:
            sprite.kill()
        for sprite in self.bullet_group:
            sprite.kill()