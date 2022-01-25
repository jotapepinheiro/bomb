import pyautogui
import time
class Application:
    def __init__(self):
        from src.config import Config
        from src.services.telegram import Telegram
        self.config = Config().read()
        self.configThreshold = self.config['threshold']
        self.telegram = Telegram()

    def importLibs(self):
        from src.log import Log
        self.log = Log()

    def start(self):
        self.importLibs()

        pyautogui.FAILSAFE = False

        input('Press Enter to start the bot...\n')
        self.log.console('Starting bot...', services=True, emoji='🤖', color='green')
        time.sleep(3)

    def stop(self):
        self.telegram.stop()
        exit()

    def checkThreshold(self):
        from src.config import Config
        config = Config().read()
        newConfigThreshold = config['threshold']

        if newConfigThreshold != self.configThreshold:
            self.configThreshold = newConfigThreshold
            self.log.console('New Threshold applied', emoji='⚙️', color='grey')
