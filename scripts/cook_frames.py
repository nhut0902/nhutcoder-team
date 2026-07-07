#!/home/z/.venv/bin/python3
"""Render 8 PIL frames for cooking video review. Warm theme + thumbnail + content."""
import os, json
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/z/my-project/download/cook_frames"
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

def paste_shot(img, path, max_w, max_h, y_start, border_color=(255, 180, 80)):
    shot = Image.open(path).convert("RGB")
    sw, sh = shot.size
    scale = min(max_w / sw, max_h / sh)
    new_w = int(sw * scale)
    new_h = int(sh * scale)
    shot_resized = shot.resize((new_w, new_h), Image.LANCZOS)
    x = (W - new_w) // 2
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x-6, y_start-6, x+new_w+6, y_start+new_h+6], radius=14, fill=(20, 15, 10), outline=border_color, width=4)
    img.paste(shot_resized, (x, y_start))

# Warm theme (cooking/family)
BG_TOP = (30, 15, 10)
BG_BOTTOM = (12, 6, 4)
ACCENT_ORANGE = (255, 140, 50)
ACCENT_RED = (240, 80, 60)
ACCENT_YELLOW = (250, 200, 80)
ACCENT_GREEN = (100, 200, 130)
ACCENT_BLUE = (100, 160, 255)
ACCENT_PINK = (255, 130, 170)
TEXT_WHITE = (250, 245, 240)
TEXT_DIM = (170, 160, 150)

THUMB = "/home/z/my-project/download/yt_thumbnail.jpg"

