from flask_login import UserMixin
from App.Data import Document, db
from bson import ObjectId

from App.Data.Models.scorecards import Scorecard


class User(Document, UserMixin):
    collection = db.users

    @property
    def scorecards(self):
        return Scorecard.get_scorecard_for_player(self.user_name)

    @property
    def friends_list(self):
        return [User.find(_id=ObjectId(user)).first_or_none() for user in self.friends]

    @property
    def friend_requests(self):
        return [User.find(_id=ObjectId(user)).first_or_none() for user in self.Oid_req]

    def get_id(self):
        return str(self._id)
