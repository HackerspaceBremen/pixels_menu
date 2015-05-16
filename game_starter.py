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
        exec_cmd = "cd "+ dir+" & python "+self.game.start_file
        print(exec_cmd)
        self.game = subprocess.Popen(exec_cmd, shell=True)