from extensions.verifications import Verify
from tests.data.web_test_data import ADMIN_USER, ADMIN_PASS, NAME, EMAIL, USER_NAME, USER_PASS, NEW_NAME, WELCOME_MESSAGE
import allure

@allure.title("Test 01 - Grafa login")
@allure.description("This test verifies that Grafana login is working")
def test_01_grafa_login(web_flows):
    web_flows.login(ADMIN_USER, ADMIN_PASS)
    Verify.text(web_flows.header_page.welcome_message, WELCOME_MESSAGE)

@allure.title("Test 02 - Create user")
@allure.description("This test verifies that user can be created")
def test_02_create_user(web_flows):
    web_flows.go_to_users_page()
    web_flows.create_user(NAME, EMAIL, USER_NAME, USER_PASS)
    Verify.contain_text(web_flows.create_user_page.page_heading, USER_NAME)

@allure.title("Test 03 - Update user")
@allure.description("This test verifies that user can be updated")
def test_03_update_user(web_flows):
    web_flows.go_to_users_page()
    web_flows.update_user(USER_NAME, NAME, NEW_NAME)
    Verify.contain_text(web_flows.update_user_page.page_content, NEW_NAME)  # תוקן: הוסרו הגרשיים מהמשתנה

@allure.title("Test 04 - Delete user")
@allure.description("This test verifies that user can be deleted")
def test_04_delete_user(web_flows):
    web_flows.go_to_users_page()
    web_flows.delete_user(NEW_NAME)
    Verify.count(web_flows.delete_user_page.user_cell(NEW_NAME), 0)


