class Assigned:
    """
    Class to represent the HTB machines assigned status
    """

    def __init__(self, identifier, assigned):
        self.identifier = identifier
        self.assigned = assigned

    def __str__(self):
        return f'id: {self.identifier}\tassigned: {self.assigned}'

    def __repr__(self):
        return f'id: {self.identifier}\tassigned: {self.assigned}'

    @staticmethod
    def json_to_assigned(json_dict):
        a = Assigned(
            json_dict['id'],
            bool(json_dict['assigned']),
        )
        return a
