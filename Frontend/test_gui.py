from playwright.sync_api import sync_playwright

def test_gui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://localhost:8000")  # Replace with your GUI URL
        page.screenshot(path="homepage.png")
        browser.close()

if __name__ == "__main__":
    test_gui()
