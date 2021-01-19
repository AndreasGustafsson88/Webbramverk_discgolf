import time

from App.Data.Models.courses import Course


def get_all_names():
    return [course.name for course in Course.all()]


def get_one_course(name):
    return Course.find(name=name).first_or_none()


def update_favorite_courses(course_id, current_user):
    if course_id not in current_user.favourite_courses:
        current_user.favourite_courses.append(course_id)
        current_user.save()
        return True
    else:
        current_user.favourite_courses.remove(course_id)
        current_user.save()
        return False


def get_course_by_id(course_id):
    return Course.find(_id=course_id).first_or_none()


def add_round(course, c_round):
    course.history.append(c_round)
    course.logged_rounds += 1
    course.save()
    return True
