#!/home/z/.venv/bin/python3
"""Render 6 BALANCED frames for Ponytail video. NO animation - just clean static frames.
Screenshots are sized to fit nicely within 1080x1920 (vertical TikTok format).
Each frame: header label + screenshot (balanced size) + Vietnamese subtitle + footer label."""
import os, json
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/z/my-project/download/pony_frames"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1080, 1920
FONT_REG = "/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

def draw_gradient(draw, top, bottom):
    for y in range(H):
        t = y / H
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def center_text(draw, text, fnt, y, fill=(255, 255, 255)):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    text_w = bbox[2] - bbox[0]
    x = (W - text_w) // 2
    draw.text((x, y), text, font=fnt, fill=fill)

def paste_screenshot_balanced(img, shot_path, max_w, max_h, y_start):
    """Paste screenshot centered, fit within max_w x max_h (preserve aspect ratio)."""
    shot = Image.open(shot_path).convert("RGB")
    sw, sh = shot.size
    # Compute scale to fit within max_w x max_h
    scale = min(max_w / sw, max_h / sh)
    new_w = int(sw * scale)
    new_h = int(sh * scale)
    shot_resized = shot.resize((new_w, new_h), Image.LANCZOS)
    # Center horizontally
    x = (W - new_w) // 2
    img.paste(shot_resized, (x, y_start))
    return new_w, new_h, x

# Dark theme - Ponytail colors (orange/brown - "lazy" vibe)
BG_TOP = (25, 18, 12)
BG_BOTTOM = (8, 5, 3)
ACCENT_ORANGE = (255, 140, 50)
ACCENT_YELLOW = (250, 200, 80)
ACCENT_RED = (240, 90, 70)
ACCENT_GREEN = (100, 200, 130)
ACCENT_BLUE = (100, 150, 240)
ACCENT_PURPLE = (180, 130, 230)
TEXT_WHITE = (245, 240, 230)
TEXT_DIM = (170, 160, 150)

SHOTS = "/home/z/my-project/download/pony_shots"

