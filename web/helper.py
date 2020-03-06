from flask import session
from web.service import read_auth_data


def cur_user():
    if 'login' in session:
        users_holder = read_auth_data()
        return users_holder.get_user_by_login(session['login'])
    return None


def update_user_level(login, level):
    users_holder = read_auth_data()
    users_holder.modify_level(login, level)
