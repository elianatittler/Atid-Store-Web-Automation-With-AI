from playwright.sync_api import Page

class CreateUserPage:
    def __init__(self, page: Page):
        self.page = page
        self.new_user_link = page.get_by_role("link", name="New user")
        self.name_input = page.get_by_label("Name *")
        self.email_input = page.get_by_label("Email")
        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password *")
        self.create_user_button = page.get_by_role("button", name="Create user")
        self.page_heading = page.locator("h1")