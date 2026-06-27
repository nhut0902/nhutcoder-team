"""Generate 8 video frames (1080x1920) for FireClaw - security proxy for AI agents."""
import os, json, subprocess
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/z/my-project/download/fireclaw_frames"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1080, 1920

FONT_PATHS = [
    "/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf",
    "/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf",
]
BOLD_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_PATH = next((p for p in FONT_PATHS if os.path.exists(p)), None)
BOLD_PATH = next((p for p in BOLD_PATHS if os.path.exists(p)), FONT_PATH)
print(f"Font: {FONT_PATH}, Bold: {BOLD_PATH}")

def font(size, bold=False):
    return ImageFont.truetype(BOLD_PATH if bold else FONT_PATH, size)

# Cyber/security theme - dark with red/orange accents (fire theme)
SCENES = [
    {
        "id": "s1",
        "bg": ((15, 5, 5), (60, 15, 5)),  # dark red gradient
        "emoji": "🛡️",
        "title": "FIRECLAW",
        "title_size": 180,
        "subtitle": "Bức tường lửa\ncho bộ não AI",
        "subtitle_size": 60,
        "footer": "github.com/raiph-ai/fireclaw",
    },
    {
        "id": "s2",
        "bg": ((30, 0, 0), (80, 20, 10)),
        "emoji": "⚠️",
        "title": "PROMPT\nINJECTION?",
        "title_size": 130,
        "subtitle": "Hacker giấu mã độc\ntrong nội dung web\nmà AI đang đọc",
        "subtitle_size": 50,
        "footer": "Mối đe dọa số 1 cho AI Agent",
    },
    {
        "id": "s3",
        "bg": ((5, 10, 25), (15, 30, 70)),
        "emoji": "🔥",
        "title": "FireClaw\nLÀ GÌ?",
        "title_size": 140,
        "subtitle": "Proxy bảo mật\nmã nguồn mở\nbởi raiph-ai",
        "subtitle_size": 50,
        "footer": "Lớp lọc giữa AI & Internet",
    },
    {
        "id": "s4",
        "bg": ((10, 5, 30), (40, 15, 90)),
        "emoji": "⚙️",
        "title": "PIPELINE\n4 GIAI ĐOẠN",
        "title_size": 120,
        "subtitle": "1. FETCHING - Tải nội dung\n2. SANITIZING - Lọc mã độc",
        "subtitle_size": 44,
        "footer": "Giai đoạn 1 & 2",
    },
    {
        "id": "s5",
        "bg": ((15, 5, 40), (50, 15, 110)),
        "emoji": "🔍",
        "title": "PIPELINE\n(tiếp)",
        "title_size": 120,
        "subtitle": "3. SUMMARIZING - Tóm tắt\n4. SCANNING - Quét threat intel",
        "subtitle_size": 44,
        "footer": "Giai đoạn 3 & 4",
    },
    {
        "id": "s6",
        "bg": ((20, 30, 5), (60, 90, 15)),
        "emoji": "✨",
        "title": "TÍNH NĂNG",
        "title_size": 130,
        "features": [
            ("🪤", "Canary Token"),
            ("📋", "Audit Logging"),
            ("🌐", "Threat Intel"),
            ("⏱️", "Rate Limiting"),
        ],
        "footer": "Đầy đủ công cụ bảo mật",
    },
    {
        "id": "s7",
        "bg": ((5, 25, 15), (15, 70, 40)),
        "emoji": "🆓",
        "title": "MIỄN PHÍ\n& OPEN SOURCE",
        "title_size": 110,
        "subtitle": "Clone repo\nCấu hình domain tiers\nTích hợp workflow",
        "subtitle_size": 48,
        "footer": "Cho cá nhân & doanh nghiệp",
    },
    {
        "id": "s8",
        "bg": ((60, 5, 30), (180, 30, 80)),
        "emoji": "🚀",
        "title": "BẮT ĐẦU\nNGAY!",
        "title_size": 150,
        "subtitle": "Bảo mật không phải tùy chọn\nLà ưu tiên số 1",
        "subtitle_size": 50,
        "url": "github.com/raiph-ai/fireclaw",
        "hashtags": "#FireClaw #AISecurity #PromptInjection",
        "footer": "Like & Subscribe ❤️",
    },
]

