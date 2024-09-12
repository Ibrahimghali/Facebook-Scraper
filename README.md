# Facebook Scraper

**Facebook Scraper** is a Python script designed to automate the process of logging into Facebook, searching for specific topics, and retrieving post content along with reactions, comments, and shares using the Playwright framework. This project demonstrates how to use Playwright for web scraping and automation tasks.

## Features

- Log in to Facebook securely using environment variables for credentials.
- Search for topics and filter results by date.
- Retrieve and display post content, reactions, comments, and shares.
- Handles dynamic content loading and pagination.
## Requirements

- Python 3.x
- `playwright`
- `python-dotenv`

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/Facebook-Scraper.git
    cd Facebook-Scraper
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install Playwright browser binaries:**

    ```bash
    playwright install
    ```

## Setup

1. **Create a `.env` file** in the root directory of the project.

2. **Add your Facebook credentials** to the `.env` file:

    ```env
    FACEBOOK_EMAIL=your_email@gmail.com
    FACEBOOK_PASSWORD=your_password
    ```

## Usage

1. **Run the scraper:**

    ```bash
    python3 facebook_scraper.py
    ```

2. **The script will:**
    - Log in to Facebook using the credentials provided.
    - Search for a specified topic.
    - Retrieve and display post content, reactions, comments, and shares.

## Notes

- Ensure you comply with Facebook's terms of service and privacy policies.
- The script interacts with the Facebook web interface, which may change over time and affect the script's functionality.

## In Progress

This project is currently a work in progress. Contributions and improvements are welcome! Feel free to submit issues or pull requests.

## Contact

For any questions or issues, please contact [ibrahim.elghali@outlook.com](mailto:ibrahim.elghali@outlook.com).