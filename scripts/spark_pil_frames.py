"""Render 8 frames with PIL: text + Gemini Spark image + gradients. Reliable - no HyperFrames."""
import os, json, subprocess
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/z/my-project/download/spark_pil_frames"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1080, 1920

# Find fonts (LXGW WenKai has good Vietnamese diacritics support)
FONT_PATHS_REGULAR = [
    "/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_PATHS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf",
]
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

def draw_orbs(draw):
    """Decorative glow circles in background"""
    import random
    random.seed(42)
    for _ in range(5):
        x = random.randint(0, W)
        y = random.randint(0, H)
        r = random.randint(150, 300)
        # Glow effect: nested circles with decreasing alpha
        for i in range(r, 0, -20):
            alpha = int(20 * (1 - i / r))
            color = (66, 133, 244, alpha)
            # PIL doesn't support alpha on RGB draw directly, so we simulate with darker shade
            shade = (
                max(0, min(255, 30 + alpha)),
                max(0, min(255, 50 + alpha)),
                max(0, min(255, 100 + alpha)),
            )
            draw.ellipse([x - i, y - i, x + i, y + i], fill=shade)

# Load Gemini Spark image (resize for scene 4)
SPARK_IMG_PATH = "/home/z/my-project/download/gemini_spark/gemini_spark_pcmag.png"
spark_img = Image.open(SPARK_IMG_PATH).convert("RGBA")
# Resize to fit width 800
target_w = 800
aspect = spark_img.height / spark_img.width
new_h = int(target_w * aspect)
spark_img = spark_img.resize((target_w, new_h), Image.LANCZOS)
print(f"Spark image resized: {spark_img.size}")

SCENES = [
    {
        "id": "s1",
        "bg": ((10, 14, 26), (45, 27, 105)),  # blue -> purple
        "emoji": "✨",
        "title_lines": ["GEMINI", "SPARK"],
        "title_size": 160,
        "subtitle_lines": ["AI Agent 24/7", "của Google"],
        "subtitle_size": 60,
        "badge": "2/7/2026",
    },
    {
        "id": "s2",
        "bg": ((20, 30, 60), (60, 50, 120)),
        "emoji": "🤖",
        "title_lines": ["Gemini Spark", "là gì?"],
        "title_size": 100,
        "subtitle_lines": ["AI agent 24/7 trên cloud", "Gemini 3.5", "+ Antigravity harness"],
        "subtitle_size": 50,
    },
    {
        "id": "s3",
        "bg": ((15, 30, 50), (40, 80, 120)),
        "emoji": "💻",
        "title_lines": ["macOS", "Beta"],
        "title_size": 140,
        "subtitle_lines": ["Tương tác file local", "Tự sắp xếp downloads", "Tạo spreadsheet từ invoice"],
        "subtitle_size": 46,
    },
    {
        "id": "s4",
        "bg": ((30, 20, 70), (80, 50, 150)),
        "emoji": "📊",
        "title_lines": ["Real-time", "Tracking"],
        "title_size": 110,
        "subtitle_lines": ["Tin tức · Tài chính", "Social media"],
        "subtitle_size": 50,
        "image": True,  # show spark image
    },
    {
        "id": "s5",
        "bg": ((10, 40, 30), (30, 100, 80)),
        "emoji": "🔗",
        "title_lines": ["Tích hợp"],
        "title_size": 130,
        "features": [
            ("📋", "Google Tasks · Keep"),
            ("🎨", "Canva · Dropbox"),
            ("🛒", "Instacart · OpenTable"),
            ("🏠", "Zillow Rentals"),
            ("🔌", "Custom MCP"),
        ],
    },
    {
        "id": "s6",
        "bg": ((40, 30, 10), (120, 80, 30)),
        "emoji": "💰",
        "title_lines": ["Giá"],
        "title_size": 130,
        "stat_value": "$99.99",
        "stat_label": "Google AI Ultra",
        "stat_desc": "/tháng · Chỉ US 18+",
        "subtitle_lines": ["Tiếng Anh"],
        "subtitle_size": 40,
    },
    {
        "id": "s7",
        "bg": ((60, 20, 60), (150, 50, 100)),
        "emoji": "⚔️",
        "title_lines": ["So sánh"],
        "title_size": 130,
        "features": [
            ("⚡", "Chạy 24/7 trên cloud"),
            ("🔇", "Không cần thiết bị bật"),
            ("🎯", "Multi-step tự chủ"),
        ],
    },
    {
        "id": "s8",
        "bg": ((60, 5, 80), (180, 30, 120)),
        "emoji": "🚀",
        "title_lines": ["Tổng kết"],
        "title_size": 130,
        "subtitle_lines": ["Bước tiến quan trọng", "trong cuộc đua AI agent"],
        "subtitle_size": 50,
        "hashtags": "#GeminiSpark #GoogleAI #AI2026",
    },
]

