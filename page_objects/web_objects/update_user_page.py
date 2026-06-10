from playwright.sync_api import Page

class UpdateUserPage:
    def __init__(self, page: Page):
        self.page = page
        self.user_link = lambda username: page.get_by_role("link", name=username)
        self.name_edit_button = lambda name: page.get_by_role("row", name=f"Name {name} Edit").get_by_role("button")
        self.name_input = page.get_by_label("Name")
        self.save_button = page.get_by_role("button", name="Save")