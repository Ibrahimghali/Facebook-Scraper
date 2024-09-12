```markdown
# Facebook Scraper

A simple Python script to log in to Facebook, search for a topic, and retrieve post content and reactions using Playwright.

## Requirements

- Python 3.7+
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
    python -m venv .venv
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
    python facebook_scraper.py
    ```

2. **The script will:**
    - Log in to Facebook using the credentials provided.
    - Search for a specified topic.
    - Retrieve and display post content, reactions, comments, and shares.

## Notes

- Ensure you comply with Facebook's terms of service and privacy policies.
- The script interacts with the Facebook web interface, which may change over time and affect the script's functionality.

## Contact

For any questions or issues, please contact [ibrahim.elghali@outlook.com](mailto:ibrahim.elghali@outlook.com).

```



