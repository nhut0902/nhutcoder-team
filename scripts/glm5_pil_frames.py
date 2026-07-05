#!/home/z/.venv/bin/python3
"""Render 8 frames for GLM-5 video with PIL. GUARANTEED text + screenshot + Vietnamese subtitle visible.
Style: dark gradient + accent colors + screenshot embedded + Vietnamese subtitle at bottom."""
import os, json
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/z/my-project/download/glm5_frames"
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

def paste_screenshot(img, shot_path, max_w, max_h, y_start):
    shot = Image.open(shot_path).convert("RGB")
    sw, sh = shot.size
    scale = min(max_w / sw, max_h / sh)
    new_w = int(sw * scale)
    new_h = int(sh * scale)
    shot_resized = shot.resize((new_w, new_h), Image.LANCZOS)
    x = (W - new_w) // 2
    # Border
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x-6, y_start-6, x+new_w+6, y_start+new_h+6], radius=14, fill=(20, 30, 60), outline=(66, 133, 244), width=4)
    img.paste(shot_resized, (x, y_start))
    return new_w, new_h

# Colors - Z.ai brand blue/purple
BG_TOP = (10, 14, 26)
BG_BOTTOM = (5, 8, 18)
ACCENT_BLUE = (66, 133, 244)
ACCENT_PURPLE = (155, 110, 220)
ACCENT_YELLOW = (250, 200, 80)
ACCENT_GREEN = (80, 200, 120)
ACCENT_ORANGE = (255, 140, 50)
ACCENT_RED = (240, 90, 70)
TEXT_WHITE = (245, 245, 250)
TEXT_DIM = (160, 160, 180)

SHOTS = "/home/z/my-project/download/glm5_shots"

