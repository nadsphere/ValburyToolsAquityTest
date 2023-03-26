import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
baseUrl = "https://valbury.co.id/campaign/trading-tools-acuity"


class Driver(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(baseUrl)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()