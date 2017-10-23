import pygame, math, json
from tools import blit_text
from random import randrange
from objects import *
from constants import *
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
        self.walk_animation = char_info["sprite_width"]
        self.throw_animation = 0
        self.life = 100
        self.stones = 0
        self.money = 0
        self.char_json = char_json
        self.thrown_stones = []
        self.inventary = {}
         
    def update(self):
        self.rect.topleft = self.pos
         
    def move_char(self,keys_pressed, screen_size, blockers, npcs):
        '''For each key that is currently pressed down, move
        the rectangle of the player in the right direction
        '''
        pixels = 4
        prev_x = self.pos[0]
        prev_y = self.pos[1]

        if pygame.K_LEFT in keys_pressed or pygame.K_RIGHT in keys_pressed or pygame.K_UP in keys_pressed or pygame.K_DOWN in keys_pressed:
            self.walk()
        else:
            self.walk_animation = self.sprite_size[0]

        self.throw()

        for key in keys_pressed:
             #print self.pos
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
             else:
                 pass

        if self.checkcollisions(blockers) != -1 or self.checkcollisions(npcs) != -1:
            self.pos = [prev_x, prev_y]

        self.rect.move(self.pos)
        self.update()

    def throw_stone(self):
        self.thrown_stones.append(Thrown_Stone(self.pos, self.direction))
        self.throw(True)
        self.stones -= 1

    def get_sprite(self):
        if self.direction == 'down':
            y = 0
        elif self.direction == 'left':
            y = self.sprite_size[1]
        elif self.direction == 'right':
            y = 2*self.sprite_size[1]
        elif self.direction == 'up':
            y = 3*self.sprite_size[1]

        x = self.walk_animation + self.throw_animation

        return (x, y, self.sprite_size[0], self.sprite_size[1])

    def checkcollisions(self, obstacles):
        i = 0
        for obstacle in obstacles:
            dif_x = self.pos[0] - obstacle.pos[0]
            dif_y = self.pos[1] - obstacle.pos[1]
            if (dif_x > -self.sprite_size[0] and dif_x < obstacle.size[0]) and (dif_y > -self.sprite_size[1] and dif_y < obstacle.size[1]):
                return i
            i = i +1
        return -1

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.get_sprite())
        screen.blit(self.portrait, (0, 0, 32, 32))
        #Draw life bar
        pygame.draw.rect(screen, RED, (34, 2, 100, 4))
        pygame.draw.rect(screen, GREEN, (34, 2, self.life, 4))

        font = pygame.font.SysFont('Arial', 10)
        resources = str(self.stones) + " piedras\n" + str(self.money) + " euros"
        blit_text(screen, resources, (34, 8), font, (0, 0, 0))

        for stone in self.thrown_stones:
            stone.draw(screen)

    def update_stones(self, blockers, npcs, mobs):
        stopped_stones = []
        mob_hit = -1

        for stone in self.thrown_stones:
            stone.move()
            speed = stone.speed
            stone.checkcollisions(blockers)
            stone.checkcollisions(npcs)
            mob_hit = stone.checkcollisions(mobs)
            if mob_hit != -1:
                mobs[mob_hit].hit_by_stone(speed)
            if stone.speed < 1:
                stopped_stones.append(stone)
        for stone in stopped_stones:
            self.thrown_stones.remove(stone)

        return mob_hit

    def walk(self):
        if self.walk_animation == 0:
            self.walk_animation = 2*self.sprite_size[0]
        elif self.walk_animation == 2*self.sprite_size[0]:
            self.walk_animation = 0
        elif self.walk_animation == self.sprite_size[0]:
            self.walk_animation = 0

    def throw(self, new_throw = False):
        if self.throw_animation == 0:
            if new_throw:
                self.throw_animation = 3*self.sprite_size[0]
        elif self.throw_animation == 3*self.sprite_size[0]:
            self.throw_animation = 6*self.sprite_size[0]
        elif self.throw_animation == 6*self.sprite_size[0]:
            self.throw_animation = 0

    def dialog(self, screen, dialog, font):

         if type(dialog) ==list:
             aux = None
             for line in dialog:
                 if not aux:
                     aux = '  ' + line
                 else:
                     aux = aux + '\n  ' + line
             dialog = aux
         textbox = pygame.Surface((300, 100))
         textbox.fill(WHITE)
         blit_text(textbox, dialog, (0, 0), font, BLACK)

         pos = self.dialog_pos(screen)

         if self.portrait != None:
             pygame.draw.rect(screen, WHITE, (pos[0] -32, pos[1], 32, 32))
             screen.blit(self.portrait, (pos[0] -32, pos[1], 32, 32))
         screen.blit(textbox, pos)

         return pos

    def dialog_pos(self, screen):
         if self.pos[1] < screen.get_size()[1]/2:
             pos_y = self.pos[1] + self.sprite_size[1]
         else:
             pos_y = self.pos[1] - 100

         if self.pos[0] < screen.get_size()[0]/2:
             pos_x = self.pos[0]
             if self.portrait != None:
                 pos_x = pos_x + 32
         else:
             pos_x = self.pos[0] + self.sprite_size[0] - 300
         return (pos_x, pos_y)

    def hit_by_mob(self, mob):
        self.life -= mob.damage
        dif_x = self.pos[0] - mob.pos[0]
        dif_y = self.pos[1] - mob.pos[1]
        #self.pos = (self.pos[0] - dif_x * mob.damage, self.pos[1] - dif_y * mob.damage)
        self.pos[0] = self.pos[0] + int((dif_x * 6)/abs(dif_x))
        self.pos[1] = self.pos[1] + int((dif_y * 6)/abs(dif_y))
        self.update()

    def use_item(self, item_name):
        for i in range(self.inventary):
            if self.inventary[i][0] == item_name:
                self.inventary[i] = (self.inventary[i][0],self.inventary[i][1] - 1)
                if self.inventary[i][1] < 1:
                    del self.inventary[i]
                break

    def add_item(self, item_json, quantity):
        item_info = json.load(open(item_json))
        if self.has_item(item_info['name']):
            for i in range(self.inventary):
                if self.inventary[i][0] == item_name:
                    self.inventary[i] = (self.inventary[i][0],self.inventary[i][1] + quantity)
                    break
        else:
            self.inventary.append((Item(item_json), quantity))

    def has_item(self, item_name):
        for item in self.inventary:
            if item_name == item[0].name:
                return True
        return False

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
        self.dialog_sequence = char_info["dialog"]
        self.direction = direction
        self.rect = pygame.Rect(self.pos, self.size)
        self.size = self.rect.size

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.get_sprite())

    def get_sprite(self):
        if self.direction == 'down':
            y = 0
        elif self.direction == 'left':
            y = self.size[1]
        elif self.direction == 'right':
            y = 2*self.size[1]
        elif self.direction == 'up':
            y = 3*self.size[1]

        x = self.size[0]

        return (x, y, self.size[0], self.size[1])

    def dialog(self, screen, dialog, font, answer):

         if type(dialog) == list:
             dialog = dialog[answer]
         textbox = pygame.Surface((300, 100))
         textbox.fill(WHITE)
         blit_text(textbox, dialog, (0, 0), font, (0, 0, 0))

         pos = self.dialog_pos(screen)

         if self.portrait != None:
             pygame.draw.rect(screen, WHITE, (pos[0] -32, pos[1], 32, 32))
             screen.blit(self.portrait, (pos[0] -32, pos[1], 32, 32))
         screen.blit(textbox, pos)

         return pos

    def dialog_pos(self, screen):

         if self.pos[1] < screen.get_size()[1]/2:
             pos_y = self.pos[1] + self.size[1]
         else:
             pos_y = self.pos[1] - 100

         if self.pos[0] < screen.get_size()[0]/2:
             pos_x = self.pos[0]
             if self.portrait != None:
                 pos_x = pos_x + 32
         else:
             pos_x = self.pos[0] + self.size[0] - 300
         return (pos_x, pos_y)

    def rotate(self, pos):
         dif_x = self.pos[0] - pos[0]
         dif_y = self.pos[1] - pos[1]
         if abs(dif_y) < abs(dif_x):
             if dif_x > 0:
                 self.direction = 'left'
             else:
                 self.direction = 'right'
         else:
             if dif_y > 0:
                 self.direction = 'up'
             else:
                 self.direction = 'down'


