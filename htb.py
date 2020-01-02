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
        print(
            f'{idx}: {machines[key].name} (id={machines[key].identifier}) user={machines[key].owned_user} root={machines[key].owned_root}')
        idx += 1

    print('user owns:')
    user_owns = client.user_owns()
    for key, machine in user_owns.items():
        print(f'name: {machine.name}\tpoints: {machine.points}')

    print('root owns:')
    root_owns = client.root_owns()
    for key, machine in root_owns.items():
        print(f'name: {machine.name}\tpoints: {machine.points}')
