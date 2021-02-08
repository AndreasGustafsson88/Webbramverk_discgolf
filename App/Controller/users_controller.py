import time
import json

from bson import ObjectId

from App.Data.Repository import users_repo as ur
from App.Data.Repository import courses_repo as cr
from App.Data.Repository import scorecards_repo as sr


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
        "favourite_courses": [],
        "friends": [],
        "history": [],
        "profile_picture": None,
        "Oid_req": [],
        "c_score_Oid": [],
        "i_score_Oid": []
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
    if current_user._id not in visited_user.friends:
        return ur.add_friend_request(current_user, visited_user)


def update_profile(current_user, update):
    return ur.update_profile(current_user, update)


def add_round(player_summary):

    if not player_summary['active']:
        scorecard = sr.get_scorecard({'_id': ObjectId(player_summary['_id'])})
        sr.save_scorecard(scorecard)

        course = cr.get_course_by_id(ObjectId(player_summary['course_id']))
        users = [ur.get_user_by_username(user['user_name']) for user in player_summary['players']]

        for i, user in enumerate(users):
            ur.add_complete_scorecard(user, player_summary['_id'])
            ur.remove_incomplete_scorecard(user, ObjectId(player_summary['_id']))

            throw_per_hole = [int(player_summary['players'][i]['stats'][key]) for key in
                              player_summary['players'][i]['stats'].keys() if 'throws' in key]
            total_throws = sum(throw_per_hole)
            rating = course.rating[str(total_throws)]

            if len(course.history) > 50:
                if str(total_throws) in course.rating:
                    u_round = []

                    u_round.append(time.strftime('%Y-%m-%d'))
                    u_round.append(rating)
                    u_round.append(total_throws)
                    u_round.append(course._id)

                    ur.add_round(user, u_round)

            if len(user.history) > 5 and -151 < user.rating - rating < 151:
                c_round = []

                c_round.append(time.strftime('%Y-%m-%d'))
                c_round.append(user.rating)
                c_round.append(total_throws)

                cr.add_round(course, c_round)

            cr.add_logged_round_and_average(course, throw_per_hole)

        return "Well played! You will be redirected to the profile page"

    if player_summary['active']:
        scorecard = sr.get_scorecard({'_id': ObjectId(player_summary['_id'])})
        sr.update_scorecard(scorecard, player_summary)

        return 'Round saved!'


def add_strokes(total_throws, hole_average, course):
    difference = total_throws - course.course_par

    if difference == 0:
        return sorted(hole_average, key=lambda x: x["hole"])

    elif difference < 0:
        for i in range(1, difference * -1 + 1):
            hole_average[-i % course.holes[0]]["strokes"] -= 1

    elif difference > 0:
        for i in range(difference):
            hole_average[i % course.holes[0]]["strokes"] += 1


def find_extra_strokes(player, course):
    total_throws = 0

    for k, v in course.rating.items():
        if v == player.rating:
            total_throws += int(k)
            return total_throws

        elif v >= player.rating:
            total_throws += int(k) + 1
            return total_throws


def calculate_extra_strokes(player, course):
    """
    Create dict and sort by average to get difficulty / hole. Add or remove extra strokes from
    hole par depending on extra strokes for each player.
    """
    hole_average = sorted([{"hole": i, "average": "{:.2f}".format(hole["average"] - hole["Par"]), "strokes": 0}
                           for i, hole in enumerate(course.holes[1:], 1)], key=lambda x: x["average"], reverse=True)

    if player.rating is None or len(course.rating) == 0:
        return sorted(hole_average, key=lambda x: x['hole'])

    total_throws = find_extra_strokes(player, course)
    add_strokes(total_throws, hole_average, course)

    return sorted(hole_average, key=lambda x: x["hole"])


def add_incomplete_scorecard(scorecard, players):
    for player in players:
        ur.add_incomplete_scorecard(player, scorecard)


def remove_incomplete_scorecard(scorecard):
    users = ur.get_users([player['user_name'] for player in scorecard.players])

    for user in users:
        ur.remove_incomplete_scorecard(user, scorecard._id)
