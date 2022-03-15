import pyautogui
from colorama import Fore
from packaging import version


class Application:
    def __init__(self):
        from src.config import Config
        from src.images import Images
        from src.services.telegram import Telegram
        self.config = Config().read()
        self.configThreshold = self.config['threshold']
        self.images = Images()
        self.telegram = Telegram()

    def importLibs(self):
        from src.log import Log
        self.log = Log()

    def start(self):
        self.importLibs()
        pyautogui.FAILSAFE = False

    def stop(self):
        self.telegram.stop()
        exit()
