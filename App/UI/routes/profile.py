import json
import os
from bson import ObjectId
from flask import Blueprint, request, redirect, url_for, Response, render_template, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from App.Controller.courses_controller import get_course_by_id
from App.Controller.my_encoder import MyEncoder
from App.Controller.scorecards_controller import get_scorecard
from App.Controller.users_controller import get_user, add_friend, add_friend_request, get_user_by_username, \
    get_all_users, delete_friend, delete_friend_request, update_profile
from App.Data.Models.flaskform import SettingsForm
from App.UI.routes.logged_in import logged_in
from config import Config

profile = Blueprint('profile', __name__)


@profile.route('/profile_page/<user_name>', methods=["GET", "POST"])
@login_required
def profile_page(user_name):
    if request.method == "POST":

        if 'button' in request.form:
            scorecard = get_scorecard(_id=ObjectId(request.form['button']))
            return redirect(url_for('scorecards.scorecard_history', scorecard_id=scorecard._id))

        visited_user_id = request.form['id']

        if request.form['action'] == 'post accept_request':
            request_user = get_user(user_name=request.form['request_username'])
            message = add_friend(current_user, request_user._id, from_request=True)
            return Response(**message)

        if request.form['action'] == 'post add_friend':
            visited_user = get_user(_id=ObjectId(visited_user_id))

            message = add_friend(current_user, visited_user_id)
            add_friend_request(current_user, visited_user)

            response = Response(**message)
            return response

    settings_form = SettingsForm()
    visited_profile = get_user_by_username(user_name)
    visited_profile.history = json.dumps(visited_profile.history, cls=MyEncoder)
    all_users = get_all_users()
    favorite_courses = [get_course_by_id(course_id).name for course_id in visited_profile.favourite_courses]

    return render_template('profile_page.html', visited_profile=visited_profile, all_users=all_users,
                           form=settings_form, favorite_courses=favorite_courses)


@profile.route('/profile_page/<user_name>', methods=["DELETE"])
@login_required
def profile_page_delete(user_name):
    if request.method == "DELETE":
        friend = get_user(user_name=request.form['username'])

        if request.form['action'] == "action remove":
            message = delete_friend(current_user, friend._id)
            response = Response(**message)
            return response

        if request.form['action'] == 'action decline_request':
            message = delete_friend_request(current_user, friend._id)
            return Response(**message)


@profile.route('/profile_page/settings', methods=['POST'])
@login_required
def profile_page_update():

    settings_form = SettingsForm()

    if settings_form.validate_on_submit():

        if settings_form.profile_picture.data is not None:
            file_name = settings_form.user_name.data.strip().replace(' ', '_')
            settings_form.profile_picture.data.save(os.path.join(Config.UPLOAD_FOLDER, f'{file_name}.jpg'))
            current_user.profile_picture = "../static/assets/img/profile_pictures/" + file_name + ".jpg"
            current_user.save()

        if get_user(email=settings_form.email.data):
            flash("Email already exists")
            return redirect(url_for('profile.profile_page', user_name=current_user.user_name))

        if get_user(user_name=settings_form.user_name.data):
            flash("Username already exists")
            return redirect(url_for('profile.profile_page', user_name=current_user.user_name))

        update_profile(current_user, settings_form.profile_picture.data, settings_form.user_name.data,
                       settings_form.email.data, generate_password_hash(settings_form.password.data, "sha256"))

        return redirect(url_for('logged_out.index'))
