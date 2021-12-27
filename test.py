#!/usr/bin/python3
# coding: utf-8

from cv2 import cv2
from numpy.random.mtrand import beta
from pyclick import HumanClicker

import numpy as np
import time
import sys
import yaml

stream = open("config.yaml", 'r')
if stream is not None:
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
    stream.close()
else:
    print('Arquivo de configuração não encontrado, saindo...')
    time.sleep(3)
    exit()

current_account = 1
browser = 0

hc = HumanClicker()

def randomMouseMovement(x,y,t):
    hc.move((int(x), int(y)), t)

def randomInt(init = 10, end = 1000):
    return np.random.randint(init, end)

def main() -> None:
    global current_account
    global browser
    time.sleep(3)

    last = [
        {
            "account": 1,
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "check_for_capcha" : 0,
            "refresh_heroes": 0,
            "bcoin_report" : 0
        },
        {
            "account": 2,
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "check_for_capcha" : 0,
            "refresh_heroes": 0,
            "bcoin_report" : 0
        }
    ]

    while True:
        now = time.time()

        if now - last[browser]["login"] > randomInt(cfl['init'], cfl['end']) * 60:
            sys.stdout.flush()
            last[browser]["login"] = now
            print(f'Foi login na conta {last[browser]["account"]}')
            randomMouseMovement(randomInt(), randomInt(), 1)
            time.sleep(randomInt(1, 3))

        if now - last[browser]["check_for_capcha"] > t['check_for_capcha'] * 60:
            last[browser]["check_for_capcha"] = now
            print(f'Foi check_for_capcha na conta {last[browser]["account"]}')
            randomMouseMovement(randomInt(), randomInt(), 1)
            time.sleep(randomInt(1, 3))

        if now - last[browser]["bcoin_report"] > t['bcoin_report'] * 60:
            last[browser]["bcoin_report"] = now
            print(f'Foi bcoin_report na conta {last[browser]["account"]}')
            randomMouseMovement(randomInt(), randomInt(), 1)
            time.sleep(randomInt(1, 3))

        if now - last[browser]["heroes"] > randomInt(shw['init'], shw['end']) * 60:
            last[browser]["heroes"] = now
            print(f'Foi heroes na conta {last[browser]["account"]}')
            randomMouseMovement(randomInt(), randomInt(), 1)
            time.sleep(randomInt(1, 3))

        if now - last[browser]["new_map"] > randomInt(cnm['init'], cnm['end']):
            last[browser]["new_map"] = now
            print('Foi new_map')
            print(f'Foi new_map na conta {last[browser]["account"]}')
            randomMouseMovement(randomInt(), randomInt(), 1)
            time.sleep(randomInt(1, 3))

        if now - last[browser]["refresh_heroes"] > randomInt(rhp['init'], rhp['end']) * 60:
            last[browser]["refresh_heroes"] = now
            print(f'Foi refresh_heroes na conta {last[browser]["account"]}')
            randomMouseMovement(randomInt(), randomInt(), 1)
            time.sleep(randomInt(1, 3))

        sys.stdout.flush()

        if c['usage_multi_account']:
            current_account = last[browser]["account"]
            browser = 1 if browser == 0 else 0
        
        time.sleep(randomInt(5, 10))
        print(f'============= {browser} =============')
        print(f'============= {current_account} =============')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()