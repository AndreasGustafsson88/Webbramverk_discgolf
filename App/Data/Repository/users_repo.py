from App.Data.Models.users import User
from bson import ObjectId


def get_all_friends(current_user):
    return [User.find(_id=ObjectId(player)).first_or_none().user_name for player in current_user.friends]


def get_users(users):
    return [User.find(user_name=user).first_or_none() for user in users]


def get_user_by_email(email):
    return User.find(email=email).first_or_none()


def get_user_by_username(username):
    return User.find(user_name=username).first_or_none()


def add_user(insert_dict):
    return User.insert_one(insert_dict)


def get_all_users():
    return [user.user_name for user in User.all()]


def add_friend(user, ob_id):

    user.friends.append(ob_id)
    user.save()