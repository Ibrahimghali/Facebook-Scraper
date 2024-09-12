from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import os
from dotenv import load_dotenv
load_dotenv()


# Load environment variables if using a .env file
from dotenv import load_dotenv
load_dotenv()

# Define the scroll function
def scroll_to_next_post(page, last_post_selector):
    """Scroll down until a new post is visible."""
    previous_posts_count = len(page.query_selector_all(last_post_selector))

    while True:
        page.evaluate("window.scrollBy(0, window.innerHeight)")  # Scroll down
        time.sleep(2)  # Wait for new content to load

        current_posts_count = len(page.query_selector_all(last_post_selector))
        if current_posts_count > previous_posts_count:
            break

def login_facebook(email: str, password: str, topic: str):
    """
    Logs in to Facebook, searches for a topic, and retrieves post content and reactions.
    
    Args:
        email (str): Facebook account email.
        password (str): Facebook account password.
        topic (str): Topic to search for on Facebook.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        
        # Navigate to Facebook login page
        page.goto("https://www.facebook.com/")
        page.get_by_placeholder("Email or phone number").fill(email)
        page.get_by_placeholder("Password").fill(password)
        page.get_by_role("button", name="Log In").click()

        if not wait_for_page_to_load(page):
            browser.close()
            return
        
        search_topic(page, topic, "2024")
        if not navigate_to_first_post(page):
            browser.close()
            return

        post = page.locator("div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z").nth(0)
        handle_post_content(page, post)
        close_open_dialogs(page)
        
        browser.close()

def wait_for_page_to_load(page):
    """Waits for the Facebook homepage to load after logging in."""
    try:
        page.wait_for_selector('div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z', timeout=40000)
        return True
    except PlaywrightTimeoutError:
        print("Timeout waiting for the page to load after login")
        return False

def search_topic(page, topic, date):
    """Searches for the topic on Facebook."""
    page.get_by_placeholder("Rechercher sur Facebook").fill(topic)
    page.get_by_placeholder("Rechercher sur Facebook").press("Enter")
    page.get_by_role("link", name="Publications").click()
    page.get_by_label("Filtrer par Date de").locator("i").click()
    page.get_by_text(date, exact=True).click()
    time.sleep(5)
    page.reload()
    time.sleep(5)

def navigate_to_first_post(page):
    """Navigates to the first post after searching for the topic."""
    try:
        posts = page.locator("div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z")
        if posts.count() > 0:
            return True
        print("No posts found.")
        return False
    except PlaywrightTimeoutError:
        print("Timeout waiting for posts to load")
        return False

def handle_post_content(page, post):
    """Extracts the post title, content, reactions, and handles comments."""
    get_post_title(post)
    get_post_content(post)
    get_reactions(post)

    comments = get_comments(post)
    shares = get_shares(post)
    if comments > 0:
        handle_comments(page, post, comments)

def get_post_title(post):
    """Extracts the post title."""
    try:
        post_title = post.locator("strong.html-strong.xdj266r.x11i5rnm").text_content(timeout=30000)
        print("Post Title:", post_title)
    except PlaywrightTimeoutError:
        print("Error getting post title: Timeout")

def get_post_content(post):
    """Extracts the full post content."""
    try:
        content_elements = post.locator('div[dir="auto"]').all_text_contents()
        full_post_content = " ".join(content_elements)
        print("Full Post Content:", full_post_content.strip())
    except PlaywrightTimeoutError:
        print("Error getting full post content: Timeout")

def get_reactions(post):
    """Extracts the reactions count."""
    try:
        reactions = post.locator('span.xt0b8zv.x1e558r4').text_content(timeout=30000)
        print(f"Reactions: {reactions}")
    except PlaywrightTimeoutError:
        print("Error getting reactions: Timeout")

def get_comments(post):
    """Extracts the comments count."""
    comments = 0
    
    try:
        comments_text = post.get_by_text("commentaire").text_content(timeout=30000)
        comments = int(comments_text.split()[0].replace(',', ''))  # Convert to integer
        print("Comments:", comments)
    except ValueError:
        print("Error converting comments count to integer. Using default value of 0.")
        comments = 0
    except Exception as e:
        print(f"Error getting comments: {e}")
        comments = 0

    return comments

def get_shares(post):
    """Extracts the shares count."""
    shares = 0
    
    try:
        shares_text = post.get_by_text("partages").text_content(timeout=30000)
        shares = int(shares_text.split()[0].replace(',', ''))  # Convert to integer
        print("Shares:", shares)
    except ValueError:
        print("Error converting shares count to integer. Using default value of 0.")
        shares = 0
    except Exception as e:
        print(f"Error getting shares: {e}")
        shares = 0
    except PlaywrightTimeoutError:
        print("Error getting shares number: Timeout")
        shares = 0

    return shares

def handle_comments(page, post, comments):
    """Handles comments, clicking buttons, and extracting comments without scrolling."""
    try:
        comments_button = post.get_by_text("Commenter")
        comments_button.click()
        print("Successfully clicked on the comments button.")
        time.sleep(10)

        if comments > 6:
            try_to_click_comments_filter(page)
            page.get_by_text("Tous les commentaires", exact=True).click()
            print("Successfully clicked on 'Tous les commentaires'.")
            time.sleep(10)

        # Directly extract comments without scrolling
        extract_comments(page)
    except Exception as e:
        print(f"Error clicking the comments button: {e}")

def extract_comments(page):
    """Extracts all visible comments without scrolling."""
    comment_containers = page.locator('div.x1lliihq.xjkvuk6.x1iorvi4')
    
    for i in range(comment_containers.count()):
        comment_divs = comment_containers.nth(i).locator('div[dir="auto"]')
        comment_text = ' '.join(comment_divs.nth(j).text_content().strip() for j in range(comment_divs.count()))
        print(f"Comment {i+1}: {comment_text.strip()}")

def try_to_click_comments_filter(page):
    """Clicks on 'Plus pertinents' or 'Les meilleurs commentaires' filter."""
    try:
        page.get_by_role("button", name="Plus pertinents").click()
        print("Clicked on 'Plus pertinents'.")
    except PlaywrightTimeoutError:
        page.get_by_role("button", name="Les meilleurs commentaires").click()
        print("Clicked on 'Les meilleurs commentaires'.")

def close_open_dialogs(page):
    """
    Close any open dialogs on the page.
    """
    try:
        page.get_by_label("Fermer").click()
    except PlaywrightTimeoutError:
        print("Error closing dialog: Timeout")
    time.sleep(10)

def main():
    """Main function to call the login_facebook function with example arguments."""
    email = os.getenv("FACEBOOK_EMAIL")
    password = os.getenv("FACEBOOK_PASSWORD")
    if not email or not password:
        print("Email or password environment variables not set.")
        return

    login_facebook(email, password, "usa")

if __name__ == "__main__":
    main()
