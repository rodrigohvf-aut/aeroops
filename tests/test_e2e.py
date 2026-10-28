from uuid import uuid4

from playwright.sync_api import expect, sync_playwright


def test_create_airport_in_browser():
    ident = f"E2E{uuid4().hex[:8].upper()}"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        try:
            page.goto("http://127.0.0.1:5500/index.html")

            page.fill("#ident", ident)
            page.fill("#name", "E2E Airport")
            page.fill("#country", "Brazil")
            page.fill("#latitude", "-23.5")
            page.fill("#longitude", "-46.6")

            page.once("dialog", lambda dialog: dialog.accept())
            page.click("button[type='submit']")

            expect(page.locator("#airport-list")).to_contain_text(
                f"{ident} - E2E Airport"
            )

        finally:
            response = page.request.get("http://127.0.0.1:8000/airports")
            if response.ok:
                airport = next(
                    (item for item in response.json()["airports"] if item["ident"] == ident),
                    None,
                )
                if airport is not None:
                    page.request.delete(
                        f"http://127.0.0.1:8000/airports/{airport['id']}"
                    )

            browser.close()