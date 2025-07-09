import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
# IMPORTANT: Replace with your actual Chrome user data path and profile name
# You can find these by typing chrome://version in your Chrome browser
chrome_user_data_dir = r"C:\Users\win10\AppData\Local\Google\Chrome\User Data\Profile 2" # Example for Windows
# chrome_user_data_dir = "/Users/YourUsername/Library/Application Support/Google/Chrome" # Example for macOS

chrome_profile_name = "Default" # Or "Profile 1", "Profile 2", etc.

search_query = "Software Development Engineer freshers jobs"
target_job_portal = "linkedin.com" # Or naukri.com, indeed.com, etc.

# IMPORTANT: Replace with the absolute path to your resume file
# Ensure your resume is a PDF as most sites prefer/require it.
RESUME_FILE_PATH = r"C:\Users\win10\Downloads\Aman CV dev1.pdf" # Example for Windows
# RESUME_FILE_PATH = "/Users/YourUsername/Documents/my_resume.pdf" # Example for macOS

# Define some basic details for form filling (YOU WILL NEED MORE FOR REAL FORMS)
your_full_name = "Aman Singh"
your_email = "amansgh0706@gmail.com"
your_phone = "7644861122" # Example for India (+91 is often handled by default or separate field)
# Add more fields as needed for specific forms (e.g., current company, experience, etc.)

