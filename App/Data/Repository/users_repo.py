from App.Data.Models.users import User
from bson import ObjectId

def get_all_friends(current_user):
    return [User.find(_id=ObjectId(player)).first_or_none().user_name for player in current_user.friends]