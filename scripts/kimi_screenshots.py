#!/home/z/.venv/bin/python3
"""Capture Kimi K2.7 screenshots from HuggingFace + GitHub."""
import os
from playwright.sync_api import sync_playwright

OUT_DIR = "/home/z/my-project/download/kimi_shots"
os.makedirs(OUT_DIR, exist_ok=True)
CHROME_PATH = "/home/z/.cache/ms-playwright/chromium-1200/chrome-linux64/chrome"

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=CHROME_PATH, headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
    )
    context = browser.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=2)
    page = context.new_page()

    # === HuggingFace Kimi-K2.7-Code ===
    print("=== HuggingFace Kimi K2.7 ===", flush=True)
    page.goto("https://huggingface.co/moonshotai/Kimi-K2.7-Code", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    # Shot 1: Top of HF page (title + description)
    page.screenshot(path=f"{OUT_DIR}/01_hf_title.png", clip={"x": 0, "y": 80, "width": 1280, "height": 250})
    print("01_hf_title captured", flush=True)

    # Shot 2: README section
    try:
        readme = page.locator('div.prose, .markdown-body, main').first
        if readme.is_visible():
            readme.scroll_into_view_if_needed()
            page.wait_for_timeout(1500)
            readme.screenshot(path=f"{OUT_DIR}/02_hf_readme.png")
            # Crop to top 700px
            from PIL import Image
            img = Image.open(f"{OUT_DIR}/02_hf_readme.png")
            if img.height > 700:
                img.crop((0, 0, img.width, 700)).save(f"{OUT_DIR}/02_hf_readme.png", "PNG")
            print("02_hf_readme captured (cropped)", flush=True)
    except Exception as e:
        print(f"  readme err: {e}", flush=True)

    # === GitHub MoonshotAI/Kimi-K2 ===
    print("\n=== GitHub MoonshotAI/Kimi-K2 ===", flush=True)
    page.goto("https://github.com/MoonshotAI/Kimi-K2", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    # Shot 3: GitHub title section
    page.screenshot(path=f"{OUT_DIR}/03_gh_title.png", clip={"x": 0, "y": 80, "width": 1280, "height": 200})
    print("03_gh_title captured", flush=True)

    # Shot 4: Files section
    page.screenshot(path=f"{OUT_DIR}/04_gh_files.png", clip={"x": 0, "y": 270, "width": 1280, "height": 400})
    print("04_gh_files captured", flush=True)

    browser.close()

# List
for f in sorted(os.listdir(OUT_DIR)):
    p = os.path.join(OUT_DIR, f)
    print(f"  {f} ({os.path.getsize(p)} bytes)")
