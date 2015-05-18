import sys
import getopt
import pygame
import led

from threading import Thread

from gameloader import GameLoader
from constants import *
from displayers import TextDisplayer
from game_starter import GameStarter

SPEED = 30
LOADING_DOT_AMOUNT = 15
DISPLAY_SIZE = (90, 20)


class Menu(object):
    def __init__(self):
        self.pixel_surface = None
        self.clock = pygame.time.Clock()
        self.displays = []
        self.games = None
        self.game_index = 0
        self.menu_sections = []
        self.menu_section_dict = {}
        self.menu_section_index = 1

    def init_displays(self, ds_ip, ds_port='8123', display_device=None, nosim=False):
        pygame.init()
        pygame.display.set_mode()
        if display_device is not None:
            self.displays.append(led.teensy.TeensyDisplay(display_device))
        if not nosim:
            self.displays.append(led.sim.SimDisplay(DISPLAY_SIZE))
        if ds_ip is None:
            self.displays.append(led.dsclient.DisplayServerClientDisplay(ds_ip, ds_port))
        # TODO: change to Exception
        if self.displays is None:
            print("No Display specified")
            sys.exit(2)
        self.pixel_surface = pygame.Surface(DISPLAY_SIZE)

    def load_games(self):
        gameloader = GameLoader()
        t = Thread(target=gameloader.load_games)
        t.start()

        display_text = TextDisplayer(self.pixel_surface)
        amount_of_dots = 1
        time_counter = 0
        while not gameloader.games_loaded:
            cancel_loading = False
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        cancel_loading = True
            if cancel_loading:
                gameloader.stopp = True
            display_text.display_loading(amount_of_dots)
            time_counter += 1
            if time_counter >= LOADING_DOT_AMOUNT-1:
                amount_of_dots += 1
                if amount_of_dots > LOADING_DOT_AMOUNT:
                    amount_of_dots = 1
                time_counter = 0
            self.update_displays()
        self.games = gameloader.games

    def init_menus(self):
        system_entries = ['Quit', 'Version']
        system_section = MenuSection('system', system_entries)
        game_info_section = MenuSection('game_info', list())
        games_section = MenuSection('games', self.games)
        self.menu_sections.append(system_section)
        self.menu_sections.append(games_section)
        self.menu_sections.append(game_info_section)

        self.create_menu_dict()
        self.update_game_info_section()

    def create_menu_dict(self):
        for index, section in enumerate(self.menu_sections):
            self.menu_section_dict[section.name] = index

    def get_menu_section_from_name(self, name):
        return self.menu_sections[self.menu_section_dict[name]]

    def update_game_info_section(self):
        game_info_section_index = self.menu_section_dict['game_info']

        games_menu = self.get_menu_section_from_name('games')
        game = games_menu.selected_entry()
        game_info_section = MenuSection('game_info', game.game_info)
        self.menu_sections[game_info_section_index] = game_info_section

    def display_menu(self):
        first = True
        while True:
            if first or self.check_keyboard_event():
                if self.menu_section_index == self.menu_section_dict['system']:
                    self.display_system_menu()
                elif self.menu_section_index == self.menu_section_dict['games']:
                    self.display_games()
                elif self.menu_section_index == self.menu_section_dict['game_info']:
                    self.display_game_info()

                self.update_displays()
                first = False

    def display_games(self):
        games_menu = self.get_menu_section_from_name('games')
        games_color = games_menu.selected_entry().theme_color
        if games_color is not None:
            TextDisplayer(self.pixel_surface).display_menu_entry(games_menu.selected_entry().name, games_color)
        else:
            TextDisplayer(self.pixel_surface).display_menu_entry(games_menu.selected_entry().name)

    def display_game_info(self):
        game_info_menu = self.get_menu_section_from_name('game_info')
        TextDisplayer(self.pixel_surface).display_menu_entry(game_info_menu.selected_entry())

    def display_system_menu(self):
        system_menu = self.get_menu_section_from_name('system')
        TextDisplayer(self.pixel_surface).display_menu_entry(system_menu.selected_entry())

    def update_displays(self):
        for display in self.displays:
            display.update(self.pixel_surface)
        self.clock.tick(30)

    def check_keyboard_event(self):
        event_received = False
        for event in pygame.event.get():
            event_received = True
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if self.menu_sections[self.menu_section_index].name == 'system':
                        self.check_events_for_system_menu(event)
                elif self.menu_sections[self.menu_section_index].name == 'games':
                        self.check_events_for_games_menu(event)
                elif self.menu_sections[self.menu_section_index].name == 'game_info':
                        self.check_events_for_game_info_menu(event)

                self.check_events_for_all(event)

        return event_received

    def check_events_for_system_menu(self, event):
        system_menu = self.get_menu_section_from_name('system')
        if event.key == KEY_LEFT:
            system_menu.decrement()
        elif event.key == KEY_RIGHT:
            system_menu.increment()
        elif event.key == KEY_ENTER:
            print(system_menu.selected_entry())
            if system_menu.selected_entry() == 'Quit':
                sys.exit()

    def check_events_for_games_menu(self, event):
        games_menu = self.get_menu_section_from_name('games')
        if event.key == KEY_LEFT:
            games_menu.decrement()
            self.update_game_info_section()
        elif event.key == KEY_RIGHT:
            games_menu.increment()
            self.update_game_info_section()
        elif event.key == KEY_ENTER:
            game = games_menu.selected_entry()
            GameStarter(game).start()

    def check_events_for_game_info_menu(self, event):
        game_info_menu = self.get_menu_section_from_name('game_info')
        if event.key == KEY_LEFT:
            game_info_menu.decrement()
        elif event.key == KEY_RIGHT:
            game_info_menu.increment()

    def check_events_for_all(self, event):
        if event.key == KEY_UP:
            self.select_previous_section()
        elif event.key == KEY_DOWN:
            self.select_next_section()

    def select_next_section(self):
        self.menu_section_index += 1
        if self.menu_section_index > len(self.menu_sections)-1:
            self.menu_section_index = len(self.menu_sections)-1

    def select_previous_section(self):
        self.menu_section_index -= 1
        if self.menu_section_index < 0:
            self.menu_section_index = 0


class MenuSection(object):
    def __init__(self, name, entries):
        self.entries = entries
        self.index = 0
        self.name = name

    def increment(self):
        self.index += 1
        if self.index > len(self.entries)-1:
            self.index = 0

    def decrement(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.entries)-1

    def selected_entry(self):
        return self.entries[self.index]


def main(argv):
    display_device = None
    # set ds_ip to None to disable that the displayserver is used without passing an explizit cmdline parameter
    ds_ip = 'localhost'
    ds_port = '8123'
    nosim = False

    try:
        opts, args = getopt.getopt(argv, "hipd", ['help', 'dsip=', 'dsport=', 'device=', 'nosim'])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            sys.exit()
        elif opt in ('-i', '--dsip'):
            ds_ip = arg
        elif opt in ('--p', '--dsport'):
            ds_port = arg
        elif opt in ('--d', '--device'):
            display_device = arg
        elif opt == 'nosim':
            nosim = True

    menu = Menu()
    menu.init_displays(display_device=display_device, ds_ip=ds_ip, ds_port=ds_port, nosim=nosim)
    menu.load_games()
    menu.init_menus()
    menu.display_menu()

if __name__ == "__main__":
    main(sys.argv[1:])
