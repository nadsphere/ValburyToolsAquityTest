import pytest
import logging

from selenium.webdriver.common.by import By

from Data.DataFeed import DataFeed

logger = logging.getLogger("RegisterTest")

# Registered test data — replace with real values from your Valbury test account
REGISTERED_EMAIL = "already_registered@test.com"
REGISTERED_PHONE = "8780106728"
LESS_THAN_NAME = "A"
LESS_THAN_PHONE_NUMBER = "8222"
INVALID_PHONE_NUMBER = "872661263845273"
INVALID_NAME = "M//rie"
INVALID_EMAIL = "abdulmuis@mail"

class TestRegistration:
    """End-to-end test suite for the Valbury registration flow."""

    def _submit_form(self, page, name, email, phone, check_terms=True):
        page.register.fill_name_field(name)
        page.register.fill_email_field(email)
        page.register.fill_phone_number(phone)
        if check_terms:
            page.register.check_tnc_checkbox()
        page.register.click_dapatkan_sekarang_button()

    # =====================================================================
    # Positive Tests
    # =====================================================================

    @pytest.mark.positive_test
    def test_success_register_with_valid_data(self, page):
        """Verify when register with a valid Full Name, Email, and Phone Number."""
        logger.info("TEST: [SUCCESS] Register with valid data")
        self._submit_form(
            page,
            name=page.data.random_name(),
            email=page.data.random_email(),
            phone=page.data.random_phonenum(),
        )
        assert page.verification_page.get_title_verification() == "Verifikasi"

    # =====================================================================
    # Negative Tests
    # =====================================================================

    @pytest.mark.negative_test
    def test_failed_register_blank_name(self, page):
        """Verify when register with empty Name field."""
        logger.info("TEST: [FAILED] Register with blank name")
        self._submit_form(page, name="", email=page.data.random_email(), phone=page.data.random_phonenum())
        assert page.register.validation_name() == "This field is required"

    @pytest.mark.negative_test
    def test_failed_register_blank_email(self, page):
        """Verify when register with empty Email field"""
        logger.info("TEST: [FAILED] Register with blank email")
        self._submit_form(page, name=page.data.random_name(), email="", phone=page.data.random_phonenum())
        assert page.register.validation_email() == "This field is required"

    @pytest.mark.negative_test
    def test_failed_register_blank_phone(self, page):
        """Verify when register with empty Phone Number field."""
        logger.info("TEST: [FAILED] Register with blank phone")
        self._submit_form(page, name=page.data.random_name(), email=page.data.random_email(), phone="")
        assert page.register.validation_phone() == "This field is required"

    @pytest.mark.negative_test
    def test_failed_register_blank_name_email(self, page):
        """Verify when register with empty Name and Email fields."""
        logger.info("TEST: [FAILED] Register with blank name and email")
        self._submit_form(page, name="", email="", phone=page.data.random_phonenum())
        assert page.register.validation_name() == "This field is required"
        assert page.register.validation_email() == "This field is required"

    @pytest.mark.negative_test
    def test_failed_register_blank_name_phone_number(self, page):
        """Verify when register with empty Name and Phone Number fields."""
        logger.info("TEST: [FAILED] Register with blank name and phone number")
        self._submit_form(page, name="", email=page.data.random_email(), phone="")
        assert page.register.validation_name() == "This field is required"
        assert page.register.validation_phone() == "This field is required"

    @pytest.mark.negative_test
    def test_failed_register_blank_email_phone_number(self, page):
        """Verify when register with empty Email and Phone Number fields."""
        logger.info("TEST: [FAILED] Register with blank email and phone number")
        self._submit_form(page, name=page.data.random_name(), email="", phone="")
        assert page.register.validation_email() == "This field is required"
        assert page.register.validation_phone() == "This field is required"

    @pytest.mark.negative_test
    def test_failed_register_all_blank_fields(self, page):
        """Verify when register with all empty fields."""
        logger.info("TEST: [FAILED] Register with all blank fields")
        self._submit_form(page, name="", email="", phone="")
        assert page.register.validation_name() == "This field is required"
        assert page.register.validation_email() == "This field is required"
        assert page.register.validation_phone() == "This field is required"

    @pytest.mark.negative_test
    @pytest.mark.registered
    def test_failed_register_with_registered_email(self, page):
        """Verify when register with an already registered Email."""
        logger.info("TEST: [FAILED] Register with registered email")
        self._submit_form(page, name=page.data.random_name(), email=REGISTERED_EMAIL, phone=page.data.random_phonenum())
        assert page.register.get_alert_popup_text() == "Maaf! Anda sudah terdaftar di Valbury"

    @pytest.mark.negative_test
    @pytest.mark.registered
    def test_failed_register_with_registered_phone(self, page):
        """Verify when register with an already registered Phone Number"""
        logger.info("TEST: [FAILED] Register with registered phone")
        self._submit_form(page, name=page.data.random_name(), email=page.data.random_email(), phone=REGISTERED_PHONE)
        assert page.register.get_alert_popup_text() == "Maaf! Anda sudah terdaftar di Valbury"

    @pytest.mark.negative_test
    def test_failed_register_with_less_than_character_phone(self, page):
        """Verify when register with the Phone Number is less than 9 characters"""
        logger.info("TEST: [FAILED] Register with less than 9 characters phone number")
        self._submit_form(page, name=page.data.random_name(), email=page.data.random_email(), phone=LESS_THAN_PHONE_NUMBER)
        assert page.register.validation_phone() == "Minimum length 9 character"

    @pytest.mark.negative_test
    def test_failed_register_with_invalid_phone(self, page):
        """Verify when register with the Phone Number is invalid"""
        logger.info("TEST: [FAILED] Register with invalid phone number")
        self._submit_form(page, name=page.data.random_name(), email=page.data.random_email(), phone=INVALID_PHONE_NUMBER)
        assert page.register.get_alert_popup_text() == "No. telepon yang anda masukan tidak valid"

    @pytest.mark.negative_test
    def test_failed_register_with_less_than_character_name(self, page):
        """Verify when register with Name field has less than 4 characters."""
        logger.info("TEST: [FAILED] Register with name less than 4 characters")
        self._submit_form(page, name=LESS_THAN_NAME, email=page.data.random_email(), phone=page.data.random_phonenum())
        assert page.register.validation_name() == "Please fill in using your full name"

    @pytest.mark.negative_test
    def test_failed_register_with_invalid_name(self, page):
        """Verify when register with Name field has invalid characters."""
        logger.info("TEST: [FAILED] Register with invalid name")
        self._submit_form(page, name=INVALID_NAME, email=page.data.random_email(), phone=page.data.random_phonenum())
        assert page.register.validation_name() == "The name you entered is invalid"

    @pytest.mark.negative_test
    def test_failed_register_invalid_email_format(self, page):
        """Verify when register with invalid email format."""
        logger.info("TEST: [FAILED] Register with invalid email format")
        self._submit_form(page, name=page.data.random_name(), email=INVALID_EMAIL, phone=page.data.random_phonenum())       
        assert page.register.validation_email() == "The email you entered is invalid"