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

        self.user_name = 'boho'
        self.full_name = 'Bosse Banan'
        self.email = 'bb@email.com'
        self.password = '1234'

        self.user_name2 = 'MansMcMan'
        self.full_name2 = 'Måns Öberg'
        self.email2 = 'mans@discgolf.com'
        self.password2 = 'MansMcMan'

    def test_signup(self):
        self.driver.get('http://127.0.0.1:5000/signup')

        full_name_field = self.driver.find_element_by_id('full_name')
        user_name_field = self.driver.find_element_by_id('user_name')
        email_field = self.driver.find_element_by_id('email')
        password_field = self.driver.find_element_by_id('password')
        confirm_password_field = self.driver.find_element_by_id('confirm_password')
        submit = self.driver.find_element_by_name('submit')

        number_of_users = len(User.all())
        print(number_of_users)

        full_name_field.send_keys(self.full_name)
        user_name_field.send_keys(self.user_name)
        email_field.send_keys(self.email)
        password_field.send_keys(self.password)
        confirm_password_field.send_keys(self.password)
        submit.send_keys(Keys.RETURN)

        number_of_users_added = len(User.all())
        print(number_of_users_added)
        self.assertEqual(number_of_users+1, number_of_users_added)

    def test_log_in(self):
        self.driver.get('http://127.0.0.1:5000')
        self.driver.find_element_by_id('button').click()

        user_name_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit_field = self.driver.find_element_by_id('submit')

        user_name_field.send_keys(self.user_name)
        password_field.send_keys(self.password)
        submit_field.click()

        title_text = self.driver.find_element_by_id('profile_title')
        self.assertEqual(self.user_name, title_text.text)

    def test_add_friends(self):

        self.driver.get('http://127.0.0.1:5000')
        self.driver.find_element_by_id('button').click()

        user_name_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit_field = self.driver.find_element_by_id('submit')

        user_name_field.send_keys(self.user_name)
        password_field.send_keys(self.password)
        submit_field.click()
        self.driver.get(f'http://127.0.0.1:5000/profile_page/{self.user_name}#')
        self.driver.find_element_by_id('friend_logo_image').click()
        search_field = self.driver.find_element_by_id('user_search')

        number_of_friends = len(self.driver.find_elements_by_class_name('friend_column'))

        search_field.send_keys('MansMcMan')
        self.driver.find_element_by_id('user_searchautocomplete-list').click()
        self.driver.find_element_by_id('img1').click()

        alert_text = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

        self.driver.get(f'http://127.0.0.1:5000/profile_page/{self.user_name}#')
        self.driver.find_element_by_id('friend_logo_image').click()
        friend_list = [item.text for item in self.driver.find_elements_by_id('friend_link_id')]
        number_of_friends_add = len(self.driver.find_elements_by_class_name('friend_column'))

        self.assertIn('MansMcMan', friend_list)
        self.assertEqual(number_of_friends+1, number_of_friends_add)

    def test_accept_friend_request(self):
        self.driver.get('http://127.0.0.1:5000')
        self.driver.find_element_by_id('button').click()

        user_name_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit_field = self.driver.find_element_by_id('submit')

        user_name_field.send_keys(self.user_name2)
        password_field.send_keys(self.password2)
        submit_field.click()
        self.driver.get(f'http://127.0.0.1:5000/profile_page/{self.user_name2}#')
        self.driver.find_element_by_id('friend_logo_image').click()
        search_field = self.driver.find_element_by_id('user_search')


        search_field.send_keys(self.user_name)
        self.driver.find_element_by_id('user_searchautocomplete-list').click()
        self.driver.find_element_by_id('img1').click()

        alert_text = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        self.driver.find_element_by_id('logout_button').click()

        self.driver.get('http://127.0.0.1:5000')
        self.driver.find_element_by_id('button').click()

        user_name_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit_field = self.driver.find_element_by_id('submit')

        user_name_field.send_keys(self.user_name)
        password_field.send_keys(self.password)
        submit_field.click()
        self.driver.get(f'http://127.0.0.1:5000/profile_page/{self.user_name}#')
        self.driver.find_element_by_id('friend_logo_image').click()
        number_of_request = len(self.driver.find_elements_by_id('friend_request_id'))
        number_of_friends = len(self.driver.find_elements_by_class_name('friend_column'))

        self.driver.find_element_by_class_name('accept_request').click()

        alert_text = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        number_of_request_accept = len(self.driver.find_elements_by_id('friend_request_id'))
        number_of_friends_accept = len(self.driver.find_elements_by_class_name('friend_column'))

        friend_list = [item.text for item in self.driver.find_elements_by_id('friend_link_id')]
        self.assertIn('MansMcMan', friend_list)
        self.assertEqual(number_of_friends+1, number_of_friends_accept)
        self.assertEqual(number_of_request-1, number_of_request_accept)

    def test_decline_friend_request(self):
        self.driver.get('http://127.0.0.1:5000')
        self.driver.find_element_by_id('button').click()

        user_name_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit_field = self.driver.find_element_by_id('submit')

        user_name_field.send_keys(self.user_name2)
        password_field.send_keys(self.password2)
        submit_field.click()
        self.driver.get(f'http://127.0.0.1:5000/profile_page/{self.user_name2}#')
        self.driver.find_element_by_id('friend_logo_image').click()
        search_field = self.driver.find_element_by_id('user_search')

        search_field.send_keys(self.user_name)
        self.driver.find_element_by_id('user_searchautocomplete-list').click()
        self.driver.find_element_by_id('img1').click()

        alert_text = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        self.driver.find_element_by_id('logout_button').click()

        self.driver.get('http://127.0.0.1:5000')
        self.driver.find_element_by_id('button').click()

        user_name_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit_field = self.driver.find_element_by_id('submit')

        user_name_field.send_keys(self.user_name)
        password_field.send_keys(self.password)
        submit_field.click()
        self.driver.get(f'http://127.0.0.1:5000/profile_page/{self.user_name}#')
        self.driver.find_element_by_id('friend_logo_image').click()
        number_of_request = len(self.driver.find_elements_by_id('friend_request_id'))
        number_of_friends = len(self.driver.find_elements_by_class_name('friend_column'))

        self.driver.find_element_by_class_name('decline_request').click()

        alert_text = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        number_of_request_decline = len(self.driver.find_elements_by_id('friend_request_id'))
        number_of_friends_accept = len(self.driver.find_elements_by_class_name('friend_column'))

        friend_list = [item.text for item in self.driver.find_elements_by_id('friend_link_id')]
        self.assertNotIn('MansMcMan', friend_list)
        self.assertEqual(number_of_friends, number_of_friends_accept)
        self.assertEqual(number_of_request-1, number_of_request_decline)

    def test_delete_friend(self):
        self.driver.get('http://127.0.0.1:5000')
        self.driver.find_element_by_id('button').click()

        user_name_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit_field = self.driver.find_element_by_id('submit')

        user_name_field.send_keys(self.user_name)
        password_field.send_keys(self.password)
        submit_field.click()
        self.driver.get(f'http://127.0.0.1:5000/profile_page/{self.user_name}#')
        self.driver.find_element_by_id('friend_logo_image').click()

        number_of_friends = len(self.driver.find_elements_by_class_name('friend_column'))

        self.driver.find_element_by_id('MansMcMan').click()

        alert_text = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

        number_of_friends_remove = len(self.driver.find_elements_by_class_name('friend_column'))
        friend_list = [item.text for item in self.driver.find_elements_by_id('friend_link_id')]
        self.assertEqual(number_of_friends-1, number_of_friends_remove)
        self.assertNotIn('MansMcMan', friend_list)

    def tearDown(self):
        pass
        #User.delete_one(user_name='boho')
        #self.driver.close()

if __name__ == '__main__':
    unittest.main()
