# Re-export fixtures from Driver/driver.py so pytest auto-discovers them.
# All fixture logic lives in Driver/driver.py — this file only enables discovery.
from Driver.driver import browser, page, pytest_runtest_makereport

__all__ = ["browser", "page", "pytest_runtest_makereport"]
