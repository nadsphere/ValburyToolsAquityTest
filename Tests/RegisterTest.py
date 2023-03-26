import time
import unittest
from Page.RegisterPage.RegisterPage import Register
from Data.DataFeed import DataFeed
from Page.VerificationPage.VerificationPage import VerificationPage
from Driver.driver import Driver


class RegisterTest(Driver):
    def test_success_register_1(self):
        register = Register(self.driver)
        verifpage = VerificationPage(self.driver)

        register.input_name_field("Muhammad Solehudin")
        time.sleep(2)
        register.input_email_field("solehmahmud@mail.com")
        time.sleep(2)
        register.input_phone_number("8780106728")
        time.sleep(2)
        register.click_checkbox()
        register.click_dapatkan()
        time.sleep(15)

        actual_result = verifpage.get_title_verification()
        self.assertEqual(actual_result, 'Verifikasi')

    def test_failed_register_blank_name_2(self):
        data = DataFeed()
        register = Register(self.driver)

        register.input_email_field(data.random_email())
        time.sleep(2)
        register.input_phone_number(data.random_phonenum())
        time.sleep(2)
        register.click_checkbox()
        register.click_dapatkan()
        time.sleep(15)

        actual_result = register.validation_name()
        self.assertEqual(actual_result, 'This field is required')

    def test_failed_register_blank_email_3(self):
        data = DataFeed()
        register = Register(self.driver)

        register.input_name_field(data.random_name())
        time.sleep(2)
        register.input_phone_number(data.random_phonenum())
        time.sleep(2)
        register.click_checkbox()
        register.click_dapatkan()
        time.sleep(15)

        actual_result = register.validation_email()
        self.assertEqual(actual_result, 'This field is required')

    def test_failed_register_blank_phone_4(self):
        data = DataFeed()
        register = Register(self.driver)

        register.input_name_field(data.random_name())
        time.sleep(2)
        register.input_email_field(data.random_email())
        time.sleep(2)
        register.click_checkbox()
        register.click_dapatkan()
        time.sleep(15)

        actual_result = register.validation_phone()
        self.assertEqual(actual_result, 'This field is required')

    def test_failed_register_with_registered_email_5(self):
        data = DataFeed()
        register = Register(self.driver)

        register.input_name_field(data.random_name())
        time.sleep(2)
        register.input_email_field(data.random_email())
        time.sleep(2)
        register.input_phone_number(data.random_phonenum())
        time.sleep(2)
        register.click_checkbox()
        register.click_dapatkan()
        time.sleep(15)

        actual_result = register.validation_email()
        self.assertEqual(actual_result, 'This field is required')

    def test_failed_register_with_registered_phone_6(self):
        data = DataFeed()
        register = Register(self.driver)

        register.input_name_field(data.random_name())
        time.sleep(2)
        register.input_email_field(data.random_email())
        time.sleep(2)
        register.input_phone_number("8780106728")
        time.sleep(2)
        register.click_checkbox()
        register.click_dapatkan()
        time.sleep(15)

        actual_result = register.get_alert_popup_text()
        self.assertEqual(actual_result, 'Maaf! Anda sudah terdaftar di Valbury')


if __name__ == "__main__":
    unittest.main()