def draw_gradient(draw, top_rgb, bottom_rgb):
    for y in range(H):
        t = y / H
        r = int(top_rgb[0] + (bottom_rgb[0] - top_rgb[0]) * t)
        g = int(top_rgb[1] + (bottom_rgb[1] - top_rgb[1]) * t)
        b = int(top_rgb[2] + (bottom_rgb[2] - top_rgb[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def text_with_outline(draw, xy, text, fnt, fill, outline=(0, 0, 0), width=4):
    x, y = xy
    for dx in range(-width, width + 1, 2):
        for dy in range(-width, width + 1, 2):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=fnt, fill=outline)
    draw.text((x, y), text, font=fnt, fill=fill)

def center_text(draw, text, fnt, y, fill=(255, 255, 255), outline=True):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    text_w = bbox[2] - bbox[0]
    x = (W - text_w) // 2
    if outline:
        text_with_outline(draw, (x, y), text, fnt, fill)
    else:
        draw.text((x, y), text, font=fnt, fill=fill)

def render_scene(scene):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, scene["bg"][0], scene["bg"][1])

    # Decorative top accent line
    draw.rectangle([(0, 0), (W, 8)], fill=(255, 80, 30))
    draw.rectangle([(0, H - 8), (W, H)], fill=(255, 80, 30))

    # Emoji at top
    emoji_font = font(220)
    center_text(draw, scene["emoji"], emoji_font, 200, outline=False)

    # Title
    title_font = font(scene.get("title_size", 150), bold=True)
    title_lines = scene["title"].split("\n")
    line_height = scene.get("title_size", 150) + 20
    start_y = 540
    for i, line in enumerate(title_lines):
        # Title with fire orange color
        center_text(draw, line, title_font, start_y + i * line_height, fill=(255, 220, 100))

    y_cursor = start_y + len(title_lines) * line_height + 60

    # Features list
    if scene.get("features"):
        feat_font = font(50, bold=True)
        feat_h = 100
        for i, (icon, text) in enumerate(scene["features"]):
            row_y = y_cursor + i * feat_h
            draw.rounded_rectangle([100, row_y - 10, W - 100, row_y + 75], radius=18,
                                    fill=(30, 20, 15), outline=(120, 60, 30), width=2)
            draw.text((135, row_y), icon, font=font(52), fill=(255, 255, 255))
            draw.text((240, row_y + 5), text, font=feat_font, fill=(255, 220, 200))
        y_cursor += len(scene["features"]) * feat_h + 50

    # Subtitle (multi-line)
    if scene.get("subtitle"):
        sub_font = font(scene.get("subtitle_size", 50))
        sub_lines = scene["subtitle"].split("\n")
        sub_h = scene.get("subtitle_size", 50) + 18
        for i, line in enumerate(sub_lines):
            center_text(draw, line, sub_font, y_cursor + i * sub_h, fill=(220, 230, 240))
        y_cursor += len(sub_lines) * sub_h + 50

    # URL
    if scene.get("url"):
        url_font = font(44, bold=True)
        bbox = draw.textbbox((0, 0), scene["url"], font=url_font)
        url_w = bbox[2] - bbox[0]
        pad_x, pad_y = 40, 20
        box_x1 = (W - url_w) // 2 - pad_x
        box_y1 = y_cursor - pad_y
        box_x2 = (W + url_w) // 2 + pad_x
        box_y2 = y_cursor + 50 + pad_y
        draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=12, fill=(30, 25, 20))
        center_text(draw, scene["url"], url_font, y_cursor, fill=(255, 180, 80), outline=False)
        y_cursor = box_y2 + 40

    # Hashtags
    if scene.get("hashtags"):
        hash_font = font(42, bold=True)
        center_text(draw, scene["hashtags"], hash_font, y_cursor, fill=(100, 200, 255))
        y_cursor += 80

    # Footer
    if scene.get("footer"):
        foot_font = font(36)
        center_text(draw, scene["footer"], foot_font, H - 130, fill=(180, 180, 180), outline=False)

    return img

# Render all
for scene in SCENES:
    img = render_scene(scene)
    out = os.path.join(OUT_DIR, f"{scene['id']}.png")
    img.save(out, "PNG")
    print(f"  {scene['id']}.png saved")

print(f"\nAll {len(SCENES)} frames in: {OUT_DIR}")
