import time
import unittest
import flask_unittest
from bson import ObjectId
from selenium.webdriver.common.keys import Keys
from App.Data.Models.courses import Course
from App.Data.Models.scorecards import Scorecard
from App.Data.Models.users import User
from App.UI import create_app
from App.Data.DB_SETTINGS import DRIVER_PATH
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestScorecardLoad(flask_unittest.ClientTestCase):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    user = {
        "full_name": "test testsson",
        "user_name": "wack_a_tree",
        "email": "please_be_unique@mail.com",
        "password": "secret",
        "confirm_password": "secret"}

    def setUp(self, client) -> None:
        pass

    def register_user(self, client):
        response = client.post('/signup', data=self.user)
        self.assertStatus(response, 302)
        self.assertLocationHeader(response, 'http://localhost/')

    def log_in_user(self, client):
        response = client.post('/', data={
            'username': self.user['user_name'],
            'password': self.user['password']
        })
        self.assertStatus(response, 302)
        self.assertLocationHeader(response, f'http://localhost/profile_page/{self.user["user_name"]}')

    def test_create_scorecard(self, client):
        self.register_user(client)
        self.log_in_user(client)

        website = client.get(
            'http://localhost/scorecard/play?course=Gässlösa&players=[%22Mcbeast%22]&rated=true&multi=1')

        self.assertStatus(website, 200)

    def tearDown(self, client) -> None:
        User.delete_one(user_name=self.user['user_name'])


