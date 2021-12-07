from cv2 import cv2
import numpy as np
import mss
import pyautogui
import time
import sys
import telegram

import yaml

if __name__ == '__main__':
    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)

t = c['time_intervals']
ct = c['threshold']
d_game = c['game']
d_telegram = c['telegram']

shw = t['send_heroes_for_work']
rhp = t['refresh_heroes_positions']
cnm = t['check_for_new_map_button']
cfl = t['check_for_login']
ibm = t['interval_between_moviments']

if not c['usage_multi_account']:
    print('>>---> Mult Account not enabled')
print('\n')

# Initialize telegram
try:
    bot = telegram.Bot(token=d_telegram["telegram_bot_key"])
except:
    print(">>--->Bot not initialized! See configuration file.\n")

pyautogui.PAUSE = np.random.randint(ibm['init'],ibm['end'])

pyautogui.FAILSAFE = True
hero_clicks = 0
new_map_clicks = 0
login_attempts = 0
open_secound_account = True
last_log_is_progress = False

COLOR = {
    'blue': '\033[94m',
    'default': '\033[99m',
    'grey': '\033[90m',
    'yellow': '\033[93m',
    'black': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m'
}

go_work_img = cv2.imread('targets/go-work.png')
common_label = cv2.imread('targets/common-label.png')
rare_label = cv2.imread('target/rare-label.png')
super_rare_label = cv2.imread('target/super-rare-label.png')
epic_label = cv2.imread('target/epic-label.png')
legend_label = cv2.imread('target/legend-label.png')
arrow_img = cv2.imread('targets/go-back-arrow.png')
hero_img = cv2.imread('targets/hero-icon.png')
x_button_img = cv2.imread('targets/x.png')
teasureHunt_icon_img = cv2.imread('targets/treasure-hunt-icon.png')
ok_btn_img = cv2.imread('targets/ok.png')
connect_wallet_btn_img = cv2.imread('targets/connect-wallet.png')
sign_btn_img = cv2.imread('targets/select-wallet-2.png')
new_map_btn_img = cv2.imread('targets/new-map.png')
green_bar = cv2.imread('targets/green-bar.png')
full_stamina = cv2.imread('targets/full-stamina.png')
puzzle_img = cv2.imread('targets/puzzle.png')
piece = cv2.imread('targets/piece.png')
robot = cv2.imread('targets/robot.png')
slider = cv2.imread('targets/slider.png')
treasure_chest_button = cv2.imread('targets/treasure_chest.png')
coin_icon = cv2.imread('targets/coin.png')
chest1 = cv2.imread('targets/chest1.png')
chest2 = cv2.imread('targets/chest2.png')
chest3 = cv2.imread('targets/chest3.png')
chest4 = cv2.imread('targets/chest4.png')
jaula = cv2.imread('targets/jaula.png')

###################### puzzle #############
def findPuzzlePieces(result, piece_img, threshold=0.5):
    piece_w = piece_img.shape[1]
    piece_h = piece_img.shape[0]
    yloc, xloc = np.where(result >= threshold)

    r= []
    for (piece_x, piece_y) in zip(xloc, yloc):
        r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])
        r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])

    r, weights = cv2.groupRectangles(r, 1, 0.2)

    if len(r) < 2:
        return findPuzzlePieces(result, piece_img,threshold-0.01)

    if len(r) == 2:
        return r

    if len(r) > 2:
        logger('💀 Overshoot by %d' % len(r))
        return r

def getRightPiece(puzzle_pieces):
    xs = [row[0] for row in puzzle_pieces]
    index_of_right_rectangle = xs.index(max(xs))

    right_piece = puzzle_pieces[index_of_right_rectangle]
    return right_piece

def getLeftPiece(puzzle_pieces):
    xs = [row[0] for row in puzzle_pieces]
    index_of_left_rectangle = xs.index(min(xs))

    left_piece = puzzle_pieces[index_of_left_rectangle]
    return left_piece

def show(rectangles, img = None):
    if img is None:
        with mss.mss() as sct:
            if (open_secound_account and c['usage_multi_account']):
                monitor = {"top": 0, 
                "left": c['screen_width'], 
                "width": c['screen_width'], 
                "height": c['screen_height']}
            else:
                monitor = {"top": 0, 
                "left": 0, 
                "width": c['screen_width'], 
                "height": c['screen_height']}

        img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow('img', img)
    cv2.waitKey(0)

