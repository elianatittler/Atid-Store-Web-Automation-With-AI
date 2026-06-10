from playwright.sync_api import Page

class CreateTeamPage:
    def __init__(self, page: Page):
        self.page = page
        self.new_team_link = page.get_by_role("link", name="New team")
        self.name_input = page.get_by_role("textbox", name="Name *")
        self.email_input = page.get_by_role("textbox", name="Email This is optional and is")
        self.create_team_button = page.get_by_role("button", name="Create")
        self.page_heading = page.locator("h1")

