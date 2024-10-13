import time
from playwright.sync_api import sync_playwright


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})

    page.goto(url_input)
    page.wait_for_selector('//*[@id="onetrust-banner-sdk"]/div/div')

    accept_button = page.locator("text='Accept'")
    accept_button.click()
    time.sleep(10)

    page.wait_for_selector('//*[@id="radix-:r0:"]')
    close_icon = page.locator('//*[@id="radix-:r0:"]/button')
    close_icon.click()  # Step 8
    time.sleep(3)

    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)

    page.wait_for_selector('footer')
    list_items = page.locator('footer a')
    count = list_items.count()
    print(f"Found {count} items in the footer.")

    for i in range(count):
        print(f"Attempting to click item {i}.")
        if list_items.nth(i).is_visible():
            list_items.nth(i).click()
            time.sleep(3)
            page.go_back()
            time.sleep(5)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)
            page.wait_for_selector('footer')
            list_items = page.locator('footer a')
        else:
            print(f"Item {i} is not visible.")

    context.close()
    browser.close()


if __name__ == "__main__":
    url_input = input("Please enter the URL: ")  # Prompt for the URL
    with sync_playwright() as playwright:
        run(playwright)