def draw_header_label(draw, text, color):
    f = font(34, bold=True)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 30, 80, (W + tw)//2 + 30, 150], radius=8, outline=color, width=3)
    draw.text(((W - tw)//2, 90), text, font=f, fill=color)

def draw_footer_label(draw, text, color):
    f = font(28, bold=True)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 20, H - 130, (W + tw)//2 + 20, H - 70], radius=6, outline=color, width=2)
    draw.text(((W - tw)//2, H - 120), text, font=f, fill=color)

def draw_subtitle(draw, lines, y_start=H - 290):
    sub_font = font(38)
    y = y_start
    for line in lines:
        center_text(draw, line, sub_font, y, fill=TEXT_WHITE)
        y += 55

# === Scene 1: Hook ===
def scene1():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "🔥 OPEN SOURCE 5/7/2026", ACCENT_ORANGE)

    # Title
    title_font = font(160, bold=True)
    center_text(draw, "GLM-5", title_font, 240, fill=ACCENT_BLUE)
    
    sub_font = font(56, bold=True)
    center_text(draw, "From Vibe Coding", sub_font, 460, fill=TEXT_WHITE)
    center_text(draw, "to Agentic Engineering", sub_font, 540, fill=ACCENT_PURPLE)
    
    # By Z.ai
    by_font = font(44)
    center_text(draw, "by Z.ai", by_font, 660, fill=TEXT_DIM)

    # Stats card
    y = 780
    draw.rounded_rectangle([80, y, W - 80, y + 400], radius=20, outline=ACCENT_BLUE, width=3, fill=(20, 25, 40))
    big_font = font(140, bold=True)
    center_text(draw, "744B", big_font, y + 40, fill=ACCENT_YELLOW)
    center_text(draw, "params (40B active MoE)", font(40, bold=True), y + 200, fill=TEXT_WHITE)
    # Sub-stats
    stat_font = font(50, bold=True)
    desc_font = font(30)
    draw.text((150, y + 280), "6K+", font=stat_font, fill=ACCENT_GREEN)
    draw.text((150, y + 340), "GitHub stars", font=desc_font, fill=TEXT_DIM)
    draw.text((440, y + 280), "200K", font=stat_font, fill=ACCENT_PURPLE)
    draw.text((440, y + 340), "context window", font=desc_font, fill=TEXT_DIM)
    draw.text((780, y + 280), "28.5T", font=stat_font, fill=ACCENT_ORANGE)
    draw.text((780, y + 340), "tokens", font=desc_font, fill=TEXT_DIM)

    draw_subtitle(draw, ["GLM-5 - mô hình open-source mới nhất của Z.ai", "744B params, mở nguồn ngày 5/7/2026"])
    draw_footer_label(draw, "OPEN SOURCE · MoE", ACCENT_BLUE)
    return img

# === Scene 2: Repo screenshot ===
def scene2():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "GITHUB REPO", ACCENT_BLUE)

    # Title
    title_font = font(60, bold=True)
    center_text(draw, "zai-org/GLM-5", title_font, 220, fill=ACCENT_BLUE)
    center_text(draw, "6,196 stars · 737 forks", font(40), 300, fill=TEXT_WHITE)

    # Screenshot
    paste_screenshot(img, f"{SHOTS}/01_title.png", max_w=1000, max_h=350, y_start=400)

    # About card
    y = 850
    draw.rounded_rectangle([80, y, W - 80, y + 380], radius=18, outline=ACCENT_PURPLE, width=2, fill=(25, 20, 40))
    cap_font = font(38)
    cap_lines = [
        "Topics:",
        "• agentic-ai · coding",
        "• llm · long-horizon",
        "",
        "Created: 9/2/2026",
        "Open source: 5/7/2026",
    ]
    yy = y + 30
    for i, line in enumerate(cap_lines):
        color = ACCENT_PURPLE if i == 0 else TEXT_WHITE
        draw.text((110, yy), line, font=cap_font, fill=color)
        yy += 55

    draw_subtitle(draw, ["Repo chính thức: github.com/zai-org/GLM-5", "Tagline: From Vibe Coding to Agentic Engineering"])
    draw_footer_label(draw, "Z.AI · OPEN SOURCE", ACCENT_BLUE)
    return img

# === Scene 3: Specs ===
def scene3():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "THÔNG SỐ KỸ THUẬT", ACCENT_YELLOW)

    title_font = font(72, bold=True)
    center_text(draw, "Specs", title_font, 220, fill=TEXT_WHITE)

    features = [
        ("📊", "744B params", "(40B active MoE)", ACCENT_YELLOW),
        ("📚", "28.5T tokens", "pre-training data", ACCENT_BLUE),
        ("🎯", "200K context", "long-context window", ACCENT_PURPLE),
        ("⚡", "DeepSeek SA", "Sparse Attention", ACCENT_GREEN),
        ("🔄", "Slime infra", "async RL", ACCENT_ORANGE),
    ]
    icon_font = font(60)
    title_card_font = font(50, bold=True)
    desc_font = font(34)
    y = 360
    for icon, title, desc, color in features:
        draw.rounded_rectangle([80, y, W - 80, y + 150], radius=14, outline=color, width=2, fill=(25, 20, 40))
        draw.text((110, y + 30), icon, font=icon_font, fill=TEXT_WHITE)
        draw.text((210, y + 25), title, font=title_card_font, fill=color)
        draw.text((210, y + 90), desc, font=desc_font, fill=TEXT_DIM)
        y += 170

    draw_subtitle(draw, ["744B tham số, 40B active MoE", "200K context, DeepSeek Sparse Attention"])
    draw_footer_label(draw, "MoE · LONG CONTEXT", ACCENT_YELLOW)
    return img

# === Scene 4: Code structure screenshot ===
def scene4():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "CODE STRUCTURE", ACCENT_GREEN)

    title_font = font(60, bold=True)
    center_text(draw, "Repo structure", title_font, 220, fill=ACCENT_GREEN)

    # Screenshot
    paste_screenshot(img, f"{SHOTS}/03_files.png", max_w=1000, max_h=600, y_start=320)

    # Tech card
    y = 980
    draw.rounded_rectangle([80, y, W - 80, y + 280], radius=14, outline=ACCENT_GREEN, width=2, fill=(25, 30, 25))
    cap_font = font(34)
    cap_lines = [
        "Architecture:",
        "• DeepSeek Sparse Attention (DSA)",
        "• Slime infrastructure (async RL)",
        "• MoE: 40B active / 744B total",
    ]
    yy = y + 20
    for i, line in enumerate(cap_lines):
        color = ACCENT_GREEN if i == 0 else TEXT_WHITE
        draw.text((110, yy), line, font=cap_font, fill=color)
        yy += 55

    draw_subtitle(draw, ["Tích hợp DeepSeek Sparse Attention", "Slime infrastructure cho async RL"])
    draw_footer_label(draw, "MoE · DSA · SLIME", ACCENT_GREEN)
    return img

# === Scene 5: Benchmark ===
def scene5():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "BENCHMARK", ACCENT_RED)

    title_font = font(70, bold=True)
    center_text(draw, "SOTA Performance", title_font, 220, fill=TEXT_WHITE)

    # Big #1 card
    y = 360
    draw.rounded_rectangle([100, y, W - 100, y + 480], radius=24, outline=ACCENT_YELLOW, width=4, fill=(30, 25, 15))
    label_font = font(36, bold=True)
    center_text(draw, "VENDING BENCH 2", label_font, y + 50, fill=ACCENT_YELLOW)
    big_font = font(220, bold=True)
    center_text(draw, "#1", big_font, y + 100, fill=ACCENT_YELLOW)
    center_text(draw, "$4,432 balance", font(48, bold=True), y + 350, fill=TEXT_WHITE)
    center_text(draw, "Xếp hạng nhất trong open-source", font(32), y + 410, fill=TEXT_DIM)

    # Other benchmarks
    y2 = y + 540
    bench_font = font(38, bold=True)
    center_text(draw, "SOTA open-source cho:", bench_font, y2, fill=ACCENT_GREEN)
    center_text(draw, "✓ Reasoning  ✓ Coding  ✓ Agentic", font(36), y2 + 60, fill=TEXT_WHITE)

    draw_subtitle(draw, ["#1 Vending Bench 2 với $4,432 balance", "SOTA open-source cho reasoning + coding"])
    draw_footer_label(draw, "STATE OF THE ART", ACCENT_RED)
    return img

