import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def automate_job_application():
    # --- Configuration ---
    # IMPORTANT: Replace with your actual Chrome user data path and profile name
    # You can find these by typing chrome://version in your Chrome browser
    chrome_user_data_dir = r"C:\Users\win10\AppData\Local\Google\Chrome\User Data\Profile 2" # Example for Windows
    # chrome_user_data_dir = "/Users/YourUsername/Library/Application Support/Google/Chrome" # Example for macOS

    chrome_profile_name = "Aman pro" # Or "Profile 1", "Profile 2", etc., based on your chrome://version

    search_query = "SDE jobs for freshers in Bengaluru"
    target_job_portal = "indeed.com" # Or indeed.com, linkedin.com, etc.

    # --- Step 1: Configure Chrome Options to Use a Specific Profile ---
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={chrome_profile_name}")
    chrome_options.add_argument("--start-maximized") # Maximize the browser window

    # Optional: Add headless mode if you don't want to see the browser
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu") # Required for headless on some systems
    # chrome_options.add_argument("--window-size=1920,1080") # Set a fixed window size for headless

    print(f"Attempting to open Chrome with profile: {chrome_profile_name}")

    # --- Step 2: Initialize WebDriver ---
    # Use ChromeDriverManager to automatically download and manage the ChromeDriver
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Chrome browser opened successfully.")
    except Exception as e:
        print(f"Error initializing Chrome WebDriver: {e}")
        print("Please ensure Chrome is updated and check your Chrome user data path and profile name.")
        return

    wait = WebDriverWait(driver, 20) # A common wait object for elements to load (up to 20 seconds)

    try:
        # --- Step 3: Go to Google ---
        driver.get("https://www.google.com")
        print("Navigated to Google.")
        time.sleep(2) # Give a moment for the page to load

        # Handle Google's "Sign in to Chrome" prompt if it appears (optional)
        # This is tricky as the prompt can vary. Sometimes it's a dismiss button.
        # inspect the element if this popup consistently blocks your automation
        # try:
        #     # Example: If there's a "No thanks" button
        #     no_thanks_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'No thanks')]")))
        #     no_thanks_button.click()
        #     print("Dismissed 'Sign in to Chrome' prompt.")
        #     time.sleep(2)
        # except:
        #     print("No 'Sign in to Chrome' prompt found or failed to dismiss.")
        #     pass

        # --- Step 4: Search on Google ---
        # Find the search bar and enter the query
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN) # Press Enter
        print(f"Searched for: '{search_query}'")
        time.sleep(3) # Wait for search results to load

        # --- Step 5: Navigate to a Specific Job Portal (e.g., Naukri.com) ---
        print(f"Looking for '{target_job_portal}' link in search results...")
        # This XPath looks for any link containing the job portal name
        # You might need to refine this based on actual search results
        job_portal_link_xpath = f"//a[contains(@href, '{target_job_portal}') or contains(., '{target_job_portal}')]"
        job_portal_link = wait.until(EC.element_to_be_clickable((By.XPATH, job_portal_link_xpath)))
        job_portal_link.click()
        print(f"Clicked on {target_job_portal} link.")
        time.sleep(5) # Wait for the job portal page to load

        # --- Step 6: Apply on one of the jobs (This is highly site-specific) ---
        print(f"Attempting to apply on a job on {target_job_portal}...")

        if "naukri.com" in driver.current_url:
            print("Detected Naukri.com. Proceeding with Naukri-specific automation...")
            # Example for Naukri (requires careful inspection of their HTML)
            # You'll need to find the actual locators for job listings and "Apply" buttons.
            # This part is the most prone to breaking due to website changes.

            # Find the first job listing (example - adjust locator)
            # You might need to find a list of job cards first, then iterate.
            # E.g., first_job_listing = wait.until(EC.presence_of_element_located((By.XPATH, "//article[@class='jobTuple bgWhite br4 mb-8']")))
            # first_job_listing.click() # Click to open job details

            # More robust way: Find all job listings, then click the first one if present
            job_listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".jobTuple.bgWhite"))) # Example CSS Selector for Naukri job cards
            if job_listings:
                print(f"Found {len(job_listings)} job listings. Clicking the first one.")
                job_listings[0].click()
                time.sleep(3) # Wait for job details page to load

                # Switch to the new window/tab if the job opens in a new one
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])
                    print("Switched to new job details tab.")
                    time.sleep(2)

                # Find the "Apply" button (example locators - inspect Naukri's current page!)
                try:
                    # Look for a button with "Apply" text or specific attributes
                    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Apply') or contains(., 'Easy Apply')] | //a[contains(., 'Apply')]")))
                    apply_button.click()
                    print("Clicked 'Apply' button.")
                    time.sleep(5) # Wait for application form/confirmation

                    # Handle potential pop-ups (e.g., login, resume upload, etc.)
                    # This is highly variable. You might need to detect popups and close them or fill forms.
                    # Example: if an "Are you sure?" confirmation appears
                    # try:
                    #     confirm_apply = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Confirm')]")))
                    #     confirm_apply.click()
                    #     print("Confirmed application.")
                    #     time.sleep(3)
                    # except:
                    #     pass # No confirmation needed or failed to find it

                except Exception as e:
                    print(f"Could not find or click 'Apply' button on Naukri. Error: {e}")
                    print("This might be due to a login requirement, different button text, or an overlay. Please inspect the page manually.")
            else:
                print("No job listings found on Naukri search results page.")

        elif "linkedin.com" in driver.current_url:
            print("Detected LinkedIn.com. Proceeding with LinkedIn-specific automation...")
            # LinkedIn often requires login first and has specific Easy Apply flows.
            # This is more complex and would require handling login, then navigating jobs.
            # Example: Search for a "Easy Apply" filter, then iterate and click.
            print("LinkedIn automation is more complex due to login and specific UI elements.")
            print("You would need to implement login handling first.")

        else:
            print(f"Automation for {target_job_portal} is not implemented or detected.")

    except Exception as e:
        print(f"An error occurred during the automation process: {e}")

    finally:
        print("Automation complete. Closing browser in 10 seconds...")
        time.sleep(10)
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    automate_job_application()