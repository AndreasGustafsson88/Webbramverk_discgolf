import json
import os
from bson import ObjectId
from flask import Blueprint, request, redirect, url_for, Response, render_template, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from App.Controller.my_encoder import MyEncoder
from App.Controller import courses_controller as cc
from App.Controller import scorecards_controller as sc
from App.Controller import users_controller as uc
from App.UI.static.flaskform.settings_form import SettingsForm
from config import Config

profile = Blueprint('profile', __name__)


@profile.route('/profile_page/<user_name>', methods=["GET", "POST"])
@login_required
def profile_page(user_name):
    if request.method == "POST":

        if 'button' in request.form:
            scorecard = sc.get_scorecard(_id=ObjectId(request.form['button']))
            return redirect(url_for('scorecards.scorecard_history', scorecard_id=scorecard._id))

        visited_user_id = request.form['id']

        if request.form['action'] == 'post accept_request':
            request_user = uc.get_user(user_name=request.form['request_username'])
            message = uc.add_friend(current_user, request_user._id, from_request=True)
            return Response(**message)

        if request.form['action'] == 'post add_friend':
            visited_user = uc.get_user(_id=ObjectId(visited_user_id))

            message = uc.add_friend(current_user, visited_user_id)
            uc.add_friend_request(current_user, visited_user)

            response = Response(**message)
            return response

    settings_form = SettingsForm()
    visited_profile = uc.get_user_by_username(user_name)
    visited_profile.history = json.dumps(visited_profile.history, cls=MyEncoder)
    all_users = uc.get_all_users()
    favorite_courses = [cc.get_course_by_id(course_id).name for course_id in visited_profile.favourite_courses]

    return render_template('profile_page.html', visited_profile=visited_profile, all_users=all_users,
                           form=settings_form, favorite_courses=favorite_courses)


@profile.route('/profile_page/<user_name>', methods=["DELETE"])
@login_required
def profile_page_delete(user_name):
    if request.method == "DELETE":
        friend = uc.get_user(user_name=request.form['username'])

        if request.form['action'] == "action remove":
            message = uc.delete_friend(current_user, friend._id)
            response = Response(**message)
            return response

        if request.form['action'] == 'action decline_request':
            message = uc.delete_friend_request(current_user, friend._id)
            return Response(**message)


@profile.route('/profile_page/settings', methods=['POST'])
@login_required
def profile_page_update():

    settings_form = SettingsForm()
    if settings_form.validate_on_submit():
        if not check_password_hash(current_user.password, settings_form.current_password.data):
            flash("Wrong password")
            return redirect(url_for('profile_page', user_name=current_user.user_name))

        update = {}

        if settings_form.profile_picture_input.data:
            file_name = current_user.user_name.strip().replace(' ', '_')
            print()
            settings_form.profile_picture_input.data.save(os.path.join(Config.UPLOAD_FOLDER, f'{file_name}.jpg'))
            update["profile_picture"] = "/assets/img/profile_pictures/" + file_name + ".jpg"

        if settings_form.email.data:
            if uc.get_user(email=settings_form.email.data):
                flash("Email already exists")
                return redirect(url_for('profile_page', user_name=current_user.user_name))
            update["email"] = settings_form.email.data

        if settings_form.user_name.data:
            if uc.get_user(user_name=settings_form.user_name.data):
                flash("Username already exists")
                return redirect(url_for('profile_page', user_name=current_user.user_name))
            update["user_name"] = settings_form.user_name.data

        if settings_form.password.data:
            update["password"] = generate_password_hash(settings_form.password.data, "sha256")

        uc.update_profile(current_user, update)

        return redirect(url_for('logged_out.index'))

    visited_profile = uc.get_user_by_username(current_user.user_name)
    visited_profile.history = json.dumps(visited_profile.history, cls=MyEncoder)
    all_users = uc.get_all_users()
    favorite_courses = [cc.get_course_by_id(course_id).name for course_id in visited_profile.favourite_courses]
    return render_template('profile_page.html', visited_profile=visited_profile, all_users=all_users,
                           form=settings_form, favorite_courses=favorite_courses)
