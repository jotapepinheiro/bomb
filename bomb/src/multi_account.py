import sys
import time

from pyclick import HumanClicker

humanClicker = HumanClicker()

class MultiAccount:
    def __init__(self):
        from src.config import Config
        from src.log import Log
        self.config = Config().read()
        self.log = Log()

        self.check_for_updates = 60
        self.next_refresh_heroes = self.config['time_intervals']['send_heroes_for_work'][0]
        self.next_refresh_heroes_positions = self.config['time_intervals']['refresh_heroes_positions'][0]

    def importLibs(self):
        from src.actions import Actions
        from src.application import Application
        from src.auth import Auth, account_active
        from src.captcha import Captcha
        from src.error import Errors
        from src.heroes import Heroes
        from src.images import Images
        from src.recognition import Recognition
        from src.treasure_hunt import TreasureHunt
        self.actions = Actions()
        self.application = Application()
        self.auth = Auth()
        self.captcha = Captcha()
        self.errors = Errors()
        self.heroes = Heroes()
        self.images = Images()
        self.recognition = Recognition()
        self.treasure_hunt = TreasureHunt()

        self.account_active = account_active

    def start(self):
        self.importLibs()
        multiAccount = self.config['app']['multi_account']['enable']
        if multiAccount != True:
            self.log.console('Multi account disabled', emoji='🧾', color='cyan')
            self.botSingle()

        if multiAccount == True:
            self.log.console('Multi account enabled', emoji='🧾', color='cyan')
            self.botMultiAccount()

    def startOnlyMapAction(self):
        self.importLibs()
        self.log.console('Multi account disabled', emoji='🧾', color='cyan')
        self.botSingleOnlyMap()

    def botSingle(self):

        last = {
            "account": 1,
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "refresh_heroes": 0,
            "check_updates": 0
        }

        while True:
            self.steps(last)

    def botSingleOnlyMap(self):

        last = {
            "new_map": 0,
        }

        while True:
            self.stepsOnlyMap(last)

    def botMultiAccount(self):
        # Define total accounts
        totalAccounts = self.config['app']['multi_account']['total_accounts']
        accounts = []
        counterAccounts = 1
        while counterAccounts <= totalAccounts:
            accounts.append({
                "login": 0,
                "heroes": 0,
                "new_map": 0,
                "refresh_heroes": 0
            })
            counterAccounts += 1

        while True:
            curretAccount = 1
            # Display with 1280x800
            clickWindow = 120

            for last in accounts:

                self.activeWindow(last, curretAccount, clickWindow)

                clickWindow += 180
                curretAccount += 1

    def steps(self, last, curretAccount):
        new_map_button = self.images.image('new_map_button')
        run_time_app = self.config['app']['run_time_app']

        currentScreen = self.recognition.currentScreen()

        if currentScreen == "login":
            self.auth.login(last['account'])

        self.errors.verify()

        now = time.time()

        if now - last["heroes"] > self.next_refresh_heroes * 60:
            last["heroes"] = now
            last["refresh_heroes"] = now
            self.heroes.getMoreHeroes()

        i = 1
        while i < 4:
          if currentScreen == "main":
              self.treasure_hunt.goToMap()

          if currentScreen == "treasure_hunt":
              if self.actions.clickButton(new_map_button):
                  last["new_map"] = now
                  self.actions.clickNewMap(curretAccount)

          if now - last["refresh_heroes"] > self.next_refresh_heroes_positions * 60:
              last["refresh_heroes"] = now
              self.heroes.refreshHeroesPositions()

          i += 1
          time.sleep(1)

        self.auth.checkLogout()
        sys.stdout.flush()
        self.actions.sleep(run_time_app, run_time_app, randomMouseMovement=False)

    def stepsOnlyMap(self, last):
        new_map_button = self.images.image('new_map_button')
        run_time_app = self.config['app']['run_time_app']

        currentScreen = self.recognition.currentScreen()

        self.errors.verify()

        now = time.time()

        if currentScreen == "treasure_hunt":
            if self.actions.clickButton(new_map_button):
                last["new_map"] = now
                self.actions.clickNewMap()

        sys.stdout.flush()
        self.actions.sleep(run_time_app, run_time_app, randomMouseMovement=False)

    def activeWindow(self, last, curretAccount, clickWindow):
        close_button = self.images.image('close_button')

        self.actions.move((int(36), int(58)), 1, forceTime=True)
        humanClicker.click()
        self.actions.sleep(1, 1, forceTime=True)
        self.actions.move((int(200), int(clickWindow)), 1, forceTime=True)
        humanClicker.click()
        self.actions.sleep(1, 1, forceTime=True)
        self.actions.clickButton(close_button)
        self.log.console('Browser Active: ' + str(curretAccount), emoji='🪟', color='cyan')
        self.actions.sleep(1, 1, forceTime=True)
        self.steps(last, curretAccount)

    def unicodeToAscii(self, text):
        return (
            str(text)
            .replace('\\xc3\\xa9', 'e')
            .replace('\\xc2\\xb7', '·')
            .replace('\\xe2\\x80\\x99', "'")
            .replace('\\xe2\\x80\\x9c', '"')
            .replace('\\xe2\\x80\\x9d', '"')
            .replace('\\xe2\\x80\\x9e', '"')
            .replace('\\xe2\\x80\\x9f', '"')
            .replace('\\xe2\\x80\\x9c', '"')
            .replace('\\xe2\\x80\\x93', '-')
            .replace('\\xe2\\x80\\x92', '-')
            .replace('\\xe2\\x80\\x94', '-')
            .replace('\\xe2\\x80\\x94', '-')
            .replace('\\xe2\\x80\\x98', "'")
            .replace('\\xe2\\x80\\x9b', "'")
            .replace('\\xe2\\x80\\x90', '-')
            .replace('\\xe2\\x80\\x91', '-')
            .replace('\\xe2\\x80\\xb2', "'")
            .replace('\\xe2\\x80\\xb3', "'")
            .replace('\\xe2\\x80\\xb4', "'")
            .replace('\\xe2\\x80\\xb5', "'")
            .replace('\\xe2\\x80\\xb6', "'")
            .replace('\\xe2\\x80\\xb7', "'")
            .replace('\\xe2\\x81\\xba', " ")
            .replace('\\xe2\\x81\\xbb', "-")
            .replace('\\xe2\\x81\\xbc', "=")
            .replace('\\xe2\\x81\\xbd', "(")
            .replace('\\xe2\\x81\\xbe', ")")
        )