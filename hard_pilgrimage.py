import pygame, math, sys, json, time
from pygame.locals import *
from tools import *
from characters import *
from objects import *

class Hard_Pilgrimage():
    '''Main class of the game, It will contain the state machine and all its methods'''
    def __init__(self, screen):
        self.screen = screen
        self.main_char = None
        self.NPCs = []
        self.mobs = []
        self.stones = []
        self.portals = []
        self.current_state = 'MAIN_TITLE'
        self.KEYSPRESSED = []
        self.saved_games = []
        self.current_map = None
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((0, 0, 0))
        self.title_font = pygame.font.SysFont('Arial', 60)
        self.subtitle_font = pygame.font.SysFont('Arial', 40)
        self.text_font = pygame.font.SysFont('Arial', 24)
        self.arrow_pos = (75, 300)
        self.interlocutor = None
        self.dialog_sequence = []
        self.dialog_index = 0

    def main_loop(self):
        '''Main loop method. It will call the method associated with the correspondent state'''

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                self.KEYSPRESSED.append(event.key)
            if event.type == KEYUP:
                self.KEYSPRESSED.remove(event.key)
            else:
                pass

            if self.current_state == 'MAIN_TITLE':
                self.main_title()
            elif self.current_state == 'NEW_GAME':
                self.new_game()
            elif self.current_state == 'LOAD_GAME':
                self.load_game()
            elif self.current_state == 'MAP_STATE':
                self.map_state()
            elif self.current_state == 'DIALOG_STATE':
                self.dialog_state()
            elif self.current_state == 'MENU_STATE':
                self.menu_state()
            elif self.current_state == 'CREDITS_STATE':
                self.roll_credits()
            elif self.current_state == 'SAVE_GAME':
                self.save_game()
            elif self.current_state == 'CONTROLS_STATE':
                self.control_state()            
            else:
                self.background = pygame.Surface(self.screen.get_size())
                self.background.fill((0, 0, 0))
                self.error()

    def main_title(self):
        self.screen.blit(self.background, (0,0))
        blit_text(self.screen, 'Hard Pilgrimage', (100, 150), self.title_font, (255, 255, 255))
        blit_text(self.screen, 'Road to Cardiff', (175, 215), self.subtitle_font, (255, 255, 255))
        blit_text(self.screen, 'Nueva partida', (100, 300), self.text_font, (255, 255, 255))
        blit_text(self.screen, 'Cargar partida', (375, 300), self.text_font, (255, 255, 255))

        for key in self.KEYSPRESSED:
            if key == pygame.K_LEFT:
                if self.arrow_pos[0] == 350:
                    self.arrow_pos = (75, 300)
            elif key == pygame.K_RIGHT:
                if self.arrow_pos[0] == 75:
                    self.arrow_pos = (350, 300)
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                if self.arrow_pos[0] == 75:
                    #Start new game
                    self.current_state = 'NEW_GAME'
                    return
                if self.arrow_pos[0] == 350:
                    f = open('data/saved_games.json')
                    self.saved_games = json.load(f)
                    f.close()
                    self.arrow_pos = (160, 100)
                    self.current_state = 'LOAD_GAME'
                    return
            else:
                pass

        vertices = [self.arrow_pos, (self.arrow_pos[0], self.arrow_pos[1]+24), (self.arrow_pos[0]+12, self.arrow_pos[1]+12)]
        pygame.draw.polygon(self.screen, (255, 0, 0), vertices)

    def error(self):
        self.screen.blit(self.background, (0,0))
        blit_text(self.screen, 'Ingame error', (150, 200), self.title_font, (255, 0, 0))  

    def new_game(self):
        self.main_char = Main_Character('data/duro.json')
        self.load_map('data/test_background.json')
        self.current_state = 'MAP_STATE'

    def load_game(self):
        
        self.screen.blit(self.background, (0,0))
        i = 0
        for game in self.saved_games:
            blit_text(self.screen, game, (200, 100+i), self.subtitle_font, (255, 255, 255))
            i = i + 40

        for key in self.KEYSPRESSED:
            if key == pygame.K_DOWN:
                if self.arrow_pos[1] < 60 + i:
                    self.arrow_pos = (160, self.arrow_pos[1]+40)
            elif key == pygame.K_UP:
                if self.arrow_pos[1] > 100:
                    self.arrow_pos = (160, self.arrow_pos[1]-40)
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                i = 0
                for game in self.saved_games:
                    if self.arrow_pos[1] == 100 + i:
                        saved_data = self.saved_games[game]
                        self.main_char = Main_Character(saved_data['char_json'])

                        self.main_char.stones = saved_data['stones']
                        self.main_char.life = saved_data['health']
                        self.load_map(saved_data['map'])
                        self.main_char.pos = saved_data['pos']
                        self.main_char.direction = saved_data['direction']
                        self.main_char.update()
                        self.mobs = saved_data['mobs']
                        self.current_state = 'MAP_STATE'
                        return
                    i = i +40
            else:
                pass

        vertices = [self.arrow_pos, (self.arrow_pos[0], self.arrow_pos[1]+40), (self.arrow_pos[0]+20, self.arrow_pos[1]+20)]
        pygame.draw.polygon(self.screen, (255, 0, 0), vertices)

    def map_state(self):

        if pygame.K_RETURN in self.KEYSPRESSED:
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill((0, 0, 0))
            self.arrow_pos = (160, 100)
            self.current_state = 'MENU_STATE'
            return

        self.screen.blit(self.background, (0,0))
        self.main_char.draw(self.screen)
        self.main_char.move_char(self.KEYSPRESSED, self.screen.get_size(), self.blockers, self.NPCs)

        if self.blockers:
            for blocker in self.blockers:
                blocker.draw(self.screen)
        if self.NPCs:
            for npc in self.NPCs:
                npc.draw(self.screen)
        if self.mobs:
            for mob in self.mobs:
                mob.draw(self.screen)
        if self.stones:
            for stone in self.stones:
                stone.draw(self.screen)
        if self.portals:
            for portal in self.portals:
                portal.draw(self.screen)

        portal_index = self.main_char.checkcollisions(self.portals)
        if portal_index != -1:
            self.load_map(self.portals[portal_index]['next_map'])
            return

    def dialog_state(self):
        self.screen.blit(self.background, (0,0))
        self.main_char.draw(self.screen)
        for blocker in self.blockers:
            blocker.draw(self.screen)
        for npc in self.NPCs:
            npc.draw(self.screen)
        for mob in self.mobs:
            mob.draw(self.screen)
        for stone in self.stones:
            stone.draw(self.screen)
        for portal in self.portals:
            portal.draw(self.screen)

        if self.dialog_index % 2:
            self.main_char.dialog(self.screen, self.dialog_sequence[self.dialog_index], self.text_font)
        else:
            self.interlocutor.dialog(self.screen, self.dialog_sequence[self.dialog_index], self.text_font)

        self.dialog_index = self.dialog_index + 1

        if len(self.dialog_sequence) < self.dialog_index + 1:
            self.dialog_index = 0
            self.current_state = 'MAP_STATE'

    def menu_state(self):
        #TODO change state according to option selected.
        self.screen.blit(self.background, (0, 0))
        menu_options = "Back to game \nMain Title \nShow controls \nSave game \nExit"
        blit_text(self.screen, menu_options, (200, 100), self.subtitle_font, (255, 255, 255))

        for key in self.KEYSPRESSED:
            if key == pygame.K_DOWN:
                if self.arrow_pos[1] < 280:
                    self.arrow_pos = (160, self.arrow_pos[1]+45)
            elif key == pygame.K_UP:
                if self.arrow_pos[1] > 100:
                    self.arrow_pos = (160, self.arrow_pos[1]-45)
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                if self.arrow_pos[1] == 100:
                    #Return to map state
                    self.current_state = 'MAP_STATE'
                    map_data = json.load(open(self.current_map))
                    self.background = pygame.image.load(map_data['image'])
                    self.background = pygame.transform.scale(self.background, self.screen.get_size())
                if self.arrow_pos[1] == 145:
                    #Return to main title
                    self.background = pygame.Surface(self.screen.get_size())
                    self.background.fill((0, 0, 0))
                    self.arrow_pos = (75, 300)
                    self.current_state = 'MAIN_TITLE'
                elif self.arrow_pos[1] == 190:
                    #Show  controls
                    pass
                elif self.arrow_pos[1] == 235:
                    #Save game
                    self.current_state = 'SAVE_GAME'
                    f = open('data/saved_games.json')
                    self.saved_games = json.load(f)
                    f.close()
                    self.arrow_pos = (160, 100)
                elif self.arrow_pos[1] == 280:
                    #Exit game
                    pygame.quit()
                    sys.exit(0)
            else:
                pass

        vertices = [self.arrow_pos, (self.arrow_pos[0], self.arrow_pos[1]+40), (self.arrow_pos[0]+20, self.arrow_pos[1]+20)]
        pygame.draw.polygon(self.screen, (255, 0, 0), vertices)

    def roll_credits(self):
        '''Display credits and return to main title'''
        pass

    def save_game(self):

        self.screen.blit(self.background, (0,0))
        i = 0
        for game in self.saved_games:
            blit_text(self.screen, game, (200, 100+i), self.subtitle_font, (255, 255, 255))
            i = i + 40
        if len(self.saved_games) < 5:
            blit_text(self.screen, 'New', (200, 100+i), self.subtitle_font, (255, 255, 255))
            i = i + 40
        blit_text(self.screen, 'Back', (200, 100+i), self.subtitle_font, (255, 255, 255))

        for key in self.KEYSPRESSED:
            if key == pygame.K_DOWN:
                if self.arrow_pos[1] < 100 + i:
                    self.arrow_pos = (160, self.arrow_pos[1]+40)
            elif key == pygame.K_UP:
                if self.arrow_pos[1] > 100:
                    self.arrow_pos = (160, self.arrow_pos[1]-40)
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                if self.arrow_pos[1] == 100 + i:
                    #Return to menu state
                    self.current_state = 'MENU_STATE'
                    self.arrow_pos = (160, 100)
                else:
                    #Save game
                    t = time.localtime()
                    t_str = str(t.tm_year)+'/'+str(t.tm_mon)+'/'+str(t.tm_mday)+' '+str(t.tm_hour)+':'+str(t.tm_min)
                    current_game = {'char_json': self.main_char.char_json, 'health': self.main_char.life, 'stones': self.main_char.stones, 'money': self.main_char.money, 'pos': self.main_char.pos, 'direction': self.main_char.direction, 'map': self.current_map, 'mobs': self.mobs}
                    i = 0
                    for game in self.saved_games:
                        if self.arrow_pos[1] == 100 + i:
                            del self.saved_games[game]
                            break
                        i = i + 40
                    self.saved_games[t_str] = current_game
                    f = open('data/saved_games.json', 'w')
                    json.dump(self.saved_games, f)
                    f.close()
            else:
                pass

        vertices = [self.arrow_pos, (self.arrow_pos[0], self.arrow_pos[1]+40), (self.arrow_pos[0]+20, self.arrow_pos[1]+20)]
        pygame.draw.polygon(self.screen, (255, 0, 0), vertices)

    def control_state(self):
        '''Method correspondent with the controls menu. Meant to display keys used. Possibility to extend functionality by personalizing controls'''
        pass

    def load_map(self, map_json):
        map_data = json.load(open(map_json))
        self.background = pygame.image.load(map_data['image'])
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.main_char.pos = map_data['initial_pos']
        self.main_char.direction = map_data['initial_direction']
        self.main_char.update()
        self.blockers = []
        for blocker in map_data['blockers']:
            self.blockers.append(Object(tuple(blocker['pos']), tuple(blocker['size']), blocker['image']))
        self.NPCs = []
        for npc in map_data['NPCs']:
            self.NPCs.append(NonPlayableCharacter(tuple(npc['pos']), npc['direction'], npc['json']))
        self.mobs = []
        for mob in map_data['mobs']:
            self.mobs.append(Mob(tuple(mob['pos']), mob['direction'], mob['json']))
        self.stones = []
        for stone in map_data['stones']:
            self.stones.append(Object(tuple(stone['pos']), tuple(stone['size']), stone['image']))
        self.portals = []
        for portal in map_data['portals']:
            self.portals.append(Portal(tuple(portal['pos']), tuple(portal['size']), portal['next_map']), portal['image'])
        self.current_map = map_json
