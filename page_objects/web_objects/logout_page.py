from playwright.sync_api import Page

class LogoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.profile_icon = page.get_by_label("Profile", exact=True)
        self.logout_button = page.get_by_role("link", name="Sign out")
