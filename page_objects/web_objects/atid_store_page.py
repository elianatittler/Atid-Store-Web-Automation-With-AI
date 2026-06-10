import allure
from playwright.sync_api import Page, expect

class AtidStorePage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.get_by_placeholder("Search products…")
        # סלקטור מדויק יותר לכותרת החנות
        self.store_title = page.locator(".woocommerce-products-header__title, .entry-title")
        self.first_product_link = page.locator(".ast-loop-product__link").first
        self.add_to_cart_btn = page.get_by_role("button", name="Add to cart")
        
        self.cart_icon = page.locator(".ast-cart-menu-wrap").first
        self.remove_product_btn = page.locator(".remove").first
        # תיקון: הוספת .first כדי לפתור את ה-Strict Mode violation
        self.empty_cart_msg = page.locator(".cart-empty, .woocommerce-info").first

        self.contact_us_link = page.get_by_role("link", name="Contact Us").first
        self.name_field = page.get_by_placeholder("Name")
        self.email_field = page.get_by_placeholder("Email")
        self.message_field = page.get_by_placeholder("Message")
        self.submit_btn = page.get_by_role("button", name="Send Message")
        self.success_msg = page.locator(".wpforms-confirmation-container")

    @allure.step("Navigate to Store page")
    def navigate(self):
        self.page.goto("https://atid.store/store/")
        # מחכים שהדף יהיה מוכן לגמרי
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Search for product: {product_name}")
    def search_product(self, product_name: str):
        self.navigate()
        self.search_input.fill(product_name)
        self.search_input.press("Enter")

    @allure.step("Verify no results found message")
    def verify_no_results(self):
        expect(self.page.locator(".woocommerce-info").first).to_contain_text("No products were found")

    @allure.step("Add current product to cart")
    def add_current_product_to_cart(self):
        self.first_product_link.click()
        self.add_to_cart_btn.wait_for(state="visible")
        self.add_to_cart_btn.click()

    @allure.step("Remove product from cart")
    def remove_from_cart(self):
        self.cart_icon.click()
        self.remove_product_btn.wait_for(state="visible")
        self.remove_product_btn.click()
        # מחכים שהודעת הריקון תופיע
        self.empty_cart_msg.wait_for(state="visible")

    @allure.step("Fill contact form")
    def fill_contact(self, name, email, message):
        self.contact_us_link.click()
        self.name_field.fill(name)
        self.email_field.fill(email)
        self.message_field.fill(message)
        self.submit_btn.click()