class TestScorecardSelenium(unittest.TestCase):
    def setUp(self) -> None:

        self.driver = webdriver.Chrome(DRIVER_PATH)
        self.std_wait = WebDriverWait(self.driver, 5)
        self.course = Course.find(name='Gässlösa').first_or_none()
        self.rating = self.course.rating[str(3 * 18)]
        self.user = [
            ["full_name", "test testsson"],
            ["user_name", "wack_a_tree"],
            ["email", "please_be_unique@mail.com"],
            ["password", "secret"],
            ["confirm_password", "secret"]]

    def register_user(self):
        self.driver.get('http://127.0.0.1:5000/signup')

        input_fields = [self.driver.find_element_by_id(field[0]) for field in self.user]

        [field.send_keys(self.user[i][1]) for i, field in enumerate(input_fields)]

        self.driver.find_element_by_id('submit').click()

        self.std_wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'display-4')))
        welcome = self.driver.find_element_by_class_name('display-4')

        self.assertEqual(welcome.text, 'About')

    def log_in_user(self):

        # Click login to open option to login
        self.driver.find_element_by_id('button').click()

        user_name_field, password_field = [self.driver.find_element_by_id(id) for id in ['username', 'password']]

        user_name_field.send_keys(self.user[1][1])
        password_field.send_keys(self.user[3][1])

        self.driver.find_element_by_id('submit').click()
        self.std_wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))

        title = self.driver.find_element_by_class_name('title')

        self.assertEqual(title.text, self.user[1][1])

    def navigate_scorecard(self):
        time.sleep(1)
        scorecard_href = self.std_wait.until(EC.element_to_be_clickable((By.ID, 'scorecard_link')))
        scorecard_href.click()

    def create_scorecard(self):

        time.sleep(1)

        course_field = self.std_wait.until(EC.element_to_be_clickable((By.ID, 'course_search')))
        course_field.send_keys(self.course.name, Keys.DOWN, Keys.RETURN)

        self.driver.find_element_by_id('create_scorecard_button').click()

    def fill_out_scorecard(self):
        time.sleep(1)

        pagination_bullets = self.std_wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'swiper-pagination-bullet')))
        input_field = self.driver.find_elements_by_class_name('throws-input')
        input_field[0].send_keys("3")

        for i, next_slide in enumerate(pagination_bullets[1:], 1):
            next_slide.click()
            time.sleep(0.3)
            if i != 18:
                input_field[i].send_keys("3")

    def assert_profile_redirect(self):
        self.std_wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
        title = self.driver.find_element_by_class_name('title')
        self.assertEqual(title.text, self.user[1][1])

    def get_test_user(self):
        return User.find_unique(user_name=self.user[1][1])

    def handle_pop_up(self):
        self.std_wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def get_to_scorecard_and_fill_out(self):
        self.register_user()
        self.log_in_user()
        self.navigate_scorecard()
        self.create_scorecard()
        self.fill_out_scorecard()

    def test_submit_scorecard(self):
        self.get_to_scorecard_and_fill_out()

        self.driver.find_element_by_id('submit_button').click()
        self.handle_pop_up()

        # Assert redirect
        self.assert_profile_redirect()

        # Assert scorecard added to c_score_Oid
        test_user = self.get_test_user()
        self.assertEqual(1, len(test_user.c_score_Oid))

        # Assert incomplete scorecard deleted
        self.assertEqual(0, len(test_user.i_score_Oid))

    def test_save_scorecard(self):
        self.get_to_scorecard_and_fill_out()

        self.driver.find_element_by_id('save_button').click()
        self.handle_pop_up()

        # Assert redirect
        self.assert_profile_redirect()

        # Assert scorecard in incomplete list
        test_user = self.get_test_user()
        self.assertEqual(1, len(test_user.i_score_Oid))

        # Assert scorecard not in complete
        self.assertEqual(0, len(test_user.c_score_Oid))

    def test_delete_scorecard(self):
        self.get_to_scorecard_and_fill_out()

        test_user_before = self.get_test_user()

        # Assert if scorecard is in database
        self.assertIsNotNone(Scorecard.find(_id=ObjectId(test_user_before.i_score_Oid[0])).first_or_none())

        self.driver.find_element_by_id('delete_button').click()
        self.handle_pop_up()

        # Assert redirect
        self.assert_profile_redirect()

        # Assert scorecard not in complete
        test_user = self.get_test_user()
        self.assertEqual(0, len(test_user.c_score_Oid))

        # Assert scorecard not in incomplete
        self.assertEqual(0, len(test_user.i_score_Oid))

        # Assert scorecard not in database
        self.assertIsNone(Scorecard.find(_id=ObjectId(test_user_before.i_score_Oid[0])).first_or_none())

    def round_submitted(self):
        self.get_to_scorecard_and_fill_out()

        self.driver.find_element_by_id('submit_button').click()
        self.handle_pop_up()

    def test_rating_after_round(self):
        self.round_submitted()

        rating_text = self.std_wait.until(EC.presence_of_element_located((By.ID, 'rating_text')))
        self.assertIn(str(self.rating), rating_text.text)

    def test_correct_amount_of_extra_throws(self):
        self.round_submitted()
        self.navigate_scorecard()
        self.create_scorecard()

        # Get number of extra throws from database
        d = {int(k): v for k, v in self.course.rating.items()}

        extra_throws = "".join([str(k) for k, v in sorted(d.items()) if v <= self.rating][0])

        # Loop through each slide to access '#et' element text
        pagination_bullets = self.std_wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'swiper-pagination-bullet')))

        all_fields = self.driver.find_elements_by_id('et')

        actual_total = 0
        actual_total += int(all_fields[0].text)

        for i, next_slide in enumerate(pagination_bullets[1:], 1):
            next_slide.click()
            time.sleep(0.3)
            if i != 18:
                actual_total += int(all_fields[i].text)

        self.assertEqual(int(extra_throws), actual_total)

    def tearDown(self) -> None:
        test_user = self.get_test_user()
        User.delete_one(user_name=self.user[1][1])
        [Scorecard.delete_one(_id=ObjectId(t_id)) for t_id in test_user.i_score_Oid]
        [Scorecard.delete_one(_id=ObjectId(t_id)) for t_id in test_user.c_score_Oid]

        self.driver.close()


if __name__ == '__main__':
    unittest.main()
