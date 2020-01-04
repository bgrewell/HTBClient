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
        self.retired_date = retired_date
        self.maker = maker
        self.maker2 = maker2
        self.rating = rating
        self.user_owns = user_owns
        self.root_owns = root_owns
        self.retired = retired
        self.free = free
        self.owned_user = False
        self.owned_root = False
        self.spawned = False
        self.assigned = False
        self.terminating = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __request_json(self, url, data=None):
        if data is None:
            data = {}
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

    def pretty_basic(self):
        print(f"machine: {self.name}")
        print(f"ip: {self.ip}")
        print(f"id: {self.identifier}")

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
