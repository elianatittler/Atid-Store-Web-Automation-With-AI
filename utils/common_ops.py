import csv
import os
import json

def load_config():
    """Loads the configuration from config.json and returns it as a dictionary."""
    # Get the absolute path of the current directory where conftest.py is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construct the correct path for config.json (move up one level if necessary)
    CONFIG_PATH = os.path.join(BASE_DIR, "../config.json")

    print(f"DEBUG: Looking for config.json at {CONFIG_PATH}")

    # Load the configuration from config.json
    try:
        with open(CONFIG_PATH, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"ERROR: Could not find config.json {CONFIG_PATH}") from e
    

def get_browser(request):
    """Extracts and sanitizes the browser selection from pytest command-line arguments."""
    browser_name = request.config.getoption("--browser")

    if not browser_name: 
            browser_name = "chromium"

    # Ensure browser_name is a string (fix issue where it's a list)
    if isinstance(browser_name, list):
            browser_name = browser_name[0]

    return browser_name.lower().strip()


def read_login_data(file_path):
     """Reads login data from a CSV file. """
     data = []
     with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
     return data