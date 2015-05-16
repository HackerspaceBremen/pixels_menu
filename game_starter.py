from game import Game

class GameStarter(object):

    def __init__(self, game):
        self.game = game

    def start(self):
        if self.game is not None:
            os.killpg(self.game.pid,signal.SIGTERM)
        exec_cmd = "cd "+game.local_repo+"; python "+game.start_file
        self.game = subprocess.Popen(exec_cmd, shell=True, preexec_fn=os.setsid)
