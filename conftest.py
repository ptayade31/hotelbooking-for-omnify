import pytest
from drivers.web_driver import get_web_driver

@pytest.fixture(scope="function")
def web_driver():
    driver = get_web_driver()
    yield driver
    driver.quit()