import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class TestCaseTask(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.options = Options()
        cls.path = Service("D:/PracticalTask/Drivers/chromedriver.exe")
        cls.driver = webdriver.Chrome(service=cls.path, options=cls.options)
        cls.driver.get("https://www.trustedshops.de/bewertung/info_X77B11C1B8A5ABA16DDEC0C30E7996C21.html")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    # Checks if the page title exists
    def test_1_title(self):
        assert (len(self.driver.title) > 0)

    # Checks if grade is visible & above zero
    def test_2_grade(self):
        grade = self.driver.find_element(By.XPATH, "//div[@class ='score-info']/span[1]")
        assert (grade.is_displayed())
        assert ((float(grade.text)) > 0)

    # Checks if popup window appears when hovered over the info icon of first review
    def test_3_popup(self):
        # Accepts the cookies
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element(By.XPATH, "//button[@id='uc-btn-accept-banner']").click()

        # Hover to info icon of the first review
        action = ActionChains(self.driver)
        i_first_review = self.driver.find_element(By.XPATH, "//div[@class ='loading-line ng-tns-c63-29']/span[2]")
        action.move_to_element(i_first_review).perform()

        popup_element = self.driver.find_element(By.XPATH, "//tooltip")
        assert (popup_element.is_displayed())

    # Validates if all 1-Star reviews have only one star
    def test_4_one_star_reviews(self):
        # Navigates to filter reviews and clicks it
        filter_review = self.driver.find_element(By.XPATH, "//review-filter-selector")
        time.sleep(4)
        filter_review.click()

        # Filters 1-star reviews
        action = ActionChains(self.driver)
        one_star = self.driver.find_element(By.XPATH, "//label[@for='stars-value-1']")
        action.move_to_element(one_star).click().perform()

        next_page = self.driver.find_element(By.XPATH, "//div[@page-index='next']")

        # Checks if all the reviews of a page contains only one star
        def validate_one_star():
            reviews = self.driver.find_elements(By.XPATH, "//async-list/review")
            for review in reviews:
                active_stars = review.find_elements(By.XPATH,
                                                    ".//span[@class='star tsproi tsproi-star-filled active ng-star-inserted']")
                assert (len(active_stars) == 1)

        # Moves to the next page of reviews and calls validate_one_star(), until it reaches the last page
        while next_page.is_displayed():
            time.sleep(4)
            validate_one_star()
            next_page.click()

    # Checks the sum of star percentage values is less than or equal to 100
    def test_5_sum_review_percentage(self):
        bars = self.driver.find_elements(By.XPATH, "//div[@class='bar-value']/span[1]")
        sum_percentage = 0
        for bar in bars[:5]:
            sum_percentage += int(bar.text)

        assert (sum_percentage <= 100)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()