# Common header/footer drawers
def draw_header_label(draw, text, color):
    label_font = font(34, bold=True)
    bbox = draw.textbbox((0, 0), text, font=label_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 30, 80, (W + tw)//2 + 30, 150], radius=8, outline=color, width=3)
    draw.text(((W - tw)//2, 90), text, font=label_font, fill=color)

def draw_footer_label(draw, text, color):
    foot_font = font(28, bold=True)
    bbox = draw.textbbox((0, 0), text, font=foot_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 20, H - 130, (W + tw)//2 + 20, H - 70], radius=6, outline=color, width=2)
    draw.text(((W - tw)//2, H - 120), text, font=foot_font, fill=color)

def draw_subtitle(draw, lines, y_start=H - 290, color=None):
    if color is None:
        color = TEXT_WHITE
    sub_font = font(40)
    y = y_start
    for line in lines:
        center_text(draw, line, sub_font, y, fill=color)
        y += 55

# === Scene 1: Hook with title screenshot ===
def scene1():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "🔥 73K STARS GITHUB", ACCENT_ORANGE)

    # Title screenshot - balanced size (900x180)
    paste_screenshot_balanced(img, f"{SHOTS}/01_title.png", max_w=1000, max_h=200, y_start=200)

    # Tagline
    y_tag = 440
    title_font = font(72, bold=True)
    lines = ["Ponytail - Plugin", "cho AI Agent", "của bạn"]
    for line in lines:
        center_text(draw, line, title_font, y_tag, fill=TEXT_WHITE if line != "cho AI Agent" else ACCENT_ORANGE)
        y_tag += 90

    # Description card
    y_card = 760
    draw.rounded_rectangle([80, y_card, W - 80, y_card + 400], radius=20, outline=ACCENT_YELLOW, width=3, fill=(35, 25, 18))
    desc_font = font(42)
    desc_lines = [
        '"Makes your AI agent think like',
        'the laziest senior dev in the room"',
        "",
        '"Code tốt nhất là code',
        'không bao giờ phải viết"',
    ]
    yy = y_card + 50
    for line in desc_lines:
        if line.startswith('"'):
            center_text(draw, line, desc_font, yy, fill=ACCENT_YELLOW)
        elif line:
            center_text(draw, line, desc_font, yy, fill=TEXT_WHITE)
        yy += 65

    draw_subtitle(draw, ["Ponytail - plugin bắt AI nghĩ như senior dev lười", "73K+ stars trên GitHub"])
    draw_footer_label(draw, "AI CODING PHILOSOPHY", ACCENT_ORANGE)
    return img

# === Scene 2: Repo overview with stars screenshot ===
def scene2():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "REPO OVERVIEW", ACCENT_BLUE)

    # Big stats
    y = 220
    big_font = font(180, bold=True)
    center_text(draw, "73.4K", big_font, y, fill=ACCENT_YELLOW)
    center_text(draw, "GitHub Stars", font(48, bold=True), y + 210, fill=TEXT_WHITE)

    # Stat row
    y_stat = y + 320
    stat_font = font(56, bold=True)
    desc_font = font(34)
    draw.text((180, y_stat), "3.8K", font=stat_font, fill=ACCENT_BLUE)
    draw.text((180, y_stat + 75), "forks", font=desc_font, fill=TEXT_DIM)
    draw.text((550, y_stat), "JS", font=stat_font, fill=ACCENT_GREEN)
    draw.text((550, y_stat + 75), "language", font=desc_font, fill=TEXT_DIM)
    draw.text((800, y_stat), "MIT", font=stat_font, fill=ACCENT_PURPLE)
    draw.text((800, y_stat + 75), "license", font=desc_font, fill=TEXT_DIM)

    # Stars screenshot (sidebar with description + topics)
    paste_screenshot_balanced(img, f"{SHOTS}/02_stars.png", max_w=550, max_h=550, y_start=720)

    draw_subtitle(draw, ["Repo DietrichGebert/ponytail - JavaScript, MIT", "Mô tả: 'laziest senior dev' mindset"])
    draw_footer_label(draw, "OPEN SOURCE · MIT", ACCENT_BLUE)
    return img

# === Scene 3: Files screenshot ===
def scene3():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "CODE STRUCTURE", ACCENT_GREEN)

    # Files screenshot - balanced width 1000
    paste_screenshot_balanced(img, f"{SHOTS}/03_files.png", max_w=1000, max_h=600, y_start=200)

    # Card below
    y_card = 850
    draw.rounded_rectangle([80, y_card, W - 80, y_card + 380], radius=18, outline=ACCENT_GREEN, width=2, fill=(35, 25, 18))
    cap_font = font(36)
    cap_lines = [
        "Topics chính:",
        "• claude-code, claude-code-plugin",
        "• cursor-rules, prompt-engineering",
        "• agent-skills, ai-agents",
        "• llm, yagni, developer-tools",
    ]
    yy = y_card + 30
    for i, line in enumerate(cap_lines):
        color = ACCENT_GREEN if i == 0 else TEXT_WHITE
        draw.text((110, yy), line, font=cap_font, fill=color)
        yy += 65

    draw_subtitle(draw, ["Repo rất gọn gàng, tập trung vào YAGNI", "Nguyên tắc: You Aren't Gonna Need It"])
    draw_footer_label(draw, "YAGNI · CLEAN CODE", ACCENT_GREEN)
    return img

# === Scene 4: README intro screenshot ===
def scene4():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "README · INTRO", ACCENT_PURPLE)

    # README screenshot - balanced
    paste_screenshot_balanced(img, f"{SHOTS}/04_readme.png", max_w=1000, max_h=900, y_start=200)

    # Description
    y_desc = 1180
    desc_font = font(40)
    draw.rounded_rectangle([60, y_desc, W - 60, y_desc + 200], radius=14, outline=ACCENT_PURPLE, width=2, fill=(35, 25, 18))
    lines = [
        "Plugin cho: Claude Code, Copilot CLI,",
        "Gemini CLI, OpenCode, Cursor",
        "",
        "Triết lý: code tốt nhất = không viết code",
    ]
    yy = y_desc + 20
    for line in lines:
        center_text(draw, line, desc_font, yy, fill=TEXT_WHITE)
        yy += 50

    draw_subtitle(draw, ["Ponytail hỗ trợ nhiều AI agent platforms", "Claude Code, Copilot, Gemini CLI, OpenCode..."])
    draw_footer_label(draw, "MULTI-AGENT SUPPORT", ACCENT_PURPLE)
    return img

# === Scene 5: Install section ===
def scene5():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "INSTALL · QUICK START", ACCENT_YELLOW)

    # Title
    title_font = font(64, bold=True)
    center_text(draw, "Cài đặt đơn giản", title_font, 220, fill=TEXT_WHITE)
    center_text(draw, "cho Claude Code", title_font, 300, fill=ACCENT_YELLOW)

    # Install code card
    y_code = 420
    draw.rounded_rectangle([60, y_code, W - 60, y_code + 500], radius=18, outline=ACCENT_YELLOW, width=3, fill=(20, 20, 25))
    code_font = font(36, bold=True)
    # Step 1
    draw.text((100, y_code + 40), "Step 1:", font=font(32, bold=True), fill=ACCENT_GREEN)
    draw.text((100, y_code + 90), "/plugin marketplace add", font=code_font, fill=TEXT_WHITE)
    draw.text((100, y_code + 140), "DietrichGebert/ponytail", font=code_font, fill=ACCENT_YELLOW)
    # Step 2
    draw.text((100, y_code + 220), "Step 2:", font=font(32, bold=True), fill=ACCENT_GREEN)
    draw.text((100, y_code + 270), "/plugin install", font=code_font, fill=TEXT_WHITE)
    draw.text((100, y_code + 320), "ponytail@ponytail", font=code_font, fill=ACCENT_YELLOW)
    # Step 3 - intensity
    draw.text((100, y_code + 400), "Step 3: Chọn intensity", font=font(32, bold=True), fill=ACCENT_GREEN)
    draw.text((100, y_code + 450), "/ponytail lite | full | ultra", font=code_font, fill=ACCENT_ORANGE)

    # Install screenshot at bottom
    paste_screenshot_balanced(img, f"{SHOTS}/05_install.png", max_w=900, max_h=300, y_start=980)

    draw_subtitle(draw, ["Cài chỉ 2 lệnh, chọn 1 trong 3 intensity", "lite, full (default), hoặc ultra"])
    draw_footer_label(draw, "EASY INSTALL · 2 COMMANDS", ACCENT_YELLOW)
    return img

# === Scene 6: Takeaway ===
def scene6():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "TAKEAWAY", ACCENT_RED)

    # Title
    title_font = font(76, bold=True)
    lines = ["The Ladder", "Ranked Checklist"]
    y = 230
    for i, line in enumerate(lines):
        color = ACCENT_RED if i == 0 else TEXT_WHITE
        center_text(draw, line, title_font, y, fill=color)
        y += 95

    # The Ladder steps
    y_ladder = 460
    draw.rounded_rectangle([80, y_ladder, W - 80, y_ladder + 600], radius=18, outline=ACCENT_RED, width=3, fill=(35, 25, 18))
    ladder_font = font(36)
    ladder_steps = [
        ("1.", "Task có thực sự cần không?", ACCENT_RED),
        ("2.", "Có thể dùng code có sẵn?", ACCENT_ORANGE),
        ("3.", "Có trong thư viện chuẩn?", ACCENT_YELLOW),
        ("4.", "Có native platform feature?", ACCENT_GREEN),
        ("5.", "Có dependency đã install?", ACCENT_BLUE),
        ("6.", "Cuối cùng: viết code mới", ACCENT_PURPLE),
    ]
    yy = y_ladder + 40
    for num, text, color in ladder_steps:
        draw.text((110, yy), num, font=font(38, bold=True), fill=color)
        draw.text((180, yy), text, font=ladder_font, fill=TEXT_WHITE)
        yy += 85

    # Hash card
    y_hash = 1130
    draw.rounded_rectangle([80, y_hash, W - 80, y_hash + 280], radius=18, outline=ACCENT_BLUE, width=3, fill=(20, 20, 30))
    hash_font = font(44, bold=True)
    center_text(draw, "github.com/DietrichGebert/ponytail", hash_font, y_hash + 30, fill=ACCENT_BLUE)
    center_text(draw, "#Ponytail #AIAgent #ClaudeCode", hash_font, y_hash + 110, fill=ACCENT_GREEN)
    center_text(draw, "#YAGNI #SeniorDev #PromptEng", hash_font, y_hash + 180, fill=ACCENT_YELLOW)

    draw_subtitle(draw, ["Agent phải check The Ladder trước khi code", "Follow kênh để cập nhật AI tools!"])
    draw_footer_label(draw, "FOLLOW FOR MORE", ACCENT_RED)
    return img

# Render all
for i, fn in enumerate([scene1, scene2, scene3, scene4, scene5, scene6], 1):
    img = fn()
    out = os.path.join(OUT_DIR, f"s{i}.png")
    img.save(out, "PNG")
    print(f"  s{i}.png saved")

print(f"\nAll 6 frames in: {OUT_DIR}")
