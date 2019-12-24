#!/usr/bin/env python3

import os
import json
import time
import requests
from bs4 import BeautifulSoup


class MachineDetails:
    """
    Class to represent the HTB machine details
    """

    def __init__(self, identifier, name, operating_system, ip, avatar, avatar_thumb, points, release, retired_date,
                 maker, maker2, ratings_pro, ratings_sucks, user_blood, root_blood, user_owns, root_owns):
        self.identifier = identifier
        self.name = name
        self.operating_system = operating_system
        self.ip = ip
        self.avatar = avatar
        self.avatar_thumb = avatar_thumb
        self.points = points
        self.release = release
        self.retired_date = retired_date
        self.maker = maker
        self.maker2 = maker2
        self.ratings_pro = ratings_pro
        self.ratings_sucks = ratings_sucks
        self.user_blood = user_blood
        self.root_blood = root_blood
        self.user_owns = user_owns
        self.root_owns = root_owns

    @staticmethod
    def json_to_machinedetails(json_dict):
        md = MachineDetails(
            json_dict['id'],
            json_dict['name'],
            json_dict['os'],
            json_dict['ip'],
            json_dict['avatar'],
            json_dict['avatar_thumb'],
            json_dict['points'],
            json_dict['release'],
            json_dict['retired_date'],
            json_dict['maker'],
            json_dict['maker2'],
            json_dict['ratings_pro'],
            json_dict['ratings_sucks'],
            json_dict['user_blood'],
            json_dict['root_blood'],
            json_dict['user_owns'],
            json_dict['root_owns'],
        )
        return md

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Machine:
    """
    Class to represent the HTB machines
    """

    def __init__(self, session, verify_cert, identifier, name, operating_system, ip, avatar_thumb, points, release,
                 retired_date, maker, maker2, rating, user_owns, root_owns, retired, free):
        self.session = session
        self.verify_cert = verify_cert
        self.identifier = identifier
        self.name = name
        self.operating_system = operating_system
        self.ip = ip
        self.avatar_thumb = avatar_thumb
        self.points = points
        self.release = release
        self.retire_date = retired_date
        self.maker = maker
        self.maker2 = maker2
        self.rating = rating
        self.user_owns = user_owns
        self.root_owns = root_owns
        self.retired = retired
        self.free = free

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __request_json(self, url, data={}):
        response = self.session.post(url, verify=self.verify_cert, data=data)
        print(f"status_code: {response.status_code}")
        print(f"response: {response.text}")
        return response.json()

    @staticmethod
    def json_to_machine(session, verify_cert, json_dict):
        m = Machine(
            session,
            verify_cert,
            json_dict['id'],
            json_dict['name'],
            json_dict['os'],
            json_dict['ip'],
            json_dict['avatar_thumb'],
            json_dict['points'],
            json_dict['release'],
            json_dict['retired_date'],
            json_dict['maker'],
            json_dict['maker2'],
            json_dict['rating'],
            json_dict['user_owns'],
            json_dict['root_owns'],
            json_dict['retired'],
            json_dict['free'],
        )
        return m

    def start(self):
        url = 'https://www.hackthebox.eu/api/vm/vip/assign/{id}'.format(id=self.identifier)
        return self.__request_json(url)

    def stop(self):
        url = 'https://www.hackthebox.eu/api/vm/vip/remove/{id}'.format(id=self.identifier)
        return self.__request_json(url)

    def extend(self):
        url = 'https://www.hackthebox.eu/api/vm/vip/extend/{id}'.format(id=self.identifier)
        return self.__request_json(url)

    def todo(self):
        url = 'https://www.hackthebox.eu/api/machines/todo/update/{id}'.format(id=self.identifier)
        return self.__request_json(url)

    def reset(self):
        url = 'https://www.hackthebox.eu/api/vm/reset/{id}'.format(id=self.identifier)
        return self.__request_json(url)

    def own(self, flag, difficulty):
        if not isinstance(difficulty, int) or difficulty < 1 or difficulty > 10:
            raise TypeError('difficulty must be an integer between 1 and 10')
        url = 'https://www.hackthebox.eu/api/machines/own'
        payload = {'flag': flag, 'difficulty': difficulty, 'id': self.identifier}
        return self.__request_json(url, data=payload)


