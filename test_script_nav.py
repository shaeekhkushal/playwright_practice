import time
from playwright.sync_api import sync_playwright


def run(playwright, url):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})

    # Navigate to the URL and handle pop-ups
    page.goto(url)
    page.wait_for_selector('//*[@id="onetrust-banner-sdk"]/div/div')
    print(f"Pop up found")

    accept_button = page.locator("text='Accept'")
    accept_button.click()
    print(f" OT Pop up Closed")
    time.sleep(10)

    page.wait_for_selector('//*[@id="radix-:r0:"]')
    print(f" Email Pop up found")
    close_icon = page.locator('//*[@id="radix-:r0:"]/button')
    close_icon.click()
    print(f" Email Pop up Closed")
    time.sleep(3)

    # Step 2: Locate the main navigation section
    main_nav_section = page.locator('header  nav')  # Adjust selector for the main nav section
    main_nav_items = main_nav_section.locator('ul > li')  # Adjust for the list of nav items
    count = main_nav_items.count()

    # Step 3: Print the list of navigation items
    print("Main Navigation Items:")
    for i in range(count):
        item_text = main_nav_items.nth(i).inner_text()
        print(f"{i + 1}: {item_text}")

    if count > 0:
        first_nav_item = main_nav_items.nth(0)
        print(f"\nHovering over: {first_nav_item.inner_text()}.")
        first_nav_item.hover()
        time.sleep(2)  # Wait for the modal to appear

        # Step 5: Look for the first anchor text in the modal
        sub_nav = first_nav_item.locator('#nav-menu')  # Adjust selector for the sub nav
        sub_items = sub_nav.locator('ul > li a')  # Adjust for the anchor selector
        sub_count = sub_items.count()

        if sub_count > 0:
            print(f"Found {sub_count} sub-navigation items under {first_nav_item.inner_text()}.")
            for j in range(sub_count):
                try:
                    print(f"Clicking on sub nav item: {sub_items.nth(j).inner_text()}.")
                    sub_items.nth(j).click()  # Click on the sub nav item
                    time.sleep(10)  # Wait for the page to load

                    # Go back to the previous page
                    page.go_back()
                    time.sleep(5)  # Wait for the page to load

                    # Re-hover to show the sub nav again for the next iteration
                    first_nav_item.hover()
                    time.sleep(2)  # Wait for the modal to appear again
                except Exception as e:
                    print(f"Failed to click on sub nav item {j + 1}: {e}")
                    continue  # Skip to the next sub item
        else:
            print("No sub-navigation items found.")
    else:
        print("No navigation items found.")

    # Close the browser
    context.close()
    browser.close()


if __name__ == "__main__":
    url_input = input("Please enter the URL: ")
    with sync_playwright() as playwright:
        run(playwright, url_input)
