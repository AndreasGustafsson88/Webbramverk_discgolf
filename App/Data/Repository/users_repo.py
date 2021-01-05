from App.Data.Models.users import User
from bson import ObjectId


def get_all_friends(current_user):
    return [User.find(_id=ObjectId(player)).first_or_none().user_name for player in current_user.friends]


def get_users(users):
    return [User.find(user_name=user).first_or_none() for user in users]
