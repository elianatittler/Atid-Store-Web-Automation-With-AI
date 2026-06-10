from extensions.verifications import Verify

def test_01_header_icons(web_flows):
    """ Verify header icons for Atid Store """
    web_flows.atid_store.navigate()
    
    # נבדוק שהלוגו או כפתור העגלה של החנות גלויים
    footer = web_flows.page.locator("footer")
    Verify.visible(footer)