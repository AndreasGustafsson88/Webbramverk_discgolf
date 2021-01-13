from App.Data.Repository import users_repo as ur


def get_all_friends(current_user):
    return ur.get_all_friends(current_user)


def get_users(users):
    return ur.get_users(users)


def get_user_by_email(email):
    return ur.get_user_by_email(email)


def get_user_by_username(username):
    return ur.get_user_by_username(username)


def get_user(**kwargs):
    return ur.get_user(kwargs)


def add_user(user_name, full_name, password, email):

    insert_dict = {
        "user_name": user_name,
        "full_name": full_name,
        "email": email,
        "password": password,
        "favorite_courses": [],
        "friends": [],
        "rating": None,
        "history": [],
        "profile_picture": None
    }
    ur.add_user(insert_dict)


def find_unique(**kwargs):
    return ur.find_unique(kwargs)
