from cv2 import cv2
import numpy as np
import mss
import pyautogui
import time
import sys
import yaml
import requests


cat = """
                                                _
                                                \`*-.
                                                 )  _`-.
                                                .  : `. .
                                                : _   '  \\
                                                ; *` _.   `*-._
                                                `-.-'          `-.
                                                  ;       `       `.
                                                  :.       .        \\
                                                  . \  .   :   .-'   .
                                                  '  `+.;  ;  '      :
                                                  :  '  |    ;       ;-.
                                                  ; '   : :`-:     _.`* ;
                                               .*' /  .*' ; .*`- +'  `*'
                                               `*-*   `*-*  `*-*'
   
 d888b  d8888b. db    db d8888b.  .d88b.     .d8b.   .o88b. db      
88' Y8b 88  `8D 88    88 88  `8D .8P  Y8.   d8' `8b d8P  Y8 88      
88      88oobY' 88    88 88oodD' 88    88   88ooo88 8P      88      
88  ooo 88`8b   88    88 88~~~   88    88   88~~~88 8b      88      
88. ~8~ 88 `88. 88b  d88 88      `8b  d8'   88   88 Y8b  d8 88booo. 
 Y888P  88   YD ~Y8888P' 88       `Y88P'    YP   YP  `Y88P' Y88888P 
=======================================================================
=========================== GRUPO ACL v1 ==============================
=======================================================================

>>---> Pressione ctrl + c para encerrar o bot.
>>---> Algumas configurações podem ser encontradas no arquivo config.yaml.
"""

print(cat)

if __name__ == '__main__':

    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)
ct = c['threshold']

pyautogui.PAUSE = c['time_intervals']['interval_between_moviments']

pyautogui.FAILSAFE = True
hero_clicks = 0
login_attempts = 0
last_log_is_progress = False


go_browser_img = cv2.imread('targets/navigator.png')
go_work_img = cv2.imread('targets/go-work.png')
commom_img = cv2.imread('targets/commom-text.png')
arrow_img = cv2.imread('targets/go-back-arrow.png')
hero_img = cv2.imread('targets/hero-icon.png')
x_button_img = cv2.imread('targets/x.png')
teasureHunt_icon_img = cv2.imread('targets/treasure-hunt-icon.png')
ok_btn_img = cv2.imread('targets/ok.png')
connect_wallet_btn_img = cv2.imread('targets/connect-wallet.png')
select_wallet_hover_img = cv2.imread('targets/select-wallet-1-hover.png')
select_metamask_no_hover_img = cv2.imread(
    'targets/select-wallet-1-no-hover.png')
sign_btn_img = cv2.imread('targets/select-wallet-2.png')
new_map_btn_img = cv2.imread('targets/new-map.png')
green_bar = cv2.imread('targets/green-bar.png')
full_stamina = cv2.imread('targets/full-stamina.png')


def logger(message, progress_indicator=False):
    global last_log_is_progress

    # Start progress indicator and append dots to in subsequent progress calls
    if progress_indicator:
        if not last_log_is_progress:
            last_log_is_progress = True
            sys.stdout.write('\n => .')
            sys.stdout.flush()
        else:
            sys.stdout.write('.')
            sys.stdout.flush()

        return

    if last_log_is_progress:
        sys.stdout.write('\n\n')
        sys.stdout.flush()
        last_log_is_progress = False

    datetime = time.localtime()
    formatted_datetime = time.strftime("%d/%m/%Y %H:%M:%S", datetime)

    formatted_message = "[{}] \n => {} \n\n".format(
        formatted_datetime, message)

    print(formatted_message)

    if (c['save_log_to_file'] == True):
        logger_file = open("logger.log", "a")
        logger_file.write(formatted_message)
        logger_file.close()

    return True


