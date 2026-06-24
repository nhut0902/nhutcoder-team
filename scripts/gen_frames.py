"""Generate video frames (1080x1920) for 6 scenes about Browser use repo.
Each scene = 1 PNG. ffmpeg will assemble them with the audio track.
"""
import os, json, subprocess
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/z/my-project/download/frames"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1080, 1920

# Load Vietnamese-capable font
FONT_PATHS = [
    "/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf",
    "/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Regular.otf",
    "/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_PATH = next((p for p in FONT_PATHS if os.path.exists(p)), None)
if not FONT_PATH:
    # Search system
    r = subprocess.run(["fc-list", ":lang=vi"], capture_output=True, text=True)
    print("Vietnamese fonts available:")
    print(r.stdout)
    # Take first one
    for line in r.stdout.split("\n"):
        if line.strip():
            FONT_PATH = line.split(":")[0]
            break
print(f"Using font: {FONT_PATH}")

def font(size, bold=False):
    # Try to find a bold variant
    if bold:
        bold_paths = [
            "/usr/share/fonts/truetype/chinese/NotoSansSC-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        for p in bold_paths:
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.truetype(FONT_PATH, size)

# Gradient backgrounds per scene (RGB tuple top, bottom)
SCENES = [
    {
        "id": "s1",
        "bg": ((10, 14, 26), (30, 20, 60)),  # dark blue -> purple
        "emoji": "🌐",
        "title": "BROWSER\nUSE",
        "title_size": 200,
        "subtitle": "Thư viện Python\ncho AI Agent",
        "subtitle_size": 56,
        "footer": "github.com/browser-use",
    },
    {
        "id": "s2",
        "bg": ((20, 10, 50), (60, 20, 90)),  # deep purple
        "emoji": "⭐",
        "title": "100K+",
        "title_size": 280,
        "subtitle": "GitHub Stars\n11K+ Forks\nMIT License",
        "subtitle_size": 60,
        "footer": "Top 1 AI Browser Tool",
    },
    {
        "id": "s3",
        "bg": ((0, 30, 40), (0, 80, 100)),  # teal
        "emoji": "📦",
        "title": "CÀI ĐẶT",
        "title_size": 130,
        "code": "pip install browser-use",
        "subtitle": "Chỉ 1 dòng lệnh\nLà bắt đầu được ngay",
        "subtitle_size": 50,
        "footer": "Quick Start",
    },
    {
        "id": "s4",
        "bg": ((40, 10, 60), (90, 30, 100)),  # magenta
        "emoji": "⚡",
        "title": "TÍNH NĂNG",
        "title_size": 130,
        "features": [
            ("🤖", "Điều khiển AI Agent"),
            ("🖱️", "Click · Type · Scroll"),
            ("📊", "Trích xuất dữ liệu"),
            ("☁️", "Cloud & Self-hosted"),
        ],
        "footer": "Powered by Playwright",
    },
    {
        "id": "s5",
        "bg": ((10, 50, 80), (30, 120, 180)),  # ocean blue
        "emoji": "🚀",
        "title": "BẮT ĐẦU\nNGAY",
        "title_size": 180,
        "subtitle": "Tương thích mọi LLM\nGPT · Claude · Gemini",
        "subtitle_size": 56,
        "url": "github.com/browser-use",
        "footer": "Open Source · Free",
    },
    {
        "id": "s6",
        "bg": ((60, 0, 80), (180, 30, 100)),  # pink/purple
        "emoji": "❤️",
        "title": "CẢM ƠN\nBẠN!",
        "title_size": 200,
        "subtitle": "Like · Share · Subscribe",
        "subtitle_size": 60,
        "hashtags": "#AI #BrowserUse #Python #Automation",
        "footer": "NhutCoder",
    },
]

def draw_gradient(draw, top_rgb, bottom_rgb):
    """Vertical gradient fill."""
    for y in range(H):
        t = y / H
        r = int(top_rgb[0] + (bottom_rgb[0] - top_rgb[0]) * t)
        g = int(top_rgb[1] + (bottom_rgb[1] - top_rgb[1]) * t)
        b = int(top_rgb[2] + (bottom_rgb[2] - top_rgb[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def text_with_outline(draw, xy, text, fnt, fill, outline=(0, 0, 0), width=4):
    """Draw text with black outline for readability."""
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

    # Emoji at top
    emoji_font = font(220)
    center_text(draw, scene["emoji"], emoji_font, 250, outline=False)

    # Title (large, gradient-like white)
    title_font = font(scene.get("title_size", 150), bold=True)
    # Handle multi-line title
    title_lines = scene["title"].split("\n")
    line_height = scene.get("title_size", 150) + 20
    start_y = 600
    for i, line in enumerate(title_lines):
        center_text(draw, line, title_font, start_y + i * line_height, fill=(255, 255, 255))

    # Code block if any
    y_cursor = start_y + len(title_lines) * line_height + 50
    if scene.get("code"):
        code_font = font(60, bold=True)
        bbox = draw.textbbox((0, 0), scene["code"], font=code_font)
        code_w = bbox[2] - bbox[0]
        code_h = bbox[3] - bbox[1]
        # background pill
        pad_x, pad_y = 50, 30
        box_x1 = (W - code_w) // 2 - pad_x
        box_y1 = y_cursor - pad_y
        box_x2 = (W + code_w) // 2 + pad_x
        box_y2 = y_cursor + code_h + pad_y
        draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=20, fill=(30, 41, 59), outline=(51, 65, 85), width=3)
        # code text
        cx = (W - code_w) // 2
        # Add $ prefix
        draw.text((cx - 50, y_cursor), "$", font=code_font, fill=(148, 163, 184))
        draw.text((cx, y_cursor), scene["code"], font=code_font, fill=(0, 255, 136))
        y_cursor = box_y2 + 60

    # Features list if any
    if scene.get("features"):
        feat_font = font(56, bold=True)
        feat_h = 90
        for i, (icon, text) in enumerate(scene["features"]):
            row_y = y_cursor + i * feat_h
            # pill bg
            draw.rounded_rectangle([100, row_y - 10, W - 100, row_y + 70], radius=18,
                                    fill=(30, 41, 59, 100), outline=(51, 65, 85), width=2)
            draw.text((130, row_y), icon, font=font(56), fill=(255, 255, 255))
            draw.text((230, row_y + 5), text, font=feat_font, fill=(255, 255, 255))
        y_cursor += len(scene["features"]) * feat_h + 40

    # Subtitle
    if scene.get("subtitle"):
        sub_font = font(scene.get("subtitle_size", 50))
        sub_lines = scene["subtitle"].split("\n")
        sub_h = scene.get("subtitle_size", 50) + 15
        for i, line in enumerate(sub_lines):
            center_text(draw, line, sub_font, y_cursor + i * sub_h, fill=(203, 213, 225))
        y_cursor += len(sub_lines) * sub_h + 40

    # URL
    if scene.get("url"):
        url_font = font(48, bold=True)
        bbox = draw.textbbox((0, 0), scene["url"], font=url_font)
        url_w = bbox[2] - bbox[0]
        pad_x, pad_y = 40, 20
        box_x1 = (W - url_w) // 2 - pad_x
        box_y1 = y_cursor - pad_y
        box_x2 = (W + url_w) // 2 + pad_x
        box_y2 = y_cursor + 50 + pad_y
        draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=12, fill=(30, 41, 59))
        center_text(draw, scene["url"], url_font, y_cursor, fill=(0, 212, 255), outline=False)
        y_cursor = box_y2 + 40

    # Hashtags
    if scene.get("hashtags"):
        hash_font = font(46, bold=True)
        center_text(draw, scene["hashtags"], hash_font, y_cursor, fill=(0, 212, 255))
        y_cursor += 80

    # Footer
    if scene.get("footer"):
        foot_font = font(38)
        center_text(draw, scene["footer"], foot_font, H - 150, fill=(148, 163, 184), outline=False)

    return img

# Render all scenes
for scene in SCENES:
    img = render_scene(scene)
    out = os.path.join(OUT_DIR, f"{scene['id']}.png")
    img.save(out, "PNG")
    print(f"  {scene['id']}.png saved ({img.size})")

print(f"\nAll frames in: {OUT_DIR}")
