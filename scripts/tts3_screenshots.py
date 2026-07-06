#!/home/z/.venv/bin/python3
"""Capture screenshots of 3 TTS voice cloning repos. Chụp TO, rõ ràng."""
import os
from playwright.sync_api import sync_playwright
from PIL import Image

OUT_DIR = "/home/z/my-project/download/tts3_shots"
os.makedirs(OUT_DIR, exist_ok=True)
CHROME_PATH = "/home/z/.cache/ms-playwright/chromium-1200/chrome-linux64/chrome"

REPOS = [
    ("CorentinJ/Real-Time-Voice-Cloning", "https://github.com/CorentinJ/Real-Time-Voice-Cloning", "rtvc"),
    ("RVC-Boss/GPT-SoVITS", "https://github.com/RVC-Boss/GPT-SoVITS", "gptsovits"),
    ("myshell-ai/OpenVoice", "https://github.com/myshell-ai/OpenVoice", "openvoice"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=CHROME_PATH, headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
    )
    context = browser.new_context(viewport={"width": 1400, "height": 900}, device_scale_factor=2)
    page = context.new_page()

    for full_name, url, short in REPOS:
        print(f"\n=== {full_name} ===", flush=True)
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        # Shot 1: title section (TO - full width 1400px)
        page.screenshot(path=f"{OUT_DIR}/{short}_01_title.png", clip={"x": 0, "y": 70, "width": 1400, "height": 250})
        print(f"  {short}_01_title captured", flush=True)

        # Shot 2: about/stars sidebar
        try:
            about = page.locator('.BorderGrid-row .BorderGrid-cell, [class*="about"] .f4').first
            if about.is_visible():
                about.screenshot(path=f"{OUT_DIR}/{short}_02_about.png")
                print(f"  {short}_02_about captured", flush=True)
            else:
                page.screenshot(path=f"{OUT_DIR}/{short}_02_about.png", clip={"x": 900, "y": 70, "width": 500, "height": 400})
        except:
            page.screenshot(path=f"{OUT_DIR}/{short}_02_about.png", clip={"x": 900, "y": 70, "width": 500, "height": 400})

        # Shot 3: files section
        page.screenshot(path=f"{OUT_DIR}/{short}_03_files.png", clip={"x": 0, "y": 280, "width": 1400, "height": 450})
        print(f"  {short}_03_files captured", flush=True)

        # Shot 4: README intro (TO)
        try:
            readme = page.locator('article.markdown-body').first
            readme.scroll_into_view_if_needed()
            page.wait_for_timeout(2000)
            readme.screenshot(path=f"{OUT_DIR}/{short}_04_readme.png")
            img = Image.open(f"{OUT_DIR}/{short}_04_readme.png")
            if img.height > 800:
                img.crop((0, 0, img.width, 800)).save(f"{OUT_DIR}/{short}_04_readme.png", "PNG")
            print(f"  {short}_04_readme captured", flush=True)
        except Exception as e:
            print(f"  readme err: {e}", flush=True)

    browser.close()

# List all
print(f"\n=== All screenshots ===")
for f in sorted(os.listdir(OUT_DIR)):
    p = os.path.join(OUT_DIR, f)
    img = Image.open(p)
    print(f"  {f} ({os.path.getsize(p)}B, {img.size[0]}x{img.size[1]})")
