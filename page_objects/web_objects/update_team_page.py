from playwright.sync_api import Page

class UpdateTeamPage:
    def __init__(self, page: Page):
        self.page = page
        self.team_link = lambda team_name: page.get_by_role("link", name=team_name, exact=True)
        self.settings_tab = page.get_by_test_id("data-testid Tab Settings")
        self.starting_day_dropdown = page.get_by_role("combobox", name="Week start")
        self.sunday_option = page.get_by_text("Sunday")
        self.save_preferences = page.get_by_test_id("data-testid-shared-prefs-save")