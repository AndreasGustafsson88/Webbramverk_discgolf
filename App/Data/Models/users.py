from flask_login import UserMixin
from App.Data import Document
from bson import ObjectId
from statistics import mean
from ast import literal_eval
from App.Data.Models.scorecards import Scorecard


class User(Document, UserMixin):
    collection = Document.db.users

    @property
    def incomplete_scorecards(self):
        return [Scorecard.find(_id=ObjectId(scorecard)).first_or_none() for scorecard in self.i_score_Oid]

    @property
    def complete_scorecards(self):
        return [Scorecard.find(_id=ObjectId(scorecard)).first_or_none() for scorecard in self.c_score_Oid]

    @property
    def friends_list(self):
        return [User.find(_id=ObjectId(user)).first_or_none() for user in self.friends]

    @property
    def friend_requests(self):
        return [User.find(_id=ObjectId(user)).first_or_none() for user in self.Oid_req]

    @property
    def rating(self):
        if isinstance(self.history, str):
            self.history = literal_eval(self.history)
        if len(self.history) > 0:
            return mean([i[1] for i in self.history[len(self.history) - 16:]])
        else:
            return None

    def get_id(self):
        return str(self._id)
