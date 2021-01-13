from App.Data.Repository import courses_repo as co

def get_all_names():
    return co.get_all_names()


def get_one_course(name):
    return co.get_one_course(name)

def add_favorite_course(course_name, current_user):
    course = co.get_one_course(course_name)
    return co.add_favorite_course(course._id, current_user)