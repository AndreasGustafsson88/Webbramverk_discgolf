from App.Data import Document
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from App.Data.DB_SETTINGS import DRIVER_PATH


class Course(Document):

    collection = Document.db.courses

    @property
    def course_par(self):
        return sum([int(hole["Par"]) for hole in self.holes if not isinstance(hole, int)])

    def update_rating(self):
        coef = np.polyfit(list(map(lambda x: x[1], self.history)), list(map(lambda x: x[2], self.history)), 1)
        predicted_ratings = [i for i in range(0, 1400)]
        predicted = list(map(int, np.polyval(coef, predicted_ratings)))
        self.rating = {str(predicted[i]): predicted_ratings[i] for i in range(len(predicted))}
        self.save()

    def update_layout(self, event_link):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=2000,1200")

        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

        driver.get(event_link)
        sleep(10)

        parent_element = driver.find_element_by_class_name('MuiAccordionDetails-root')
        children = parent_element.find_elements_by_xpath('.//*')
        all_holes = [child.get_attribute("innerText") for child in children if
                     child.get_attribute("innerText").isnumeric() and len(child.get_attribute("innerText")) < 4]

        new_holes = [{"Par": all_holes[x + 2], "length": all_holes[x + 1], "average": all_holes[x + 2]}
                     for x in range(0, len(all_holes), 3)]

        new_holes.insert(0, len(new_holes))

        self.holes = new_holes
        self.save()

    def average_per_hole(self, throw_per_hole):
        for i in range(1, len(self.holes)):
            if self.logged_rounds - 1:
                average = ((self.holes[i]['average'] * (self.logged_rounds - 1)) + throw_per_hole[
                    i - 1]) / self.logged_rounds
            else:
                average = throw_per_hole[i - 1]

            self.holes[i]['average'] = average
        self.save()
        return True
