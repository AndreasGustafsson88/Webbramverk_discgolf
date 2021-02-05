import time

from App.Data.Models.users import User
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UserTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('chromedriver.exe')

        self.user1 = [
            ["full_name", "Bosse Banan"],
            ["user_name", "boho"],
            ["email", "bb@email.com"],
            ["password", "1234"],
            ["confirm_password", "1234"]]
        self.user2 = [
            ["full_name", "Bosses Kompis"],
            ["user_name", "boko"],
            ["email", "bk@email.com"],
            ["password", "1234"],
            ["confirm_password", "1234"]]

    def signup_user_1(self):
        self.driver.get('http://127.0.0.1:5000/signup')

        input_fields = [self.driver.find_element_by_id(field[0]) for field in self.user1]

        [field.send_keys(self.user1[i][1]) for i, field in enumerate(input_fields)]

        self.driver.find_element_by_id('submit').click()

    def signup_user_2(self):
        self.driver.get('http://127.0.0.1:5000/signup')

        input_fields = [self.driver.find_element_by_id(field[0]) for field in self.user2]

        [field.send_keys(self.user2[i][1]) for i, field in enumerate(input_fields)]

        self.driver.find_element_by_id('submit').click()

    def sign_in_user_1(self):
        self.driver.get('http://127.0.0.1:5000')
        self.driver.find_element_by_id('button').click()

        user_name_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit_field = self.driver.find_element_by_id('submit')

        user_name_field.send_keys(self.user1[1][1])
        password_field.send_keys(self.user1[3][1])
        self.driver.find_element_by_id('submit').click()

    def sign_in_user_2(self):
        self.driver.get('http://127.0.0.1:5000')
        self.driver.find_element_by_id('button').click()

        user_name_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit_field = self.driver.find_element_by_id('submit')

        user_name_field.send_keys(self.user2[1][1])
        password_field.send_keys(self.user2[3][1])
        self.driver.find_element_by_id('submit').click()

    def user_1_navigate_to_friends(self):
        self.driver.get(f'http://127.0.0.1:5000/profile_page/{self.user1[1][1]}#')
        self.driver.find_element_by_id('friend_logo_image').click()

    def user_2_navigate_to_friends(self):
        self.driver.get(f'http://127.0.0.1:5000/profile_page/{self.user2[1][1]}#')
        self.driver.find_element_by_id('friend_logo_image').click()

    def search_add_user_2(self):
        search_field = self.driver.find_element_by_id('user_search')
        search_field.send_keys(self.user2[1][1])
        self.driver.find_element_by_id('user_searchautocomplete-list').click()
        self.driver.find_element_by_id('img1').click()

    def search_add_user_1(self):
        search_field = self.driver.find_element_by_id('user_search')
        search_field.send_keys(self.user1[1][1])
        self.driver.find_element_by_id('user_searchautocomplete-list').click()
        self.driver.find_element_by_id('img1').click()

    def accept_alert(self):
        alert_text = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def log_out(self):
        self.driver.find_element_by_id('logout_button').click()

    def test_signup(self):
        number_of_users_1 = len(User.all())
        self.signup_user_1()
        number_of_users_added_1 = len(User.all())
        self.assertEqual(number_of_users_1 + 1, number_of_users_added_1)

        number_of_users_2 = len(User.all())
        self.signup_user_2()
        number_of_users_added_2 = len(User.all())
        self.assertEqual(number_of_users_2 + 1, number_of_users_added_2)

    def test_email_exists(self):
        self.signup_user_1()
        error_text = self.driver.find_elements_by_id('error_msg')
        result = [item.text for item in error_text]
        self.assertIn("Email already exists", result)

    def test_username_exists(self):
        self.user1[2][1] = 'wrong@email.com'
        self.signup_user_1()
        error_text = self.driver.find_elements_by_id('error_msg')
        result = [item.text for item in error_text]
        self.assertIn("Username already exists", result)

    def test_password_not_same(self):
        self.user1[3][1] = 'different_password'
        self.signup_user_1()
        error_text = self.driver.find_elements_by_id('error_msg')
        result = [item.text for item in error_text]
        self.assertIn("Password are not the same", result)

    def test_log_in(self):
        self.sign_in_user_1()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
        title = self.driver.find_element_by_class_name('title')
        self.assertEqual(title.text, self.user1[1][1])

    def test_add_friends(self):

        self.sign_in_user_1()
        self.user_1_navigate_to_friends()
        number_of_friends = len(self.driver.find_elements_by_class_name('friend_column'))
        self.search_add_user_2()
        self.accept_alert()
        self.user_1_navigate_to_friends()
        friend_list = [item.text for item in self.driver.find_elements_by_id('friend_link_id')]
        number_of_friends_add = len(self.driver.find_elements_by_class_name('friend_column'))
        self.assertIn(self.user2[1][1], friend_list)
        self.assertEqual(number_of_friends+1, number_of_friends_add)

    def test_accept_friend_request(self):
        self.sign_in_user_2()
        self.user_2_navigate_to_friends()

        number_of_request = len(self.driver.find_elements_by_id('friend_request_id'))
        number_of_friends = len(self.driver.find_elements_by_class_name('friend_column'))

        self.driver.find_element_by_class_name('accept_request').click()

        self.accept_alert()

        number_of_request_accept = len(self.driver.find_elements_by_id('friend_request_id'))
        number_of_friends_accept = len(self.driver.find_elements_by_class_name('friend_column'))

        friend_list = [item.text for item in self.driver.find_elements_by_id('friend_link_id')]
        self.assertIn(self.user1[1][1], friend_list)
        self.assertEqual(number_of_friends+1, number_of_friends_accept)
        self.assertEqual(number_of_request-1, number_of_request_accept)

    def test_delete_friend(self):
        self.sign_in_user_1()
        self.user_1_navigate_to_friends()

        number_of_friends = len(self.driver.find_elements_by_class_name('friend_column'))

        self.driver.find_element_by_id(self.user2[1][1]).click()
        self.accept_alert()

        number_of_friends_remove = len(self.driver.find_elements_by_class_name('friend_column'))
        friend_list = [item.text for item in self.driver.find_elements_by_id('friend_link_id')]
        self.assertEqual(number_of_friends-1, number_of_friends_remove)
        self.assertNotIn(self.user2[1][1], friend_list)

        self.sign_in_user_2()
        self.user_2_navigate_to_friends()

        number_of_friends = len(self.driver.find_elements_by_class_name('friend_column'))

        self.driver.find_element_by_id(self.user1[1][1]).click()
        self.accept_alert()

        number_of_friends_remove = len(self.driver.find_elements_by_class_name('friend_column'))
        friend_list = [item.text for item in self.driver.find_elements_by_id('friend_link_id')]
        self.assertEqual(number_of_friends - 1, number_of_friends_remove)
        self.assertNotIn(self.user1[1][1], friend_list)

    def test_decline_friend_request(self):
        self.sign_in_user_1()
        self.user_1_navigate_to_friends()
        self.search_add_user_2()
        self.accept_alert()
        self.log_out()

        self.sign_in_user_2()
        self.user_2_navigate_to_friends()

        number_of_request = len(self.driver.find_elements_by_id('friend_request_id'))
        number_of_friends = len(self.driver.find_elements_by_class_name('friend_column'))

        self.driver.find_element_by_class_name('decline_request').click()

        self.accept_alert()

        number_of_request_decline = len(self.driver.find_elements_by_id('friend_request_id'))
        number_of_friends_decline = len(self.driver.find_elements_by_class_name('friend_column'))

        self.assertEqual(number_of_friends, number_of_friends_decline)
        self.assertEqual(number_of_request - 1, number_of_request_decline)

    def tearDown(self):
        pass
        #User.delete_one(user_name='boho')
        #self.driver.close()

if __name__ == '__main__':
    unittest.main()