class Mob(pygame.sprite.Sprite):

    def __init__(self, pos, direction, char_json):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        char_info = json.load(open(char_json))
        self.image = pygame.image.load(char_info["sprite"])
        self.sprite_size = (char_info["sprite_width"], char_info["sprite_height"])
        self.direction = direction
        self.rect = pygame.Rect(self.pos, self.sprite_size)
        self.size = self.rect.size
        self.speed = char_info["speed"]
        self.life = char_info["health"]
        self.health = self.life
        self.damage = char_info["damage"]
        self.char_json = char_json
        if char_info['event'] != None:
            self.event = Game_Event(char_info['event'])
        else:
            self.event = None
        self.animation = self.size[0]

    def update(self):
        self.rect.topleft = self.pos

    def move_mob(self, pos, limits, blockers):
        prev_pos = self.pos
        if self.distance(pos) < 50:
            self.animate()
            self.rotate(pos)
            dist = 2 * self.speed
            if self.direction == 'left':
                self.pos = (self.pos[0] - dist, self.pos[1])
            elif self.direction == 'right':
                self.pos = (self.pos[0] + dist, self.pos[1])
            elif self.direction == 'up':
                self.pos = (self.pos[0], self.pos[1] - dist)
            elif self.direction == 'down':
                self.pos = (self.pos[0], self.pos[1] + dist)            
        else:
            still = randrange(0, 2, 1)
            if not still:
                self.animate()
                dir_list = ['left', 'right', 'up', 'down']
                self.direction = dir_list[randrange(0, 3, 1)]
                dist = randrange(0, 2, 1)
                dist = dist * self.speed
                if self.direction == 'left':
                    self.pos = (self.pos[0] - dist, self.pos[1])
                elif self.direction == 'right':
                    self.pos = (self.pos[0] + dist, self.pos[1])
                elif self.direction == 'up':
                    self.pos = (self.pos[0], self.pos[1] - dist)
                elif self.direction == 'down':
                    self.pos = (self.pos[0], self.pos[1] + dist)
            else:
                self.animation = self.size[0]

        if self.pos[0] < 0 or self.pos[1] < 0 or self.pos[0] > limits[0] -self.size[0] or self.pos[1] > limits[1] -self.size[1] or (self.checkcollisions(blockers) != 1):
            self.pos = prev_pos
        self.update()

    def checkcollisions(self, obstacles):
        i = 0
        for obstacle in obstacles:
            dif_x = self.pos[0] - obstacle.pos[0]
            dif_y = self.pos[1] - obstacle.pos[1]
            if (dif_x > -self.sprite_size[0] and dif_x < obstacle.size[0]) and (dif_y > -self.sprite_size[1] and dif_y < obstacle.size[1]):
                return i
            i = i +1
        return -1

    def animate(self):
        if self.animation == 0:
            self.animation = 2*self.sprite_size[0]
        elif self.animation == 2*self.sprite_size[0]:
            self.animation = 0
        elif self.animation == self.sprite_size[0]:
            self.animation = 0

    def distance(self, pos):
        dif_x = self.pos[0] - pos[0]
        dif_y = self.pos[1] - pos[1]
        return math.sqrt(dif_x*dif_x + dif_y*dif_y)

    def rotate(self, pos):
         dif_x = self.pos[0] - pos[0]
         dif_y = self.pos[1] - pos[1]
         if abs(dif_y) < abs(dif_x):
             if dif_x > 0:
                 self.direction = 'left'
             else:
                 self.direction = 'right'
         else:
             if dif_y > 0:
                 self.direction = 'up'
             else:
                 self.direction = 'down'

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.get_sprite())
        pygame.draw.rect(screen, RED, (self.pos[0], self.pos[1] - 6, self.health, 4))
        pygame.draw.rect(screen, GREEN, (self.pos[0], self.pos[1] - 6, self.life, 4))

    def get_sprite(self):
        if self.direction == 'down':
            y = 0
        elif self.direction == 'left':
            y = self.size[1]
        elif self.direction == 'right':
            y = 2*self.size[1]
        elif self.direction == 'up':
            y = 3*self.size[1]

        x = self.animation

        return (x, y, self.size[0], self.size[1])

    def hit_by_stone(self, speed):
        self.life -= speed

