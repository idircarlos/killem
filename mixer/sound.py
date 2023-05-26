import pygame.mixer
pygame.mixer.init()

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