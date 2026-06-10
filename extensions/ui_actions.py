from playwright.sync_api import Page, Locator
import allure

class UIActions:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Click on element")
    def click(self, element: Locator):
        """
        Wrapper for Playwright's click() method.
        Ensures the element is visible before clicking.
        """
        element.wait_for(state="visible")        
        element.click()

    @allure.step("Fill element with text")
    def fill(self, element: Locator, text: str):
        """
        Wrapper for Playwright's fill() method.
        Ensures the element is visible before filling.
        """
        element.wait_for(state="visible")
        element.fill(text)

    @allure.step("Get text from element")
    def get_text(self, element: Locator) -> str:
        """
        Wrapper for Playwright's inner_text() method.
        Ensures the element is visible before getting text.
        """
        element.wait_for(state="visible")
        return element.inner_text()
    
    @allure.step("Wait for element to be visible")
    def wait_for_element(self, element: Locator, timeout: int = 5000):
        """
        Wrapper for Playwright's wait_for() method.
        Waits for the element to be visible within the specified timeout.
        """
        element.wait_for(state="visible", timeout=timeout)

    @allure.step("Count elements")
    def count_elements(self, element: Locator) -> int:
        """
        Wrapper for Playwright's count_elements() method.
        Counts the number of elements matching the given locator.
        """
        return element.count()