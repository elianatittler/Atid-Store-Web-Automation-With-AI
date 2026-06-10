from playwright.sync_api import Page

class DeleteTeamPage:
    def __init__(self, page: Page):
        self.page = page
        self.delete_team_button = lambda team_name: page.get_by_role("button", name=f"Delete team {team_name}")
        self.confirm_delete_button = page.get_by_role("button", name="Delete", exact=True)