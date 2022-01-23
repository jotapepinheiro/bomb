import time

totalAccounts = 4
accounts = []
counterAccounts = 1
while counterAccounts <= totalAccounts : 
    accounts.append({
        "login": 0,
        "heroes": 0,
        "new_map": 0,
        "refresh_heroes": 0
    })
    counterAccounts += 1

while True:

    curretAccount = 1
    clickWindow = 120
    for last in accounts:

        print('[{}] curret account'.format(curretAccount))
        print('[{}] window'.format(clickWindow))

        now = time.time()

        i = 1
        while i < 4:
            if now - last["heroes"] > 1 * 60:
                last["heroes"] = now
                last["refresh_heroes"] = now
                print('[{}] Heroes and Refresh heroes'.format(curretAccount))

            if now - last["refresh_heroes"] > 1 * 60:
                last["refresh_heroes"] = now
                print('[{}] Refresh heroes'.format(curretAccount))

            time.sleep(1)
            i += 1

        print('############################################################')

        clickWindow += 180
        curretAccount += 1

        time.sleep(3)
