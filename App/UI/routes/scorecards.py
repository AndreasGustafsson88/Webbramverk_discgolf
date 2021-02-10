import json
from bson import ObjectId
from flask import Blueprint, request, Response, render_template
from flask_login import current_user, login_required
from App.Controller import courses_controller as cc
from App.Controller import scorecards_controller as sc
from App.Controller import users_controller as uc

scorecards = Blueprint('scorecards', __name__)


@scorecards.route('/scorecard', methods=["POST", "GET"])
@login_required
def scorecard():
    if request.method == 'POST':
        course = cc.get_one_course(request.form["course"])
        response = Response(
            response=json.dumps(course.holes[0]),
            status=200,
            mimetype="application/json"
        )
        return response
    friends = uc.get_all_friends(current_user)

    all_courses = cc.get_all_names()

    return render_template("create_scorecard.html", all_courses=all_courses, friends=friends, current_user=current_user)


@scorecards.route("/scorecard/play", methods=['GET', 'POST'])
@login_required
def scorecard_play():
    if request.method == 'POST':
        player_summary = json.loads(request.form['p_summary'])
        message = uc.add_round(player_summary)
        response = Response(
            response=json.dumps(message),
            status=200,
            mimetype="application/json"
        )
        return response

    players = uc.get_users(request.args.get("players").replace("[", "").replace("]", "").replace('"', '').split(","))
    course = cc.get_one_course(request.args.get("course"))
    rated = True if request.args.get("rated") == "true" else False
    multi = int(request.args.get("multi"))

    for player in players:
        player.hcp = uc.calculate_extra_strokes(player, course)

    scorecard = sc.create_scorecard(course, players, multi, rated)
    uc.add_incomplete_scorecard(scorecard, players)

    return render_template("scorecard.html", round_summary=scorecard)


@scorecards.route('/scorecard/<scorecard_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def scorecard_history(scorecard_id):

    if request.method == 'POST':
        scorecard = sc.get_scorecard(_id=ObjectId(request.form['button']))

        return render_template('scorecard.html', round_summary=scorecard)

    if request.method == 'DELETE':

        scorecard = sc.get_scorecard(_id=ObjectId(json.loads(request.form['p_summary'])['_id']))

        uc.remove_incomplete_scorecard(scorecard)
        sc.delete_scorecard(scorecard)

        return 'Scorecard deleted'

    scorecard = sc.get_scorecard(_id=ObjectId(scorecard_id))
    return render_template('scorecard.html', round_summary=scorecard)