def automate_job_application_with_resume():
    if not os.path.exists(RESUME_FILE_PATH):
        print(f"Error: Resume file not found at {RESUME_FILE_PATH}. Please check the path.")
        return

    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={chrome_profile_name}")
    chrome_options.add_argument("--start-maximized")

    # Optional: Headless mode
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--window-size=1920,1080")

    print(f"Attempting to open Chrome with profile: {chrome_profile_name}")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Chrome browser opened successfully.")
    except Exception as e:
        print(f"Error initializing Chrome WebDriver: {e}")
        print("Please ensure Chrome is updated and check your Chrome user data path and profile name.")
        return

    wait = WebDriverWait(driver, 30) # Increased wait time for more complex interactions

    try:
        # --- Step 1: Go to Google ---
        driver.get("https://www.google.com")
        print("Navigated to Google.")
        time.sleep(2)

        # --- Step 2: Search on Google ---
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        print(f"Searched for: '{search_query}'")
        time.sleep(3)

        # --- Step 3: Navigate to a Specific Job Portal ---
        print(f"Looking for '{target_job_portal}' link in search results...")
        job_portal_link_xpath = f"//a[contains(@href, '{target_job_portal}') or contains(., '{target_job_portal}')]"
        try:
            job_portal_link = wait.until(EC.element_to_be_clickable((By.XPATH, job_portal_link_xpath)))
            job_portal_link.click()
            print(f"Clicked on {target_job_portal} link.")
            time.sleep(5)
        except Exception as e:
            print(f"Could not find or click {target_job_portal} link in search results: {e}")
            print("Please manually check if the link appears or adjust the search query.")
            return

        # --- Step 4: Search for jobs within the job portal (Highly site-specific) ---
        print(f"Searching for jobs on {target_job_portal}...")

        if "linkedin.com" in driver.current_url:
            print("Detected LinkedIn.com. Proceeding with LinkedIn-specific automation.")
            # LinkedIn typically requires login first for "Easy Apply"
            # If you are already logged in via your profile, this might skip.
            # Otherwise, you'd need to automate login here.

            # Example: Navigate to jobs page if not already there
            if "linkedin.com/jobs" not in driver.current_url:
                driver.get("https://www.linkedin.com/jobs/")
                print("Navigated to LinkedIn Jobs page.")
                time.sleep(3)

            # Find the search bar on LinkedIn Jobs (locators might change)
            try:
                # Assuming the search bar is present after navigating to jobs
                search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.jobs-search-box__text-input[aria-label='Search by title, skill, or company']")))
                search_input.clear()
                search_input.send_keys(search_query.replace("SDE ", "").replace(" freshers", "")) # Adjust query for LinkedIn
                search_input.send_keys(Keys.RETURN)
                print(f"Searched for '{search_query}' on LinkedIn.")
                time.sleep(5) # Wait for job listings to load

                # Find the 'Easy Apply' filter (crucial for automated application)
                # Locators for filters can be tricky and change frequently
                try:
                    easy_apply_filter = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Easy Apply')]")))
                    easy_apply_filter.click()
                    print("Applied 'Easy Apply' filter.")
                    time.sleep(5)
                except:
                    print("Could not find/click 'Easy Apply' filter. Proceeding without it.")


                # Iterate through job listings and try to apply
                job_listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container"))) # Example selector
                print(f"Found {len(job_listings)} job listings.")

                for i, job_listing in enumerate(job_listings[:5]): # Try the first 5 jobs
                    if i > 0: # Click next job after applying/skipping previous
                        job_listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container")))
                        job_listing = job_listings[i] # Re-locate to avoid StaleElementReferenceException

                    try:
                        job_title_element = job_listing.find_element(By.CSS_SELECTOR, ".job-card-container__link")
                        job_title = job_title_element.text
                        job_title_element.click()
                        print(f"Clicked on job: {job_title}")
                        time.sleep(3) # Wait for job details to load

                        # Wait for the "Easy Apply" button on the job details page
                        easy_apply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-apply-button"))) # Common LinkedIn button
                        if "Easy Apply" in easy_apply_button.text:
                            print(f"Found 'Easy Apply' button for {job_title}. Clicking it.")
                            easy_apply_button.click()
                            time.sleep(3)

                            # --- Handle the Easy Apply Modal/Form ---
                            print("Handling Easy Apply modal...")
                            # This is a multi-step form. Need to find fields and click 'Next'/'Review'/'Submit'
                            # You need to manually inspect the HTML of LinkedIn's Easy Apply form steps.

                            # Loop through form steps until "Review" or "Submit"
                            while True:
                                try:
                                    # Find the resume upload field
                                    # This is usually an <input type="file">
                                    # Sometimes it's labeled 'Upload resume' or similar.
                                    # The actual input might be hidden, but you can send_keys to it.
                                    resume_upload_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][name='file']"))) # Common LinkedIn file input
                                    if resume_upload_input:
                                        print(f"Uploading resume: {RESUME_FILE_PATH}")
                                        resume_upload_input.send_keys(RESUME_FILE_PATH)
                                        print("Resume uploaded (sent keys to input).")
                                        time.sleep(2)

                                    # Try to find the "Next" button
                                    next_button = None
                                    try:
                                        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Continue') or contains(., 'Next')]")))
                                    except:
                                        pass

                                    # Try to find the "Review" button (final step before submit)
                                    review_button = None
                                    try:
                                        review_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Review your application')]")))
                                    except:
                                        pass

                                    # Try to find the "Submit" button
                                    submit_button = None
                                    try:
                                        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit application')]")))
                                    except:
                                        pass

                                    # Prioritize clicking Submit, then Review, then Next
                                    if submit_button:
                                        submit_button.click()
                                        print(f"Successfully applied to {job_title}!")
                                        time.sleep(5) # Wait for confirmation or redirect
                                        break # Exit the while loop for this job
                                    elif review_button:
                                        review_button.click()
                                        print("Clicked 'Review' button.")
                                        time.sleep(3)
                                    elif next_button:
                                        next_button.click()
                                        print("Clicked 'Next' button.")
                                        time.sleep(3)
                                    else:
                                        print("No 'Next', 'Review', or 'Submit' button found. Form might be complete or stuck.")
                                        break # Exit the while loop for this job

                                except Exception as form_e:
                                    print(f"Error during form filling for {job_title}: {form_e}")
                                    print("Likely missing required fields, or new step in form. Skipping this job.")
                                    break # Exit the while loop for this job

                            # Close the application modal (if it's still open)
                            try:
                                close_modal_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Dismiss']")))
                                close_modal_button.click()
                                print("Dismissed application modal.")
                                time.sleep(2)
                            except:
                                pass # Modal already closed or no dismiss button


                        else:
                            print(f"'{job_title}' does not have an 'Easy Apply' option. Skipping.")
                    except Exception as job_e:
                        print(f"Error processing job listing {i+1}: {job_e}. Skipping to next job.")
                        # This might happen if the element becomes stale or unclickable
                        continue # Continue to the next job in the loop

            except Exception as e:
                print(f"Could not search or process jobs on LinkedIn. Error: {e}")

        elif "naukri.com" in driver.current_url:
            print("Detected Naukri.com. Proceeding with Naukri-specific automation.")
            # For Naukri, you'll need to locate job search inputs,
            # filters, then iterate job listings.

            # Example: Searching on Naukri if not already searched
            try:
                # Find search inputs (adjust locators based on Naukri's current design)
                keyword_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter skills / designations / companies']")))
                keyword_input.clear()
                keyword_input.send_keys(search_query)

                location_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter location']")))
                location_input.clear()
                location_input.send_keys("Bengaluru") # Or your desired location
                location_input.send_keys(Keys.RETURN) # Submit location, often triggers search
                print("Performed search on Naukri.")
                time.sleep(5)

                # Iterate through job listings
                job_listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".srp-jobtuple-wrapper"))) # Common Naukri job card selector
                print(f"Found {len(job_listings)} job listings on Naukri.")

                for i, job_listing in enumerate(job_listings[:5]): # Try first 5 jobs
                    if i > 0:
                        job_listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".srp-jobtuple-wrapper")))
                        job_listing = job_listings[i]

                    try:
                        job_title_element = job_listing.find_element(By.CSS_SELECTOR, ".title.ellipsis") # Example
                        job_title = job_title_element.text
                        job_title_element.click() # Click to open job details
                        print(f"Clicked on job: {job_title}")
                        time.sleep(3)

                        # Switch to the new tab/window if it opens
                        if len(driver.window_handles) > 1:
                            driver.switch_to.window(driver.window_handles[1])
                            print("Switched to new job details tab.")
                            time.sleep(2)

                        # Find and click the 'Apply' button on Naukri job details page
                        apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Apply now') or contains(., 'Apply')]")))
                        if apply_button:
                            print(f"Found 'Apply' button for {job_title}. Clicking it.")
                            apply_button.click()
                            time.sleep(3)

                            # --- Handle Naukri Application Form/Pop-up ---
                            print("Handling Naukri application form/pop-up...")
                            # Naukri might have a quick apply, or a multi-step form.
                            # Look for the resume upload input first.

                            try:
                                # This is a common locator for file input fields
                                resume_upload_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][name='file']")))
                                if resume_upload_input:
                                    print(f"Uploading resume: {RESUME_FILE_PATH}")
                                    resume_upload_input.send_keys(RESUME_FILE_PATH)
                                    print("Resume uploaded (sent keys to input).")
                                    time.sleep(2)

                                # Fill any other required fields that pop up
                                # Example: Name, Email, Phone (if not pre-filled by login)
                                # Check if these fields are present and fill them
                                try:
                                    name_field = driver.find_element(By.ID, "name") # Example ID
                                    if name_field.get_attribute('value') == "":
                                        name_field.send_keys(your_full_name)
                                        print("Filled name field.")
                                        time.sleep(0.5)
                                except: pass
                                try:
                                    email_field = driver.find_element(By.ID, "email") # Example ID
                                    if email_field.get_attribute('value') == "":
                                        email_field.send_keys(your_email)
                                        print("Filled email field.")
                                        time.sleep(0.5)
                                except: pass
                                try:
                                    phone_field = driver.find_element(By.ID, "mobile") # Example ID
                                    if phone_field.get_attribute('value') == "":
                                        phone_field.send_keys(your_phone)
                                        print("Filled phone field.")
                                        time.sleep(0.5)
                                except: pass

                                # Find and click the final submit button
                                submit_final_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit') or contains(., 'Apply')]")))
                                submit_final_button.click()
                                print(f"Successfully applied to {job_title} on Naukri!")
                                time.sleep(5) # Wait for confirmation

                            except Exception as form_e:
                                print(f"Error during form filling for {job_title} on Naukri: {form_e}")
                                print("Likely missing required fields, or new step in form. Skipping this job.")

                        else:
                            print(f"Could not find 'Apply' button for {job_title} on Naukri. Skipping.")

                        # Close the current job tab and switch back to main search results
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        print("Closed job tab and returned to main search.")
                        time.sleep(2)

                    except Exception as job_e:
                        print(f"Error processing job listing {i+1} on Naukri: {job_e}. Skipping to next job.")
                        # Ensure we close the new tab if it opened before error
                        if len(driver.window_handles) > 1:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        continue

            except Exception as e:
                print(f"Could not search or process jobs on Naukri. Error: {e}")

        else:
            print(f"Automation for {target_job_portal} is not implemented or detected.")
            print("Please extend the script with specific logic for this portal.")


    except Exception as e:
        print(f"An overarching error occurred during the automation process: {e}")

    finally:
        print("Automation complete. Closing browser in 10 seconds...")
        time.sleep(10)
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    automate_job_application_with_resume()