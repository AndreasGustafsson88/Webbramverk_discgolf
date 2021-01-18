from App.Data.Models.courses import Course


def get_all_names():
    return [course.name for course in Course.all()]


def get_one_course(name):
    return Course.find(name=name).first_or_none()


def add_favorite_course(course_id, current_user):
    if course_id not in current_user.favourite_courses:
        current_user.favourite_courses.append(course_id)
        current_user.save()
        return True
    return False






