import os
import csv
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)

class GithubScraper:
    def __init__(self, email: str, password: str, target_profile: str):
        """Initialize the scraper and set up the driver."""
        self.email = email
        self.password = password
        self.target_profile = target_profile  # e.g., 'octocat'
        self.driver = self._initialize_driver()
        # Use a generous wait time for elements to load
        self.wait = WebDriverWait(self.driver, 15)
        self.profile_data = {} 
        self.repositories = []  # List of dictionaries with repo 'name' and 'link'

    def _initialize_driver(self):
        """Initialize Chrome WebDriver."""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            # Uncomment the next line to run headless:
            # options.add_argument("--headless")
            driver = webdriver.Chrome(service=ChromeService(), options=options)
            return driver
        except WebDriverException as e:
            print("WebDriver initialization failed:", e)
            raise

    def login(self):
        """Log in to GitHub using provided credentials."""
        try:
            self.driver.get("https://github.com/login")
            print("Opened GitHub login page.")
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "login_field"))
            )
            email_field.send_keys(self.email)
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            sign_in_button = self.driver.find_element(By.NAME, "commit")
            sign_in_button.click()
            # Allow some time for redirection
            time.sleep(30)
            self.driver.save_screenshot("after_login.png")
            print("after login took a screenshot")
            # Wait for an element that confirms a successful login
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "summary[aria-label='Add this repository to a list']")
                )
            )
            print("Login successful.")
        except TimeoutException:
            print("Timeout during login. Check your credentials, network, or if 2FA is enabled.")
            self.quit()
            raise
        except Exception as e:
            print("An error occurred during login:", e)
            self.quit()
            raise

    def navigate_to_profile(self):
        """Navigate to the target GitHub profile page."""
        profile_url = f"https://github.com/{self.target_profile}"
        print(f"Attempting to navigate to profile URL: {profile_url}")
        self.driver.get(profile_url)
        try:
            # Instead of waiting for a specific name element, wait for a container that exists on all profiles.
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.js-profile-editable-area"))
            )
            print("Profile page loaded. Current URL:", self.driver.current_url)
        except TimeoutException as e:
            print("Timeout navigating to profile. The page may not have loaded as expected.")
            self.driver.save_screenshot("profile_navigation_error.png")
            raise e

    def extract_profile_data(self):
        """Extract profile name, job title, and location."""
        try:
            full_name = self.driver.find_element(By.CLASS_NAME, "vcard-fullname").text.strip()
        except NoSuchElementException:
            full_name = "N/A"
        try:
            # Sometimes the job title element might not exist or may be in a different position.
            job_title = self.driver.find_element(By.CSS_SELECTOR, "div.vcard-details > div:nth-child(2)").text.strip()
        except NoSuchElementException:
            job_title = "N/A"
        try:
            location = self.driver.find_element(By.CSS_SELECTOR, "li[itemprop='homeLocation']").text.strip()
        except NoSuchElementException:
            location = "N/A"

        self.profile_data = {
            "full_name": full_name,
            "job_title": job_title,
            "location": location,
        }
        print("Profile data extracted:", self.profile_data)

    def extract_repositories(self):
        """Extract repository names and links from the repositories tab."""
        try:
            repos_tab = self.driver.find_element(By.XPATH, "//a[contains(@href, '?tab=repositories')]")
            repos_tab.click()
            print("Clicked on the repositories tab.")
            self.wait.until(EC.presence_of_element_located((By.ID, "user-repositories-list")))
            time.sleep(2)  # Allow dynamic content to load
            repo_elements = self.driver.find_elements(By.XPATH, "//li[contains(@itemprop, 'owns')]//a[@itemprop='name codeRepository']")
            for repo in repo_elements:
                repo_name = repo.text.strip()
                repo_link = repo.get_attribute("href")
                self.repositories.append({"name": repo_name, "link": repo_link})
            print(f"Extracted {len(self.repositories)} repositories.")
        except Exception as e:
            print("An error occurred while extracting repositories:", e)
            # Continue with what has been extracted

    def export_to_csv(self, filename="github_profile.csv"):
        """Export extracted profile data and repositories to a CSV file."""
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["full_name", "job_title", "location", "repositories"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                repo_str = "; ".join([f"{repo['name']} ({repo['link']})" for repo in self.repositories])
                row = {
                    "full_name": self.profile_data.get("full_name", "N/A"),
                    "job_title": self.profile_data.get("job_title", "N/A"),
                    "location": self.profile_data.get("location", "N/A"),
                    "repositories": repo_str,
                }
                writer.writerow(row)
            print(f"Data exported to {filename}.")
        except Exception as e:
            print("Failed to export data to CSV:", e)

    def quit(self):
        """Quit the WebDriver session."""
        if self.driver:
            self.driver.quit()
            print("Driver session ended.")

if __name__ == "__main__":
    load_dotenv()
    EMAIL = os.getenv("GITHUB_EMAIL")
    PASS = os.getenv("GITHUB_PASSWORD")
    PROFILE = os.getenv("TARGET_PROFILE")
    if not EMAIL or not PASS or not PROFILE:
        print("Missing environment variables. Please check your .env file.")
        exit(1)
    scraper = GithubScraper(EMAIL, PASS, PROFILE)
    try:
        scraper.login()
        scraper.navigate_to_profile()
        scraper.extract_profile_data()
        scraper.extract_repositories()
        scraper.export_to_csv()
    except Exception as err:
        print("An error occurred during the scraping process:", err)
    finally:
        scraper.quit()
