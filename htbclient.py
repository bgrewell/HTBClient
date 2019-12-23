import os
import requests
from bs4 import BeautifulSoup

class HTBClient(object):

    login_url = "https://www.hackthebox.eu/login"
    session = None
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36", 'Referer': "https://www.hackthebox.eu/"}
    csrf_token = None

    def __init__(self):
        pass

    def Login(self, username, password):
        data = {}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        response = self.session.get(self.login_url)
        soup = BeautifulSoup(response.text)
        self.csrf_token = soup.find('input', {'name': '_token'})['value']
        data['_token'] = self.csrf_token
        data['email'] = username
        data['password'] = password
        response = self.session.post(self.login_url, headers=self.headers, data=data)
        print(response)





if __name__ == '__main__':

    htb_user = os.getenv('HTB_USER')
    htb_pass = os.getenv('HTB_PASS')

    client = HTBClient()
    client.Login(htb_user, htb_pass)