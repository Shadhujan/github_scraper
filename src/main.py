from github_scraper import GithubScraper
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    EMAIL = os.getenv("GITHUB_EMAIL")
    PASS = os.getenv("GITHUB_PASSWORD")
    PROFILE = os.getenv("TARGET_PROFILE")
    
    if not EMAIL or not PASS or not PROFILE:
        print("ERROR: GITHUB_EMAIL, GITHUB_PASSWORD, and TARGET_PROFILE must be set in the .env file.")
        exit(1)

    scraper = GithubScraper(EMAIL, PASS, PROFILE)
    try:
        scraper.login()
        scraper.navigate_to_profile()
        scraper.extract_profile_data()
        scraper.extract_repositories()
        scraper.export_to_csv()
    except Exception as err:
        print("An error occurred:", err)
    finally:
        scraper.quit()

if __name__ == "__main__":
    main()
