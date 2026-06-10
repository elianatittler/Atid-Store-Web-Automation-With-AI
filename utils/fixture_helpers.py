import os
import allure
from playwright.sync_api import sync_playwright
from .common_ops import load_config, get_browser #if utils.common_ops is in the same directory then it should be from .common_ops import ....

CONFIG = load_config()
BASE_URL_UI = CONFIG.get("BASE_URL_UI")
DEFAULT_TIMEOUT = CONFIG.get("DEFAULT_TIMEOUT")
BROWSER_WIDTH = CONFIG.get("BROWSER_WIDTH")
BROWSER_HEIGHT = CONFIG.get("BROWSER_HEIGHT")
BROWSER_POSITION_X = CONFIG.get("BROWSER_POSITION").get("x")
BROWSER_POSITION_Y = CONFIG.get("BROWSER_POSITION").get("y")
VIDEOS_DIR = CONFIG.get("VIDEOS_DIR")
TRACES_DIR = CONFIG.get("TRACES_DIR")
RECORD_VIDEO = CONFIG.get("RECORD_VIDEO")
ALLURE_RESULTS_DIR = CONFIG.get("ALLURE_RESULTS_DIR")
APPLITOOLS_API_KEY = CONFIG.get('APPLITOOLS_API_KEY')

TRACE_MESSAGE = "To view Trace file, please open 'Trace Manager', go to: {} , and select file: {}"


def attach_screenshot(page, item_name, screenshot_path):
    """Captures and attaches a screenshot to the Allure report."""
    page.screenshot(path=screenshot_path)
    with open(screenshot_path, "rb") as screenshot_file:
        allure.attach(
            screenshot_file.read(),
            name=f"Failure Screenshot: {item_name}",
            attachment_type=allure.attachment_type.PNG,
        )


def attach_video(page, item_name):
    """Attaches a video to the Allure report if available."""
    video_path = page.video.path()
    if video_path and os.path.exists(video_path):  # Check if video exists
        with open(video_path, "rb") as video_file:
            allure.attach(
                video_file.read(),
                name=f"Test Video: {item_name}",
                attachment_type=allure.attachment_type.MP4,
            )


def attach_trace(page, item_name, trace_path):
    """Attaches a Playwright trace to the Allure report."""
    page.context.tracing.stop(path=trace_path)
    trace_location = os.path.join(os.getcwd(), ALLURE_RESULTS_DIR) 
    if os.path.exists(trace_path):
        message = TRACE_MESSAGE.format(trace_location, os.path.basename(trace_path))
        allure.attach(message, name=f"Trace Message", attachment_type=allure.attachment_type.HTML)


def create_browser_context(browser):
    """Creates a new browser context with specified options."""
    context_options = {
        "viewport": {"width": BROWSER_WIDTH, "height": BROWSER_HEIGHT}
    }
    if RECORD_VIDEO:
        context_options["record_video_dir"] = VIDEOS_DIR
        context_options["record_video_size"] = {"width": BROWSER_WIDTH, "height": BROWSER_HEIGHT}
    return browser.new_context(**context_options)


def launch_browser(playwright, browser_name):
    """Launches the specified browser with configured arguments."""
    launch_args = [f"--window-position={BROWSER_POSITION_X},{BROWSER_POSITION_Y}"]

    if browser_name == "chromium" or browser_name == "msedge":
        browser = playwright.chromium.launch(headless=False, args=launch_args, channel="msedge" if browser_name == "msedge" else None)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False, args=launch_args)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=False, args=launch_args)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    return browser