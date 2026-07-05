#!/home/z/.venv/bin/python3
"""Capture GitHub screenshots for GLM-5 repo."""
import os
from playwright.sync_api import sync_playwright

OUT_DIR = "/home/z/my-project/download/glm5_shots"
os.makedirs(OUT_DIR, exist_ok=True)
REPO_URL = "https://github.com/zai-org/GLM-5"
CHROME_PATH = "/home/z/.cache/ms-playwright/chromium-1200/chrome-linux64/chrome"

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=CHROME_PATH, headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
    )
    context = browser.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=2)
    page = context.new_page()
    page.goto(REPO_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    # Shot 1: title section
    page.screenshot(path=f"{OUT_DIR}/01_title.png", clip={"x": 0, "y": 80, "width": 1280, "height": 200})
    print("01_title captured", flush=True)

    # Shot 2: stars sidebar
    try:
        about = page.locator('.BorderGrid-row .BorderGrid-cell, [class*="about"] .f4').first
        if about.is_visible():
            about.screenshot(path=f"{OUT_DIR}/02_about.png")
            print("02_about captured", flush=True)
        else:
            page.screenshot(path=f"{OUT_DIR}/02_about.png", clip={"x": 800, "y": 80, "width": 480, "height": 400})
    except:
        page.screenshot(path=f"{OUT_DIR}/02_about.png", clip={"x": 800, "y": 80, "width": 480, "height": 400})

    # Shot 3: files
    page.screenshot(path=f"{OUT_DIR}/03_files.png", clip={"x": 0, "y": 270, "width": 1280, "height": 400})
    print("03_files captured", flush=True)

    # Shot 4: README intro
    readme = page.locator('article.markdown-body').first
    readme.scroll_into_view_if_needed()
    page.wait_for_timeout(2000)
    readme.screenshot(path=f"{OUT_DIR}/04_readme.png")
    # Crop to top 700px
    from PIL import Image
    img = Image.open(f"{OUT_DIR}/04_readme.png")
    if img.height > 700:
        img.crop((0, 0, img.width, 700)).save(f"{OUT_DIR}/04_readme.png", "PNG")
    print("04_readme captured (cropped to 700px)", flush=True)

    browser.close()

# List
for f in sorted(os.listdir(OUT_DIR)):
    p = os.path.join(OUT_DIR, f)
    print(f"  {f} ({os.path.getsize(p)} bytes)")
