import sys
import os
import time
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import shutil
import json

from config import (
    UBLOCK_LITE_PATH,
    USER_DATA_DIR
)

# Set this URL 
URL_TO_INSPECT = "https://www.example.com"

# LOAD CONFIG

# try:
#     with open('config.json', 'r') as f:
#         config_data = json.load(f)
# except FileNotFoundError as e:
#     print(f"Error: Configuration file not found. Make sure 'config.json' exists.")
#     print(f"Details: {e}")
#     sys.exit(1)

# PATHS_CONFIG = config_data['paths']

# UBLOCK_LITE_PATH = os.path.abspath(PATHS_CONFIG['ublock_extension'])
# USER_DATA_DIR = PATHS_CONFIG['playwright_user_data']


def launch_inspector(use_adblock: bool):
    """
    Launches a browser with Playwright's Inspector for a given URL.
    
    Args:
        use_adblock: If True, loads the browser with the uBlock Lite extension.
    """
    print("-" * 60)
    print(f"Attempting to launch Inspector for: {URL_TO_INSPECT}")
    print(f"Ad Blocker Enabled: {use_adblock}")
    print("-" * 60)

    try:
        with sync_playwright() as p:
            context = None
            try:
                launch_args = ["--start-maximized"]
                if use_adblock:
                    if not os.path.exists(UBLOCK_LITE_PATH):
                        print(f"[ERROR] Ad blocker path not found: {UBLOCK_LITE_PATH}")
                        print("Please ensure the path is correct in the script's configuration section.")
                        return
                        
                    print("BROWSER: Ad blocker is ENABLED for this run.")
                    launch_args.extend([
                        f"--disable-extensions-except={UBLOCK_LITE_PATH}",
                        f"--load-extension={UBLOCK_LITE_PATH}"
                    ])
                else:
                    print("BROWSER: Ad blocker is DISABLED for this run.")

                # Launch a persistent context to use the extension
                context = p.chromium.launch_persistent_context(
                    USER_DATA_DIR,
                    headless=False,
                    channel="chromium",
                    args=launch_args,
                    no_viewport=True
                )

                if use_adblock:
                    print("BROWSER: Waiting for ad blocker service worker to initialize...")
                    # Wait for the extension's background process to start
                    if not context.service_workers:
                        context.wait_for_event('serviceworker', timeout=10000)
                    time.sleep(3) # Give it a moment to fully initialize

                page = context.new_page()
                
                # Apply stealth to make the browser appear more like a regular user's
                stealth = Stealth()
                stealth.apply_stealth_sync(page)

                print(f"BROWSER: Navigating to {URL_TO_INSPECT}...")
                page.goto(URL_TO_INSPECT, timeout=90000, wait_until="domcontentloaded")

                # Open playwright in inspect mode
                print("\n" + "="*60)
                print("BROWSER: PAUSING SCRIPT TO LAUNCH INSPECTOR.")
                print("Use the 'Pick locator' tool in the Inspector window to find elements.")
                print("Copy the generated locator and use it to update your 'sites.json' file.")
                print("CLOSE THE BROWSER WINDOW to end the script.")
                print("="*60 + "\n")
                page.pause()
                # The script will be paused here until you close the browser window.

            finally:
                if context:
                    context.close()
                    print("BROWSER: Browser context closed.")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] An error occurred during browser launch: {e}")

# ==============================================================================
# MAIN EXECUTION LOGIC
# ==============================================================================

def main():
    """Main function to get user input and run the inspector."""
    print("--- Playwright Element Inspector ---")
    
    # Clean up old user data for a fresh start
    if os.path.exists(USER_DATA_DIR):
        print(f"Removing old inspector user data directory: {USER_DATA_DIR}")
        shutil.rmtree(USER_DATA_DIR)

    while True:
        choice = input("Enable ad blocker for this inspection? (y/n): ").lower().strip()
        if choice in ['y', 'n']:
            use_adblock = (choice == 'y')
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            
    launch_inspector(use_adblock=use_adblock)
    
    print("\nInspector script finished.")

if __name__ == "__main__":
    main()