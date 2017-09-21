import pygame, math, json
from pygame.locals import *

class Object(pygame.sprite.Sprite):

    def __init__(self, pos, size, image=None):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.size = size
        if image != None:
            self.image = pygame.image.load(image)
        else:
            self.image = None

    def draw(self, screen):
        if self.image != None:
            screen.blit(self.image, self.pos)

class Portal(pygame.sprite.Sprite):

    def __init__(self, pos, size, next_map, image=None):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.size = size
        if image != None:
            self.image = pygame.image.load(image)
        else:
            self.image = None
        self.next_map = next_map

    def draw(self, screen):
        if self.image != None:
            screen.blit(self.image, self.pos)

class Game_Event():

    def __init__(self, game, event_dict):
        self.game = game
        self.type = event_dict['type']

        if self.type == 'dialog':
            self.dialog = event_dict['dialog']
            self.interlocutor = event_dict['interlocutor']
        elif self.type == 'reward':
            self.reward_type = event_dict['reward_type']
            self.reward_quantity = event_dict['reward']
        elif self.type == 'update_protagonist':
            self.char_json = event_dict['char_json']
        elif self.type == 'restore_health':
            self.char_json = event_dict['char_json']
        else:
            self.game.current_state = 'ERROR_STATE'

    def trigger_event(self):
        if self.type == 'dialog':
            self.start_dialog()
        elif self.type == 'reward':
            self.give_reward()
        elif self.type == 'update_protagonist':
            self.update_protagonist()
        elif self.type == 'restore_health':
            self.game.main_char.life = 100

    def start_dialog(self):
        self.game.current_state = 'DIALOG_STATE'
        self.game.dialog_sequence = self.dialog
        self.game.interlocutor = self.interlocutor

    def give_reward(self):
        if self.reward_type == 'money':
            units = ' euros'
            self.game.main_char.money += self.reward_quantity
        elif self.reward_type == 'stones':
            units = ' piedras'
            self.game.main_char.stones += self.reward_quantity

        self.game.current_state = 'DIALOG_STATE'
        self.game.dialog_sequence = [None, "He conseguido "+str(self.reward_quantity)+units]

    def update_protagonist(self):
        self.game.main_char.char_json = self.char_json
        char_info = json.load(open(self.char_json))
        self.image = pygame.image.load(char_info["sprite"])
        self.portrait = pygame.image.load(char_info["portrait"])
        self.sprite_size = (char_info["sprite_width"], char_info["sprite_height"])
        self.rect = pygame.Rect(self.pos, self.sprite_size)
        self.size = self.rect.size
        self.animation = char_info["sprite_width"]

