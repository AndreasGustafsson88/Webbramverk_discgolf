import json
from bson import ObjectId
from flask import Blueprint, request, Response, render_template
from flask_login import current_user, login_required
from App.Controller.courses_controller import get_one_course, get_all_names
from App.Controller.scorecards_controller import get_scorecard, delete_scorecard
from App.Controller.users_controller import get_all_friends, add_round, get_users, calculate_extra_strokes, \
    add_incomplete_scorecard, remove_incomplete_scorecard
from App.Data.Models.scorecards import Scorecard
from App.UI.routes.logged_in import logged_in

scorecards = Blueprint('scorecards', __name__)


@scorecards.route('/scorecard', methods=["POST", "GET"])
@login_required
def scorecard():
    if request.method == 'POST':
        course = get_one_course(request.form["course"])
        response = Response(
            response=json.dumps(course.holes[0]),
            status=200,
            mimetype="application/json"
        )
        return response
    friends = get_all_friends(current_user)

    all_courses = get_all_names()

    return render_template("create_scorecard.html", all_courses=all_courses, friends=friends, current_user=current_user)


@scorecards.route("/scorecard/play", methods=['GET', 'POST'])
@login_required
def scorecard_play():
    if request.method == 'POST':
        player_summary = json.loads(request.form['p_summary'])
        message = add_round(player_summary)
        response = Response(
            response=json.dumps(message),
            status=200,
            mimetype="application/json"
        )
        return response

    players = get_users(request.args.get("players").replace("[", "").replace("]", "").replace('"', '').split(","))
    course = get_one_course(request.args.get("course"))
    rated = True if request.args.get("rated") == "true" else False
    multi = int(request.args.get("multi"))

    for player in players:
        player.hcp = calculate_extra_strokes(player, course)

    round_summary = {'course_id': str(course._id),
                     'course': course.name,
                     'course_holes': course.holes,
                     'rated': rated,
                     'players': [{'user_name': player.user_name,
                                  'full_name': player.full_name,
                                  'hcp': player.hcp,
                                  'stats': {f'hole{i+1}{v}': "" for i in range(course.holes[0] * multi)
                                                   for v in ['_points', '_par', '_throws']}} for player in players],
                     'active': True,
                     'multi': multi
                     }
    scorecard = Scorecard.insert_one(round_summary)

    add_incomplete_scorecard(scorecard, players)

    return render_template("scorecard.html", round_summary=scorecard)


@scorecards.route('/scorecard/<scorecard_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def scorecard_history(scorecard_id):

    if request.method == 'POST':
        scorecard = get_scorecard(_id=ObjectId(request.form['button']))

        return render_template('scorecard.html', round_summary=scorecard)

    if request.method == 'DELETE':

        scorecard = get_scorecard(_id=ObjectId(json.loads(request.form['p_summary'])['_id']))

        remove_incomplete_scorecard(scorecard)
        delete_scorecard(scorecard)

        return 'Scorecard deleted'

    scorecard = get_scorecard(_id=ObjectId(scorecard_id))
    return render_template('scorecard.html', round_summary=scorecard)
