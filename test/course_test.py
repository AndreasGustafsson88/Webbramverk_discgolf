import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



class CourseTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('chromedriver.exe')

    def test_search_test(self):
        self.driver.get('http://127.0.0.1:5000/courses')
        search_bar = self.driver.find_element_by_id("courses-search-input")
        search_bar.clear()
        search_bar.send_keys("ansgarsgården")
        search_bar.send_keys(Keys.RETURN)
        search_results = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.ID, "courseobject")))
        time.sleep(2)
        results = [element.text.lower() for element in search_results]
        self.assertIn("ansgarsgården", results)

    def test_add_and_remove_favorite_course(self):
        self.driver.get('http://127.0.0.1:5000/')
        login_bar = self.driver.find_element_by_id("button")
        login_bar.click()
        time.sleep(2)
        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys("johan2")
        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys("123")
        submit_field = self.driver.find_element_by_id("submit")
        submit_field.click()
        self.driver.get("http://127.0.0.1:5000/courses")

        search_bar = self.driver.find_element_by_id("courses-search-input")
        search_bar.clear()
        search_bar.send_keys("blankaholm")
        search_bar.send_keys(Keys.RETURN)

        search_results = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "courseobject")))
        add_course = self.driver.find_element_by_id("star")
        add_course.click()
        self.driver.get("http://127.0.0.1:5000/profile_page/johan2")

        time.sleep(2)
        favorite_coureses_button = self.driver.find_element_by_id("favourite_courses_picture")
        print(favorite_coureses_button)
        favorite_coureses_button.click()
        results_courses = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.ID, "favorite-courses-tag")))
        time.sleep(10)
        results = [element.text for element in self.driver.find_elements_by_id('id_courses')]
        self.assertIn("Blankaholm", results)
        time.sleep(3)

        loggedOut_button = self.driver.find_element_by_id("logout_button")
        loggedOut_button.click()

        self.driver.get("http://127.0.0.1:5000/")
        login_bar2 = self.driver.find_element_by_id("button")
        login_bar2.click()
        username_field2 = self.driver.find_element_by_id("username")
        username_field2.send_keys("johan2")
        password_field2 = self.driver.find_element_by_id("password")
        password_field2.send_keys("123")
        submit_field2 = self.driver.find_element_by_id("submit")
        submit_field2.click()
        self.driver.get("http://127.0.0.1:5000/courses")

        search_bar2 = self.driver.find_element_by_id("courses-search-input")
        search_bar2.clear()
        search_bar2.send_keys("blankaholm")
        search_bar2.send_keys(Keys.RETURN)

        search_results = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "courseobject")))
        add_course = self.driver.find_element_by_id("star")
        add_course.click()
        self.driver.get("http://127.0.0.1:5000/profile_page/johan2")

        time.sleep(2)
        favorite_coureses_button2 = self.driver.find_element_by_id("favourite_courses_picture")
        favorite_coureses_button2.click()
        results_courses2 = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.ID, "favorite-courses-tag")))
        time.sleep(10)
        results2 = [element.text for element in self.driver.find_elements_by_id('id_courses')]
        self.assertNotIn("Blankaholm", results2)
        time.sleep(3)

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
