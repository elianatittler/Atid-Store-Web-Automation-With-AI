from playwright.sync_api import Page

class DeleteUserPage:
    def __init__(self, page: Page):
        self.page = page
        self.user_edit_button = lambda name: self.page.get_by_label(f"Edit user {name}")
        self.delete_user_button = page.get_by_role("button", name="Delete user")
        self.confirm_delete_button = page.get_by_test_id("data-testid Confirm Modal Danger Button")
        self.user_cell = lambda name: self.page.get_by_role("cell", name=name, exact=True)
