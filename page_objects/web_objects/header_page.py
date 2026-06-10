from playwright.sync_api import Page

class HeaderPage:
    def __init__(self, page: Page):
        self.page = page
        self.welcome_message = page.locator("div[data-testid='data-testid panel content'] h1")
        self.help_message = page.locator("div[data-testid='data-testid panel content'] h3")
        self.profile = page.get_by_label("Profile")
        self.kiosk = page.get_by_label("Enable kiosk mode")
        self.news = page.get_by_label("News")
        self.help = page.get_by_label("Help")
    