def draw_header(draw, text, color):
    f = font(34, bold=True)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 30, 80, (W + tw)//2 + 30, 150], radius=8, outline=color, width=3)
    draw.text(((W - tw)//2, 90), text, font=f, fill=color)

def draw_footer(draw, text, color):
    f = font(28, bold=True)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(W - tw)//2 - 20, H - 130, (W + tw)//2 + 20, H - 70], radius=6, outline=color, width=2)
    draw.text(((W - tw)//2, H - 120), text, font=f, fill=color)

def draw_subtitle(draw, lines, y_start=H - 280):
    sub_font = font(38)
    y = y_start
    for line in lines:
        center_text(draw, line, sub_font, y, fill=TEXT_WHITE)
        y += 52

def draw_card(draw, y, icon, title, desc, color):
    draw.rounded_rectangle([80, y, W - 80, y + 150], radius=14, outline=color, width=2, fill=(25, 18, 12))
    draw.text((110, y + 30), icon, font=font(56), fill=TEXT_WHITE)
    draw.text((200, y + 25), title, font=font(42, bold=True), fill=color)
    draw.text((200, y + 80), desc, font=font(34), fill=TEXT_DIM)

# === Scene 1: Hook ===
def scene1():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🔥 VIDEO VIRAL REVIEW", ACCENT_ORANGE)
    # Thumbnail
    paste_shot(img, THUMB, max_w=900, max_h=500, y_start=200, border_color=ACCENT_ORANGE)
    # Title
    title_font = font(56, bold=True)
    center_text(draw, "Bầu Huy Vào Bếp", title_font, 730, fill=ACCENT_ORANGE)
    center_text(draw, "Cho Bầu Ni", title_font, 800, fill=ACCENT_YELLOW)
    center_text(draw, "Kênh: Thiện Tiên Vlog", font(38), 880, fill=TEXT_DIM)
    # Stats
    y = 950
    draw.rounded_rectangle([80, y, W - 80, y + 200], radius=14, outline=ACCENT_RED, width=2, fill=(25, 15, 12))
    stat_font = font(50, bold=True)
    draw.text((130, y + 25), "📺 YouTube Viral", font=stat_font, fill=ACCENT_RED)
    draw.text((130, y + 90), "👨‍🍳 Chồng nấu cơm cho vợ bầu", font=font(36), fill=TEXT_WHITE)
    draw.text((130, y + 140), "❤️ Tình cảm gia đình ấm áp", font=font(36), fill=TEXT_WHITE)
    draw_subtitle(draw, ["Video viral: Bầu Huy nấu cơm cho vợ bầu", "Kênh Thiện Tiên Vlog trên YouTube"])
    draw_footer(draw, "VIRAL VIDEO · FAMILY VLOG", ACCENT_ORANGE)
    return img

# === Scene 2: What happens ===
def scene2():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "NỘI DUNG VIDEO", ACCENT_YELLOW)
    title_font = font(64, bold=True)
    center_text(draw, "Câu chuyện", title_font, 220, fill=TEXT_WHITE)
    features = [
        ("🥬", "Rửa rau", "tươi sạch, cẩn thận", ACCENT_GREEN),
        ("🍚", "Nấu cơm", "đơn giản, ấm áp", ACCENT_YELLOW),
        ("🍽️", "Bày biện", "chăm chút tỉ mỉ", ACCENT_ORANGE),
        ("❤️", "Tình yêu", "chăm sóc vợ bầu", ACCENT_PINK),
    ]
    y = 340
    for icon, title, desc, color in features:
        draw_card(draw, y, icon, title, desc, color)
        y += 170
    draw_subtitle(draw, ["Bầu Huy: rửa rau, nấu cơm, bày biện", "Đơn giản nhưng ấm áp, chân thực"])
    draw_footer(draw, "SIMPLE · WARM · AUTHENTIC", ACCENT_YELLOW)
    return img

# === Scene 3: Why viral ===
def scene3():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "VÌ SAO VIRAL?", ACCENT_RED)
    title_font = font(68, bold=True)
    center_text(draw, "Tính chân thực", title_font, 220, fill=ACCENT_RED)
    center_text(draw, "🤍", font(180), 330, fill=TEXT_WHITE)
    # Card
    y = 560
    draw.rounded_rectangle([80, y, W - 80, y + 400], radius=18, outline=ACCENT_RED, width=3, fill=(25, 12, 10))
    draw.text((110, y + 20), "Điều làm video viral:", font=font(38, bold=True), fill=ACCENT_RED)
    draw.text((110, y + 80), "✗ Không công thức cầu kỳ", font=font(36), fill=TEXT_DIM)
    draw.text((110, y + 130), "✗ Không drama", font=font(36), fill=TEXT_DIM)
    draw.text((110, y + 180), "✗ Không special effects", font=font(36), fill=TEXT_DIM)
    draw.text((110, y + 240), "✓ Chỉ là người đàn ông", font=font(38, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 290), "  làm việc cần thiết", font=font(38, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 340), "  chăm sóc vợ", font=font(38, bold=True), fill=ACCENT_GREEN)
    draw_subtitle(draw, ["Viral vì tính chân thực, không drama", "Đơn giản: chồng chăm sóc vợ bầu"])
    draw_footer(draw, "AUTHENTICITY > POLISH", ACCENT_RED)
    return img

# === Scene 4: Domestic care ===
def scene4():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "DOMESTIC CARE", ACCENT_PINK)
    title_font = font(64, bold=True)
    center_text(draw, "Lao động chăm sóc", title_font, 220, fill=TEXT_WHITE)
    center_text(draw, "vô hình", title_font, 290, fill=ACCENT_PINK)
    # Card
    y = 420
    draw.rounded_rectangle([80, y, W - 80, y + 450], radius=18, outline=ACCENT_PINK, width=3, fill=(25, 15, 20))
    draw.text((110, y + 20), "💬 Cuộc trò chuyện:", font=font(38, bold=True), fill=ACCENT_PINK)
    draw.text((110, y + 80), "Video tạo ra thảo luận về:", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 140), "• Domestic care - chăm sóc gia đình", font=font(34), fill=TEXT_WHITE)
    draw.text((110, y + 195), "• Lao động vô hình trong nhà", font=font(34), fill=TEXT_WHITE)
    draw.text((110, y + 250), "• Đặc biệt khi vợ mang thai", font=font(34), fill=TEXT_WHITE)
    draw.text((110, y + 305), "• Việc nhỏ nhưng quan trọng", font=font(34), fill=TEXT_WHITE)
    draw.text((110, y + 370), "• Thường không được ghi nhận", font=font(34), fill=ACCENT_YELLOW)
    draw_subtitle(draw, ["Video tạo thảo luận về domestic care", "Lao động chăm sóc vô hình trong gia đình"])
    draw_footer(draw, "DOMESTIC CARE · INVISIBLE LABOR", ACCENT_PINK)
    return img

# === Scene 5: Comments ===
def scene5():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "PHẢN HỒI NGƯỜI XEM", ACCENT_BLUE)
    title_font = font(64, bold=True)
    center_text(draw, "Bình luận", title_font, 220, fill=TEXT_WHITE)
    # Comment cards
    comments = [
        ("👩", "Loại chăm sóc này thường vô hình", "ngay cả trong tình yêu", ACCENT_PINK),
        ("👨", "Ca ngợi người chồng", "step up, consistent care", ACCENT_BLUE),
        ("🤰", "Chia sẻ trải nghiệm riêng", "đồng cảm với vợ bầu", ACCENT_YELLOW),
        ("💡", "Hành động nhỏ > cử chỉ lớn", "quiet, steady care", ACCENT_GREEN),
    ]
    y = 340
    for icon, title, desc, color in comments:
        draw_card(draw, y, icon, title, desc, color)
        y += 170
    draw_subtitle(draw, ["Bình luận đầy ắp người xem chia sẻ", "Hành động nhỏ quan trọng hơn cử chỉ lớn"])
    draw_footer(draw, "COMMUNITY · RESONANCE", ACCENT_BLUE)
    return img

