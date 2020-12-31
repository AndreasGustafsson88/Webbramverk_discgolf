from App.Data import Document, db
import numpy as np


class Course(Document):
    collection = db.courses

    @property
    def course_par(self):
        return sum([hole["Par"] for hole in self.holes if not isinstance(hole, int)])

    def update_rating(self):
        coef = np.polyfit(list(map(lambda x: x[1], self.history)), list(map(lambda x: x[2], self.history)), 1)
        predicted_ratings = [i for i in range(500, 1200)]
        predicted = list(map(int, np.polyval(coef, predicted_ratings)))
        self.rating = {str(predicted[i]): predicted_ratings[i] for i in range(len(predicted))}
        self.save()
