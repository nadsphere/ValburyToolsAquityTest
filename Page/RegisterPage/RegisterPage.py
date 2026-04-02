import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger("RegisterPage")

TIMEOUT = 10  # seconds


class Register:
    """Page Object — registration form. All methods use explicit WebDriverWait."""

    def __init__(self, driver):
        self.driver = driver

    def input_name_field(self, name):
        wait = WebDriverWait(self.driver, TIMEOUT)
        el = wait.until(EC.visibility_of_element_located((By.ID, "name")))
        el.clear()
        el.send_keys(name)
        logger.info("Entered name: %s", name)

    def input_email_field(self, email):
        wait = WebDriverWait(self.driver, TIMEOUT)
        el = wait.until(EC.visibility_of_element_located((By.ID, "email")))
        el.clear()
        el.send_keys(email)
        logger.info("Entered email: %s", email)

    def input_phone_number(self, phonenum):
        wait = WebDriverWait(self.driver, TIMEOUT)
        el = wait.until(EC.visibility_of_element_located((By.ID, "telepon")))
        el.clear()
        el.send_keys(phonenum)
        logger.info("Entered phone: %s", phonenum)

    def click_checkbox(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        el = wait.until(EC.element_to_be_clickable((By.ID, "flexCheckChecked")))
        if not el.is_selected():
            el.click()
        logger.info("Terms checkbox checked")

    def click_dapatkan(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-daftar']")))
        btn.click()
        logger.info("Clicked submit button")

    def validation_name(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        el = wait.until(EC.visibility_of_element_located((By.ID, "error-name")))
        return el.text

    def validation_email(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        el = wait.until(EC.visibility_of_element_located((By.ID, "error-email")))
        return el.text

    def validation_phone(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        el = wait.until(EC.visibility_of_element_located((By.ID, "error-telepon")))
        return el.text

    def get_alert_popup_text(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        el = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'alert-modal')]//h6")
        ))
        logger.info("Alert modal text: %s", el.text)
        return el.text

    def click_pop_up_alert(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'alert-modal')]//button")
        ))
        btn.click()
        logger.info("Alert modal closed")

    def is_alert_visible(self, timeout=5):
        """Returns True if the alert modal is visible, False if it times out."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class,'alert-modal')]//h6")
                )
            )
            return True
        except Exception:
            return False
