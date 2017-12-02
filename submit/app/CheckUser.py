from DBInteract import DBInteract


class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.dbi = DBInteract()

    def verify(self):
        if self.password == self.dbi.get_password(self.username):
            return True
        else:
            return False
