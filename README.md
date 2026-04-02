# ValburyToolsAquityTest

![CI](https://github.com/nadsphere/ValburyToolsAquityTest/actions/workflows/ci.yml/badge.svg)

UI automation test suite for the **Valbury** registration flow on the [Trading Tools Acuity campaign page](https://valbury.co.id/campaign/trading-tools-acuity).

## Tech Stack

| Tool | Purpose |
|---|---|
| [Python 3.x](https://www.python.org/) | Core language |
| [Selenium](https://www.selenium.dev/) | Browser automation |
| [pytest](https://pytest.org/) | Test runner & framework |
| [pytest-html](https://pypi.org/project/pytest-html/) | HTML test reports |
| [Webdriver Manager](https://github.com/SergeyPirogov/webdriver_manager) | Auto-manages ChromeDriver |
| [Faker](https://faker.readthedocs.io/) | Randomized test data generation |

## Project Structure

```
ValburyToolsAquityTest/
├── conftest.py                    # pytest auto-discovery (imports fixtures from Driver/)
├── pytest.ini                     # pytest configuration
├── requirements.txt               # Python dependencies
├── Data/
│   └── DataFeed.py               # Test data generator (names, emails, phones)
├── Driver/
│   └── driver.py                 # pytest fixtures — browser, page, screenshot-on-failure
├── Page/
│   ├── RegisterPage/
│   │   └── RegisterPage.py       # Page Object — registration form
│   └── VerificationPage/
│       └── VerificationPage.py    # Page Object — post-registration verification
├── Tests/
│   └── RegisterTest.py           # 9 test cases (pytest-style)
└── .github/
    └── workflows/
        └── ci.yml                # GitHub Actions CI pipeline
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
pytest Tests/RegisterTest.py -v -m success      # happy-path only
pytest Tests/RegisterTest.py -v -m failed       # negative tests only
pytest Tests/RegisterTest.py -v -m "not registered"  # skip registered-data tests

# Generate HTML report
pytest Tests/RegisterTest.py -v --html=reports/report.html --self-contained-html
```

## Test Cases

| # | Test | Marker | Description |
|---|------|--------|-------------|
| 1 | `test_success_register_with_valid_data` | `@success` | Happy-path — all valid fields, expects "Verifikasi" title |
| 2 | `test_failed_register_blank_name` | `@failed` | Blank name — expects "This field is required" |
| 3 | `test_failed_register_blank_email` | `@failed` | Blank email — expects "This field is required" |
| 4 | `test_failed_register_blank_phone` | `@failed` | Blank phone — expects "This field is required" |
| 5 | `test_failed_register_invalid_email_format` | `@failed` | Invalid email format — expects validation error |
| 6 | `test_failed_register_unchecked_terms` | `@failed` | Terms unchecked — expects form not to submit |
| 7 | `test_failed_register_max_length_name` | `@failed` | Name exceeds max length — expects truncation/error |
| 8 | `test_failed_register_with_registered_email` | `@failed @registered` | Pre-registered email — expects alert modal |
| 9 | `test_failed_register_with_registered_phone` | `@failed @registered` | Pre-registered phone — expects alert modal |

> Tests marked `@registered` require pre-registered test data. Set `REGISTERED_EMAIL` and `REGISTERED_PHONE` in `Tests/RegisterTest.py` before running.

## Architecture

The project follows the **Page Object Model (POM)** pattern:

- **`Driver/driver.py`** — all pytest fixtures: `browser` (session-scoped WebDriver), `page` (per-test page objects), screenshot-on-failure hook
- **`conftest.py`** — thin re-export file so pytest auto-discovers fixtures from `Driver/driver.py`
- **`Page/RegisterPage/`** — encapsulates locators and interactions for the registration form
- **`Page/VerificationPage/`** — encapsulates locators for the post-registration verification page
- **`Data/DataFeed.py`** — provides randomized test data via Faker
- **`Tests/RegisterTest.py`** — test scenarios using pytest markers (`@success`, `@failed`, `@registered`)

## CI/CD

Every push and pull request to `main` automatically:
1. Spins up an Ubuntu runner
2. Installs dependencies
3. Runs all tests headless (`HEADLESS=1`)
4. Skips `@registered` tests (requires live backend data)
5. Uploads the HTML test report and failure screenshots as build artifacts

## Browser Support

- **Chrome** (default) — run in headless mode with `HEADLESS=1`
- Other browsers can be added by extending `get_chrome_options()` in `conftest.py`

## License

MIT License — see [LICENSE](LICENSE).
