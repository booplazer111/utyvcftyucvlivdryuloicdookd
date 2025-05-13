import asyncio
from playwright.async_api import async_playwright
import re

def title_from_url(url):
    return url.rstrip('/').split('/')[-1].replace('-', ' ')

async def main():
    # Read the list of game page URLs
    with open("links.txt") as f:
        links = [l.strip() for l in f if l.strip()]

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page    = await browser.new_page()

        for link in links:
            print("Processing:", link)
            await page.goto(f"view-source:{link}", wait_until="domcontentloaded")
            body_text = await page.text_content("body")

            # Find the loader URL
            idx = body_text.find("https://script.google.com/macros/s/")
            if idx == -1:
                print("  ✗ No macros URL found")
                continue
            end = body_text.find("/exec", idx)
            if end == -1:
                print("  ✗ Found start but no /exec")
                continue
            game_url = body_text[idx:end + len("/exec")]

            # Derive the title from URL path
            title = title_from_url(link)

            print(f"  → {title}: {game_url}")

            # Append to file immediately
            with open("game_urls.txt", "a", encoding="utf-8") as out:
                out.write(f"{title}: {game_url}\n")

        await browser.close()

asyncio.run(main())