# === Scene 6: Thinking Budget ===
def scene6():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "THINKING BUDGET", ACCENT_PURPLE)

    title_font = font(70, bold=True)
    center_text(draw, "reasoning_effort", title_font, 220, fill=ACCENT_PURPLE)

    # Code block
    y = 360
    draw.rounded_rectangle([80, y, W - 80, y + 350], radius=14, outline=ACCENT_PURPLE, width=3, fill=(20, 18, 30))
    code_font = font(36, bold=True)
    draw.text((110, y + 30), "param:", font=font(32, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 75), "reasoning_effort", font=code_font, fill=ACCENT_PURPLE)
    draw.text((110, y + 130), "default: max", font=code_font, fill=ACCENT_YELLOW)
    draw.text((110, y + 200), "options:", font=font(32, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 245), "low · medium · high · max", font=code_font, fill=TEXT_WHITE)
    draw.text((110, y + 300), "trade-off: quality vs speed", font=font(30), fill=TEXT_DIM)

    # Explanation card
    y2 = y + 400
    draw.rounded_rectangle([80, y2, W - 80, y2 + 220], radius=14, outline=ACCENT_BLUE, width=2, fill=(20, 25, 40))
    cap_font = font(36)
    cap_lines = [
        "✓ max: chất lượng cao nhất",
        "✓ low: nhanh hơn, tiết kiệm token",
        "✓ Tuỳ chọn theo use case",
    ]
    yy = y2 + 20
    for line in cap_lines:
        draw.text((110, yy), line, font=cap_font, fill=TEXT_WHITE)
        yy += 60

    draw_subtitle(draw, ["reasoning_effort param kiểm soát thinking budget", "default: max - chất lượng cao nhất"])
    draw_footer_label(draw, "CONTROLLABLE REASONING", ACCENT_PURPLE)
    return img

# === Scene 7: Use Cases ===
def scene7():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "USE CASES", ACCENT_BLUE)

    title_font = font(70, bold=True)
    center_text(draw, "Ứng dụng", title_font, 220, fill=TEXT_WHITE)

    features = [
        ("🔧", "Complex systems engineering", ACCENT_BLUE),
        ("📋", "Long-horizon agentic tasks", ACCENT_PURPLE),
        ("💻", "Coding & reasoning", ACCENT_GREEN),
        ("🎯", "Multi-step orchestration", ACCENT_ORANGE),
        ("🚀", "Production AI agents", ACCENT_YELLOW),
    ]
    icon_font = font(64)
    title_card_font = font(42, bold=True)
    y = 360
    for icon, text, color in features:
        draw.rounded_rectangle([80, y, W - 80, y + 140], radius=14, outline=color, width=2, fill=(25, 20, 40))
        draw.text((110, y + 30), icon, font=icon_font, fill=TEXT_WHITE)
        draw.text((220, y + 40), text, font=title_card_font, fill=color)
        y += 160

    draw_subtitle(draw, ["Phù hợp cho complex systems engineering", "Long-horizon agentic tasks, coding, reasoning"])
    draw_footer_label(draw, "AGENTIC ENGINEERING", ACCENT_BLUE)
    return img

# === Scene 8: Takeaway ===
def scene8():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header_label(draw, "TAKEAWAY", ACCENT_GREEN)

    title_font = font(80, bold=True)
    lines = ["Bước tiến", "quan trọng", "của Z.ai"]
    y = 250
    for i, line in enumerate(lines):
        color = ACCENT_GREEN if i == 1 else TEXT_WHITE
        center_text(draw, line, title_font, y, fill=color)
        y += 100

    sub_font = font(40)
    center_text(draw, "trong cuộc đua open-source AI", sub_font, y + 20, fill=TEXT_DIM)

    # Hash card
    y_hash = y + 130
    draw.rounded_rectangle([80, y_hash, W - 80, y_hash + 280], radius=18, outline=ACCENT_BLUE, width=3, fill=(20, 20, 30))
    hash_font = font(46, bold=True)
    center_text(draw, "github.com/zai-org/GLM-5", hash_font, y_hash + 40, fill=ACCENT_BLUE)
    center_text(draw, "#GLM5 #Zai #OpenSource", hash_font, y_hash + 120, fill=ACCENT_GREEN)
    center_text(draw, "#AI2026 #AgenticAI", hash_font, y_hash + 190, fill=ACCENT_YELLOW)

    draw_subtitle(draw, ["GLM-5 - SOTA open-source cho agentic tasks", "Follow kênh để cập nhật AI mới nhất!"])
    draw_footer_label(draw, "FOLLOW FOR MORE", ACCENT_GREEN)
    return img

# Render all
for i, fn in enumerate([scene1, scene2, scene3, scene4, scene5, scene6, scene7, scene8], 1):
    img = fn()
    out = os.path.join(OUT_DIR, f"s{i}.png")
    img.save(out, "PNG")
    print(f"  s{i}.png saved")

print(f"\nAll 8 frames in: {OUT_DIR}")
