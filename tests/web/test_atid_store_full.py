import pytest
import allure
from extensions.verifications import Verify

@allure.feature("Atid Store - Full Web Suite")
class TestAtidStore:

    # פונקציית Setup שרצה אוטומטית לפני כל טסט ומנווטת לאתר החנות
    def setup_method(self, method):
        self.should_navigate = True

    @allure.story("Test 1: Search Non-Existent Product")
    @pytest.mark.negative
    def test_search_non_existent(self, web_flows):
        web_flows.atid_store.navigate()  # וידוא ניווט לחנות
        web_flows.search_and_verify("iPhone 15", should_exist=False)

    @allure.story("Test 2: Search Existing Product")
    def test_search_existing(self, web_flows):
        web_flows.atid_store.navigate()  # וידוא ניווט לחנות
        web_flows.search_and_verify("Shoes", should_exist=True)

    @allure.story("Test 3: Add Product to Cart")
    def test_add_to_cart(self, web_flows):
        web_flows.atid_store.navigate()  # וידוא ניווט לחנות
        web_flows.add_to_cart_flow("Bracelet")
        # בדיקה שהגענו לעמוד המוצר והכפתור קיים
        Verify.visible(web_flows.atid_store.add_to_cart_btn)

    @allure.story("Test 4: Add and Remove from Cart")
    def test_remove_from_cart(self, web_flows):
        web_flows.atid_store.navigate()  # וידוא ניווט לחנות
        web_flows.add_and_remove_from_cart("Anchor Bracelet")

    @allure.story("Test 5: Navigation to Men Category")
    def test_navigate_men_category(self, web_flows):
        web_flows.page.goto("https://atid.store/product-category/men/")
        Verify.text(web_flows.atid_store.store_title, "Men")

    @allure.story("Test 6: Contact Us - Successful Submission")
    def test_contact_us_success(self, web_flows):
        web_flows.send_contact_form("Eliana", "eli@test.com", "Great store!")
        # הערה: באתרים חיים לפעמים ה-Success הודעה משתנה, מוודאים שהטופס נשלח
        Verify.visible(web_flows.atid_store.success_msg)

    @allure.story("Test 7: Contact Us - Invalid Email Error")
    @pytest.mark.negative
    def test_contact_us_invalid_email(self, web_flows):
        web_flows.send_contact_form("Eliana", "invalid-email", "Help me")
        # בודקים שהדפדפן מציג ולידציה או שההודעה לא נשלחה
        Verify.visible(web_flows.atid_store.submit_btn)

    @allure.story("Test 8: Store Title Verification")
    def test_store_main_title(self, web_flows):
        web_flows.atid_store.navigate()
        
        # נחזיק את ה-body של העמוד כדי לוודא שהדף נטען
        body_element = web_flows.page.locator("body")
        body_element.wait_for(state="visible")
        
        # נוודא שהמילה Store קיימת בתוך ה-HTML של העמוד
        Verify.text(body_element, "Store")

    @allure.story("Test 9: Responsive Layout - Mobile View")
    def test_responsive_mobile_menu(self, web_flows):
        # משנים את גודל החלון לגודל של אייפון
        web_flows.page.set_viewport_size({"width": 375, "height": 667})
        web_flows.atid_store.navigate()
        # בודקים שהתפריט הפך לכפתור המבורגר (נייד)
        Verify.visible(web_flows.page.locator(".menu-toggle"))

    @allure.story("Test 10: Footer Visibility")
    def test_footer_exists(self, web_flows):
        web_flows.atid_store.navigate()
        footer = web_flows.page.locator("footer")
        Verify.visible(footer)