# === Scene 6: Content lesson ===
def scene6():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "💡 BÀI HỌC CREATOR", ACCENT_GREEN)
    title_font = font(60, bold=True)
    center_text(draw, "Bài học cho", title_font, 220, fill=TEXT_WHITE)
    center_text(draw, "content creator", title_font, 290, fill=ACCENT_GREEN)
    # Lesson card
    y = 400
    draw.rounded_rectangle([80, y, W - 80, y + 420], radius=18, outline=ACCENT_GREEN, width=3, fill=(15, 25, 18))
    draw.text((110, y + 20), "🎯 Key takeaway:", font=font(38, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 85), "Tính chân thực", font=font(44, bold=True), fill=ACCENT_YELLOW)
    draw.text((110, y + 145), "+ gần gũi", font=font(44, bold=True), fill=ACCENT_YELLOW)
    draw.text((110, y + 210), ">", font=font(48, bold=True), fill=ACCENT_RED)
    draw.text((110, y + 270), "sự hoàn hảo", font=font(44, bold=True), fill=TEXT_DIM)
    draw.text((110, y + 340), "Biến real-life moments thành content", font=font(34), fill=TEXT_WHITE)
    draw.text((110, y + 385), "cần công cụ streamline workflow", font=font(34), fill=TEXT_WHITE)
    draw_subtitle(draw, ["Chân thực + gần gũi > hoàn hảo", "Real-life moments = content mạnh nhất"])
    draw_footer(draw, "AUTHENTIC > POLISHED", ACCENT_GREEN)
    return img

# === Scene 7: AI tools for creators ===
def scene7():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🛠️ AI TOOLS FOR CREATORS", ACCENT_BLUE)
    title_font = font(56, bold=True)
    center_text(draw, "Biến cuộc sống", title_font, 220, fill=TEXT_WHITE)
    center_text(draw, "thành content", title_font, 290, fill=ACCENT_BLUE)
    tools = [
        ("🎙️", "TTS Voice Cloning", "VieNeu - clone giọng Việt", ACCENT_ORANGE),
        ("🎬", "Video Editing", "ffmpeg + PIL automation", ACCENT_YELLOW),
        ("📱", "Social Media Auto", "Zernio API - FB + TikTok", ACCENT_GREEN),
        ("🤖", "Content Generation", "Riff - video → blog + posts", ACCENT_BLUE),
    ]
    y = 400
    for icon, title, desc, color in tools:
        draw_card(draw, y, icon, title, desc, color)
        y += 170
    draw_subtitle(draw, ["AI tools giúp streamline content creation", "TTS + Video + Auto-post + Content gen"])
    draw_footer(draw, "AI · STREAMLINE · AUTOMATE", ACCENT_BLUE)
    return img

# === Scene 8: Takeaway ===
def scene8():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "TAKEAWAY", ACCENT_ORANGE)
    title_font = font(64, bold=True)
    lines = ["Tình yêu", "không phải lúc nào", "ở cử chỉ lớn"]
    y = 250
    for i, line in enumerate(lines):
        color = ACCENT_ORANGE if i == 0 else TEXT_WHITE
        center_text(draw, line, title_font, y, fill=color)
        y += 85
    sub_font = font(42, bold=True)
    center_text(draw, "Đôi khi, nó nằm", sub_font, y + 10, fill=ACCENT_YELLOW)
    center_text(draw, "trong bát cơm", sub_font, y + 65, fill=ACCENT_YELLOW)
    center_text(draw, "bạn nấu cho partner", sub_font, y + 120, fill=ACCENT_YELLOW)
    # Hash card
    y_hash = y + 210
    draw.rounded_rectangle([80, y_hash, W - 80, y_hash + 220], radius=18, outline=ACCENT_ORANGE, width=3, fill=(25, 18, 12))
    hash_font = font(38, bold=True)
    center_text(draw, "youtube.com/@thientienvlog8821", hash_font, y_hash + 30, fill=ACCENT_ORANGE)
    center_text(draw, "#ViralVideo #FamilyVlog #DomesticCare", hash_font, y_hash + 100, fill=ACCENT_GREEN)
    center_text(draw, "#ContentCreator #AItools", hash_font, y_hash + 160, fill=ACCENT_BLUE)
    draw_subtitle(draw, ["Tình yêu = bát cơm bạn nấu cho partner", "Follow kênh để cập nhật AI tools!"])
    draw_footer(draw, "FOLLOW FOR MORE", ACCENT_ORANGE)
    return img

# Render all 8
for i, fn in enumerate([scene1, scene2, scene3, scene4, scene5, scene6, scene7, scene8], 1):
    img = fn()
    out = os.path.join(OUT_DIR, f"s{i}.png")
    img.save(out, "PNG")
    print(f"  s{i}.png saved")

print(f"\nAll 8 frames in: {OUT_DIR}")
