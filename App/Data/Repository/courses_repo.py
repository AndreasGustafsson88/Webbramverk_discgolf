from App.Data.Models.courses import Course


def get_all_names():
    return [course.name for course in Course.all()]


def get_one_course(name):
    return Course.find(name=name).first_or_none()


