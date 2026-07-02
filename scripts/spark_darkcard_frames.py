"""Render 8 dark card-style frames for Gemini Spark video, mimicking reference style.
Key features from reference:
- Dark gradient background (brown/black)
- Header labels in bordered boxes: "HOOK", "WHAT IS IT", "FEATURES", etc.
- Card-based content with thin borders
- Footer labels in caps: "24/7 AI AGENT", "GOOGLE AI ULTRA", etc.
- Accent colors for highlights
- Large stat numbers
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/z/my-project/download/spark_darkcard_frames"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1080, 1920

FONT_PATHS_REGULAR = ["/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf"]
FONT_PATHS_BOLD = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
FONT_REG = next(p for p in FONT_PATHS_REGULAR if os.path.exists(p))
FONT_BOLD = next(p for p in FONT_PATHS_BOLD if os.path.exists(p))
print(f"Fonts: regular={FONT_REG}, bold={FONT_BOLD}")

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
    return x, text_w  # return for further drawing

def draw_box(draw, x1, y1, x2, y2, outline=(80, 80, 80), width=2, fill=None, radius=8):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=outline, width=width, fill=fill)

def draw_text_box(draw, text, fnt, cx, cy, pad_x=20, pad_y=10, outline=(100, 100, 100), fill_bg=None, text_fill=(220, 220, 220), width=2):
    """Draw text centered at (cx, cy) inside a bordered box"""
    bbox = draw.textbbox((0, 0), text, font=fnt)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x1 = cx - text_w // 2 - pad_x
    y1 = cy - text_h // 2 - pad_y
    x2 = cx + text_w // 2 + pad_x
    y2 = cy + text_h // 2 + pad_y
    draw_box(draw, x1, y1, x2, y2, outline=outline, width=width, fill=fill_bg, radius=6)
    draw.text((cx - text_w // 2, cy - text_h // 2 - bbox[1] // 2), text, font=fnt, fill=text_fill)
    return x1, y1, x2, y2

def draw_card(draw, x1, y1, x2, y2, outline=(60, 60, 60), fill=(25, 25, 30), radius=14, width=2):
    """Draw a content card with subtle background"""
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=outline, width=width, fill=fill)

# Common colors (dark theme)
BG_TOP = (20, 16, 22)         # dark brown-purple
BG_BOTTOM = (8, 6, 12)        # near black
ACCENT_BLUE = (66, 133, 244)
ACCENT_GREEN = (80, 200, 120)
ACCENT_YELLOW = (250, 200, 80)
ACCENT_ORANGE = (255, 140, 60)
ACCENT_RED = (240, 90, 90)
ACCENT_PURPLE = (155, 110, 220)
TEXT_WHITE = (240, 240, 240)
TEXT_DIM = (160, 160, 170)
TEXT_LABEL = (200, 200, 200)
CARD_BG = (28, 24, 32)
CARD_OUTLINE = (75, 65, 80)

# Load Gemini Spark image
SPARK_IMG_PATH = "/home/z/my-project/download/gemini_spark/gemini_spark_pcmag.png"
spark_img_orig = Image.open(SPARK_IMG_PATH).convert("RGBA")
target_w = 720
aspect = spark_img_orig.height / spark_img_orig.width
spark_img = spark_img_orig.resize((target_w, int(target_w * aspect)), Image.LANCZOS)
print(f"Spark image: {spark_img.size}")

# === Scene 1: HOOK / SHOCK ===
def scene1():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    # Top label box: "HOOK / SHOCK"
    label_font = font(34, bold=True)
    draw_text_box(draw, "HOOK / SHOCK", label_font, W // 2, 130, pad_x=30, pad_y=12, outline=ACCENT_RED, text_fill=ACCENT_RED)

    # Main title - large, white, multi-line
    title_font = font(78, bold=True)
    title_lines = ["Google vừa ra mắt", "AI Agent 24/7", "mà thiết bị tắt", "vẫn chạy được"]
    y = 230
    for i, line in enumerate(title_lines):
        color = ACCENT_YELLOW if i == 1 else TEXT_WHITE
        center_text(draw, line, title_font, y, fill=color)
        y += 95

    # Dashboard card with key stats
    y_card = 720
    draw_card(draw, 100, y_card, W - 100, y_card + 440, outline=ACCENT_BLUE, width=3)
    # Top of card - label
    draw_text_box(draw, "GEMINI SPARK", font(36, bold=True), W // 2, y_card + 50, pad_x=24, pad_y=10, outline=ACCENT_BLUE, text_fill=ACCENT_BLUE)
    # Big stat - $99.99
    big_font = font(180, bold=True)
    center_text(draw, "$99.99", big_font, y_card + 100, fill=ACCENT_YELLOW)
    # Per month
    center_text(draw, "/tháng · Google AI Ultra", font(40), y_card + 290, fill=TEXT_WHITE)
    # Stats row
    stat_font = font(50, bold=True)
    sub_font = font(28)
    draw.text((170, y_card + 360), "24/7", font=stat_font, fill=ACCENT_GREEN)
    draw.text((170, y_card + 410), "Cloud Agent", font=sub_font, fill=TEXT_DIM)
    draw.text((440, y_card + 360), "1M", font=stat_font, fill=ACCENT_PURPLE)
    draw.text((440, y_card + 410), "Token context", font=sub_font, fill=TEXT_DIM)
    draw.text((720, y_card + 360), "macOS", font=stat_font, fill=ACCENT_BLUE)
    draw.text((720, y_card + 410), "Beta 2/7/26", font=sub_font, fill=TEXT_DIM)

    # Footer label
    draw_text_box(draw, "24/7 AI AGENT", font(30, bold=True), W // 2, H - 90, pad_x=20, pad_y=10, outline=ACCENT_BLUE, text_fill=ACCENT_BLUE)
    return img

# === Scene 2: WHAT IS IT ===
def scene2():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    draw_text_box(draw, "WHAT IS IT", font(34, bold=True), W // 2, 130, pad_x=30, pad_y=12, outline=ACCENT_PURPLE, text_fill=ACCENT_PURPLE)

    title_font = font(72, bold=True)
    center_text(draw, "Gemini Spark là gì?", title_font, 220, fill=TEXT_WHITE)

    # Card with description
    y = 360
    draw_card(draw, 80, y, W - 80, y + 580, outline=CARD_OUTLINE, width=2)
    desc_font = font(46)
    sub_font = font(38)
    lines = [
        ("AI agent cá nhân", ACCENT_BLUE),
        ("hoạt động 24/7 trên cloud Google", TEXT_WHITE),
        ("", TEXT_WHITE),
        ("Sử dụng Gemini 3.5", ACCENT_GREEN),
        ("+ Antigravity harness", ACCENT_YELLOW),
        ("", TEXT_WHITE),
        ("Tự quản lý tác vụ", TEXT_WHITE),
        ("khi thiết bị đã offline", ACCENT_ORANGE),
    ]
    yy = y + 60
    for text, color in lines:
        if text:
            center_text(draw, text, desc_font, yy, fill=color)
        yy += 65

    # Footer label
    draw_text_box(draw, "GOOGLE AI ULTRA", font(30, bold=True), W // 2, H - 90, pad_x=20, pad_y=10, outline=ACCENT_BLUE, text_fill=ACCENT_BLUE)
    return img

# === Scene 3: 2/7/2026 UPDATE ===
def scene3():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    draw_text_box(draw, "UPDATE 2/7/2026", font(34, bold=True), W // 2, 130, pad_x=30, pad_y=12, outline=ACCENT_ORANGE, text_fill=ACCENT_ORANGE)

    title_font = font(70, bold=True)
    center_text(draw, "Beta trên macOS", title_font, 230, fill=TEXT_WHITE)
    center_text(draw, "Desktop App", title_font, 310, fill=ACCENT_BLUE)

    # Card with 3 features
    y = 440
    features = [
        ("💻", "Tương tác file local", ACCENT_GREEN),
        ("📁", "Tự sắp xếp downloads", ACCENT_BLUE),
        ("📊", "Tạo spreadsheet từ invoice", ACCENT_PURPLE),
    ]
    icon_font = font(64)
    title_card_font = font(44, bold=True)
    for i, (icon, text, color) in enumerate(features):
        yy = y + i * 180
        draw_card(draw, 80, yy, W - 80, yy + 150, outline=color, width=2)
        draw.text((120, yy + 40), icon, font=icon_font, fill=TEXT_WHITE)
        draw.text((230, yy + 50), text, font=title_card_font, fill=color)

    # Footer label
    draw_text_box(draw, "DESKTOP AI AGENT", font(30, bold=True), W // 2, H - 90, pad_x=20, pad_y=10, outline=ACCENT_ORANGE, text_fill=ACCENT_ORANGE)
    return img

# === Scene 4: REAL-TIME TRACKING + IMAGE ===
def scene4():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    draw_text_box(draw, "REAL-TIME TRACKING", font(34, bold=True), W // 2, 130, pad_x=30, pad_y=12, outline=ACCENT_GREEN, text_fill=ACCENT_GREEN)

    title_font = font(70, bold=True)
    center_text(draw, "Theo dõi", title_font, 220, fill=TEXT_WHITE)
    center_text(draw, "theo thời gian thực", title_font, 300, fill=ACCENT_GREEN)

    # Gemini Spark image
    img_x = (W - spark_img.width) // 2
    img_y = 410
    draw_card(draw, img_x - 16, img_y - 16, img_x + spark_img.width + 16, img_y + spark_img.height + 16, outline=ACCENT_BLUE, width=3)
    img.paste(spark_img, (img_x, img_y), spark_img)

    # Below image - topics
    y = img_y + spark_img.height + 50
    topics = [
        ("📰", "Tin tức", ACCENT_BLUE),
        ("💰", "Tài chính", ACCENT_GREEN),
        ("📱", "Social media", ACCENT_PURPLE),
    ]
    icon_font = font(52)
    text_font = font(40, bold=True)
    for i, (icon, text, color) in enumerate(topics):
        xx = 120 + i * 300
        draw.text((xx, y), icon, font=icon_font, fill=TEXT_WHITE)
        draw.text((xx + 80, y + 8), text, font=text_font, fill=color)

    # Footer label
    draw_text_box(draw, "ALWAYS-ON AGENT", font(30, bold=True), W // 2, H - 90, pad_x=20, pad_y=10, outline=ACCENT_GREEN, text_fill=ACCENT_GREEN)
    return img

# === Scene 5: INTEGRATIONS ===
def scene5():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    draw_text_box(draw, "INTEGRATIONS", font(34, bold=True), W // 2, 130, pad_x=30, pad_y=12, outline=ACCENT_BLUE, text_fill=ACCENT_BLUE)

    title_font = font(70, bold=True)
    center_text(draw, "Tích hợp", title_font, 220, fill=TEXT_WHITE)
    center_text(draw, "ecosystem mở rộng", title_font, 300, fill=ACCENT_BLUE)

    # 6 integration cards in 2 columns
    integrations = [
        ("📋", "Google Tasks", ACCENT_BLUE),
        ("📝", "Keep", ACCENT_YELLOW),
        ("🎨", "Canva", ACCENT_PURPLE),
        ("📦", "Dropbox", ACCENT_BLUE),
        ("🛒", "Instacart", ACCENT_GREEN),
        ("🍽️", "OpenTable", ACCENT_RED),
        ("🏠", "Zillow", ACCENT_BLUE),
        ("🔌", "Custom MCP", ACCENT_ORANGE),
    ]
    icon_font = font(60)
    text_font = font(38, bold=True)
    sub_font = font(28)
    y_start = 430
    card_w = 440
    card_h = 160
    for i, (icon, text, color) in enumerate(integrations):
        col = i % 2
        row = i // 2
        x1 = 80 + col * (card_w + 40)
        y1 = y_start + row * (card_h + 25)
        draw_card(draw, x1, y1, x1 + card_w, y1 + card_h, outline=color, width=2)
        draw.text((x1 + 30, y1 + 40), icon, font=icon_font, fill=TEXT_WHITE)
        draw.text((x1 + 130, y1 + 50), text, font=text_font, fill=color)

    # Footer label
    draw_text_box(draw, "GOOGLE WORKSPACE + MORE", font(28, bold=True), W // 2, H - 90, pad_x=20, pad_y=10, outline=ACCENT_BLUE, text_fill=ACCENT_BLUE)
    return img

# === Scene 6: LESSON / DIFFERENTIATOR ===
def scene6():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    draw_text_box(draw, "DIFFERENTIATOR", font(34, bold=True), W // 2, 130, pad_x=30, pad_y=12, outline=ACCENT_YELLOW, text_fill=ACCENT_YELLOW)

    title_font = font(70, bold=True)
    center_text(draw, "Khác biệt", title_font, 220, fill=TEXT_WHITE)
    center_text(draw, "với ChatGPT & Claude", title_font, 300, fill=ACCENT_YELLOW)

    # 3 differentiator cards
    diffs = [
        ("⚡", "24/7 Cloud", "Chạy ngay cả khi thiết bị tắt", ACCENT_GREEN),
        ("🎯", "Multi-step", "Antigravity harness tự chủ", ACCENT_PURPLE),
        ("🌐", "Google Ecosystem", "Workspace + MCP integration", ACCENT_BLUE),
    ]
    icon_font = font(70)
    title_font_card = font(50, bold=True)
    desc_font = font(34)
    y = 440
    for i, (icon, title, desc, color) in enumerate(diffs):
        yy = y + i * 230
        draw_card(draw, 80, yy, W - 80, yy + 200, outline=color, width=2)
        draw.text((120, yy + 30), icon, font=icon_font, fill=TEXT_WHITE)
        draw.text((240, yy + 40), title, font=title_font_card, fill=color)
        draw.text((240, yy + 110), desc, font=desc_font, fill=TEXT_DIM)

    # Footer label
    draw_text_box(draw, "NOT JUST A CHATBOT", font(28, bold=True), W // 2, H - 90, pad_x=20, pad_y=10, outline=ACCENT_YELLOW, text_fill=ACCENT_YELLOW)
    return img

# === Scene 7: AVAILABILITY ===
def scene7():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    draw_text_box(draw, "AVAILABILITY", font(34, bold=True), W // 2, 130, pad_x=30, pad_y=12, outline=ACCENT_RED, text_fill=ACCENT_RED)

    title_font = font(70, bold=True)
    center_text(draw, "Giá & Khả dụng", title_font, 220, fill=TEXT_WHITE)

    # Big pricing card
    y = 380
    draw_card(draw, 100, y, W - 100, y + 480, outline=ACCENT_YELLOW, width=3)
    # Label
    draw_text_box(draw, "GOOGLE AI ULTRA", font(34, bold=True), W // 2, y + 60, pad_x=24, pad_y=10, outline=ACCENT_YELLOW, text_fill=ACCENT_YELLOW)
    # Price
    big_font = font(170, bold=True)
    center_text(draw, "$99.99", big_font, y + 110, fill=ACCENT_YELLOW)
    # Per month
    center_text(draw, "/tháng", font(48, bold=True), y + 300, fill=TEXT_WHITE)
    # Restrictions
    res_font = font(34)
    center_text(draw, "Chỉ dành cho US · 18+", res_font, y + 380, fill=TEXT_DIM)
    center_text(draw, "Tiếng Anh", res_font, y + 430, fill=TEXT_DIM)

    # Footer label
    draw_text_box(draw, "PREMIUM SUBSCRIPTION", font(28, bold=True), W // 2, H - 90, pad_x=20, pad_y=10, outline=ACCENT_RED, text_fill=ACCENT_RED)
    return img

# === Scene 8: TAKEAWAY ===
def scene8():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)

    draw_text_box(draw, "TAKEAWAY", font(34, bold=True), W // 2, 130, pad_x=30, pad_y=12, outline=ACCENT_GREEN, text_fill=ACCENT_GREEN)

    # Big quote
    title_font = font(76, bold=True)
    lines = ["Muốn AI làm", "việc thay mình", "24/7? Spark", "đáng cân nhắc"]
    y = 250
    for i, line in enumerate(lines):
        color = ACCENT_GREEN if i == 2 else TEXT_WHITE
        center_text(draw, line, title_font, y, fill=color)
        y += 95

    # Sub text
    sub_font = font(40)
    center_text(draw, "Bước tiến quan trọng của Google", sub_font, y + 30, fill=TEXT_DIM)
    center_text(draw, "trong cuộc đua AI agent", sub_font, y + 80, fill=TEXT_DIM)

    # Hashtag card
    y_hash = y + 200
    draw_card(draw, 100, y_hash, W - 100, y_hash + 200, outline=ACCENT_BLUE, width=2)
    hash_font = font(46, bold=True)
    center_text(draw, "#GeminiSpark #GoogleAI", hash_font, y_hash + 50, fill=ACCENT_BLUE)
    center_text(draw, "#AIAgent #AI2026", hash_font, y_hash + 120, fill=ACCENT_GREEN)

    # Footer label
    draw_text_box(draw, "THESIS BEFORE BUILD", font(30, bold=True), W // 2, H - 90, pad_x=20, pad_y=10, outline=ACCENT_GREEN, text_fill=ACCENT_GREEN)
    return img

# Render all
SCENES_FUNCS = [scene1, scene2, scene3, scene4, scene5, scene6, scene7, scene8]
for i, fn in enumerate(SCENES_FUNCS, 1):
    img = fn()
    out = os.path.join(OUT_DIR, f"s{i}.png")
    img.save(out, "PNG")
    print(f"  s{i}.png saved")

print(f"\nAll {len(SCENES_FUNCS)} frames in: {OUT_DIR}")
