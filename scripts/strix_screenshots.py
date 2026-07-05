#!/home/z/.venv/bin/python3
"""Capture 4 screenshots of usestrix/strix GitHub repo: title section, stars section, files section, readme section.
Each screenshot captures only one specific area as user requested."""
import os, time
from playwright.sync_api import sync_playwright

OUT_DIR = "/home/z/my-project/download/strix_shots"
os.makedirs(OUT_DIR, exist_ok=True)

REPO_URL = "https://github.com/usestrix/strix"

# Use existing chrome binary
CHROME_PATH = "/home/z/.cache/ms-playwright/chromium-1200/chrome-linux64/chrome"

print(f"=== Launching Chrome ===")
with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=CHROME_PATH,
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
    )
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        device_scale_factor=2,  # high DPI for sharp screenshots
    )
    page = context.new_page()

    print(f"=== Navigate to {REPO_URL} ===", flush=True)
    page.goto(REPO_URL, wait_until="domcontentloaded", timeout=60000)
    # Wait for content to load
    page.wait_for_timeout(3000)

    # Take full page screenshot for reference first
    page.screenshot(path=f"{OUT_DIR}/full_page.png", full_page=False)
    print("  Full page screenshot saved", flush=True)

    # === Shot 1: Title section (repo title + description) ===
    print("\n=== Shot 1: Title section ===", flush=True)
    try:
        # The title area is usually at top - h1 with repo name
        title_el = page.locator('h1').first
        if title_el.is_visible():
            title_el.screenshot(path=f"{OUT_DIR}/01_title.png")
            print("  Title element screenshot saved", flush=True)
        else:
            # Fallback: take top portion of page
            page.screenshot(path=f"{OUT_DIR}/01_title.png", clip={"x": 0, "y": 0, "width": 1280, "height": 250})
            print("  Title region screenshot saved (fallback)", flush=True)
    except Exception as e:
        print(f"  Title err: {e}", flush=True)
        page.screenshot(path=f"{OUT_DIR}/01_title.png", clip={"x": 0, "y": 0, "width": 1280, "height": 250})

    # === Shot 2: Stars/fork counts section ===
    print("\n=== Shot 2: Stars section ===", flush=True)
    try:
        # GitHub stores star count in #repo-stars-counter-star
        star_el = page.locator('#repo-stars-counter-star, #repo-stars-counter-star-aria-live').first
        if star_el.is_visible():
            # Capture the broader area around stars (about-box or repo header actions)
            # Use parent container
            parent = star_el.locator('xpath=..')
            parent.screenshot(path=f"{OUT_DIR}/02_stars.png")
            print("  Stars section screenshot saved", flush=True)
        else:
            # Fallback: capture the file navigation bar area where stars typically are
            page.screenshot(path=f"{OUT_DIR}/02_stars.png", clip={"x": 0, "y": 80, "width": 1280, "height": 200})
            print("  Stars region screenshot saved (fallback)", flush=True)
    except Exception as e:
        print(f"  Stars err: {e}", flush=True)
        page.screenshot(path=f"{OUT_DIR}/02_stars.png", clip={"x": 0, "y": 80, "width": 1280, "height": 200})

    # === Shot 3: Files section (file list) ===
    print("\n=== Shot 3: Files section ===", flush=True)
    try:
        # The file list area
        files_el = page.locator('[aria-label="Files"] , .file-navigation, .js-navigation-container').first
        if files_el.is_visible():
            files_el.screenshot(path=f"{OUT_DIR}/03_files.png")
            print("  Files section screenshot saved", flush=True)
        else:
            # Fallback: capture middle area where files are listed
            page.screenshot(path=f"{OUT_DIR}/03_files.png", clip={"x": 0, "y": 280, "width": 1280, "height": 400})
            print("  Files region screenshot saved (fallback)", flush=True)
    except Exception as e:
        print(f"  Files err: {e}", flush=True)
        page.screenshot(path=f"{OUT_DIR}/03_files.png", clip={"x": 0, "y": 280, "width": 1280, "height": 400})

    # === Shot 4: README section ===
    print("\n=== Shot 4: README section ===", flush=True)
    try:
        readme_el = page.locator('article.markdown-body, #readme, .markdown-body').first
        if readme_el.is_visible():
            readme_el.screenshot(path=f"{OUT_DIR}/04_readme.png")
            print("  README section screenshot saved", flush=True)
        else:
            # Scroll down and capture
            page.evaluate("window.scrollTo(0, 800)")
            page.wait_for_timeout(2000)
            page.screenshot(path=f"{OUT_DIR}/04_readme.png", clip={"x": 0, "y": 600, "width": 1280, "height": 500})
            print("  README region screenshot saved (fallback)", flush=True)
    except Exception as e:
        print(f"  README err: {e}", flush=True)
        page.screenshot(path=f"{OUT_DIR}/04_readme.png", clip={"x": 0, "y": 600, "width": 1280, "height": 500})

    browser.close()
    print("\n=== Done ===", flush=True)
    print(f"Screenshots in: {OUT_DIR}", flush=True)

# List output
for f in sorted(os.listdir(OUT_DIR)):
    p = os.path.join(OUT_DIR, f)
    print(f"  {f} ({os.path.getsize(p)} bytes)")
