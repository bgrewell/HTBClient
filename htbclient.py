import os
import requests
from bs4 import BeautifulSoup


class HTBClient(object):

    login_url = 'https://www.hackthebox.eu/login'
    session = None
    additional_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36', 'Referer': 'https://www.hackthebox.eu/'}
    _token = None
    logged_in = False
    verify_cert = True

    def __init__(self, verify_cert=True):
        self.verify_cert = verify_cert
        pass

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
        auth_key_lindex = response.text.find("apiToken\":\"") + 11              # TODO: Clean up, sloppy way to get the apiToken
        auth_key_rindex = response.text.find("\"", auth_key_lindex)
        auth_key = response.text[auth_key_lindex:auth_key_rindex]
        self.session.headers.update({'X-CSRF-TOKEN': csrf_token, 'X-Requested-With': 'XMLHttpRequest',
                                     'X-XSRF-TOKEN': self._token, 'Authorization': 'Bearer ' + auth_key})
        self.logged_in = response.status_code == 200
        return self.logged_in

    def list_machines(self):
        list_machines_url = 'https://www.hackthebox.eu/api/machines/get/all'
        if not self.logged_in:
            raise ConnectionError('You are not logged in. You must first call login()')
        response = self.session.get(list_machines_url, verify=self.verify_cert)
        print(response.text)


if __name__ == '__main__':

    htb_user = os.getenv('HTB_USER')
    htb_pass = os.getenv('HTB_PASS')

    client = HTBClient(verify_cert=False)
    logged_in = client.login(htb_user, htb_pass)
    print("Logged in: " + str(logged_in))
    client.list_machines()
