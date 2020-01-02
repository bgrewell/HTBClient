import os
import json
import time
import requests
from bs4 import BeautifulSoup
from HTBClient.machine import Machine
from HTBClient.machinedetails import MachineDetails
from HTBClient.own import Own
from HTBClient.spawned import Spawned
from HTBClient.assigned import Assigned
from HTBClient.terminating import Terminating


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
        return self.__machines()

    def machines_free(self):
        return self.__machines(free_only=True)

    def machines_active(self, skip_owned=False):
        return self.__machines(active_only=True, skip_owned=skip_owned)

    def machines_retired(self):
        return self.__machines(retired_only=True)

    def __machines(self, active_only=False, retired_only=False, free_only=False, skip_owned=False):
        if not self.logged_in:
            raise ConnectionError('You are not logged in. You must first call login()')
        list_machines_url = 'https://www.hackthebox.eu/api/machines/get/all'
        response = self.session.get(list_machines_url, verify=self.verify_cert)
        machines_json = response.json()
        machines = {}
        owns = self.owns()
        spawned = self.spawned()
        assigned = self.assigned()
        terminating = self.terminating()
        for machine_json in machines_json:
            machine = Machine.json_to_machine(self.session, self.verify_cert, machine_json)
            if machine.identifier in terminating:
                machine.terminating = terminating[machine.identifier].terminating
            if machine.identifier in assigned:
                machine.assigned = assigned[machine.identifier].assigned
            if machine.identifier in spawned:
                machine.spawned = spawned[machine.identifier].spawned
            if machine.identifier in owns:
                machine.owned_user = owns[machine.identifier].owned_user
                machine.owned_root = owns[machine.identifier].owned_root
            if skip_owned and machine.owned_user and machine.owned_root:
                continue
            if active_only and not machine.retired:
                machines[machine.name.lower()] = machine
            elif retired_only and machine.retired:
                machines[machine.name.lower()] = machine
            elif free_only and machine.free:
                machines[machine.name.lower()] = machine
            else:
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
        owns_json = response.json()
        owns = {}
        for own_json in owns_json:
            own = Own.json_to_own(own_json)
            owns[own.identifier] = own
        return owns

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
        spawned_json = response.json()
        spawned = {}
        for spawn_json in spawned_json:
            s = Spawned.json_to_spawned(spawn_json)
            spawned[s.identifier] = s
        return spawned

    def terminating(self):
        url = 'https://www.hackthebox.eu/api/machines/terminating'
        response = self.session.get(url, verify=self.verify_cert)
        terminating_json = response.json()
        terminating = {}
        for terminate_json in terminating_json:
            t = Terminating.json_to_terminating(terminate_json)
            terminating[t.identifier] = t
        return terminating

    def assigned(self):
        url = 'https://www.hackthebox.eu/api/machines/assigned'
        response = self.session.get(url, verify=self.verify_cert)
        assigned_json = response.json()
        assigned = {}
        for assign_json in assigned_json:
            a = Assigned.json_to_assigned(assign_json)
            assigned[a.identifier] = a
        return assigned

    def expiry(self):
        url = 'https://www.hackthebox.eu/api/machines/expiry'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()

    def resetting(self):
        url = 'https://www.hackthebox.eu/api/machines/resetting'
        response = self.session.get(url, verify=self.verify_cert)
        return response.json()

    def user_owns(self):
        return self.__machine_owns(include_user=True)

    def root_owns(self):
        return self.__machine_owns(include_root=True)

    def complete_owns(self):
        return self.__machine_owns(include_user=True, include_root=True)

    def __machine_owns(self, include_user=False, include_root=False):
        machines = self.machines()
        owned_machines = {}
        if not include_root and not include_user:
            return owned_machines  # Doesn't really make sense to ask for owns but exclude both types
        for key, machine in machines.items():
            if include_root and not machine.owned_root:
                continue
            if include_user and not machine.owned_user:
                continue
            owned_machines[machine.name] = machine
        return owned_machines
