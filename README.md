# GitHub Profile Scraper

This project automates the process of logging into GitHub, navigating to a specific user profile, extracting details such as the profile name, job title, location, and a list of repositories, and then storing this data in a CSV file.

## Overview

This project automates the process of scraping GitHub profile information using Python and Selenium. The scraper performs the following tasks:
- **Automated GitHub Login:** Uses your GitHub email and password (securely stored in a `.env` file) to log in.
- **Navigation:** Visits a specified GitHub profile.
- **Data Extraction:** Retrieves the profile's full name, job title, and location, along with a list of repositories (each with its name and link).
- **Data Storage:** Exports the extracted information to a CSV file.

The solution follows object-oriented principles, ensures secure handling of sensitive data, and includes robust error handling.

## Folder Structure

```
github_scraper/
├── src/
│   ├── __init__.py          # Initializes the src package
│   ├── github_scraper.py    # Contains the GithubScraper class with all functionality
│   └── main.py              # Entry point to run the scraper
├── .env                     # Environment variables (GITHUB_EMAIL, GITHUB_PASSWORD, TARGET_PROFILE)
├── requirements.txt         # Python dependencies
└── README.md                # This documentation file
```

## Setup Instructions

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/github_scraper.git
    cd github_scraper
    ```

2. **Create and Activate a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables:**

    Create a `.env` file in the project root directory with the following content:

    ```ini
    # .env file (do not commit this file to version control)
    GITHUB_EMAIL=your_email@example.com
    GITHUB_PASSWORD=your_github_password
    TARGET_PROFILE=octocat
    ```

    Replace `your_email@example.com`, `your_github_password`, and `octocat` with your actual GitHub email, password, and the target profile username respectively.

5. **Run the Scraper:**

    Execute the main script to start the scraping process:

    ```bash
    python src/main.py
    ```
