class Terminating:
    """
    Class to represent the HTB machines terminating status
    """

    def __init__(self, identifier, terminating):
        self.identifier = identifier
        self.terminating = terminating

    def __str__(self):
        return f'id: {self.identifier}\tterminating: {self.terminating}'

    def __repr__(self):
        return f'id: {self.identifier}\tterminating: {self.terminating}'

    @staticmethod
    def json_to_terminating(json_dict):
        t = Terminating(
            json_dict['id'],
            bool(json_dict['terminating']),
        )
        return t
