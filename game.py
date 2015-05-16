import os

class Game(object):
    def __init__(self, url, start_file):
        self.url = url
        self.start_file = start_file
        directory = url.split('/')[-2]+"_"+url.split('/')[-1]
        self.local_repo = os.path.join(os.getcwd(),"games",directory)
        self.name = start_file
        self.author = "Unknown"
        self.theme_color = "#ffffff"

