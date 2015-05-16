import os

class Game(object):
    def __init__(self, url, start_file, start_directory):
        self.url = url
        self.start_file = start_file
        directory = url.split('/')[-2]+"_"+url.split('/')[-1]
        self.local_repo = os.path.join(os.getcwd(),"games",directory)
        self.name = start_file
        self.author = "Unknown"
        self.theme_color = "#ffffff"
        self.game_info = []
        self.start_directory = start_directory

    def create_game_info(self):
        self.game_info.append('Author='+self.author)
        self.game_info.append('Name='+self.name)

