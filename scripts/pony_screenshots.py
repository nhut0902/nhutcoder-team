#!/home/z/.venv/bin/python3
"""Capture balanced screenshots of ponytail repo - each sized to fit nicely in 1080x1920 frame.
Viewport 1280x800 (16:10) so screenshots are landscape and can be resized to fit width 1000."""
import os
from playwright.sync_api import sync_playwright

OUT_DIR = "/home/z/my-project/download/pony_shots"
os.makedirs(OUT_DIR, exist_ok=True)

REPO_URL = "https://github.com/DietrichGebert/ponytail"
CHROME_PATH = "/home/z/.cache/ms-playwright/chromium-1200/chrome-linux64/chrome"

print(f"=== Launch Chrome ===")
with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=CHROME_PATH,
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
    )
    # Balanced viewport: 1280x800 - good landscape ratio
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        device_scale_factor=2,
    )
    page = context.new_page()

    print(f"=== Navigate to {REPO_URL} ===", flush=True)
    page.goto(REPO_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    # === Shot 1: Title + description section (top of repo) ===
    print("\n=== Shot 1: Title + description ===", flush=True)
    try:
        # Repo header area - includes name + "Public" + fork/star counts
        # Capture from top down to about 200px to get title + buttons
        page.screenshot(path=f"{OUT_DIR}/01_title.png", clip={"x": 0, "y": 80, "width": 1280, "height": 200})
        print("  Title section captured", flush=True)
    except Exception as e:
        print(f"  err: {e}", flush=True)

    # === Shot 2: Star/Fork counts (about box) ===
    print("\n=== Shot 2: Stars + fork counts ===", flush=True)
    try:
        # About sidebar - usually on right side, contains description + topics + stars
        # On mobile/single column it's below; let's capture sidebar
        about = page.locator('.BorderGrid-row .BorderGrid-cell, [class*="about"] .f4').first
        if about.is_visible():
            about.screenshot(path=f"{OUT_DIR}/02_stars.png")
            print("  Stars section captured", flush=True)
        else:
            # Fallback: capture star button area (top right)
            page.screenshot(path=f"{OUT_DIR}/02_stars.png", clip={"x": 800, "y": 80, "width": 480, "height": 100})
            print("  Stars fallback captured", flush=True)
    except Exception as e:
        print(f"  err: {e}", flush=True)
        page.screenshot(path=f"{OUT_DIR}/02_stars.png", clip={"x": 800, "y": 80, "width": 480, "height": 100})

    # === Shot 3: Files (file list section) ===
    print("\n=== Shot 3: Files ===", flush=True)
    try:
        # File list - capture from y=270 down 400px
        page.screenshot(path=f"{OUT_DIR}/03_files.png", clip={"x": 0, "y": 270, "width": 1280, "height": 400})
        print("  Files captured", flush=True)
    except Exception as e:
        print(f"  err: {e}", flush=True)

    # === Shot 4: README (intro section) ===
    print("\n=== Shot 4: README intro ===", flush=True)
    try:
        readme = page.locator('article.markdown-body').first
        if readme.is_visible():
            # Capture just first 800px of README (intro)
            readme_box = readme.bounding_box()
            if readme_box:
                # Get only top portion
                capture_h = min(800, readme_box['height'])
                page.screenshot(path=f"{OUT_DIR}/04_readme.png", clip={
                    "x": readme_box['x'],
                    "y": readme_box['y'],
                    "width": readme_box['width'],
                    "height": capture_h
                })
                print(f"  README intro captured ({readme_box['width']}x{capture_h})", flush=True)
            else:
                page.screenshot(path=f"{OUT_DIR}/04_readme.png", clip={"x": 0, "y": 600, "width": 1280, "height": 600})
        else:
            # Scroll down first
            page.evaluate("window.scrollTo(0, 700)")
            page.wait_for_timeout(2000)
            page.screenshot(path=f"{OUT_DIR}/04_readme.png", clip={"x": 0, "y": 700, "width": 1280, "height": 600})
            print("  README fallback captured", flush=True)
    except Exception as e:
        print(f"  err: {e}", flush=True)

    # === Shot 5: README - Installation section ===
    print("\n=== Shot 5: Install commands ===", flush=True)
    try:
        # Search for install section by scrolling
        page.evaluate("window.scrollTo(0, 1200)")
        page.wait_for_timeout(2000)
        page.screenshot(path=f"{OUT_DIR}/05_install.png", clip={"x": 0, "y": 1100, "width": 1280, "height": 500})
        print("  Install section captured", flush=True)
    except Exception as e:
        print(f"  err: {e}", flush=True)

    browser.close()
    print(f"\n=== Done. Files in: {OUT_DIR} ===", flush=True)

# List
for f in sorted(os.listdir(OUT_DIR)):
    p = os.path.join(OUT_DIR, f)
    print(f"  {f} ({os.path.getsize(p)} bytes)")
