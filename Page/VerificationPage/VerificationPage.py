from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By


class VerificationPage(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    def get_title_verification(self):
        return self.driver.find_element(By.XPATH, "//h3[text()='Verifikasi']").text
