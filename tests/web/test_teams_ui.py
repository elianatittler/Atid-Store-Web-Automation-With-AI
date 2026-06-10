import allure  
import pytest
from extensions.verifications import Verify
from tests.data.web_test_data import ADMIN_USER, ADMIN_PASS, WELCOME_MESSAGE, TEAM_NAME, TEAM_EMAIL, FIRST_DAY_OF_THE_WEEK, NO_TEAMS

@allure.title("Test 01 - Grafa login")
@allure.description("This test verifies that Grafana login is working")
def test_01_grafa_login(web_flows):
    web_flows.login(ADMIN_USER, ADMIN_PASS)
    
    # הוספת שורת המתנה קטנה כדי לוודא שהאלמנט מופיע על המסך לפני הבדיקה
    web_flows.header_page.welcome_message.wait_for(state="visible", timeout=5000)
    
    Verify.text(web_flows.header_page.welcome_message, WELCOME_MESSAGE)


def test_02_create_team(web_flows):
    web_flows.go_to_teams_page()
    web_flows.create_team(TEAM_NAME, TEAM_EMAIL)
    Verify.contain_text(web_flows.create_team_page.page_heading, TEAM_NAME)


def test_03_update_team(web_flows):
    web_flows.go_to_teams_page()  # שונה כאן מהגרסה הקודמת
    web_flows.update_team(TEAM_NAME)
    Verify.value(web_flows.update_team_page.starting_day_dropdown, FIRST_DAY_OF_THE_WEEK)


def test_04_delete_team(web_flows):
    web_flows.go_to_teams_page()  # שונה כאן וסודרו הרווחים בתחילת השורה
    web_flows.delete_team(TEAM_NAME)
    Verify.contain_text(web_flows.delete_team_page.page_content, NO_TEAMS)