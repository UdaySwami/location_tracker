class InvalidCredentials(Exception):
    def __init__(self):
        super(InvalidCredentials, self).__init__("Invalid Credentials Provided")


class InvalidUser(Exception):
    def __init__(self):
        super(InvalidUser, self).__init__("User with the given email does not exist")


class InvalidAPIRequest(Exception):
    def __init__(self):
        super(InvalidAPIRequest, self).__init__("This API is not Allowed")
