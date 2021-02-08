import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import basedir


class SignupTest(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome('chromedriver.exe')

    def log_in(self, username='CMcCrush', password='CMcCrush'):
        self.driver.get('http://127.0.0.1:5000/')
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'button')))
        except TimeoutError:
            self.driver.quit()

        self.driver.find_element_by_id('button').click()
        input_field = self.driver.find_element_by_id('username')
        input_field.send_keys(username)
        input_field = self.driver.find_element_by_id('password')
        input_field.send_keys(password)
        self.driver.find_element_by_id('submit').click()

    def go_to_settings(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'settings')))
            self.driver.find_element_by_xpath("//div[@class='profile-tabs']//a[@data-target='#settings']").click()
        except TimeoutError:
            self.driver.quit()

    def submit(self, password="CMcCrush"):
        try:
            self.driver.find_element_by_id('current_password').send_keys(password)
            self.driver.find_element_by_id('submit').click()
        except:
            self.driver.quit()

    def log_out(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'navbarSupportedContent')))
            self.driver.find_element_by_xpath("//div[@id='navbarSupportedContent']//a[@href='/log_out']").click()
        except TimeoutError:
            self.driver.quit()

    def test_change_profile_picture(self):
        self.log_in()
        self.go_to_settings()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'profile_picture_input')))
        self.driver.find_element_by_id('profile_picture_input').send_keys(basedir + '\\App\\UI\\static\\assets\\img\\dog.jpg')
        self.submit()
        self.log_out()

    def test_change_username(self):
        self.log_in()
        self.go_to_settings()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'user_name')))
        self.driver.find_element_by_id('user_name').send_keys('test testsson')
        self.submit()
        self.log_out()

        # reset
        self.log_in(username="test testsson")
        self.go_to_settings()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'user_name')))
        self.driver.find_element_by_id('user_name').send_keys('CMcCrush')
        self.submit()
        self.log_out()

    def test_change_email(self):
        self.log_in()
        self.go_to_settings()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
        self.driver.find_element_by_id('email').send_keys('test@email.com')
        self.log_out()

    def test_change_password(self):
        self.log_in()
        self.go_to_settings()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
        self.driver.find_element_by_id('password').send_keys('123')
        self.driver.find_element_by_id('confirm_password').send_keys('123')
        self.submit()
        self.log_out()

        # reset
        self.log_in(password='123')
        self.go_to_settings()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
        self.driver.find_element_by_id('password').send_keys('CMcCrush')
        self.driver.find_element_by_id('confirm_password').send_keys('CMcCrush')
        self.submit(password='123')
        self.log_out()

    def tearDown(self) -> None:
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()