"""Browser automation setup — pytest fixtures for Selenium WebDriver."""

import os
import logging
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
_logger = logging.getLogger("driver")


def get_chrome_options():
    options = Options()
    if os.environ.get("HEADLESS", "").lower() in ("1", "true", "yes"):
        _logger.info("Running in HEADLESS mode")
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")

    return options


@pytest.fixture(scope="session")
def browser():
    """Session-scoped Chrome WebDriver — one browser instance per test session."""
    
    # Configure environment to handle Chrome version mismatches
    os.environ['WDM_LOG'] = '0'  # Reduce WDM logging verbosity
    
    options = get_chrome_options()
    
    #Try direct initialization without version checking
    try:
        _logger.info("Attempting to initialize Chrome WebDriver...")
        
        # Disable binary location check temporarily
        service = Service()
        
        # Create driver with relaxed version checking
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(0)
        driver.maximize_window()
        
        _logger.info("✓ Chrome browser successfully initialized")
        
    except Exception as e:
        error_msg = str(e)
        _logger.error(f"✗ Direct Chrome initialization failed: {error_msg[:200]}")
        
        # If error is version-related, try to work around it
        if "only supports Chrome version" in error_msg or "session not created" in error_msg:
            _logger.info("Version mismatch detected. Attempting workaround...")
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                _logger.info("Downloading compatible ChromeDriver...")
                driver_path = ChromeDriverManager().install()
                _logger.info(f"ChromeDriver installed at: {driver_path}")
                service = Service(driver_path)
                driver = webdriver.Chrome(service=service, options=options)
                driver.implicitly_wait(0)
                driver.maximize_window()
                _logger.info("✓ Chrome initialized with compatible driver")
            except Exception as second_error:
                _logger.error(f"✗ Workaround failed: {str(second_error)[:200]}")
                raise
        else:
            raise
    
    _logger.info("Browser session started")
    yield driver
    
    try:
        driver.quit()
        _logger.info("✓ Browser session closed")
    except Exception as e:
        _logger.warning(f"Error closing browser: {e}")


@pytest.fixture(scope="function")
def page(browser):
    """Per-test fixture — provides fresh page objects and navigates to the app."""
    from Page.RegisterPage.RegisterPage import Register
    from Page.VerificationPage.VerificationPage import VerificationPage
    from Data.DataFeed import DataFeed

    browser.get("https://valbury.co.id/campaign/trading-tools-acuity")
    _logger.info("Navigated to: %s", browser.current_url)

    class PageObjects:
        register = Register(browser)
        verification_page = VerificationPage(browser)
        data = DataFeed()

    return PageObjects()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and attach to HTML report."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser")
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}_{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            _logger.error("TEST FAILED — screenshot saved: %s", screenshot_path)
