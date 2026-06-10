import pytest
import allure
import json
import os
from playwright.sync_api import sync_playwright

# טעינת הגדרות מקובץ config
with open('config.json') as f:
    CONFIG = json.load(f)

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser_type = CONFIG.get("BROWSER", "chromium")
        if browser_type == "firefox":
            browser = p.firefox.launch(headless=False)
        elif browser_type == "webkit":
            browser = p.webkit.launch(headless=False)
        else:
            browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture
def page(context):
    # הגנה מפני שגיאות Tracing - בודק אם כבר רץ לפני שמתחיל
    try:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    except Exception:
        pass
    
    page = context.new_page()
    # הגדלת זמן המתנה ל-10 שניות כדי למנוע Timeouts
    page.set_default_timeout(10000)
    
    yield page
    
    # סגירת Tracing בצורה בטוחה
    try:
        trace_path = os.path.join("allure-results", "trace.zip")
        context.tracing.stop(path=trace_path)
    except Exception:
        pass
    page.close()

@pytest.fixture
def web_flows(page):
    from workflows.web_flows import WebFlows
    return WebFlows(page)