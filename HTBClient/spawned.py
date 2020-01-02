class Spawned:
    """
    Class to represent the HTB machines spawned status
    """

    def __init__(self, identifier, spawned):
        self.identifier = identifier
        self.spawned = spawned

    def __str__(self):
        return f'id: {self.identifier}\tspawned: {self.spawned}'

    def __repr__(self):
        return f'id: {self.identifier}\tspawned: {self.spawned}'

    @staticmethod
    def json_to_spawned(json_dict):
        s = Spawned(
            json_dict['id'],
            bool(json_dict['spawned']),
        )
        return s
