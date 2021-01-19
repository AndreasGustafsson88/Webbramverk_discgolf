import time
import json

from bson import ObjectId

from App.Data.Repository import users_repo as ur
from App.Data.Repository import courses_repo as cr


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
        "profile_picture": None,
        "Oid_req": []
    }
    ur.add_user(insert_dict)


def find_unique(**kwargs):
    return ur.find_unique(kwargs)


def get_all_users():
    return ur.get_all_users()


def add_friend(user, id, from_request=False):
    ob_id = ObjectId(id)
    if ob_id not in user.friends:
        return ur.add_friend(user, ob_id, from_request)
    else:
        return {
            'status': 200,
            'mimetype': 'application/json',
            'response': json.dumps('already in you friends list')
        }


def delete_friend(user, friend):
    if friend in user.friends:
        return ur.delete_friend(user, friend)
    else:
        return {
            'status': 200,
            'mimetype': 'application/json',
            'response': json.dumps('Not in your friend list')
        }


def delete_friend_request(user, ob_id):
    return ur.delete_friend_request(user, ob_id)


def add_friend_request(current_user, visited_user):
    if current_user not in visited_user.friends_list:
        return ur.add_friend_request(current_user, visited_user)


def update_profile(current_user, profile_picture, user_name, email, password):
    return ur.update_profile(current_user, profile_picture, user_name, email, password)


def add_round(player_summary):
    course = cr.get_course_by_id(ObjectId(player_summary['Course']))
    users = [ur.get_user_by_username(user) for user in player_summary.keys() if isinstance(player_summary[user], dict)]

    for user in users:
        u_round = []
        u_round.append(time.strftime('%Y-%m-%d'))
        total_throws = sum([int(player_summary[user.user_name][key]) for key in player_summary[user.user_name].keys() if 'throws' in key])
        throw_per_hole = [int(player_summary[user.user_name][key]) for key in player_summary[user.user_name].keys() if 'throws' in key]
        if str(total_throws) in course.rating:
            rating = course.rating[str(total_throws)]
            u_round.append(rating)
        u_round.append(total_throws)
        #TODO Fråga Joakim om u_round.copy()?! loggar ObjectId på första runda utan.copy()
        cr.add_round(course, u_round.copy())
        u_round.append(course._id)
        ur.add_round(user, u_round)
        course.average_per_hole(throw_per_hole)
    return True
