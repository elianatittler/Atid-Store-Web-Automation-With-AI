from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_test_id("data-testid Username input field")
        self.password_input = page.get_by_test_id("data-testid Password input field")
        self.login_button = page.get_by_test_id("data-testid Login button")
        self.skip_password_button = page.get_by_test_id("data-testid Skip change password button")
        self.login_failed_message = page.locator("div[data-testid='data-testid Alert error'] span")