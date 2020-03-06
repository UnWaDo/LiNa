from hashlib import md5


class User:
    def __init__(self, log, pas, lvl):
        self.login = log
        self.password = pas
        self.level = lvl

    def check_pass(self, pas):
        return md5(pas.encode()).hexdigest() == self.password


class UsersHolder:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def get_user_by_login(self, log):
        for user in self.users:
            if log == user.login:
                return user
        return None

    def get_logins_list(self):
        logins = []
        for user in self.users:
            logins.append(user.login)
        return logins

    def check_logpas(self, log, pas):
        user = self.get_user_by_login(log)
        if user is None:
            return 1
        elif user.check_pass(pas):
            return 0
        else:
            return 2

    def modify_level(self, login, level):
        us = self.get_user_by_login(login)
        us.level = level
        f = open('web/control.txt', 'w')
        string = ""
        for user in self.users:
            string += user.login+':'+user.password+':'+str(user.level)+';'
        f.write(string)


def read_auth_data():
    try:
        f = open('web/control.txt', 'r')
    except OSError:
        f = open('web/def_control.txt', 'r')
    line = f.readline()
    split_line = line.split(';')
    uh = UsersHolder()
    split_line.pop(len(split_line) - 1)
    for user in split_line:
        u, p, a = user.split(':')
        uh.add_user(User(u, p, int(a)))

    return uh