def getPiecesPosition(t=150):
    popup_pos = positions(robot)
    if len(popup_pos) == 0:
        return None
    rx, ry, _, _ = popup_pos[0]

    w = 380
    h = 200
    x_offset = -40
    y_offset = 65

    y = ry + y_offset
    x = rx + x_offset

    img = printSreen()

    cropped = img[ y : y + h , x: x + w]
    blurred = cv2.GaussianBlur(cropped, (3, 3), 0)
    edges = cv2.Canny(blurred, threshold1=t/2, threshold2=t,L2gradient=True)
    piece_img = cv2.cvtColor(piece, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(edges,piece_img,cv2.TM_CCORR_NORMED)

    puzzle_pieces = findPuzzlePieces(result, piece_img)

    if puzzle_pieces is None:
        return

    # show(puzzle_pieces, edges)
    # exit()

    absolute_puzzle_pieces = []
    for i, puzzle_piece in enumerate(puzzle_pieces):
        px, py, pw, ph = puzzle_piece
        absolute_puzzle_pieces.append( [ x + px, y + py, pw, ph])

    absolute_puzzle_pieces = np.array(absolute_puzzle_pieces)
    # show(absolute_puzzle_pieces)
    return absolute_puzzle_pieces

def getSliderPosition():
    slider_pos = positions(slider)
    if len (slider_pos) == 0:
        return None
    x, y, w, h = slider_pos[0]
    position = [x+(w/2),y+(h/2)]
    return position

def solveCapcha():
    global open_secound_account

    logger('🧩 Checking for captcha')
    pieces_start_pos = getPiecesPosition()
    if pieces_start_pos is None :
        return "not-found"

    slider_start_pos = getSliderPosition()
    if slider_start_pos is None:
        logger('🧩 slider_start_pos')
        return "fail"

    x,y = slider_start_pos
    pyautogui.moveTo(x, y, 1)
    pyautogui.mouseDown()
    if (open_secound_account and c['usage_multi_account']):
        pyautogui.moveTo(x+c['screen_width']+300, y, 0.5)
    else:
        pyautogui.moveTo(x+300, y, 0.5)

    pieces_end_pos = getPiecesPosition()
    if pieces_end_pos is None:
        logger('🧩 pieces_end_pos')
        return "fail"

    piece_start, _, _, _ = getLeftPiece(pieces_start_pos)
    piece_end, _, _, _ = getRightPiece(pieces_end_pos)
    piece_middle, _, _, _  = getRightPiece(pieces_start_pos)
    slider_start, _, = slider_start_pos
    slider_end_pos = getSliderPosition()
    if slider_end_pos is None:
        logger('🧩 slider_end_pos')
        return "fail"

    slider_end, _ = slider_end_pos

    piece_domain = piece_end - piece_start
    middle_piece_in_percent = (piece_middle - piece_start)/piece_domain

    slider_domain = slider_end - slider_start
    slider_awnser = slider_start + (middle_piece_in_percent * slider_domain)
    # arr = np.array([[int(piece_start),int(y-20),int(10),int(10)],[int(piece_middle),int(y-20),int(10),int(10)],[int(piece_end-20),int(y),int(10),int(10)],[int(slider_awnser),int(y),int(20),int(20)]])

    if (open_secound_account and c['usage_multi_account']):
        pyautogui.moveTo(slider_awnser+c['screen_width'], y, 0.5)
    else:
        pyautogui.moveTo(slider_awnser, y, 0.5)

    pyautogui.mouseUp()

    return True
    # show(arr)
    #########################################

# Send telegram message
def sendTelegramMessage(message):
    try:
        if(len(d_telegram["telegram_chat_id"]) > 0):
            for chat_id in d_telegram["telegram_chat_id"]:
                bot.send_message(text=message, chat_id=chat_id)
    except:
        print("⛔ Unable to send telegram message. See configuration file.")

def dateFormatted(format = '%Y-%m-%d %H:%M:%S'):
    datetime = time.localtime()
    formatted = time.strftime(format, datetime)
    return formatted

def logger(message, progress_indicator = False, telegram = False, color = 'default'):
    global last_log_is_progress

    color_formatted = COLOR.get(color.lower(), COLOR['default'])

    formatted_datetime = dateFormatted()

    if (open_secound_account and c['usage_multi_account']):
        account = "Account 2"
    else:
        account = "Account 1"

    formatted_message = "{} - [{}] \n => {} \n".format(account, formatted_datetime, message)
    formatted_message_colored  = color_formatted + formatted_message + '\033[0m'

    # Start progress indicator and append dots to in subsequent progress calls
    if progress_indicator:
        if not last_log_is_progress:
            last_log_is_progress = True
            formatted_message = color_formatted + "{} - [{}] \n => {} \n".format(account, formatted_datetime, '⬆️  Processing last action..')
            sys.stdout.write(formatted_message)
            sys.stdout.flush()
        else:
            sys.stdout.write(color_formatted + '.')
            sys.stdout.flush()
        return

    if last_log_is_progress:
        sys.stdout.write('\n')
        sys.stdout.flush()
        last_log_is_progress = False    

    print(formatted_message_colored)

    if telegram == True:
        sendTelegramMessage(formatted_message)

    if (c['save_log_to_file'] == True):
        logger_file = open("./logs/logger.log", "a", encoding='utf-8')
        logger_file.write(formatted_message + '\n')
        logger_file.close()

    return True

# Send MAP report to telegram
def sendMapReport():
    if(len(d_telegram["telegram_chat_id"]) <= 0 or d_telegram["enable_map_report"] is False):
        return

    time.sleep(np.random.randint(3, 5))

    back = positions(arrow_img)
    
    if len(back) <= 0:
        return

    rx, ry, _, _ = back[0]

    sct_img = printSreen()

    w = 962
    h = 603
    x_offset = 0
    y_offset = 0

    y = ry - y_offset
    x = rx + x_offset

    crop_img = sct_img[ y : y + h , x: x + w]
    #resized = cv2.resize(crop_img, (500, 250))

    cv2.imwrite('./logs/map-report.png', crop_img)
    time.sleep(1)
    try:
        for chat_id in d_telegram["telegram_chat_id"]:
            bot.send_photo(chat_id=chat_id, photo=open('./logs/map-report.png', 'rb'))
    except:
        logger("Telegram offline...")

    try:
        sendPossibleAmountReport(sct_img)
    except:
        logger("Error finding chests.")

    clickBtn(x_button_img)
    logger("📝 Map Report sent. ", False, True)

# Count all chests in the map and calculate a value in BCoins.
def sendPossibleAmountReport(baseImage):
    c1 = len(positions(chest1, 0.5, baseImage))
    c2 = len(positions(chest2, 0.5, baseImage))
    c3 = len(positions(chest3, 0.5, baseImage))
    c4 = len(positions(chest4, 0.5, baseImage))
    c5 = len(positions(jaula, 0.5, baseImage))
    
    value1 = c1 * d_game["value_chest1"]
    value2 = c2 * d_game["value_chest2"]
    value3 = c3 * d_game["value_chest3"]
    value4 = c4 * d_game["value_chest4"]

    total = value1 + value2 + value3 + value4

    report = """
Possible quantity chest per type:
🟤  ==> """+str(c1)+"""
🟣  ==> """+str(c2)+"""
🟡  ==> """+str(c3)+"""
🔵  ==> """+str(c4)+"""
🤪  ==> Jaula """+str(c5)+"""
Possible amount : 💣 """+f'{total:.3f} bcoin'+"""
"""
    logger(report, False, True)

# Sent BCOIN report to telegram
def sendBCoinReport():
    if(len(d_telegram["telegram_chat_id"]) <= 0 or d_telegram["enable_coin_report"] is False):
        return

    try:
        clickBtn(treasure_chest_button)
    except:
        return

    time.sleep(np.random.randint(3, 5))

    coin = positions(coin_icon)

    if len(coin) <= 0:
        return

    rx, ry, _, _ = coin[0]

    sct_img = printSreen()

    w = 220
    h = 240
    x_offset = -35
    y_offset = -54

    y = ry + y_offset
    x = rx + x_offset

    crop_img = sct_img[ y : y + h , x: x + w]

    #resized = cv2.resize(crop_img, (500, 250))

    cv2.imwrite('./logs/bcoin-report.png', crop_img)
    time.sleep(1)
    try:
        for chat_id in d_telegram["telegram_chat_id"]:
            bot.send_photo(chat_id=chat_id, photo=open('./logs/bcoin-report.png', 'rb'))
    except:
        logger("Telegram offline...")
         
    clickBtn(x_button_img)
    logger("💰 BCoin Report sent. ", False, True)

def clickBtn(img, name=None, timeout=3, threshold=ct['default']):
    global open_secound_account

    logger(None, progress_indicator=True)
    if not name is None:
        pass
        # print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    clicked = False
    while(not clicked):
        matches = positions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass
                    # print('timed out')
                return False
            # print('button not found yet')
            continue

        x,y,w,h = matches[0]
        pos_click_x = x+(w/2)
        pos_click_y = y+(h/2)
        if (open_secound_account and c['usage_multi_account']):
            randomMouseMovement(False, pos_click_x+c['screen_width'], pos_click_y)
        else:
            randomMouseMovement(False, pos_click_x, pos_click_y)

        pyautogui.doubleClick()
        return True

def printSreen():
    global open_secound_account

    with mss.mss() as sct:
        # The screen part to capture
        # monitor = sct.monitors[0]
        if (open_secound_account and c['usage_multi_account']):
            monitor = {"top": 0, 
            "left": c['screen_width'], 
            "width": c['screen_width'], 
            "height": c['screen_height']}
            # logger('Open screen rigth')
        else:
            monitor = {"top": 0, 
            "left": 0, 
            "width": c['screen_width'], 
            "height": c['screen_height']}
            # logger('Open screen left')

        # Grab the data
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:,:,:3]

