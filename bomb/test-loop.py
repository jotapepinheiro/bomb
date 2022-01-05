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
        

        for last in accounts:

            if last["conta"] == 1:
                print('[{}] check mult'.format(last["conta"]))

            if last["conta"] == 2:
                print('[{}] check mult'.format(last["conta"]))

            if last["conta"] == 3:
                print('[{}] check mult'.format(last["conta"]))

            i = 1
            while i < 6:
                now = time.time()

                if now - last["time"]["heroes"] > 1 * 60:
                    last["time"]["heroes"] = now
                    last["time"]["refresh_heroes"] = now
                    print('[{}] Heroes and Refresh heroes'.format(last["conta"]))

                if now - last["time"]["refresh_heroes"] > 1 * 60:
                    last["time"]["refresh_heroes"] = now
                    print('[{}] Refresh heroes'.format(last["conta"]))

                print('[{}] Counter'.format(i)) 
                i += 1

            print('############################################################')
            #print('[{}] farmando'.format(last["conta"]))
            time.sleep(3)
