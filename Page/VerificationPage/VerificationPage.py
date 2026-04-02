import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger("VerificationPage")


class VerificationPage:
    TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver

    def get_title_verification(self):
        wait = WebDriverWait(self.driver, self.TIMEOUT)
        el = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//h3[text()='Verifikasi']")
        ))
        logger.info("Verification page title found")
        return el.text
