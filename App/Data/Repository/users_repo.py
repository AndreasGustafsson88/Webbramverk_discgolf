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


def update_profile(current_user, update):
    if "profile_picture" in update:
        current_user.profile_picture = update["profile_picture"]
    if "email" in update:
        current_user.email = update["email"]
    if "user_name" in update:
        current_user.user_name = update["user_name"]
    if "password" in update:
        current_user.password = update["password"]
    current_user.save()
    return True


def add_round(user, user_round):
    user.history.append(user_round)
    user.save()


def add_complete_scorecard(user, id):
    user.c_score_Oid.append(id)
    user.save()


def add_incomplete_scorecard(user, scorecard):
    user.i_score_Oid.append(scorecard._id)
    user.save()


def remove_incomplete_scorecard(user, id):
    user.i_score_Oid.remove(id)
    user.save()
