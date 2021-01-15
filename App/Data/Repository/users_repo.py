import json
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


def get_user(kwargs):
    return User.find(**kwargs).first_or_none()


def get_all_users():
    return [user.user_name for user in User.all()]


def add_user(insert_dict):
    return User.insert_one(insert_dict)


def add_friend(user, ob_id, from_request=False):
    try:
        user.friends.append(ob_id)
        if from_request:
            user.Oid_req.remove(ob_id)
        user.save()
        return {
            'status': 200,
            'mimetype': 'application/json',
            'response': json.dumps('added as you friend!')
        }
    except:
        return {
            'status': 200,
            'mimetype': 'application/json',
            'response': json.dumps('Unknown error, contact Admin')
        }


def find_unique(kwargs):
    return User.find_unique(**kwargs)


def delete_friend(user, ob_id):
    try:
        user.friends.remove(ob_id)
        user.save()
        return {
            'status': 200,
            'mimetype': 'application/json',
            'response': json.dumps('removed as friend!')
        }
    except:
        return {
            'status': 200,
            'mimetype': 'application/json',
            'response': json.dumps('Unknown error, contact Admin')
        }


def add_friend_request(current_user, visited_user):
    visited_user.Oid_req.append(current_user._id)
    visited_user.save()


def delete_friend_request(user, ob_id):
    try:
        user.Oid_req.remove(ob_id)
        user.save()
        return {
            'status': 200,
            'mimetype': 'application/json',
            'response': json.dumps('wasn\'t added as your friend')
        }
    except:
        return {
            'status': 200,
            'mimetype': 'application/json',
            'response': json.dumps('Unknown error, contact Admin')
        }
