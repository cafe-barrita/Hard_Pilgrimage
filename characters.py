import pygame, math, json
from pygame.locals import *

class Main_Character(pygame.sprite.Sprite):
    '''The main character of the game.
     
    Attributes
        pos     -- position on the screen
        image   -- surface object representing the player
        rect    -- rectangle of the the main character
    '''
    def __init__(self, char_json):
        pygame.sprite.Sprite.__init__(self)
        self.pos = [0,0]
        char_info = json.load(open(char_json))
        self.image = pygame.image.load(char_info["sprite"])
        self.portrait = pygame.image.load(char_info["portrait"])
        self.sprite_size = (char_info["sprite_width"], char_info["sprite_height"])
        self.direction = 'down'
        self.rect = pygame.Rect(self.pos, self.sprite_size)
        self.size = self.rect.size
        self.animation = char_info["sprite_height"]
        self.life = 100
        self.stones = 0
        self.money = 0
        self.char_json = char_json
        self.thrown_stones = []
         
    def update(self):
        self.rect.topleft = self.pos
         
    def move_char(self,keys_pressed, screen_size, blockers, npcs):
        '''For each key that is currently pressed down, move
        the rectangle of the player in the right direction
        '''
        pixels = 4
        prev_x = self.pos[0]
        prev_y = self.pos[1]

        #if pygame.K_LEFT in keys_pressed or pygame.K_RIGHT in keys_pressed or pygame.K_UP in keys_pressed or pygame.K_DOWN in keys_pressed:
        #    self.walk_animation()
        #else:
        #    self.animation = self.sprite_size[0]
        #print self.animation

        for key in keys_pressed:
             print self.pos
             if key == pygame.K_LEFT:
                 self.pos[0] = self.pos[0] - pixels
                 if self.pos[0] < 0:
                     self.pos[0] = 0 
                 self.direction = 'left'
     
             elif key == pygame.K_RIGHT:
                 self.pos[0] = self.pos[0] + pixels 
                 if self.pos[0] > (screen_size[0] - self.sprite_size[0]):
                     self.pos[0] = screen_size[0] - self.sprite_size[0]
                 self.direction = 'right' 

             elif key == pygame.K_UP:
                 self.pos[1] = self.pos[1] - pixels 
                 if self.pos[1] < 0:
                     self.pos[1] = 0
                 self.direction = 'up'  
   
             elif key == pygame.K_DOWN:
                 self.pos[1] = self.pos[1] + pixels 
                 if self.pos[1] > (screen_size[1] - self.sprite_size[1]):
                     self.pos[1] = screen_size[1] - self.sprite_size[1]
                 self.direction = 'down'

        if self.checkcollisions(blockers) != -1:
            self.pos = [prev_x, prev_y]

        self.rect.move(self.pos)
        self.update()

    def get_sprite(self):
        if self.direction == 'down':
            y = 0
        elif self.direction == 'left':
            y = self.sprite_size[1]
        elif self.direction == 'right':
            y = 2*self.sprite_size[1]
        elif self.direction == 'up':
            y = 3*self.sprite_size[1]

        x = self.animation

        return (x, y, self.sprite_size[0], self.sprite_size[1])

    def checkcollisions(self, obstacles):
        i = 0
        for obstacle in obstacles:
            dif_x = self.pos[0] - obstacle.pos[0]
            dif_y = self.pos[1] - obstacle.pos[1]
            if (dif_x > self.sprite_size[0] and dif_x < obstacle.size[0]) and (dif_y > self.sprite_size[1] and dif_y < obstacle.size[1]):
                return i
            i = i +1
        return -1

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.get_sprite())

    def walk_animation(self):
        if self.animation == 0:
            self.animation = 2*self.sprite_size[0]
        elif self.animation == 2*self.sprite_size[0]:
            self.animation = 0
        elif self.animation == self.sprite_size[0]:
            self.animation = 0

class NonPlayableCharacter(pygame.sprite.Sprite):

    def __init__(self, pos, direction, char_json):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        char_info = json.load(open(char_json))
        self.image = pygame.image.load(char_info["sprite"])
        if char_info["portrait"]:
            self.portrait = pygame.image.load(char_info["portrait"])
        else:
            self.portrait = None
        self.size = (char_info["sprite_width"], char_info["sprite_height"])
        self.direction = direction
        self.rect = pygame.Rect(self.pos, self.sprite_size)
        self.size = self.rect.size

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Mob(pygame.sprite.Sprite):

    def __init__(self, pos, direction, char_json):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        char_info = json.load(open(char_json))
        self.image = pygame.image.load(char_info["sprite"])
        if char_info["portrait"]:
            self.portrait = pygame.image.load(char_info["portrait"])
        else:
            self.portrait = None
        self.sprite_size = (char_info["sprite_width"], char_info["sprite_height"])
        self.direction = direction
        self.rect = pygame.Rect(self.pos, self.sprite_size)
        self.size = self.rect.size

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class ThrownStone(pygame.sprite.Sprite):
    '''Thrown stones are technically an object but they're associated to a playable charachter'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pass
