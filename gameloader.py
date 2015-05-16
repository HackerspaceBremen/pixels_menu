from git import Repo
from git.exc import NoSuchPathError, GitCommandError
import json
import os

from game import Game

class GameLoader(object):
    def __init__(self):
        self.games = []
        self.games_loaded = False

    def load_games(self):
        self.load_game_data()
        self.load_game_info()

    def load_game_data(self):
        with open("games/gamelist.json") as gamelist_data:
            games = json.load(gamelist_data)

        for game_json in games:
            game = Game(game_json['url'], game_json['start_file'])
            self.games.append(game)
            print(game.local_repo)
            try:
                repo = Repo(game.local_repo)
                repo.remotes.origin.pull()
                print("Done ... PULL")
            except NoSuchPathError:
                Repo.clone_from(game.url, game.local_repo)
                print("Done ... CHECKOUT")
            except GitCommandError:
                print("No Network connection :-/")
        self.games_loaded = True
        # TODO throw away old games

    def load_game_info(self):
        for game in self.games:
            try:
                with open(os.path.join(game.local_repo,"pixels_info.json")) as info_data:
                    pixels_info = json.load(info_data)
                    game.name = pixels_info['name']
                    game.author = pixels_info['author']
                    game.theme_color = pixels_info['theme_color']
            except IOError:
                print("pixels_info.json not found for '"+game.local_repo+"'")
