import os
import pandas as pd
from playwright.sync_api import sync_playwright
from services.genai_auditor import audit_ui_ux_with_gemini

def process_and_audit_batch(file_path: str, max_sites: int = 5):
    df = pd.read_csv(file_path)
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for idx, row in df.head(max_sites).iterrows():
            url = row.get("website", "")
            name = row.get("name", f"site_{idx}")

            if not url:
                continue
            if not url.startswith("http"):
                url = "http://" + url

            try:
                page = browser.new_page()
                page.goto(url, timeout=15000)
                title = page.title()
                text = page.inner_text("body")[:1000]

                screenshot_path = f"screenshots/{name.replace(' ', '_')}.png"
                os.makedirs("screenshots", exist_ok=True)
                page.screenshot(path=screenshot_path, full_page=True)
                page.close()

                # Audit using Gemini
                metadata = {
                    "url": url,
                    "title": title,
                    "text": text,
                    "screenshot_path": screenshot_path
                }
                audit_result = audit_ui_ux_with_gemini(metadata)

                results.append({
                    "name": name,
                    "url": url,
                    "title": title,
                    "audit": audit_result
                })

            except Exception as e:
                results.append({
                    "name": name,
                    "url": url,
                    "error": f"Playwright error: {str(e)}"
                })

        browser.close()
        
    return results
