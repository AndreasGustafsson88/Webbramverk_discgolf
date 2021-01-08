from App.Data.Repository import users_repo as ur


def get_all_friends(current_user):
    return ur.get_all_friends(current_user)


def get_users(users):
    return ur.get_users(users)


def get_user_by_email(email):
    return ur.get_user_by_email(email)


def get_user_by_username(username):
    return ur.get_user_by_username(username)
