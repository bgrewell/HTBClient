#!/usr/bin/env python3

import os
import time
import argparse
from HTBClient import client


def main():

    htb_user = os.getenv('HTB_USER')
    htb_pass = os.getenv('HTB_PASS')

    parser = argparse.ArgumentParser(description='hackthebox.eu command line client')
    parser.add_argument('--assigned', action='store_true', help='show your currently spawned machine')
    parser.add_argument('--start', type=str, help='start the specified machine')
    parser.add_argument('--stop', action='store_true', help='stops your spawned machine')
    parser.add_argument('--reset', type=str, help='reset the specified machine')
    parser.add_argument('--todo', type=str, help='toggle todo on specified machine')
    parser.add_argument('--list', choices=['all', 'owned', 'todo', 'spawned', 'active', 'retired', 'incomplete',
                                           'roots', 'users', 'terminating'],
                        help='lists machine names and ip addresses')
    parser.add_argument('--username', type=str, help='htb username <only needed if you dont have env variables>')
    parser.add_argument('--password', type=str, help='htb username <only needed if you dont have env variables>')

    args = parser.parse_args()

    if (htb_user is None and args.username is None) or (htb_pass is None and args.password is None):
        print('[!] Error: Username and Password must be set in environmental variables.')
        print('[!] Below is an example')
        print('\nexport HTB_USER=someone@address.com')
        print('export HTB_PASS=hopefullyagoodpassword')
        exit(-1)

    client = client.Client()
    client.login(htb_user, htb_pass)

    if args.assigned:
        assigned_machine = {k: v for k, v in client.machines().items() if v.assigned}
        pretty_print(assigned_machine)

    if args.start is not None:
        machines = client.machines()
        target = args.start.lower()
        for key, value in machines.items():
            if value.assigned:
                message = "finishes terminating" if value.terminating else "is stopped"
                print(f'cannot start a new machine until {value.name} {message}')
                exit(-1)
        machine = machines.get(target, None)
        if machine is None:
            print('machine not found')
            exit(-1)
        machine.start()

    if args.stop:
        machines = client.machines()
        for key, value in machines.items():
            if value.assigned:
                value.stop()

    if args.list:
        list_arg = args.list
        if list_arg == 'owned':
            owned_machines = {k: v for k, v in client.machines().items() if v.owned_root and v.owned_user}
            pretty_print(owned_machines)
        elif list_arg == 'todo':
            todos = client.todo()
            pretty_print(todos)
            todo_machines = {k: v for k, v in client.machines().items() if v.identifier in todos}
            pretty_print(todo_machines)
        elif list_arg == 'spawned':
            spawned_machines = {k: v for k, v in client.machines().items() if v.spawned}
            pretty_print(spawned_machines)
        elif list_arg == 'active':
            active_machines = {k: v for k, v in client.machines().items() if not v.retired}
            pretty_print(active_machines)
        elif list_arg == 'retired':
            retired_machines = {k: v for k, v in client.machines().items() if v.retired}
            pretty_print(retired_machines)
        elif list_arg == 'incomplete':
            incomplete_machines = {k: v for k, v in client.machines().items() if not v.owned_user or not v.owned_root}
            pretty_print(incomplete_machines)
        elif list_arg == 'roots':
            owned_machines = {k: v for k, v in client.machines().items() if v.owned_root}
            pretty_print(owned_machines)
        elif list_arg == 'users':
            owned_machines = {k: v for k, v in client.machines().items() if v.owned_user}
            pretty_print(owned_machines)
        elif list_arg == 'terminating':
            terminating_machines = {k: v for k, v in client.machines().items() if v.terminating}
            pretty_print(terminating_machines)
        else:
            pretty_print(client.machines())


def pretty_print(machines):
    for key, value in machines.items():
        value.pretty_basic()


if __name__ == '__main__':
    main()
