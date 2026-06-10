import os
import json
import pytest
import allure
from playwright.sync_api import sync_playwright
from utils.ai_handler import WebAIHandler

# מחפש את config.json תיקייה אחת למעלה מתיקיית tests
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path, 'r') as f:
    CONFIG = json.load(f)

# אתחול ה-AI Handler הגלובלי לפרויקט
ai_handler = WebAIHandler()

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
def page(context, request):
    # הגנה מפני שגיאות Tracing - בודק אם כבר רץ לפני שמתחיל
    try:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    except Exception:
        pass
    
    page = context.new_page()
    # הגדלת זמן המתנה ל-10 שניות כדי למנוע Timeouts
    page.set_default_timeout(10000)
    
    # שומר את אובייקט ה-page על ה-request כדי שה-Hook של ה-AI יוכל לגשת אליו בכישלון
    request.node.page_instance = page
    
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

# ==========================================
# 🤖 AI FAILURE INTERCEPTOR HOOK
# ==========================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook של Pytest שתופס את תוצאות הטסט.
    אם הטסט נכשל, הוא מפיק צילום מסך ושולח אותו לניתוח AI.
    """
    outcome = yield
    report = outcome.get_result()

    # פועל רק אם הטסט נכשל בשלב הריצה (call)
    if report.when == "call" and report.failed:
        page = getattr(item, "page_instance", None)
        
        if page:
            screenshot_dir = os.path.join(os.path.dirname(__file__), "failure_screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            
            try:
                # 1. צילום מסך אוטומטי של הדפדפן ברגע הכישלון
                page.screenshot(path=screenshot_path)
                print(f"\n[AI-Interceptor] Screenshot captured at: {screenshot_path}")
                
                # 2. שליחת הודעת השגיאה וצילום המסך לניתוח ה-AI
                print(f"[AI-Interceptor] Sending failure analysis request to Claude 3.5 Sonnet...")
                ai_analysis = ai_handler.analyze_ui_failure(
                    error_message=str(report.longrepr),
                    screenshot_path=screenshot_path
                )
                
                # 3. הדפסת הניתוח החכם ישירות לקונסול של Pytest
                print("\n" + "="*50 + "\n🤖 AI FAILURE ANALYSIS & SELF-HEALING REPORT\n" + "="*50)
                print(ai_analysis)
                print("="*50 + "\n")
                
                # הוספת הדו"ח בצורה בטוחה לתוך מערך הייצוג של Pytest
                # זה פותר את שגיאת ה-No Setter
                if hasattr(report, "sections"):
                    report.sections.append(("🤖 AI Failure Analysis", ai_analysis))
                
            except Exception as e:
                print(f"\n[AI-Interceptor] Failed to generate AI analysis: {str(e)}")