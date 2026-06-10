import allure
from page_objects.web_objects.login_page import LoginPage
from page_objects.web_objects.navigation_page import NavigationPage
from page_objects.web_objects.create_user_page import CreateUserPage
from page_objects.web_objects.update_user_page import UpdateUserPage
from page_objects.web_objects.delete_user_page import DeleteUserPage
from page_objects.web_objects.header_page import HeaderPage
from page_objects.web_objects.create_team_page import CreateTeamPage
from page_objects.web_objects.update_team_page import UpdateTeamPage
from page_objects.web_objects.delete_team_page import DeleteTeamPage
from page_objects.web_objects.logout_page import LogoutPage

# דף החנות שלנו
from page_objects.web_objects.atid_store_page import AtidStorePage

from extensions.ui_actions import UIActions
from extensions.verifications import Verify
from tests.data.web_test_data import LOGIN_FAILED_MESSAGE

class WebFlows:
    def __init__(self, page):
        self.page = page
        self.actions = UIActions(page)
        self.login_page = LoginPage(page)
        self.navigation_page = NavigationPage(page)
        self.create_user_page = CreateUserPage(page)
        self.update_user_page = UpdateUserPage(page)
        self.delete_user_page = DeleteUserPage(page)
        self.header_page = HeaderPage(page)
        self.create_team_page = CreateTeamPage(page)
        self.update_team_page = UpdateTeamPage(page)
        self.delete_team_page = DeleteTeamPage(page)
        self.logout_page = LogoutPage(page)
        
        # אתחול דף החנות
        self.atid_store = AtidStorePage(page)

    # --- פונקציות Flow עבור Atid Store ---

    @allure.step("Flow: Search and verify product results")
    def search_and_verify(self, product_name, should_exist=True):
        self.atid_store.search_product(product_name)
        if should_exist:
            Verify.visible(self.atid_store.first_product_link)
        else:
            self.atid_store.verify_no_results()

    @allure.step("Flow: Add product to cart")
    def add_to_cart_flow(self, product_name):
        self.atid_store.search_product(product_name)
        self.atid_store.add_current_product_to_cart()

    @allure.step("Flow: Add and then remove product from cart")
    def add_and_remove_from_cart(self, product_name):
        self.add_to_cart_flow(product_name)
        self.atid_store.remove_from_cart()
        Verify.visible(self.atid_store.empty_cart_msg)

    @allure.step("Flow: Contact Us form submission")
    def send_contact_form(self, name, email, msg):
        self.atid_store.navigate()
        self.atid_store.fill_contact(name, email, msg)

    # --- פונקציות של Grafana ---
    def login(self, username, password, is_ddt=False):
        """Perfrom login flow"""
        # הוסיפי את השורה הזו כדי שהדפדפן ינווט אוטומטית לגראפנה לפני הלוגין:
        self.page.goto("http://localhost:3000") 
        
        self.actions.fill(self.login_page.username_input, username)
        self.actions.fill(self.login_page.password_input, password)
        self.actions.click(self.login_page.login_button) 
        if is_ddt:
            pass
        else:
            self.actions.click(self.login_page.skip_password_button)

    def login_ddt(self, username, password, expected_result):
        """Performs login flow with data-driven testing."""
        self.login(username, password, True)
        if expected_result == "success":
            Verify.visible(self.login_page.skip_password_button)
            self.actions.click(self.login_page.skip_password_button)
            self.logout()
        else:
            Verify.text(self.login_page.login_failed_message, LOGIN_FAILED_MESSAGE)         

    def create_user(self, name, email, username, password):
        """Performs user creation flow."""
        self.actions.click(self.create_user_page.new_user_link)
        self.actions.fill(self.create_user_page.name_input, name)
        self.actions.fill(self.create_user_page.email_input, email)
        self.actions.fill(self.create_user_page.username_input, username)
        self.actions.fill(self.create_user_page.password_input, password)
        self.actions.click(self.create_user_page.create_user_button)

    def update_user(self, user_name, old_name, new_name):
        """Performs user update flow."""
        self.actions.click(self.update_user_page.user_link(user_name))
        self.actions.click(self.update_user_page.name_edit_button(old_name))
        self.actions.fill(self.update_user_page.name_input, new_name)
        self.actions.click(self.update_user_page.save_button)
        
    def delete_user(self, name):
        """Performs user deletion flow."""
        self.actions.click(self.delete_user_page.user_edit_button(name))
        self.actions.click(self.delete_user_page.delete_user_button)
        self.actions.click(self.delete_user_page.confirm_delete_button)

    def go_to_users_page(self):
        """Navigates to the users page."""
        self.actions.click(self.navigation_page.administration_link)
        self.actions.click(self.navigation_page.users_access_link)
        self.actions.click(self.navigation_page.users_link)

    def verify_header_icons(self):
        """Verifies the presence of header icons."""
        Verify.soft_text(self.header_page.welcome_message, "Welcome to Grafana", "Text: 'Welcome to Grafana' mismatch")
        Verify.soft_text(self.header_page.help_message, "Need help?", "Text: 'Need help?' mismatch")
        Verify.soft_is_visible(self.header_page.profile, "Element 'Profile' is not visible")
        Verify.soft_is_visible(self.header_page.kiosk, "Element 'Enable kiosk mode' is not visible")
        Verify.soft_is_visible(self.header_page.news, "Element 'News' is not visible")
        Verify.soft_is_visible(self.header_page.help, "Element 'Help' is not visible")

    def go_to_teams_page(self):
        """Navigates to the teams page."""
        self.actions.click(self.navigation_page.administration_link)
        self.actions.click(self.navigation_page.users_access_link)
        self.actions.click(self.navigation_page.teams_link)

    def create_team(self, team_name, team_email):
        """Performs team creation flow."""
        self.actions.click(self.create_team_page.new_team_link)
        self.actions.fill(self.create_team_page.name_input, team_name)
        self.actions.fill(self.create_team_page.email_input, team_email)
        self.actions.click(self.create_team_page.create_team_button)

    def logout(self):
        """Performs logout flow."""
        self.actions.click(self.logout_page.profile_icon)
        self.actions.click(self.logout_page.logout_button)