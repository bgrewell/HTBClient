#!/usr/bin/env python3

import os
import time
from HTBClient import client

if __name__ == '__main__':

    htb_user = os.getenv('HTB_USER')
    htb_pass = os.getenv('HTB_PASS')

    if htb_user is None or htb_pass is None:
        print('[!] Error: Username and Password must be set in environmental variables.')
        print('[!] Below is an example')
        print('\nexport HTB_USER=someone@address.com')
        print('export HTB_PASS=hopefullyagoodpassword')
        exit(-1)

    client = client.Client()
    client.login(htb_user, htb_pass)
    machines = client.machines()
    idx = 1
    for key, value in machines.items():
        print(f'{idx}: {machines[key].name} (id={machines[key].identifier})')
        idx += 1

    player_two = machines['playertwo']
    r = player_two.start()
    print(r)
    print(client.assigned())
    time.sleep(5)
    r = player_two.todo()
    print(r)
    time.sleep(5)
    r = player_two.stop()
    print(r)
    print(client.terminating())

    print(client.todo())

    print(client.expiry())
