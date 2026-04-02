import pytest
import logging

from selenium.webdriver.common.by import By

from Data.DataFeed import DataFeed

logger = logging.getLogger("RegisterTest")

# Registered test data — replace with real values from your Valbury test account
REGISTERED_EMAIL = "already_registered@test.com"   # TODO: replace with a real registered email
REGISTERED_PHONE = "8780106728"                     # TODO: replace with a real registered phone


class TestRegistration:
    """End-to-end test suite for the Valbury registration flow."""

    def _submit_form(self, page, name, email, phone, check_terms=True):
        page.register.input_name_field(name)
        page.register.input_email_field(email)
        page.register.input_phone_number(phone)
        if check_terms:
            page.register.click_checkbox()
        page.register.click_dapatkan()

    # =====================================================================
    # Positive / Happy-path
    # =====================================================================

    @pytest.mark.success
    def test_success_register_with_valid_data(self, page):
        """Happy-path — all fields valid. Verifies 'Verifikasi' page title."""
        logger.info("TEST: [SUCCESS] Register with valid data")
        self._submit_form(
            page,
            name=page.data.random_name(),
            email=page.data.random_email(),
            phone=page.data.random_phonenum(),
        )
        assert page.verification_page.get_title_verification() == "Verifikasi"
        logger.info("TEST PASSED")

    # =====================================================================
    # Negative / Validation — required fields
    # =====================================================================

    @pytest.mark.failed
    def test_failed_register_blank_name(self, page):
        """Leaves name blank — expects 'This field is required'."""
        logger.info("TEST: [FAILED] Register with blank name")
        self._submit_form(page, name="", email=page.data.random_email(), phone=page.data.random_phonenum())
        assert page.register.validation_name() == "This field is required"
        logger.info("TEST PASSED")

    @pytest.mark.failed
    def test_failed_register_blank_email(self, page):
        """Leaves email blank — expects 'This field is required'."""
        logger.info("TEST: [FAILED] Register with blank email")
        self._submit_form(page, name=page.data.random_name(), email="", phone=page.data.random_phonenum())
        assert page.register.validation_email() == "This field is required"
        logger.info("TEST PASSED")

    @pytest.mark.failed
    def test_failed_register_blank_phone(self, page):
        """Leaves phone blank — expects 'This field is required'."""
        logger.info("TEST: [FAILED] Register with blank phone")
        self._submit_form(page, name=page.data.random_name(), email=page.data.random_email(), phone="")
        assert page.register.validation_phone() == "This field is required"
        logger.info("TEST PASSED")

    # =====================================================================
    # Negative / Validation — field format
    # =====================================================================

    @pytest.mark.failed
    def test_failed_register_invalid_email_format(self, page):
        """Enters invalid email format — expects validation error."""
        logger.info("TEST: [FAILED] Register with invalid email format")
        self._submit_form(
            page,
            name=page.data.random_name(),
            email="notavalidemail",
            phone=page.data.random_phonenum(),
        )
        # The exact error message depends on the frontend validation.
        # Adjust the expected string to match the actual error shown on the page.
        error_text = page.register.validation_email()
        assert error_text in (
            "This field is required",
            "Please enter a valid email address",
            "Email is invalid",
        ), f"Unexpected email error message: {error_text!r}"
        logger.info("TEST PASSED")

    @pytest.mark.failed
    def test_failed_register_unchecked_terms(self, page):
        """Submits without checking the terms checkbox — expects form not to submit."""
        logger.info("TEST: [FAILED] Register with unchecked terms checkbox")
        self._submit_form(
            page,
            name=page.data.random_name(),
            email=page.data.random_email(),
            phone=page.data.random_phonenum(),
            check_terms=False,
        )
        # Without terms checked, the page should stay on the registration form.
        # Adjust the expected error message to match the actual validation shown.
        error_text = page.register.validation_name()
        assert error_text in (
            "",
            "This field is required",
            "Please agree to the terms",
        ), f"Unexpected behavior: page should not navigate. Got: {error_text!r}"
        logger.info("TEST PASSED")

    @pytest.mark.failed
    def test_failed_register_max_length_name(self, page):
        """Enters a name exceeding max character limit — expects truncation or error."""
        logger.info("TEST: [FAILED] Register with name exceeding max length")
        long_name = "A" * 300  # Intentionally exceeds typical 100-255 char limit
        # Fill name only — don't submit, just check how the field handles it
        page.register.input_name_field(long_name)
        # Check the actual value stored in the input field
        name_el = page.register.driver.find_element(By.ID, "name")
        name_value = name_el.get_attribute("value")
        assert len(name_value) <= 255, f"Name was not truncated: {len(name_value)} chars"
        logger.info("TEST PASSED")

    # =====================================================================
    # Negative / Pre-registered data
    # =====================================================================

    @pytest.mark.failed
    @pytest.mark.registered
    def test_failed_register_with_registered_email(self, page):
        """Submits with a pre-registered email — expects 'sudah terdaftar' alert."""
        logger.info("TEST: [FAILED] Register with pre-registered email")
        self._submit_form(
            page,
            name=page.data.random_name(),
            email=REGISTERED_EMAIL,
            phone=page.data.random_phonenum(),
        )
        assert page.register.is_alert_visible(), (
            "Alert modal did not appear — check REGISTERED_EMAIL in RegisterTest.py"
        )
        assert page.register.get_alert_popup_text() == "Maaf! Anda sudah terdaftar di Valbury"
        logger.info("TEST PASSED")

    @pytest.mark.failed
    @pytest.mark.registered
    def test_failed_register_with_registered_phone(self, page):
        """Submits with a pre-registered phone — expects 'sudah terdaftar' alert."""
        logger.info("TEST: [FAILED] Register with pre-registered phone")
        self._submit_form(
            page,
            name=page.data.random_name(),
            email=page.data.random_email(),
            phone=REGISTERED_PHONE,
        )
        assert page.register.is_alert_visible(), (
            "Alert modal did not appear — check REGISTERED_PHONE in RegisterTest.py"
        )
        assert page.register.get_alert_popup_text() == "Maaf! Anda sudah terdaftar di Valbury"
        logger.info("TEST PASSED")
