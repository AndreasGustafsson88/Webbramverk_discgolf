import json
from flask import Blueprint, request, Response, render_template
from flask_login import current_user
from App.Controller import courses_controller as cc

courses_bp = Blueprint('courses_bp', __name__)


@courses_bp.route('/courses', methods=["POST", "GET"])
def courses():
    if request.method == "POST":

        if "loading" in request.form:
            favorites = [cc.get_course_by_id(course).name for course in current_user.favourite_courses]
            response = Response(
                response=json.dumps({"favorites": favorites}),
                status=200,
                mimetype="application/json"
            )
            return response
        if "course" in request.form:
            course_name = request.form["course"]
            if cc.update_favorite_courses(course_name, current_user):
                message = "Course added to favorites"
            else:
                message = "Course removed from favorites"
            response = Response(
                response=json.dumps(message),
                status=200,
                mimetype="application/json"
            )
            return response

    all_courses = [[course.name, len(course.history)] for course in cc.get_all_courses()]

    return render_template('courses.html', all_courses=json.dumps(all_courses))
