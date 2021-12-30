import time

accounts = [
    {
        "conta": 1,
        "time": {
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "refresh_heroes": 0,
            "check_mult": 0
        }
    },
    {
        "conta": 2,
        "time": {
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "refresh_heroes": 0,
            "check_mult": 0
        }
    },
    {
        "conta": 3,
        "time": {
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "refresh_heroes": 0,
            "check_mult": 0
        }
    }
]

while True:
        now = time.time()

        for last in accounts:

            if now - last["time"]["heroes"] > 1 * 60:
                last["time"]["heroes"] = now
                last["time"]["refresh_heroes"] = now
                print('[{}] Heroes and Refresh heroes'.format(last["conta"]))

            if now - last["time"]["refresh_heroes"] > 1 * 60:
                last["time"]["refresh_heroes"] = now
                print('[{}] Refresh heroes'.format(last["conta"]))

            #if now - last["time"]["check_mult"] > 1 * 60:
            if last["conta"] == 1:
                print('[{}] check mult'.format(last["conta"]))
                last["time"]["check_mult"] = now

            if last["conta"] == 2:
                print('[{}] check mult'.format(last["conta"]))
                last["time"]["check_mult"] = now

            if last["conta"] == 3:
                print('[{}] check mult'.format(last["conta"]))
                last["time"]["check_mult"] = now
            
            print('############################################################')
            #print('[{}] farmando'.format(last["conta"]))
            time.sleep(3)