def positions(target, threshold=ct['default'], layout=False):
    if layout is False:
        screenshot = printSreen()
    else:
        screenshot = layout

    result = cv2.matchTemplate(screenshot,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, _ = cv2.groupRectangles(rectangles, 1, 0.2)
    
    return rectangles

def scroll():
    commoms = positions(common_label, threshold=ct['commom'])
    if (len(commoms) == 0):
        # print('no commom text found')
        return
    x,y,_,_ = commoms[len(commoms)-1]
    # print('moving to {},{} and scrolling'.format(x,y))

    randomMouseMovement(False, x, y)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0, -c['click_and_drag_amount'], duration=1, button='left')

def clickButtons():
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        randomMouseMovement(False, x+(w/2), y+(h/2))
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            logger('⛔ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(buttons)

def isWorking(bar, buttons):
    y = bar[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True

def clickGreenBarButtons():
    # ele clicka nos q tao trabaiano mas axo q n importa
    offset = 130
    green_bars = positions(green_bar, threshold=ct['green_bar'])
    logger('🟩 %d green bars detected' % len(green_bars))
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])
    logger('🆗 %d buttons detected' % len(buttons))

    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger('🆗 %d buttons with green bar detected' % len(not_working_green_bars))
        logger('👆 Clicking in %d heroes.' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        randomMouseMovement(False, x+offset+(w/2), y+(h/2))
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        if hero_clicks > 20:
            logger('⛔ Too many hero clicks, try to increase the go_to_work_btn threshold')
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
        logger('👆 Clicking in %d heroes.' % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        randomMouseMovement(False, x+offset+(w/2), y+(h/2))
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
    
    return len(not_working_full_bars)

def loggerMapClicked():
    global new_map_clicks
    new_map_clicks = new_map_clicks + 1
    logger('🗺️ {} - New Map button clicked!'.format(new_map_clicks), False, True)
    logger_file = open("./logs/new-map.log", "a", encoding='utf-8')
    logger_file.write(dateFormatted() + '\n')
    logger_file.close()

    randomMouseMovement()
    solveCapcha()
    time.sleep(np.random.randint(3, 5))
    sendMapReport()
    randomMouseMovement()

def goToHeroes():
    if clickBtn(arrow_img):
        global login_attempts
        login_attempts = 0

    solveCapcha()
    time.sleep(np.random.randint(1, 3))
    randomMouseMovement()
    clickBtn(hero_img)
    time.sleep(np.random.randint(1, 3))
    randomMouseMovement()
    solveCapcha()

def goToGame():
    # in case of server overload popup
    clickBtn(x_button_img)
    randomMouseMovement()
    # time.sleep(3)
    clickBtn(x_button_img)
    randomMouseMovement()
    clickBtn(teasureHunt_icon_img)

def refreshHeroesPositions():
    logger('🔃 Refreshing Heroes Positions')
    clickBtn(arrow_img)
    clickBtn(teasureHunt_icon_img)
    randomMouseMovement()
    # time.sleep(3)
    clickBtn(teasureHunt_icon_img)
    randomMouseMovement()

def login():
    global login_attempts
    logger('😿 Checking if game has disconnected')

    if login_attempts > 3:
        logger('🔃 Too many login attempts, refreshing.')
        login_attempts = 0
        
        if (open_secound_account and c['usage_multi_account']):
            randomMouseMovement(False, c['screen_width']+(c['screen_width']/2), c['screen_height']/2)
        else:
            randomMouseMovement(False, c['screen_width']/2, c['screen_height']/2)

        if(c['is_macos']):
            pyautogui.hotkey('command','r')
            return
        else:
            pyautogui.hotkey('ctrl','f5')
            return
    
    if clickBtn(connect_wallet_btn_img, name='connectWalletBtn', timeout=10):
        solveCapcha()
        login_attempts = login_attempts + 1
        logger('🔑 Connect wallet button detected, logging in!')
        #TODO mto ele da erro e poco o botao n abre
        # time.sleep(10)

    if clickBtn(sign_btn_img, name='signButton', timeout=8):
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
    logger('🏢 Search for heroes to work', False, True)

    goToHeroes()

    if c['select_heroes_mode'] == "full":
        logger("⚒️ Sending heroes with full stamina bar to work!", 'green')
    elif c['select_heroes_mode'] == "green":
        logger("⚒️ Sending heroes with green stamina bar to work!", 'green')
    else:
        logger("⚒️ Sending all heroes to work!", 'green')

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
        time.sleep(np.random.randint(1, 3))
    logger('💪 {} heroes sent to work'.format(hero_clicks), False, True)
    goToGame()

def getRandonPixels(range=10):
    return np.random.randint(-range, range)

def randomMouseMovement(v_rand=True, x=c['screen_width'], y=c['screen_height']):
    effects = [
        pyautogui.easeInQuad, 
        pyautogui.easeOutQuad, 
        pyautogui.easeInOutQuad,
        pyautogui.easeInBounce,
        pyautogui.easeInElastic,
        pyautogui.easeOutElastic,
        pyautogui.easeInOutElastic,
        pyautogui.easeInBack,
        pyautogui.easeOutBack,
        pyautogui.easeInOutBack,
        pyautogui.easeInCirc
    ]

    if (v_rand):
        xAccount2 = np.random.randint(0, x+(x/2))
        xAccount1 = np.random.randint(0, x)
        yAccount = np.random.randint(0, y)
    else:
        xAccount2 = xAccount1 = x
        yAccount = y

    if (open_secound_account and c['usage_multi_account']):
        rx = xAccount2 + getRandonPixels()
    else:
        rx = xAccount1 + getRandonPixels()

    ry = yAccount + getRandonPixels()

    choice = np.random.choice(effects)
    time.sleep(0.5)
    pyautogui.moveTo(rx, ry, np.random.randint(1,2), choice)

def main():
    time.sleep(5)
    t = c['time_intervals']
    global open_secound_account

    last = {
    "login" : 0,
    "heroes" : 0,
    "new_map" : 0,
    "check_for_capcha" : 0,
    "refresh_heroes" : 0,
    "bcoin_report" : 0
    }

    logger('🏁 Starting...', False, True)

    while True:
        now = time.time()

        if now - last["login"] > np.random.randint(cfl['init'],cfl['end']) * 60:
            sys.stdout.flush()
            last["login"] = now
            if c['usage_multi_account']:
                open_secound_account = not open_secound_account
                logger('🆎 Secound Account Positions {}'.format(open_secound_account))
            login()
            randomMouseMovement()

        if now - last["check_for_capcha"] > t['check_for_capcha'] * 60:
            last["check_for_capcha"] = now
            solveCapcha()
            randomMouseMovement()

        if now - last["bcoin_report"] > t['bcoin_report'] * 60:
            last["bcoin_report"] = now
            sendBCoinReport()
            randomMouseMovement()

        if now - last["heroes"] > np.random.randint(shw['init'],shw['end']) * 60:
            last["heroes"] = now
            refreshHeroes()
            randomMouseMovement()

        if now - last["new_map"] > np.random.randint(cnm['init'],cnm['end']):
            last["new_map"] = now
            if clickBtn(new_map_btn_img):
                loggerMapClicked()
            randomMouseMovement()

        if now - last["refresh_heroes"] > np.random.randint(rhp['init'],rhp['end']) * 60 :
            solveCapcha()
            last["refresh_heroes"] = now
            refreshHeroesPositions()

        randomMouseMovement()
        #clickBtn(teasureHunt)
        logger(None, progress_indicator=True)

        sys.stdout.flush()

        time.sleep(np.random.randint(5,10))

main()

#cv2.imshow('img',sct_img)
#cv2.waitKey()

# chacar se tem o sign antes de aperta o connect wallet ?
# arrumar aquela parte do codigo copiado onde tem q checar o sign 2 vezes ?
# colocar o botao em pt
# melhorar o log
# salvar timestamp dos clickes em newmap em um arquivo
# soh resetar posiçoes se n tiver clickado em newmap em x segundos

# pegar o offset dinamicamente
# clickar so no q nao tao trabalhando pra evitar um loop infinito no final do scroll se ainda tiver um verdinho
