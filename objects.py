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
