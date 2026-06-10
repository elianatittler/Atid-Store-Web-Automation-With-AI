from playwright.sync_api import Page

class NavigationPage:
    def __init__(self, page: Page):
        self.page = page
        self.administration_link = page.get_by_role("link", name="Administration")
        self.users_access_link = page.get_by_role("link", name="Users and access")
        self.users_link = page.get_by_role("link", name="Users", exact=True)
        self.users_access_updated_link = page.get_by_role("heading", name="Users and access").get_by_role("link")
        self.users_updated_link = page.get_by_role("heading", name="Users", exact=True).get_by_role("link")
        self.teams_link = page.get_by_role("link", name="Teams")
        self.teams_updated_link = page.get_by_role("heading", name="Teams", exact=True).get_by_role("link")