from App.Data import Document, db


class User(Document):
    collection = db.users

    def player_hcp(self, course):

        hole_average = sorted([{"hole": i, "average": "{:.2f}".format(hole["average"] - hole["Par"]), "strokes": 0}
                               for i, hole in enumerate(course.holes[1:], 1)], key=lambda x: x["average"])

        if self.rating is None:
            return hole_average

        total_throws = 0

        for k, v in course.rating.items():
            if v >= self.rating:
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
