class Own:
    """
    Class to represent the HTB machines
    """

    def __init__(self, identifier, owned_user, owned_root):
        self.identifier = identifier
        self.owned_user = owned_user
        self.owned_root = owned_root

    def __str__(self):
        return f'id: {self.identifier}\towned_user: {self.owned_user}\towned_root: {self.owned_root}'

    def __repr__(self):
        return f'id: {self.identifier}\towned_user: {self.owned_user}\towned_root: {self.owned_root}'

    @staticmethod
    def json_to_own(json_dict):
        o = Own(
            json_dict['id'],
            json_dict['owned_user'],
            json_dict['owned_root'],
        )
        return o
