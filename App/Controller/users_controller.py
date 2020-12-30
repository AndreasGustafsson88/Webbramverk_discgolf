from App.Data.Repository import users_repo as ur

def get_all_friends(current_user):
    return ur.get_all_friends(current_user)
