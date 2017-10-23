import pygame, math, sys, json, time
from pygame.locals import *
from tools import *
from characters import *
from objects import *
from constants import *

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
        self.KEYSEDGE = []
        self.saved_games = []
        self.current_map = None
        self.background = pygame.Surface(screen.get_size())
        self.background.fill(BLACK)
        self.title_font = pygame.font.SysFont('Arial', TITLE_SIZE)
        self.subtitle_font = pygame.font.SysFont('Arial', SUBTITLE_SIZE)
        self.text_font = pygame.font.SysFont('Arial', TEXT_SIZE)
        self.arrow_pos = (TITLE_POS_X - TEXT_SIZE, 300)
        self.interlocutor = None
        self.dialog_sequence = []
        self.dialog_index = 0
        self.answer = 0

    def main_loop(self):
        '''Main loop method. It will call the method associated with the correspondent state'''

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                self.KEYSPRESSED.append(event.key)
                self.KEYSEDGE.append(event.key)
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
        elif self.current_state == 'INVENTARY_STATE':
            self.display_inventary()  
        elif self.current_state == 'GAME_OVER':
            self.game_over() 
        else:
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill(BLACK)
            self.error()

        del self.KEYSEDGE[:]

    def main_title(self):
        self.screen.blit(self.background, (0,0))
        blit_text(self.screen, 'Hard Pilgrimage', (TITLE_POS_X, 150), self.title_font, WHITE)
        blit_text(self.screen, 'Road to Cardiff', (175, 215), self.subtitle_font, WHITE)
        blit_text(self.screen, 'Nueva partida', (TITLE_POS_X, 300), self.text_font, WHITE)
        blit_text(self.screen, 'Cargar partida', (375, 300), self.text_font, WHITE)

        for key in self.KEYSEDGE:
            if key == pygame.K_LEFT:
                if self.arrow_pos[0] == 350:
                    self.arrow_pos = (TITLE_POS_X - TEXT_SIZE, 300)
            elif key == pygame.K_RIGHT:
                if self.arrow_pos[0] == TITLE_POS_X - TEXT_SIZE:
                    self.arrow_pos = (350, 300)
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                if self.arrow_pos[0] == TITLE_POS_X - TEXT_SIZE:
                    #Start new game
                    self.current_state = 'NEW_GAME'
                    return
                if self.arrow_pos[0] == 350:
                    f = open(SAVED_GAMES_FILE)
                    self.saved_games = json.load(f)
                    f.close()
                    self.arrow_pos = (160, 100)
                    self.current_state = 'LOAD_GAME'
                    return
            else:
                pass

        vertices = [self.arrow_pos, (self.arrow_pos[0], self.arrow_pos[1]+TEXT_SIZE), (self.arrow_pos[0]+TEXT_SIZE/2, self.arrow_pos[1]+TEXT_SIZE/2)]
        pygame.draw.polygon(self.screen, RED, vertices)

    def error(self):
        self.screen.blit(self.background, (0,0))
        blit_text(self.screen, 'Ingame error', (150, 200), self.title_font, RED)  

    def new_game(self):
        self.control_state()
        if len(self.KEYSEDGE):
            self.main_char = Main_Character(MAIN_CHAR)
            self.load_map(INITIAL_MAP)

    def load_game(self):
        
        self.screen.blit(self.background, (0,0))
        i = 0
        for game in self.saved_games:
            blit_text(self.screen, game, (200, 100+i), self.subtitle_font, WHITE)
            i = i + 40
        blit_text(self.screen, 'Volver', (200, 100+i), self.subtitle_font, WHITE)

        for key in self.KEYSEDGE:
            if key == pygame.K_DOWN:
                if self.arrow_pos[1] < 100 + i:
                    self.arrow_pos = (160, self.arrow_pos[1]+SUBTITLE_SIZE)
            elif key == pygame.K_UP:
                if self.arrow_pos[1] > 100:
                    self.arrow_pos = (160, self.arrow_pos[1]-SUBTITLE_SIZE)
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
                        self.mobs = []
                        for mob_dict in saved_data['mobs']:
                            mob = Mob(mob_dict['pos'], mob_dict['direction'], mob_dict['char_json'])
                            mob.life = mob_dict['life']
                            self.mobs.append(mob)
                        for item in saved_data['inventary']:
                            self.main_char.inventary.append((Item(item[0]), item[1]))
                        self.current_state = 'MAP_STATE'
                        return
                    i = i +40
                self.arrow_pos = (TITLE_POS_X - TEXT_SIZE, 300)
                self.current_state = 'MAIN_TITLE'
            else:
                pass

        vertices = [self.arrow_pos, (self.arrow_pos[0], self.arrow_pos[1]+40), (self.arrow_pos[0]+20, self.arrow_pos[1]+20)]
        pygame.draw.polygon(self.screen, (255, 0, 0), vertices)

    def map_state(self):

        if pygame.K_RETURN in self.KEYSEDGE:
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill(BLACK)
            self.arrow_pos = (160, 100)
            self.current_state = 'MENU_STATE'
            return

        self.screen.blit(self.background, (0,0))
        if pygame.K_s in self.KEYSEDGE:
            if self.main_char.stones > 0:
                self.main_char.throw_stone()
        self.main_char.move_char(self.KEYSPRESSED, self.screen.get_size(), self.blockers, self.NPCs)
        self.main_char.draw(self.screen)

        if self.blockers:
            for blocker in self.blockers:
                blocker.draw(self.screen)
                #pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(blocker.pos, blocker.size))
        if self.NPCs:
            for npc in self.NPCs:
                npc.draw(self.screen)
            if pygame.K_a in self.KEYSEDGE:
                i = self.main_char.checkcollisions(self.NPCs)
                if i != 1:
                    self.NPCs[i].rotate(self.main_char.pos)
                    self.interlocutor = self.NPCs[i]
                    self.dialog_sequence = self.NPCs[i].dialog_sequence
                    self.current_state = 'DIALOG_STATE'
                    return
        if self.mobs:
            for mob in self.mobs:
                mob.move_mob(self.main_char.pos, self.screen.get_size(), self.blockers)
                mob.draw(self.screen)
            hitting_mob = self.main_char.checkcollisions(self.mobs)
            if hitting_mob != -1:
                self.main_char.hit_by_mob(self.mobs[hitting_mob])
                if self.main_char.life < 1:
                    self.current_state = 'GAME_OVER'
                    self.arrow_pos = (TITLE_POS_X - TEXT_SIZE, 300)
                    self.background = pygame.Surface(self.screen.get_size())
                    self.background.fill(BLACK)
                    return
        if self.stones:
            for stone in self.stones:
                stone.draw(self.screen)
            if self.main_char.stones < 999:
                touching_stone = self.main_char.checkcollisions(self.stones)
                if touching_stone != -1:
                    self.main_char.stones += 1
                    self.stones.remove(self.stones[touching_stone])
        if self.portals:
            for portal in self.portals:
                portal.draw(self.screen)

        mob_hit = self.main_char.update_stones(self.blockers, self.NPCs, self.mobs)
        if mob_hit != -1:
            remaining_health = self.mobs[mob_hit].life
            if remaining_health < 1:
                if self.mobs[mob_hit].event != None:
                    self.mobs[mob_hit].event.trigger_event()
                self.mobs.remove(self.mobs[mob_hit])

        portal_index = self.main_char.checkcollisions(self.portals)
        if portal_index != -1:
            black_screen = pygame.Surface(self.screen.get_size())
            black_screen.fill(BLACK)
            self.screen.blit(black_screen, (0, 0))
            self.load_map(self.portals[portal_index].next_map)
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

        if not self.dialog_sequence[self.dialog_index]:
            self.dialog_index = self.dialog_index + 1
            return

        if self.dialog_index % 2:
            pos = self.main_char.dialog(self.screen, self.dialog_sequence[self.dialog_index], self.text_font)
            if type(self.dialog_sequence[self.dialog_index]) == list:
                for key in self.KEYSEDGE:
                    if key == pygame.K_DOWN:
                        if self.arrow_pos[1] < pos[1] + TEXT_SIZE*len(self.dialog_sequence[self.dialog_index]):
                            self.arrow_pos = (self.arrow_pos[0], self.arrow_pos[1] + TEXT_SIZE)
                    if key == pygame.K_UP:
                        if self.arrow_pos[1] > pos[1]:
                            self.arrow_pos = (self.arrow_pos[0], self.arrow_pos[1] - TEXT_SIZE)
                    elif key == pygame.K_SPACE or key == pygame.K_RETURN:

                        self.answer = (self.arrow_pos[1] - pos[1])/TEXT_SIZE
                        self.dialog_index = self.dialog_index + 1
                        return

                vertices = [self.arrow_pos, (self.arrow_pos[0], self.arrow_pos[1]+TEXT_SIZE), (self.arrow_pos[0]+TEXT_SIZE/2, self.arrow_pos[1]+TEXT_SIZE/2)]
                pygame.draw.polygon(self.screen, RED, vertices)
        else:
            pos = self.interlocutor.dialog(self.screen, self.dialog_sequence[self.dialog_index], self.text_font, self.answer)
            if len(self.KEYSEDGE) > 0 and type(self.dialog_sequence[self.dialog_index]) == list:
                self.dialog_index = self.dialog_index + 1
                if len(self.dialog_sequence) < self.dialog_index + 1:
                    self.dialog_index = 0
                    self.current_state = 'MAP_STATE'
                return

        if len(self.KEYSEDGE) > 0 and type(self.dialog_sequence[self.dialog_index]) != list:
            self.dialog_index = self.dialog_index + 1
            if self.dialog_index < len(self.dialog_sequence) and type(self.dialog_sequence[self.dialog_index]) == list:
                if self.dialog_index % 2:
                    self.arrow_pos = self.main_char.dialog_pos(self.screen)
                else:
                    self.arrow_pos = self.interlocutor.dialog_pos(self.screen)

        if len(self.dialog_sequence) < self.dialog_index + 1:
            self.dialog_index = 0
            self.current_state = 'MAP_STATE'

    def menu_state(self):

        self.screen.blit(self.background, (0, 0))
        menu_options = MENU_OPTIONS
        blit_text(self.screen, menu_options, (200, 100), self.subtitle_font, WHITE)

        for key in self.KEYSEDGE:
            if key == pygame.K_DOWN:
                if self.arrow_pos[1] < 325:
                    self.arrow_pos = (160, self.arrow_pos[1]+(SUBTITLE_SIZE+5))
            elif key == pygame.K_UP:
                if self.arrow_pos[1] > 100:
                    self.arrow_pos = (160, self.arrow_pos[1]-(SUBTITLE_SIZE+5))
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                if self.arrow_pos[1] == 100:
                    #Return to map state
                    self.current_state = 'MAP_STATE'
                    map_data = json.load(open(self.current_map))
                    self.background = pygame.image.load(map_data['image'])
                    self.background = pygame.transform.scale(self.background, self.screen.get_size())
                elif self.arrow_pos[1] == 145:
                    #Display inventary
                    self.current_state = 'INVENTARY_STATE'
                    self.arrow_pos = (160, 100)
                elif self.arrow_pos[1] == 190:
                    #Return to main title
                    self.background = pygame.Surface(self.screen.get_size())
                    self.background.fill(BLACK)
                    self.arrow_pos = (TITLE_POS_X - TEXT_SIZE, 300)
                    self.current_state = 'MAIN_TITLE'
                    pygame.mixer.music.stop()
                elif self.arrow_pos[1] == 235:
                    #Show  controls
                    self.current_state = 'CONTROLS_STATE'
                elif self.arrow_pos[1] == 280:
                    #Save game
                    self.current_state = 'SAVE_GAME'
                    f = open(SAVED_GAMES_FILE)
                    self.saved_games = json.load(f)
                    f.close()
                    self.arrow_pos = (160, 100)
                elif self.arrow_pos[1] == 325:
                    #Exit game
                    pygame.quit()
                    sys.exit(0)
            else:
                pass

        vertices = [self.arrow_pos, (self.arrow_pos[0], self.arrow_pos[1]+SUBTITLE_SIZE), (self.arrow_pos[0]+SUBTITLE_SIZE/2, self.arrow_pos[1]+SUBTITLE_SIZE/2)]
        pygame.draw.polygon(self.screen, RED, vertices)

    def roll_credits(self):
        '''Display credits and return to main title'''
        credits = CREDITS_LIST
        self.screen.blit(self.background, (0, 0))
        blit_text(self.screen, credits[self.dialog_index], (10, 10), self.subtitle_font, WHITE)
        if len(self.KEYSEDGE):
            self.dialog_index += 1
            if len(credits) < self.dialog_index +1:
                self.dialog_index = 0
                self.current_state = 'MAIN_TITLE'
                self.arrow_pos = (TITLE_POS_X - TEXT_SIZE, 300)

    def save_game(self):

        self.screen.blit(self.background, (0,0))
        i = 0
        for game in self.saved_games:
            blit_text(self.screen, game, (200, 100+i), self.subtitle_font, WHITE)
            i = i + 40
        if len(self.saved_games) < 5:
            blit_text(self.screen, 'Nuevo', (200, 100+i), self.subtitle_font, WHITE)
            i = i + 40
        blit_text(self.screen, 'Volver', (200, 100+i), self.subtitle_font, WHITE)

        for key in self.KEYSEDGE:
            if key == pygame.K_DOWN:
                if self.arrow_pos[1] < 100 + i:
                    self.arrow_pos = (160, self.arrow_pos[1]+SUBTITLE_SIZE)
            elif key == pygame.K_UP:
                if self.arrow_pos[1] > 100:
                    self.arrow_pos = (160, self.arrow_pos[1]-SUBTITLE_SIZE)
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                if self.arrow_pos[1] == 100 + i:
                    #Return to menu state
                    self.current_state = 'MENU_STATE'
                    self.arrow_pos = (160, 100)
                else:
                    #Save game
                    t = time.localtime()
                    t_str = str(t.tm_year)+'/'+str(t.tm_mon)+'/'+str(t.tm_mday)+' '+str(t.tm_hour)+':'+str(t.tm_min)
                    mobs = []
                    for mob in self.mobs:
                        mobs.append({"pos": mob.pos, "direction": mob.direction, "char_json": mob.char_json, "life": mob.life})
                    items = []
                    for item in self.main_char.inventary:
                         items.append([item[0].item_json, item[1]])
                    current_game = {'char_json': self.main_char.char_json, 'health': self.main_char.life, 'inventary': items, 'stones': self.main_char.stones, 'money': self.main_char.money, 'pos': self.main_char.pos, 'direction': self.main_char.direction, 'map': self.current_map, 'mobs': mobs}
                    i = 0
                    for game in self.saved_games:
                        if self.arrow_pos[1] == 100 + i:
                            del self.saved_games[game]
                            break
                        i = i + 40
                    self.saved_games[t_str] = current_game
                    f = open(SAVED_GAMES_FILE, 'w')
                    json.dump(self.saved_games, f)
                    f.close()
            else:
                pass

        vertices = [self.arrow_pos, (self.arrow_pos[0], self.arrow_pos[1]+SUBTITLE_SIZE), (self.arrow_pos[0]+SUBTITLE_SIZE/2, self.arrow_pos[1]+SUBTITLE_SIZE/2)]
        pygame.draw.polygon(self.screen, RED, vertices)

    def display_inventary(self):
        self.screen.blit(self.background, (0,0))
        i = 0
        for item in self.main_char.inventary:
            blit_text(self.screen, item[0].name, (200, 100+i), self.subtitle_font, WHITE)
            i = i + 40
        for item in self.main_char.inventary:
            blit_text(self.screen, item[1], (400, 100+i), self.subtitle_font, RED)
            i = i + 40
        blit_text(self.screen, 'Volver', (200, 100+i), self.subtitle_font, WHITE)

        if self.arrow_pos[1] < 100 + i:
            selected_item = self.main_char.inventary[(self.arrow_pos[1] - 100)/40][0]
            self.display_info(selected_item.effect)

        for key in self.KEYSEDGE:
            if key == pygame.K_DOWN:
                if self.arrow_pos[1] < 100 + i:
                    self.arrow_pos = (160, self.arrow_pos[1]+SUBTITLE_SIZE)
            elif key == pygame.K_UP:
                if self.arrow_pos[1] > 100:
                    self.arrow_pos = (160, self.arrow_pos[1]-SUBTITLE_SIZE)
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                if self.arrow_pos[1] == 100 + i:
                    #Return to menu state
                    self.current_state = 'MENU_STATE'
                    self.arrow_pos = (160, 100)
                else:
                    selected_item = self.main_char.inventary[(self.arrow_pos[1] - 100)/40][0].name
                    self.main_char.use_item(selected_item)
            else:
                pass

        vertices = [self.arrow_pos, (self.arrow_pos[0], self.arrow_pos[1]+SUBTITLE_SIZE), (self.arrow_pos[0]+SUBTITLE_SIZE/2, self.arrow_pos[1]+SUBTITLE_SIZE/2)]
        pygame.draw.polygon(self.screen, RED, vertices)

    def control_state(self):
        '''Method correspondent with the controls menu. Meant to display keys used. Possibility to extend functionality by personalizing controls'''
        controls = CONTROL_LIST_STRING
        description = CONTROL_DESC
        self.screen.blit(self.background, (0, 0))
        blit_text(self.screen, controls, (20, 100), self.subtitle_font, RED)
        blit_text(self.screen, description, (340, 100), self.subtitle_font, WHITE)
        if len(self.KEYSEDGE):
            self.current_state = 'MENU_STATE'

    def game_over(self):
        self.screen.blit(self.background, (0,0))
        blit_text(self.screen, 'Game Over', (150, 200), self.title_font, RED) 
        if len(self.KEYSEDGE):
            self.current_state = 'MAIN_TITLE' 

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
            self.portals.append(Portal(tuple(portal['pos']), tuple(portal['size']), portal['next_map'], portal['image']))
        self.current_map = map_json
        self.current_state = 'MAP_STATE'
        if map_data['background_music'] != None:
            pygame.mixer.music.load(map_data['background_music'])
            pygame.mixer.music.play(-1, 0.0)
        else:
            pygame.mixer.music.stop()
        if map_data['event'] != None:
            event = Game_Event(self, map_data['event'])
            event.trigger_event()

    def display_info(self, info):
        text_box = pygame.Surface((640, 120))
        text_box.fill(WHITE)
        blit_text(text_box, info, (0, 0), self.text_font, BLACK)
        self.screen.blit(text_box, (0,480-120))
