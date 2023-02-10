import pygame
from player import *
from enemy  import *
from bullet import *
from respawn import *
from rand import Rand

class EntityManager:
    def __init__(self,screen,clock):
        self.screen = screen
        self.rand = Rand()
        self.player = Player()
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.left_respawn  = Spawn(LEFT,clock,self.rand)
        self.right_respawn  = Spawn(RIGHT,clock,self.rand)
        self.enemy_group = pygame.sprite.Group()
        self.clock = clock
        
    def player_attack(self):
        can_attack = self.player.attack()
        if can_attack:
            self.bullet_group.add(Bullet(self.player.hitbox,self.player.orientation))
            
    def player_block(self):
        if not self.player.is_animating:
            self.player.block()
        
    def player_flip(self,dir):
        self.player.flip(dir)
            
    def try_spawn(self):
        if self.left_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.left_respawn.x,self.left_respawn.y),(0,0,0,0),RIGHT if self.left_respawn.position is LEFT else LEFT))
        if self.right_respawn.try_spawn():
            self.enemy_group.add(Enemy((self.right_respawn.x,self.right_respawn.y),(0,0,0,0),RIGHT if self.right_respawn.position is LEFT else LEFT))
            
    def check_collisions(self):
        for bullet in self.bullet_group:
            for enemy in self.enemy_group:
                if enemy.orientation == LEFT:
                    if bullet.rect.x + bullet.rect.width >= enemy.rect.x + int(enemy.rect.width/2 + 25) and enemy.alive:
                        print(bullet.rect.x, enemy.rect.x)
                        enemy.alive = False
                        #enemy.kill()
                        #self.enemy_group.remove(enemy)
                        bullet.kill()
                else:
                    if bullet.rect.x <= enemy.rect.x + (enemy.rect.width/2 - 25) and enemy.alive:
                        enemy.kill()
                        bullet.kill()
                        pass
            
    def update(self):
        self.check_collisions()
        self.player_group.draw(self.screen)
        self.player_group.update()
        self.enemy_group.draw(self.screen)
        self.enemy_group.update()
        self.bullet_group.draw(self.screen)
        self.bullet_group.update()
        self.try_spawn()