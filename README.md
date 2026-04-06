# ValburyToolsAquityTest

> UI automation test suite for the **Valbury** registration flow on the [Trading Tools Acuity campaign page](https://valbury.co.id/campaign/trading-tools-acuity).

ValburyToolsAquityTest is a Python-based UI automation test suite that validates the registration flow on Valbury's Trading Tools Acuity campaign page.

## Features

- 15 automated test cases covering positive and negative scenarios
- Page Object Model (POM) architecture for maintainable test code
- Randomized test data generation using Faker
- Screenshot capture on test failures
- HTML test report generation
- Headless browser support
- pytest markers for selective test execution

## Tech Stack

| Tool | Purpose |
|---|---|
| [Python 3.x](https://www.python.org/) | Core language |
| [Selenium](https://selenium.dev/) | Browser automation |
| [pytest](https://pytest.org/) | Test runner & framework |
| [pytest-html](https://pypi.org/project/pytest-html/) | HTML test reports |
| [Webdriver Manager](https://github.com/SergeyPirogov/webdriver_manager) | Auto-manages ChromeDriver |
| [Faker](https://faker.readthedocs.io/) | Randomized test data generation |

## Project Structure

```
ValburyToolsAquityTest/
├── conftest.py                      # pytest auto-discovery (imports fixtures from Driver/)
├── pytest.ini                       # pytest configuration
├── requirements.txt                 # Python dependencies
├── Data/
│   └── DataFeed.py                 # Test data generator (names, emails, phones)
├── Driver/
│   └── driver.py                   # pytest fixtures — browser, page, screenshot-on-failure
├── Page/
│   ├── RegisterPage/
│   │   └── RegisterPage.py         # Page Object — registration form
│   └── VerificationPage/
│       └── VerificationPage.py     # Page Object — post-registration verification
└── Tests/
    └── RegisterTest.py            # 15 test cases
```

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/nadsphere/ValburyToolsAquityTest.git
cd ValburyToolsAquityTest

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests
# All tests (headless)
HEADLESS=1 pytest Tests/RegisterTest.py -v

# Run by marker
pytest Tests/RegisterTest.py -v -m positive_test        # happy-path only
pytest Tests/RegisterTest.py -v -m negative_test        # validation tests only
pytest Tests/RegisterTest.py -v -m "not registered"     # skip registered-data tests
pytest Tests/RegisterTest.py -k "test_00[1-5]"          # specific range (runs 001-005)
pytest Tests/RegisterTest.py::TestRegistration::test_003_failed_register_blank_email # specific test

# Generate HTML report
pytest Tests/RegisterTest.py -v --html=reports/report.html --self-contained-html
```

## Test Cases

| # | Test | Marker | Description |
|---|------|--------|-------------|
| 001 | `test_001_success_register_with_valid_data` | `@positive_test` | Happy-path — valid name, email, phone; expects "Verifikasi" title |
| 002 | `test_002_failed_register_blank_name` | `@negative_test` | Blank name — expects "This field is required" |
| 003 | `test_003_failed_register_blank_email` | `@negative_test` | Blank email — expects "This field is required" |
| 004 | `test_004_failed_register_blank_phone` | `@negative_test` | Blank phone — expects "This field is required" |
| 005 | `test_005_failed_register_blank_name_email` | `@negative_test` | Blank name and email — expects both validation errors |
| 006 | `test_006_failed_register_blank_name_phone_number` | `@negative_test` | Blank name and phone — expects both validation errors |
| 007 | `test_007_failed_register_blank_email_phone_number` | `@negative_test` | Blank email and phone — expects both validation errors |
| 008 | `test_008_failed_register_all_blank_fields` | `@negative_test` | All fields blank — expects all three validation errors |
| 009 | `test_009_failed_register_with_registered_email` | `@negative_test @registered` | Pre-registered email — expects alert modal |
| 010 | `test_010_failed_register_with_registered_phone` | `@negative_test @registered` | Pre-registered phone — expects alert modal |
| 011 | `test_011_failed_register_with_less_than_character_phone` | `@negative_test` | Phone < 9 chars — expects "Minimum length 9 character" |
| 012 | `test_012_failed_register_with_invalid_phone` | `@negative_test` | Invalid phone number — expects "No. telepon yang anda masukan tidak valid" |
| 013 | `test_013_failed_register_with_less_than_character_name` | `@negative_test` | Name < 4 chars — expects "Please fill in using your full name" |
| 014 | `test_014_failed_register_with_invalid_name` | `@negative_test` | Invalid name characters — expects "The name you entered is invalid" |
| 015 | `test_015_failed_register_invalid_email_format` | `@negative_test` | Invalid email format — expects "The email you entered is invalid" |

> Tests marked `@registered` require pre-registered test data. Set `REGISTERED_EMAIL` and `REGISTERED_PHONE` in `Tests/RegisterTest.py` before running.

## Architecture

The project follows the **Page Object Model (POM)** pattern:

- **`Driver/driver.py`** — pytest fixtures: `browser` (session-scoped WebDriver), `page` (per-test page objects), screenshot-on-failure hook
- **`conftest.py`** — thin re-export file so pytest auto-discovers fixtures from `Driver/driver.py`
- **`Page/RegisterPage/`** — encapsulates locators and interactions for the registration form
- **`Page/VerificationPage/`** — encapsulates locators for the post-registration verification page
- **`Data/DataFeed.py`** — provides randomized test data via Faker
- **`Tests/RegisterTest.py`** — test scenarios using pytest markers (`@positive_test`, `@negative_test`, `@registered`)

## Browser Support

- **Chrome** (default) — run in headless mode with `HEADLESS=1`
- Other browsers can be added by extending `get_chrome_options()` in `Driver/driver.py`

## License

MIT License — see [LICENSE](LICENSE).
