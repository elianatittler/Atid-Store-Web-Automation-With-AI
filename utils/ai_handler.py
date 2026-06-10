import os
import json
import base64
from anthropic import Anthropic

class WebAIHandler:
    def __init__(self):
        # טעינת המפתח מתוך קובץ ה-config החסוי
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.client = Anthropic(api_key=config.get("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20261022"

    def analyze_ui_failure(self, error_message, screenshot_path, page_source=""):
        """
        שולח את הודעת השגיאה וצילום המסך ל-AI כדי לקבל ניתוח חכם והמלצת תיקון לסלקטור
        """
        if not os.path.exists(screenshot_path):
            return "Screenshot not found for analysis."

        # המרת צילום המסך ל-Base64 כדי שקלאוד יוכל 'לראות' אותו
        with open(screenshot_path, "rb") as image_file:
            screenshot_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        prompt = f"""
        You are an expert QA Automation AI Assistant. A Web UI automation test has failed.
        
        [Original Playwright Error]:
        {error_message}
        
        [Task]:
        Analyze the attached screenshot of the failure state alongside the error message.
        Provide a concise, professional analysis in English containing:
        1. Root Cause: Why did the test fail based on the visual state and error? (e.g., Element hidden, locator changed, dynamic content timeout).
        2. Suggested Fix / Self-Healing Selector: Provide the exact updated Playwright locator/strategy to fix this test.
        """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": screenshot_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"AI Analysis failed due to an exception: {str(e)}"