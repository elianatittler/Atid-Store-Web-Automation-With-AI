from utils.common_ops import read_login_data
import pytest

LOGIN_DATA_PATH = "tests/data/ddt/login_data.csv"

@pytest.mark.parametrize("login_data", read_login_data(LOGIN_DATA_PATH))
def test_login(page, web_flows, login_data):
    """Data-drive testing for login functionality."""
    username = login_data["username"]
    password = login_data["password"]
    expected_result = login_data["expected_result"]
    web_flows.login_ddt(username, password, expected_result)
    