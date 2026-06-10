# Atid Store - Web UI Automation Framework with AI Self-Healing

An advanced Web UI automation testing framework built for the **Atid Store** e-commerce platform using **Python**, **Pytest**, and **Playwright**. This repository features an innovative **AI-driven failure analysis interceptor** powered by Claude 3.5 Sonnet to automatically diagnose UI flaky tests and locator breaking changes.

---

## 🛠️ Key Features

* **Modern Web Automation:** Pure Page Object Model (POM) infrastructure using Playwright's native speed and stability.
* **🤖 AI Failure Interceptor:** Custom Pytest hooks intercept runtime failures, capture contextual screenshots, and consult **Claude 3.5 Sonnet** to deliver real-time self-healing selector suggestions.
* **Comprehensive Test Artifacts:** Automatic Playwright Tracing generation captured dynamically on failure.
* **Data-Driven Testing (DDT):** Seamless CSV test data decoupling for dynamic test suite execution.

---

## 🚀 Quick Start & Directory Structure

Get the framework up and running locally in less than 2 minutes:

```text
1. Clone the repository:
   git clone [https://github.com/elianatittler/Atid-Store-Web-Automation-With-AI.git](https://github.com/elianatittler/Atid-Store-Web-Automation-With-AI.git)
   cd Atid-Store-Web-Automation-With-AI

2. Set up the virtual environment & install dependencies:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

3. Install Playwright Browsers:
   playwright install

4. Run the test suite:
   python -m pytest tests/web/test_general_ui.py -s -v

5. Directory Structure:
   Atid-Store-Web-Automation-With-AI/
   ├── config.json               # Native environment keys (Excluded via .gitignore)
   ├── config.example.json       # Structural blueprint for environment configuration
   ├── utils/
   │   ├── ai_handler.py         # Anthropic Vision API integration layer
   │   ├── common_ops.py         # Global execution dynamic helpers
   │   └── fixture_helpers.py    # Playwright Request Context factories
   ├── page_objects/             # Page Object Model (POM) encapsulation layer
   ├── workflows/                # Business logic flow abstractions
   └── tests/
       ├── conftest.py           # Root test configuration & AI interceptor hook
       └── web/                  # Browser testing suites