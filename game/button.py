import pygame
from mixer.mixer import GLOBAL_MIXER, OPTION_CHANGE


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_1 = self.font.render(self.text_input, True, pygame.Color("#536878"))
        if self.image is None:
            self.image = self.text
            self.image_1 = self.text_1
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rect_1 = self.image_1.get_rect(center=(self.x_pos + 3, self.y_pos + 3))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect_1 = self.text_1.get_rect(center=(self.x_pos + 3, self.y_pos + 3))
        self.entered = False

    def update(self, screen):
        screen.blit(self.text_1, self.text_rect_1)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position, option_selected, using_mouse, play_sound=True):
        option_selected = None if using_mouse == True else option_selected
        position = (0,0) if using_mouse == False else position
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom) or option_selected == self.text_input:
            if not self.entered and play_sound:
                GLOBAL_MIXER.play(OPTION_CHANGE)
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.text_rect = self.text.get_rect(center=(self.x_pos+2, self.y_pos+2))
            self.text_rect_1 = self.text_1.get_rect(center=(self.x_pos + 5, self.y_pos + 5))
            self.entered = True
            return (True,self.text_input)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
            self.text_rect_1 = self.text.get_rect(center=(self.x_pos+3, self.y_pos+3))
            self.entered = False
            return (False,self.text_input)