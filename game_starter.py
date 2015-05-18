import os
import subprocess

from game import Game

class GameStarter(object):

    def __init__(self, game):
        self.game = game

    def start(self):
        dir = self.game.local_repo
        if self.game.start_directory is not None:
            dir = os.path.join(self.game.local_repo,self.game.start_directory)
        seperator = ";"
        if os.name == "nt":
            seperator = "&"
        args = ["cd", dir, seperator, "python", self.game.start_file]
        print args
        self.game = subprocess.Popen(args, shell=True)