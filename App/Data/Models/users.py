from flask_login import UserMixin
from App.Data import Document, db
from bson import ObjectId
from statistics import mean
from ast import literal_eval


class User(Document, UserMixin):
    collection = db.users

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

    def player_hcp(self, course):

        hole_average = sorted([{"hole": i, "average": "{:.2f}".format(hole["average"] - hole["Par"]), "strokes": 0}
                               for i, hole in enumerate(course.holes[1:], 1)], key=lambda x: x["average"], reverse=True)

        if self.rating is None or len(course.rating) == 0:
            return sorted(hole_average, key=lambda x: x['hole'])

        total_throws = 0

        for k, v in course.rating.items():
            if v == self.rating:
                total_throws += int(k)
                break

            elif v >= self.rating:
                total_throws += int(k) + 1
                break

        difference = total_throws - course.course_par

        if difference == 0:
            return sorted(hole_average, key=lambda x: x["hole"])

        elif difference < 0:
            for i in range(1, difference * -1 + 1):
                hole_average[-i % course.holes[0]]["strokes"] -= 1

        elif difference > 0:
            for i in range(difference):
                hole_average[i % course.holes[0]]["strokes"] += 1

        return sorted(hole_average, key=lambda x: x["hole"])
