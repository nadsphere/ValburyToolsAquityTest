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

    def fill_name_field(self, name):
        wait = WebDriverWait(self.driver, TIMEOUT)
        field_name = wait.until(EC.element_to_be_clickable((By.ID, "name")))
        field_name.clear()
        field_name.send_keys(name)
        logger.info("Entered name: %s", name)

    def fill_email_field(self, email):
        wait = WebDriverWait(self.driver, TIMEOUT)
        field_email = wait.until(EC.element_to_be_clickable((By.ID, "email")))
        field_email.clear()
        field_email.send_keys(email)
        logger.info("Entered email: %s", email)

    def fill_phone_number(self, phonenum):
        wait = WebDriverWait(self.driver, TIMEOUT)
        field_phone_number = wait.until(EC.element_to_be_clickable((By.ID, "telepon")))
        field_phone_number.clear()
        field_phone_number.send_keys(phonenum)
        logger.info("Entered phone: %s", phonenum)

    def check_tnc_checkbox(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        checkbox_tnc = wait.until(EC.element_to_be_clickable((By.ID, "flexCheckChecked")))
        if not checkbox_tnc.is_selected():
            checkbox_tnc.click()
        logger.info("Terms checkbox checked")

    def click_dapatkan_sekarang_button(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        button_dapatkan_sekarang = wait.until(EC.element_to_be_clickable((By.ID, "btn-daftar")))
        button_dapatkan_sekarang.click()
        logger.info("Clicked submit button")

    def validation_name(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        error_name = wait.until(EC.visibility_of_element_located((By.ID, "error-name")))
        return error_name.text

    def validation_email(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        error_email = wait.until(EC.visibility_of_element_located((By.ID, "error-email")))
        return error_email.text

    def validation_phone(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        error_phone = wait.until(EC.visibility_of_element_located((By.ID, "error-telepon")))
        return error_phone.text

    def get_alert_popup_text(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        error_registered = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".modal-body.text-center h6")
        ))
        logger.info("Alert modal text: %s", error_registered.text)
        return error_registered.text