def render_scene(scene):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, scene["bg"][0], scene["bg"][1])
    draw_orbs(draw)

    # Top accent bar
    draw.rectangle([(0, 0), (W, 6)], fill=(66, 133, 244))
    draw.rectangle([(0, H - 6), (W, H)], fill=(66, 133, 244))

    # Badge (top)
    y_cursor = 250
    if scene.get("badge"):
        badge_font = font(44, bold=True)
        badge_text = scene["badge"]
        bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
        bw = bbox[2] - bbox[0]
        bh = bbox[3] - bbox[1]
        # Badge background pill
        pad_x, pad_y = 30, 16
        bx1 = (W - bw) // 2 - pad_x
        by1 = y_cursor - pad_y
        bx2 = (W + bw) // 2 + pad_x
        by2 = y_cursor + bh + pad_y
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=20,
                                fill=(30, 50, 100), outline=(66, 133, 244), width=3)
        center_text(draw, badge_text, badge_font, y_cursor, fill=(100, 180, 255))
        y_cursor = by2 + 50

    # Emoji
    emoji_font = font(220)
    center_text(draw, scene["emoji"], emoji_font, y_cursor, fill=(255, 255, 255))
    y_cursor += 280

    # Title (multi-line)
    title_font = font(scene.get("title_size", 120), bold=True)
    line_h = scene.get("title_size", 120) + 20
    for line in scene.get("title_lines", []):
        # Title with white color (could add gradient later)
        center_text(draw, line, title_font, y_cursor, fill=(255, 255, 255))
        y_cursor += line_h
    y_cursor += 40

    # Image if any
    if scene.get("image"):
        # Paste spark_img centered
        img_x = (W - spark_img.width) // 2
        img_y = y_cursor
        # Draw border
        draw.rounded_rectangle([img_x - 6, img_y - 6, img_x + spark_img.width + 6, img_y + spark_img.height + 6],
                                radius=18, fill=(20, 30, 60), outline=(66, 133, 244), width=4)
        # Paste image
        img.paste(spark_img, (img_x, img_y), spark_img if spark_img.mode == "RGBA" else None)
        y_cursor = img_y + spark_img.height + 50

    # Features list
    if scene.get("features"):
        feat_font = font(48, bold=True)
        feat_icon_font = font(56)
        feat_h = 110
        for i, (icon, text) in enumerate(scene["features"]):
            row_y = y_cursor + i * feat_h
            # Pill background
            draw.rounded_rectangle([80, row_y - 10, W - 80, row_y + 80], radius=18,
                                    fill=(30, 41, 59), outline=(66, 133, 244), width=2)
            draw.text((110, row_y + 5), icon, font=feat_icon_font, fill=(255, 255, 255))
            draw.text((210, row_y + 12), text, font=feat_font, fill=(220, 230, 255))
        y_cursor += len(scene["features"]) * feat_h + 40

    # Stat block
    if scene.get("stat_value"):
        stat_font = font(120, bold=True)
        label_font = font(38, bold=True)
        desc_font = font(36)
        # Box
        box_h = 380
        draw.rounded_rectangle([150, y_cursor, W - 150, y_cursor + box_h], radius=24,
                                fill=(30, 41, 59), outline=(255, 200, 80), width=3)
        center_text(draw, scene["stat_label"], label_font, y_cursor + 30, fill=(200, 200, 200))
        center_text(draw, scene["stat_value"], stat_font, y_cursor + 90, fill=(255, 200, 80))
        center_text(draw, scene["stat_desc"], desc_font, y_cursor + 250, fill=(220, 230, 255))
        y_cursor += box_h + 30

    # Subtitle (multi-line)
    if scene.get("subtitle_lines"):
        sub_font = font(scene.get("subtitle_size", 50))
        sub_h = scene.get("subtitle_size", 50) + 18
        for line in scene["subtitle_lines"]:
            center_text(draw, line, sub_font, y_cursor, fill=(220, 230, 255))
            y_cursor += sub_h
        y_cursor += 40

    # Hashtags
    if scene.get("hashtags"):
        hash_font = font(42, bold=True)
        center_text(draw, scene["hashtags"], hash_font, y_cursor, fill=(100, 200, 255))

    # Footer (always visible at bottom)
    foot_font = font(32)
    center_text(draw, "Nguồn: blog.google · TechCrunch · PCMag", foot_font, H - 100, fill=(150, 160, 180))

    return img

# Render all scenes
for scene in SCENES:
    img = render_scene(scene)
    out = os.path.join(OUT_DIR, f"{scene['id']}.png")
    img.save(out, "PNG")
    print(f"  {scene['id']}.png saved")

print(f"\nAll {len(SCENES)} frames in: {OUT_DIR}")
