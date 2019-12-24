import os
import json
import time
import requests
from bs4 import BeautifulSoup
from HTBClient.machine import Machine
from HTBClient.machinedetails import MachineDetails


class Client(object):
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
