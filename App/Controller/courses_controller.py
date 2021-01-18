from App.Data.Repository import courses_repo as co


def get_all_names():
    return co.get_all_names()


def get_one_course(name):
    return co.get_one_course(name)


def update_favorite_courses(course_name, current_user):
    course = co.get_one_course(course_name)
    return co.update_favorite_courses(course._id, current_user)


def get_course_by_id(course_id):
    return co.get_course_by_id(course_id)

