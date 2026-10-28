from playwright.sync_api import sync_playwright


def test_create_airport_in_browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.goto("http://127.0.0.1:5500/index.html")

        page.fill("#ident", "E2E01")
        page.fill("#name", "E2E Airport")
        page.fill("#country", "Brazil")
        page.fill("#latitude", "-23.5")
        page.fill("#longitude", "-46.6")

        page.once("dialog", lambda dialog: dialog.accept())
        page.click("button[type='submit']")

        page.wait_for_timeout(500)

        assert "E2E Airport" in page.locator("#airport-list").inner_text()

        browser.close()