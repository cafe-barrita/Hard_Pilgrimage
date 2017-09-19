import pygame, sys
from pygame.locals import *
from hard_pilgrimage import Hard_Pilgrimage

def main():
    '''Starting point of the game'''
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    HP_instance = Hard_Pilgrimage(screen)
    while True:
         HP_instance.main_loop()
         pygame.display.flip()

if __name__ == '__main__':
    main()
