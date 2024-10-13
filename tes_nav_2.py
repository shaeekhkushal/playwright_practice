import time
from playwright.sync_api import sync_playwright


def run(playwright, url):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})

    # Navigate to the URL and handle pop-ups
    page.goto(url)

    # Close the first pop-up
    page.wait_for_selector('//*[@id="onetrust-banner-sdk"]/div/div')
    accept_button = page.locator("text='Accept'")
    accept_button.click()
    print("OT Pop up Closed")
    time.sleep(5)

    # Close the second pop-up
    page.wait_for_selector('//*[@id="radix-:r0:"]')
    close_icon = page.locator('//*[@id="radix-:r0:"]/button')
    close_icon.click()
    print("Email Pop up Closed")
    time.sleep(3)

    # Locate the main navigation section
    main_nav_section = page.locator('header nav')
    main_nav_items = main_nav_section.locator('ul > li')
    nav_count = main_nav_items.count()

    # Loop through each main navigation item
    for i in range(nav_count):
        main_nav_item = main_nav_items.nth(i)
        item_text = main_nav_item.inner_text()
        print(f"Hovering over: {item_text}")

        # Hover over the main nav item
        main_nav_item.hover()
        time.sleep(2)

        # Locate any sub-menu (anchored links) under the current nav item
        submenu = main_nav_item.locator('ul > li a')
        submenu_count = submenu.count()

        if submenu_count > 0:
            print(f"Found {submenu_count} anchored items under '{item_text}'")

            # Loop through each submenu item
            for j in range(submenu_count):
                submenu_item = submenu.nth(j)
                submenu_item_text = submenu_item.inner_text()
                print(f"Clicking on sub-item: {submenu_item_text}")

                # Click on the submenu item and wait for the page to load
                submenu_item.click()
                page.wait_for_load_state("load")
                print(f"Page loaded for: {submenu_item_text}")
                time.sleep(5)

                # Go back to the previous page
                page.go_back()
                page.wait_for_load_state("load")
                time.sleep(5)

                # Re-fetch the main navigation items after page reload
                main_nav_section = page.locator('header nav')
                main_nav_items = main_nav_section.locator('ul > li')
                nav_count = main_nav_items.count()

                # Hover over the same main nav item again after coming back
                main_nav_item = main_nav_items.nth(i)  # Re-select the main nav item
                main_nav_item.hover()
                time.sleep(2)

        else:
            print(f"No sub-menu found under '{item_text}'")

    print("Completed navigation through all main items.")


if __name__ == "__main__":
    url_input = input("Please enter the URL: ")
    with sync_playwright() as playwright:
        run(playwright, url_input)