def clickBtn(img, name=None, timeout=3, threshold=ct['default']):
    logger(None, progress_indicator=True)
    if not name is None:
        pass
        # print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    clicked = False
    while(not clicked):
        matches = positions(img, threshold=threshold)
        if(len(matches) == 0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass
                    # print('timed out')
                return False
            # print('button not found yet')
            continue

        x, y, w, h = matches[0]
        pyautogui.moveTo(x+w/2, y+h/2, 1)
        pyautogui.click()
        return True


def printSreen():
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        #sct_img = np.array(sct.grab(monitor))
        sct_img = np.array(sct.grab(sct.monitors[0]))
        return sct_img[:, :, :3]


def positions(target, threshold=ct['default']):
    img = printSreen()
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles


def scroll():

    commoms = positions(commom_img, threshold=ct['commom'])
    if (len(commoms) == 0):
        # print('no commom text found')
        return
    x, y, w, h = commoms[len(commoms)-1]
    # print('moving to {},{} and scrolling'.format(x,y))
#
    pyautogui.moveTo(x, y, 1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0, -c['click_and_drag_amount'],
                          duration=1, button='left')


def clickButtons():
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        pyautogui.moveTo(x+(w/2), y+(h/2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            logger('too many hero clicks, tente aumentar o limite em go_to_work_btn')
            return
    return len(buttons)


def isWorking(bar, buttons):
    y = bar[1]

    for (_, button_y, _, button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True


def clickGreenBarButtons():
    # ele clicka nos q tao trabaiano mas axo q n importa
    offset = 130
    green_bars = positions(green_bar, threshold=ct['green_bar'])
    logger('%d barras verdes detectadas' % len(green_bars))
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])
    logger('%d botões detectadas' % len(buttons))

    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger('%d buttons with green bar detected' %
               len(not_working_green_bars))
        logger('Clicking in %d heroes.' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        pyautogui.moveTo(x+offset+(w/2), y+(h/2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        if hero_clicks > 20:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)


def clickFullBarButtons():
    offset = 100
    full_bars = positions(full_stamina, threshold=ct['default'])
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])

    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        logger('Clicking in %d heroes.' % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        pyautogui.moveTo(x+offset+(w/2), y+(h/2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1

    return len(not_working_full_bars)


def goToHeroes():
    if clickBtn(arrow_img):
        global login_attempts
        login_attempts = 0

    # time.sleep(5)
    clickBtn(hero_img)
    # time.sleep(5)


def goToGame():
    # in case of server overload popup
    clickBtn(x_button_img)
    # time.sleep(3)
    clickBtn(x_button_img)

    clickBtn(teasureHunt_icon_img)


def refreshHeroesPositions():
    clickBtn(arrow_img)
    clickBtn(teasureHunt_icon_img)
    # time.sleep(3)
    clickBtn(teasureHunt_icon_img)


def login():
    global login_attempts

    if login_attempts > 3:
        logger('Too many login attempts, refreshing.')
        login_attempts = 0
        pyautogui.hotkey('ctrl', 'f5')
        return

    if clickBtn(connect_wallet_btn_img, name='connectWalletBtn', timeout=10):
        login_attempts = login_attempts + 1
        logger('Connect wallet button detected, logging in!')
        # TODO mto ele da erro e poco o botao n abre
        # time.sleep(10)

    if clickBtn(sign_btn_img, name='sign button', timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        # time.sleep(5)
        if clickBtn(teasureHunt_icon_img, name='teasureHunt', timeout=15):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)
        return
        # click ok button

    if not clickBtn(select_metamask_no_hover_img, name='selectMetamaskBtn'):
        if clickBtn(select_wallet_hover_img, name='selectMetamaskHoverBtn', threshold=ct['select_wallet_buttons']):
            pass
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)
    else:
        pass
        # print('sleep in case there is no metamask text removed')
        # time.sleep(20)

    if clickBtn(sign_btn_img, name='signBtn', timeout=20):
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        # time.sleep(25)
        if clickBtn(teasureHunt_icon_img, name='teasureHunt', timeout=25):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)

    if clickBtn(ok_btn_img, name='okBtn', timeout=5):
        pass
        # time.sleep(15)
        # print('ok button clicked')


def refreshHeroes():
    goToHeroes()

    if c['select_heroes_mode'] == "full":
        logger("Sending heroes with full stamina bar to work!")
    elif c['select_heroes_mode'] == "green":
        logger("Sending heroes with green stamina bar to work!")
    else:
        logger("Sending all heroes to work!")

    buttonsClicked = 1
    empty_scrolls_attempts = c['scroll_attemps']

    while(empty_scrolls_attempts > 0):
        if c['select_heroes_mode'] == 'full':
            buttonsClicked = clickFullBarButtons()
        elif c['select_heroes_mode'] == 'green':
            buttonsClicked = clickGreenBarButtons()
        else:
            buttonsClicked = clickButtons()

        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
        scroll()
        time.sleep(2)
    logger('{} heroes sent to work so far'.format(hero_clicks))
    goToGame()


def main():
    time.sleep(5)
    t = c['time_intervals']

    browser = 0
    last = [
        {
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "refresh_heroes": 0,
        },
        {
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "refresh_heroes": 0,
        }
    ]

    while True:
        now = time.time()

        if now - last[browser]["heroes"] > t['send_heroes_for_work'] * 60:
            last[browser]["heroes"] = now
            logger('Sending heroes to work.')
            refreshHeroes()

        if now - last[browser]["login"] > t['check_for_login'] * 60:
            logger("Checking if game has disconnected.")
            sys.stdout.flush()
            last[browser]["login"] = now
            login()

        if now - last[browser]["new_map"] > t['check_for_new_map_button']:
            last[browser]["new_map"] = now
            if clickBtn(new_map_btn_img):
                with open('new-map.log', 'a') as new_map_log:
                    new_map_log.write(str(time.time())+'\n')
                logger('New Map button clicked!')

        if now - last[browser]["refresh_heroes"] > t['refresh_heroes_positions'] * 60:
            last[browser]["refresh_heroes"] = now
            logger('Refreshing Heroes Positions.')
            refreshHeroesPositions()

        browser_list = positions(go_browser_img, threshold=ct['default'])
        if len(browser_list) > 1:
            logger('Trocando de browser')
            browser = 1 if browser == 0 else 0
            x, y, w, h = browser_list[browser]
            pyautogui.moveTo(x+w/2, y+h/2, 1)
            pyautogui.click()
            time.sleep(1)

        logger(None, progress_indicator=True)

        sys.stdout.flush()

        time.sleep(1)


main()


# cv2.imshow('img',sct_img)
# cv2.waitKey()

# chacar se tem o sign antes de aperta o connect wallet ?
# arrumar aquela parte do codigo copiado onde tem q checar o sign 2 vezes ?
# colocar o botao em pt
# melhorar o log
# salvar timestamp dos clickes em newmap em um arquivo
# soh resetar posiçoes se n tiver clickado em newmap em x segundos

# pegar o offset dinamicamente
# clickar so no q nao tao trabalhando pra evitar um loop infinito no final do scroll se ainda tiver um verdinho
