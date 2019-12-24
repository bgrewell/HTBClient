

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