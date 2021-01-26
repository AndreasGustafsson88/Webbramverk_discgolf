from App.Data import Document, db


class Scorecard(Document):
    collection = db.scorecards

    @classmethod
    def get_scorecard_for_player(cls, username):
        return [cls(item) for item in cls.collection.find({
            "players.user_name": username,
            "active": True
        })]

    def __repr__(self):
        return '\n'.join(f'{k}: {v}' for k, v in self.__dict__.items())