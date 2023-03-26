from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By


class Register(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    def input_name_field(self, name):
        self.driver.find_element(By.ID, "name").send_keys(name)

    def input_email_field(self, email):
        self.driver.find_element(By.ID, "email").send_keys(email)

    def input_phone_number(self, phonenum):
        self.driver.find_element(By.ID, "telepon").send_keys(phonenum)

    def click_checkbox(self):
        self.driver.find_element(By.ID, "flexCheckChecked").click()

    def click_dapatkan(self):
        self.driver.find_element(By.XPATH, "//button[@id='btn-daftar']").click()

    def validation_name(self):
        return self.driver.find_element(By.ID, "error-name").text

    def validation_email(self):
        return self.driver.find_element(By.ID, "error-email").text

    def validation_phone(self):
        return self.driver.find_element(By.ID, "error-telepon").text

    def get_alert_popup_text(self):
        return self.driver.find_element(By.XPATH, "//div[@id='alert-modal']//h6").text

    def click_pop_up_alert(self):
        self.driver.find_element(By.XPATH, "//div[@id='alert-modal']//button").click()