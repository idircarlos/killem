import pygame
from player import *
from enemy  import *
from bullet import *
from shield import *
from shoot import *
from respawn import *
from shoot_respawn import *
from rand import Rand
from debug import *
from mixer import GLOBAL_MIXER, SHOOT_SOUND, ENEMY_DEATH_SOUND

PLAYER_DEAD = 0
ENEMY_DEAD  = 1
SHOOT_BLOCKED = 2

class EntityManager:
    def __init__(self,screen,clock,assets):
        self.screen = screen
        self.rand = Rand()
        self.player = Player(assets["player"])
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.shield_group = pygame.sprite.Group()
        self.shoot_group = pygame.sprite.Group()
        self.left_respawn  = Spawn(LEFT,clock,self.rand)
        self.right_respawn  = Spawn(RIGHT,clock,self.rand)
        self.top_respawn  = Spawn(TOP,clock,self.rand)
        self.bottom_respawn  = Spawn(BOTTOM,clock,self.rand)
        self.shoot_respawn = ShootRespawn(clock,self.rand)
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
            self.bullet_group.add(Bullet(self.player.hitbox,self.player.orientation,self.assets["bullet"]))
            GLOBAL_MIXER.play(SHOOT_SOUND)
            
    def player_block(self,orientation):
        can_block = self.player.block()
        if can_block:
            self.shield_group.add(Shield(orientation,self.assets["block"]))
        
    def player_flip(self,dir):
        self.player.flip(dir)
            
    def try_spawn(self):
        if self.left_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.left_respawn.x,self.left_respawn.y),(0,0,0,0),self.assets["enemy"],LEFT))
        if self.right_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.right_respawn.x,self.right_respawn.y),(0,0,0,0),self.assets["enemy"],RIGHT))
        if self.top_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.top_respawn.x,self.top_respawn.y),(0,0,0,0),self.assets["enemy"],TOP))
        if self.bottom_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.bottom_respawn.x,self.bottom_respawn.y),(0,0,0,0),self.assets["enemy"],BOTTOM))
            
        if self.shoot_respawn.try_spawn():
            data = self.shoot_respawn.generate_shoot_pos()
            self.shoot_group.add(Shoot(data["coords"],data["orientation"],self.assets["shoot"]))

    
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
            
    def check_collisions(self):
        for bullet in self.bullet_group:
            for enemy in self.enemy_group:
                if enemy.spawn == RIGHT:
                    if pygame.Rect.colliderect(bullet.rect,enemy.rect) and bullet.rect.x + bullet.rect.width >= enemy.rect.x + int(enemy.rect.width/2 + 25) and (enemy.spawn != TOP and enemy.spawn != BOTTOM) and enemy.alive:
                        danger_zone = 0
                        if self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_4):
                            danger_zone = DANGER_ZONE_RIGHT_4
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_3):
                            danger_zone = DANGER_ZONE_RIGHT_3
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_2):
                            danger_zone = DANGER_ZONE_RIGHT_2
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_1):
                            danger_zone = DANGER_ZONE_RIGHT_1
                        elif self.enemy_in_danger_zone(enemy,DANGER_ZONE_RIGHT_0):
                            danger_zone = DANGER_ZONE_RIGHT_0
                        enemy.alive = False
                        GLOBAL_MIXER.play(ENEMY_DEATH_SOUND)
                        #enemy.kill()
                        #self.enemy_group.remove(enemy)
                        enemy.animate("dead")
                        bullet.kill()
                        #print(str(round(bullet.timer,5)))
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
                        #enemy.kill()
                        enemy.animate("dead")
                        bullet.kill()
                        #print(str(round(bullet.timer,5)))
                        return ENEMY_DEAD, danger_zone
        for enemy in self.enemy_group:
            if pygame.Rect.colliderect(self.player.hitbox,enemy.rect):
                self.player.kill()
                return PLAYER_DEAD, -1
        for shoot in self.shoot_group:
            if pygame.Rect.colliderect(self.player.hitbox,shoot.rect):
                self.player.kill()
                shoot.kill()
                print("TOCADO")
                return PLAYER_DEAD, -1
            for shield in self.shield_group:
                if pygame.Rect.colliderect(shield.hitbox,shoot.rect):
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
    
    def is_player_blocking(self):
        if len(self.shield_group) >= 1:
            for shield in self.shield_group:
                #print(shield.orientation)
                return shield.orientation == LEFT, shield.orientation == RIGHT 
        return False, False
    def update(self,dt):
        if TRAINING:
            dt = 1
        self.check_collisions()
        self.player_group.draw(self.screen)
        self.player_group.update(dt)
        self.enemy_group.draw(self.screen)
        self.enemy_group.update(dt)
        self.bullet_group.draw(self.screen)
        self.bullet_group.update(dt)
        self.shield_group.draw(self.screen)
        self.shield_group.update(dt)
        self.shoot_group.draw(self.screen)
        self.shoot_group.update(dt)
        self.try_spawn()
        #pygame.draw.rect(self.screen,(0,255,0),self.player.rect,1)
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
            #pygame.draw.rect(self.screen,(255,0,0),enemy.rect,1)
            #pygame.draw.circle(self.screen,(0,0,255),(enemy.rect.x,enemy.rect.y),10,20)
            #pygame.draw.line(self.screen,(0,255,255),(CENTER_X,CENTER_Y),(SCREEN_WIDTH,SCREEN_HEIGHT))
            #pygame.draw.line(self.screen,(0,255,255),(CENTER_X,CENTER_Y),(SCREEN_WIDTH/2,SCREEN_HEIGHT))
            #pygame.draw.line(self.screen,(0,255,255),(CENTER_X,CENTER_Y),(SCREEN_WIDTH,SCREEN_HEIGHT/2))
            pass
        #pygame.draw.circle(self.screen,(0,0,255),(CENTER_X,CENTER_Y),10,20)
        for shield in self.shield_group:
            #pygame.draw.rect(self.screen,(0,255,255),shield.hitbox,1)
            pass
            
        for shoot in self.shoot_group:
            #pygame.draw.rect(self.screen,(255,255,0),shoot.rect,1)
            #record_text = self.font.render("dy: " +str(round(shoot.dy*dt*TARGET_FPS)), False, (255,255,255))
            #self.screen.blit(record_text, shoot.rect)
            #print("XD")
            pass
        
        #pygame.draw.circle(self.screen,(255,0,255),(BATTLE_SCREEN_WIDTH/2,BATTLE_SCREEN_HEIGHT/2),10,100)
        
    def free(self):
        for sprite in self.player_group:
            sprite.kill()
        for sprite in self.enemy_group:
            sprite.kill()
        for sprite in self.bullet_group:
            sprite.kill()
            print(str(round(sprite.timer,5)))