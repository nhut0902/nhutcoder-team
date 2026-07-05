#!/home/z/.venv/bin/python3
"""Render 6 frames for Strix video. Each frame includes a screenshot + Vietnamese subtitle at bottom.
Frames designed for vertical 1080x1920 (TikTok)."""
import os, json
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/z/my-project/download/strix_frames"
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

# Dark theme - strix/security vibe (black/red/orange)
BG_TOP = (15, 5, 5)
BG_BOTTOM = (5, 5, 5)
ACCENT_RED = (240, 70, 70)
ACCENT_ORANGE = (255, 140, 50)
ACCENT_YELLOW = (250, 200, 80)
ACCENT_GREEN = (80, 200, 120)
ACCENT_BLUE = (66, 133, 244)
TEXT_WHITE = (240, 240, 240)
TEXT_DIM = (160, 160, 170)

# Load screenshots
SHOTS_DIR = "/home/z/my-project/download/strix_shots"

# === Scene 1: Hook - Title screenshot ===
def scene1():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    # Top label
    label_font = font(34, bold=True)
    bbox = draw.textbbox((0, 0), "TRENDING #1 GITHUB 3/7/2026", font=label_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 30, 90, (W + tw)//2 + 30, 160], radius=8, outline=ACCENT_RED, width=3)
    draw.text(((W - tw)//2, 100), "TRENDING #1 GITHUB 3/7/2026", font=label_font, fill=ACCENT_RED)

    # Embed title screenshot (top portion)
    shot = Image.open(f"{SHOTS_DIR}/01_title.png").convert("RGB")
    # Resize to fit width 1000 (keep aspect)
    target_w = 1000
    aspect = shot.height / shot.width
    new_h = int(target_w * aspect)
    shot_resized = shot.resize((target_w, new_h), Image.LANCZOS)
    # Place screenshot in upper area
    img.paste(shot_resized, ((W - target_w)//2, 200))

    # Stat row
    stat_y = 200 + new_h + 50
    stat_font = font(72, bold=True)
    sub_font = font(34)
    # +2,137 stars today
    draw.text((140, stat_y), "+2,137", font=stat_font, fill=ACCENT_GREEN)
    draw.text((140, stat_y + 80), "stars trong 24h", font=sub_font, fill=TEXT_DIM)
    # 35.4k total
    draw.text((550, stat_y), "35.4K", font=stat_font, fill=ACCENT_YELLOW)
    draw.text((550, stat_y + 80), "total stars", font=sub_font, fill=TEXT_DIM)
    # Python
    draw.text((900, stat_y), "Python", font=stat_font, fill=ACCENT_BLUE)
    draw.text((900, stat_y + 80), "language", font=sub_font, fill=TEXT_DIM)

    # Subtitle (Vietnamese caption at bottom)
    sub_y = H - 280
    sub_font = font(40)
    sub_lines = ["Hôm nay 3/7/2026, Strix lên top trending GitHub", "tăng 2,137 sao chỉ trong 24 giờ!"]
    for line in sub_lines:
        center_text(draw, line, sub_font, sub_y, fill=TEXT_WHITE)
        sub_y += 55

    # Footer label
    foot_font = font(28, bold=True)
    bbox = draw.textbbox((0, 0), "AI PENTESTING TOOL", font=foot_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 20, H - 130, (W + tw)//2 + 20, H - 70], radius=6, outline=ACCENT_RED, width=2)
    draw.text(((W - tw)//2, H - 120), "AI PENTESTING TOOL", font=foot_font, fill=ACCENT_RED)

    return img

# === Scene 2: Repo Overview - Stars section ===
def scene2():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    label_font = font(34, bold=True)
    bbox = draw.textbbox((0, 0), "REPO OVERVIEW", font=label_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 30, 90, (W + tw)//2 + 30, 160], radius=8, outline=ACCENT_BLUE, width=3)
    draw.text(((W - tw)//2, 100), "REPO OVERVIEW", font=label_font, fill=ACCENT_BLUE)

    # Big stats card
    stat_y = 250
    draw.rounded_rectangle([80, stat_y, W - 80, stat_y + 400], radius=20, outline=ACCENT_YELLOW, width=3, fill=(25, 20, 30))

    big_font = font(180, bold=True)
    center_text(draw, "35.4K", big_font, stat_y + 50, fill=ACCENT_YELLOW)
    center_text(draw, "GitHub Stars", font(48, bold=True), stat_y + 260, fill=TEXT_WHITE)

    # Other stats
    sub_stat_font = font(56, bold=True)
    desc_font = font(34)
    draw.text((180, stat_y + 340), "3.6K", font=sub_stat_font, fill=ACCENT_BLUE)
    draw.text((180, stat_y + 410), "forks", font=desc_font, fill=TEXT_DIM)
    draw.text((550, stat_y + 340), "Python", font=sub_stat_font, fill=ACCENT_GREEN)
    draw.text((550, stat_y + 410), "language", font=desc_font, fill=TEXT_DIM)
    draw.text((820, stat_y + 340), "MIT", font=sub_stat_font, fill=ACCENT_ORANGE)
    draw.text((820, stat_y + 410), "license", font=desc_font, fill=TEXT_DIM)

    # Subtitle
    sub_y = H - 280
    sub_font = font(40)
    sub_lines = ["Repo usestrix/strix - công cụ pentest bằng AI", "Viết bằng Python, 35.4K sao, 3.6K fork"]
    for line in sub_lines:
        center_text(draw, line, sub_font, sub_y, fill=TEXT_WHITE)
        sub_y += 55

    # Footer
    foot_font = font(28, bold=True)
    bbox = draw.textbbox((0, 0), "OPEN SOURCE · MIT", font=foot_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 20, H - 130, (W + tw)//2 + 20, H - 70], radius=6, outline=ACCENT_BLUE, width=2)
    draw.text(((W - tw)//2, H - 120), "OPEN SOURCE · MIT", font=foot_font, fill=ACCENT_BLUE)

    return img

# === Scene 3: Files section screenshot ===
def scene3():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    label_font = font(34, bold=True)
    bbox = draw.textbbox((0, 0), "CODE STRUCTURE", font=label_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 30, 90, (W + tw)//2 + 30, 160], radius=8, outline=ACCENT_GREEN, width=3)
    draw.text(((W - tw)//2, 100), "CODE STRUCTURE", font=label_font, fill=ACCENT_GREEN)

    # Embed files screenshot
    shot = Image.open(f"{SHOTS_DIR}/03_files.png").convert("RGB")
    target_w = 1000
    aspect = shot.height / shot.width
    new_h = int(target_w * aspect)
    shot_resized = shot.resize((target_w, new_h), Image.LANCZOS)
    img.paste(shot_resized, ((W - target_w)//2, 220))

    # Caption box (right below screenshot)
    cap_y = 220 + new_h + 30
    draw.rounded_rectangle([60, cap_y, W - 60, cap_y + 200], radius=14, outline=ACCENT_GREEN, width=2, fill=(25, 20, 30))
    cap_font = font(34)
    cap_lines = [
        "Mới cập nhật: Migration sang uv",
        "SARIF emitter cho CI integration",
        "Bump lên phiên bản 1.0.0",
    ]
    yy = cap_y + 20
    for line in cap_lines:
        draw.text((100, yy), "• " + line, font=cap_font, fill=ACCENT_GREEN)
        yy += 50

    # Subtitle
    sub_y = H - 280
    sub_font = font(40)
    sub_lines = ["Cấu trúc repo chuyên nghiệp, mới bump 1.0.0", "Migration sang uv, tích hợp SARIF cho CI"]
    for line in sub_lines:
        center_text(draw, line, sub_font, sub_y, fill=TEXT_WHITE)
        sub_y += 55

    # Footer
    foot_font = font(28, bold=True)
    bbox = draw.textbbox((0, 0), "ACTIVE MAINTENANCE", font=foot_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 20, H - 130, (W + tw)//2 + 20, H - 70], radius=6, outline=ACCENT_GREEN, width=2)
    draw.text(((W - tw)//2, H - 120), "ACTIVE MAINTENANCE", font=foot_font, fill=ACCENT_GREEN)

    return img

# === Scene 4: README screenshot ===
def scene4():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    label_font = font(34, bold=True)
    bbox = draw.textbbox((0, 0), "README · WHAT IS STRIX?", font=label_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 30, 90, (W + tw)//2 + 30, 160], radius=8, outline=ACCENT_ORANGE, width=3)
    draw.text(((W - tw)//2, 100), "README · WHAT IS STRIX?", font=label_font, fill=ACCENT_ORANGE)

    # Embed readme screenshot
    shot = Image.open(f"{SHOTS_DIR}/04_readme.png").convert("RGB")
    target_w = 1000
    aspect = shot.height / shot.width
    new_h = int(target_w * aspect)
    shot_resized = shot.resize((target_w, new_h), Image.LANCZOS)
    img.paste(shot_resized, ((W - target_w)//2, 200))

    # Subtitle
    sub_y = 200 + new_h + 50
    sub_font = font(40)
    sub_lines = ["Strix = công cụ pentest AI mã nguồn mở", "Autonomous AI hackers tự tìm + sửa lỗ hổng"]
    for line in sub_lines:
        center_text(draw, line, sub_font, sub_y, fill=TEXT_WHITE)
        sub_y += 55

    # Footer
    foot_font = font(28, bold=True)
    bbox = draw.textbbox((0, 0), "AI HACKERS · AUTONOMOUS", font=foot_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 20, H - 130, (W + tw)//2 + 20, H - 70], radius=6, outline=ACCENT_ORANGE, width=2)
    draw.text(((W - tw)//2, H - 120), "AI HACKERS · AUTONOMOUS", font=foot_font, fill=ACCENT_ORANGE)

    return img

# === Scene 5: Features (text-only card) ===
def scene5():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    label_font = font(34, bold=True)
    bbox = draw.textbbox((0, 0), "KEY FEATURES", font=label_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 30, 90, (W + tw)//2 + 30, 160], radius=8, outline=ACCENT_YELLOW, width=3)
    draw.text(((W - tw)//2, 100), "KEY FEATURES", font=label_font, fill=ACCENT_YELLOW)

    title_font = font(70, bold=True)
    center_text(draw, "Tính năng nổi bật", title_font, 220, fill=TEXT_WHITE)

    features = [
        ("🌐", "HTTP Interception Proxy", ACCENT_BLUE),
        ("🖱️", "Browser Exploitation (XSS/CSRF)", ACCENT_PURPLE := (155, 110, 220)),
        ("⌨️", "Terminal / Command Execution", ACCENT_GREEN),
        ("🐍", "Custom Python Exploit Runtime", ACCENT_YELLOW),
        ("🔍", "Recon / OSINT", ACCENT_ORANGE),
        ("📋", "Static + Dynamic Code Analysis", ACCENT_RED),
        ("🤖", "Vulnerability Knowledge Base", ACCENT_BLUE),
        ("🔄", "GitHub Actions CI Integration", ACCENT_GREEN),
    ]
    icon_font = font(56)
    title_card_font = font(42, bold=True)
    y = 360
    for icon, text, color in features:
        draw.rounded_rectangle([60, y, W - 60, y + 130], radius=14, outline=color, width=2, fill=(25, 20, 30))
        draw.text((100, y + 30), icon, font=icon_font, fill=TEXT_WHITE)
        draw.text((200, y + 35), text, font=title_card_font, fill=color)
        y += 145

    # Subtitle
    sub_y = H - 280
    sub_font = font(38)
    sub_lines = ["HTTP proxy, browser exploitation, terminal execution", "Python exploit runtime, CI/CD integration"]
    for line in sub_lines:
        center_text(draw, line, sub_font, sub_y, fill=TEXT_WHITE)
        sub_y += 55

    # Footer
    foot_font = font(28, bold=True)
    bbox = draw.textbbox((0, 0), "FULL PENTEST STACK", font=foot_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 20, H - 130, (W + tw)//2 + 20, H - 70], radius=6, outline=ACCENT_YELLOW, width=2)
    draw.text(((W - tw)//2, H - 120), "FULL PENTEST STACK", font=foot_font, fill=ACCENT_YELLOW)

    return img

# === Scene 6: Takeaway ===
def scene6():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    label_font = font(34, bold=True)
    bbox = draw.textbbox((0, 0), "TAKEAWAY", font=label_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 30, 90, (W + tw)//2 + 30, 160], radius=8, outline=ACCENT_GREEN, width=3)
    draw.text(((W - tw)//2, 100), "TAKEAWAY", font=label_font, fill=ACCENT_GREEN)

    title_font = font(76, bold=True)
    lines = ["Công cụ tuyệt vời", "cho bug bounty", "và CTF!"]
    y = 250
    for i, line in enumerate(lines):
        color = ACCENT_GREEN if i == 0 else TEXT_WHITE
        center_text(draw, line, title_font, y, fill=color)
        y += 95

    # Hash card
    y_hash = y + 80
    draw.rounded_rectangle([80, y_hash, W - 80, y_hash + 300], radius=20, outline=ACCENT_BLUE, width=3, fill=(25, 20, 30))
    hash_font = font(48, bold=True)
    center_text(draw, "github.com/usestrix/strix", hash_font, y_hash + 40, fill=ACCENT_BLUE)
    center_text(draw, "#Strix #AIPentest #CyberSecurity", hash_font, y_hash + 130, fill=ACCENT_GREEN)
    center_text(draw, "#BugBounty #CTF #Python", hash_font, y_hash + 200, fill=ACCENT_YELLOW)

    # Subtitle
    sub_y = H - 250
    sub_font = font(38)
    sub_lines = ["Tích hợp GitHub Actions, quét mỗi PR", "Follow kênh để cập nhật AI mới nhất!"]
    for line in sub_lines:
        center_text(draw, line, sub_font, sub_y, fill=TEXT_WHITE)
        sub_y += 55

    # Footer
    foot_font = font(28, bold=True)
    bbox = draw.textbbox((0, 0), "FOLLOW FOR MORE", font=foot_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 20, H - 130, (W + tw)//2 + 20, H - 70], radius=6, outline=ACCENT_GREEN, width=2)
    draw.text(((W - tw)//2, H - 120), "FOLLOW FOR MORE", font=foot_font, fill=ACCENT_GREEN)

    return img

# Render all
SCENES_FUNCS = [scene1, scene2, scene3, scene4, scene5, scene6]
for i, fn in enumerate(SCENES_FUNCS, 1):
    img = fn()
    out = os.path.join(OUT_DIR, f"s{i}.png")
    img.save(out, "PNG")
    print(f"  s{i}.png saved ({img.size})")

print(f"\nAll {len(SCENES_FUNCS)} frames in: {OUT_DIR}")