class Thrown_Stone(pygame.sprite.Sprite):
    '''Thrown stones are technically an object but they're associated to a playable character'''
    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 12
        self.pos = pos
        self.direction = direction
        self.image = pygame.image.load('images/thrown_stone.png')
        self.sprite_size = (12, 12)
        self.rect = pygame.Rect(self.pos, self.sprite_size)
        self.size = self.rect.size

    def update(self):
        self.rect.topleft = self.pos

    def move(self):
        self.image = pygame.transform.rotate(self.image, self.speed)
        dist = self.speed
        if self.direction == 'left':
            self.pos = (self.pos[0] - dist, self.pos[1])
        elif self.direction == 'right':
            self.pos = (self.pos[0] + dist, self.pos[1])
        elif self.direction == 'up':
            self.pos = (self.pos[0], self.pos[1] - dist)
        elif self.direction == 'down':
            self.pos = (self.pos[0], self.pos[1] + dist)

        self.update()
        self.speed -= 1

    def checkcollisions(self, obstacles):
        i = 0
        for obstacle in obstacles:
            dif_x = self.pos[0] - obstacle.pos[0]
            dif_y = self.pos[1] - obstacle.pos[1]
            if (dif_x > -self.sprite_size[0] and dif_x < obstacle.size[0]) and (dif_y > -self.sprite_size[1] and dif_y < obstacle.size[1]):
                self.speed = 0
                return i
            i = i +1
        return -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
