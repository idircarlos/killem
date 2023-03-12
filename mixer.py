import pygame.mixer
pygame.mixer.init()
from util.settings import *
import random

SHOOT_SOUND = 0
ENEMY_DEATH_SOUND = 1


class Music:
    
    def __init__(self,file_path,vol=1.0):
        pygame.mixer.music.load(file_path)
        self.vol = vol
        pygame.mixer.music.set_volume(vol)
        
    def play(self):
        pygame.mixer.music.play(-1,0)
        
    def mute(self):
        if pygame.mixer.music.get_volume() != 0:
            pygame.mixer.music.set_vol(self.vol)
        else:
            pygame.mixer.music.set_vol(0)
        

class Sound:
    
    def __init__(self,file_path,vol=1.0):
        self.sound = pygame.mixer.Sound(file_path)
        self.vol = vol
        self.sound.set_volume(vol)
        self.is_mute = False
        
    def play(self):
        self.sound.play()
        
    def mute(self):
        if not self.is_mute:
            self.sound.set_volume(0)
        else:
            self.sound.set_volume(self.vol)
        self.is_mute = not self.is_mute

class Mixer:
    
    def __init__(self):
        self.bg_music = []
        self.sounds = {SHOOT_SOUND:[],ENEMY_DEATH_SOUND:[]}
        self.current_music = 0
        self.vol = 0.15
        self.is_mute = False
        
    def _add_bg_music(self,bg_music_files):
        for bg_music in bg_music_files: 
            self.bg_music.append(bg_music)
    
    def _add_sound(self,key,sound_file,vol):
        sound = Sound(sound_file,vol)
        self.sounds[key].append(sound)
        
    def start_loop_bg_music(self):
        pygame.mixer.music.load(self.bg_music[0])
        pygame.mixer.music.set_volume(self.vol)
        pygame.mixer.music.play()
        
    def play_next_bg_music_if_needed(self):
        if not pygame.mixer.music.get_busy():
            # Actualizar el índice de canción actual y volver al principio de la lista si llegamos al final
            self.current_music = (self.current_music + 1) % len(self.bg_music)
            # Cargar y reproducir la siguiente canción en la lista
            pygame.mixer.music.load(self.bg_music[self.current_music])
            pygame.mixer.music.play()

    def clear_queue(self):
        pygame.mixer.music.stop()
        
    def mute(self):
        if not self.is_mute:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.vol)
        for list_sound in self.sounds.values():
                for sound in list_sound:
                    sound.mute()
        self.is_mute = not self.is_mute
        
    def play(self,key):
        sound = random.choice(self.sounds[key])
        sound.play()
        
        
def _create_mixer():
        mixer = Mixer()
        mixer._add_bg_music([BG_MUSIC_AUDIO_1,BG_MUSIC_AUDIO_2])
        
        mixer._add_sound(SHOOT_SOUND,SHOOT_PATH_1,0.05)
        mixer._add_sound(SHOOT_SOUND,SHOOT_PATH_2,0.05)
        mixer._add_sound(SHOOT_SOUND,SHOOT_PATH_3,0.05)
        mixer._add_sound(SHOOT_SOUND,SHOOT_PATH_4,0.05)
        
        mixer._add_sound(ENEMY_DEATH_SOUND,DEATH_PATH_1,0.15)
        mixer._add_sound(ENEMY_DEATH_SOUND,DEATH_PATH_2,0.15)
        mixer._add_sound(ENEMY_DEATH_SOUND,DEATH_PATH_3,0.15)
        mixer._add_sound(ENEMY_DEATH_SOUND,DEATH_PATH_4,0.15)
        return mixer

GLOBAL_MIXER = _create_mixer()