class HTBClient(object):
    additional_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.98 Safari/537.36',
        'Referer': 'https://www.hackthebox.eu/'}
    login_url = 'https://www.hackthebox.eu/login'
    verify_cert = True
    logged_in = False
    session = None
    _token = None

    def __init__(self, verify_cert=True):
        self.verify_cert = verify_cert
        if "HTB_NO_CERTCHECK" in os.environ:
            self.verify_cert = False
        if "HTB_USER_AGENT" in os.environ:
            self.additional_headers = {'user-agent': os.getenv('HTB_USER_AGENT')}

    def login(self, username, password):
        self.session = requests.Session()
        self.session.headers.update(self.additional_headers)
        response = self.session.get(self.login_url, verify=self.verify_cert)
        soup = BeautifulSoup(response.text, features='lxml')
        self._token = soup.find('input', {'name': '_token'})['value']
        data = {'_token': self._token, 'email': username, 'password': password}
        response = self.session.post(self.login_url, data=data, verify=self.verify_cert)
        soup = BeautifulSoup(response.text, features='lxml')
        csrf_token = soup.select_one('meta[name="csrf-token"]')['content']
        response = self.session.get("https://www.hackthebox.eu/home/machines", verify=self.verify_cert)
        auth_key_lindex = response.text.find("apiToken\":\"") + 11  # TODO: Clean up, sloppy way to get the apiToken
        auth_key_rindex = response.text.find("\"", auth_key_lindex)
        auth_key = response.text[auth_key_lindex:auth_key_rindex]
        self.session.headers.update({'X-CSRF-TOKEN': csrf_token, 'X-Requested-With': 'XMLHttpRequest',
                                     'X-XSRF-TOKEN': self._token, 'Authorization': 'Bearer ' + auth_key})
        self.logged_in = response.status_code == 200
        return self.logged_in

    def machines(self):
        if not self.logged_in:
            raise ConnectionError('You are not logged in. You must first call login()')
        list_machines_url = 'https://www.hackthebox.eu/api/machines/get/all'
        response = self.session.get(list_machines_url, verify=self.verify_cert)
        machines_json = response.json()
        machines = {}
        for machine_json in machines_json:
            machine = Machine.json_to_machine(self.session, self.verify_cert, machine_json)
            machines[machine.name.lower()] = machine
        return machines

    def machine_details(self, identifier):
        if not self.logged_in:
            raise ConnectionError('You are not logged in. You must first call login()')
        url = "https://www.hackthebox.eu/api/machines/get/{id}".format(id=identifier)
        response = self.session.get(url, verify=self.verify_cert)
        machine = MachineDetails.json_to_machinedetails(response.json())
        return machine

    def owns(self):
        url = 'https://www.hackthebox.eu/api/machines/owns'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()

    def difficulty(self):
        url = 'https://www.hackthebox.eu/api/machines/difficulty'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()

    def reviews(self):
        url = 'https://www.hackthebox.eu/api/machines/reviews'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()

    def todo(self):
        url = 'https://www.hackthebox.eu/api/machines/todo'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()

    def spawned(self):
        url = 'https://www.hackthebox.eu/api/machines/spawned'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()

    def terminating(self):
        url = 'https://www.hackthebox.eu/api/machines/terminating'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()

    def assigned(self):
        url = 'https://www.hackthebox.eu/api/machines/assigned'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()

    def expiry(self):
        url = 'https://www.hackthebox.eu/api/machines/expiry'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()

    def resetting(self):
        url = 'https://www.hackthebox.eu/api/machines/resetting'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()


if __name__ == '__main__':

    htb_user = os.getenv('HTB_USER')
    htb_pass = os.getenv('HTB_PASS')

    if htb_user is None or htb_pass is None:
        print('[!] Error: Username and Password must be set in environmental variables.')
        print('[!] Below is an example')
        print('\nexport HTB_USER=someone@address.com')
        print('export HTB_PASS=hopefullyagoodpassword')
        exit(-1)

    client = HTBClient()
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
