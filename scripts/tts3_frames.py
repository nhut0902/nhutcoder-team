#!/home/z/.venv/bin/python3
"""Render 12 PIL frames for Top 3 TTS tools video.
Screenshots TO (large), icons, background gradient, Vietnamese subtitles."""
import os, json
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/z/my-project/download/tts3_frames"
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

def paste_shot(img, path, max_w, max_h, y_start, border_color=(100, 200, 255)):
    shot = Image.open(path).convert("RGB")
    sw, sh = shot.size
    scale = min(max_w / sw, max_h / sh)
    new_w = int(sw * scale)
    new_h = int(sh * scale)
    shot_resized = shot.resize((new_w, new_h), Image.LANCZOS)
    x = (W - new_w) // 2
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x-6, y_start-6, x+new_w+6, y_start+new_h+6], radius=14, fill=(15, 20, 35), outline=border_color, width=4)
    img.paste(shot_resized, (x, y_start))

# Purple/pink theme (TTS/audio vibe)
BG_TOP = (20, 10, 35)
BG_BOTTOM = (8, 5, 18)
ACCENT_PURPLE = (180, 100, 240)
ACCENT_PINK = (255, 100, 180)
ACCENT_CYAN = (0, 220, 200)
ACCENT_YELLOW = (250, 200, 80)
ACCENT_GREEN = (80, 220, 130)
ACCENT_BLUE = (100, 160, 255)
ACCENT_ORANGE = (255, 150, 50)
TEXT_WHITE = (245, 240, 255)
TEXT_DIM = (170, 160, 190)

SHOTS = "/home/z/my-project/download/tts3_shots"

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
    sub_font = font(36)
    y = y_start
    for line in lines:
        center_text(draw, line, sub_font, y, fill=TEXT_WHITE)
        y += 50

# === Scene 1: Hook ===
def scene1():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🎙️ TOP 3 TTS VOICE CLONING", ACCENT_PINK)
    # Big icons
    icon_font = font(180)
    center_text(draw, "🎙️🔧🎤", icon_font, 230, fill=TEXT_WHITE)
    # Title
    title_font = font(90, bold=True)
    center_text(draw, "Top 3 Công Cụ", title_font, 480, fill=ACCENT_PINK)
    center_text(draw, "TTS Voice Cloning", title_font, 580, fill=ACCENT_CYAN)
    center_text(draw, "Open Source 2026", font(48, bold=True), 690, fill=TEXT_DIM)
    # Stats card
    y = 800
    draw.rounded_rectangle([80, y, W - 80, y + 380], radius=20, outline=ACCENT_PURPLE, width=3, fill=(20, 15, 35))
    stat_font = font(56, bold=True)
    desc_font = font(36)
    draw.text((120, y + 30), "🥇 Real-Time-Voice-Cloning", font=stat_font, fill=ACCENT_YELLOW)
    draw.text((120, y + 95), "   59,986 stars", font=desc_font, fill=TEXT_WHITE)
    draw.text((120, y + 155), "🥈 GPT-SoVITS", font=stat_font, fill=ACCENT_CYAN)
    draw.text((120, y + 220), "   59,488 stars", font=desc_font, fill=TEXT_WHITE)
    draw.text((120, y + 280), "🥉 OpenVoice", font=stat_font, fill=ACCENT_ORANGE)
    draw.text((120, y + 345), "   36,873 stars", font=desc_font, fill=TEXT_WHITE)
    draw_subtitle(draw, ["Top 3 công cụ TTS voice cloning open source", "hot nhất 2026 trên GitHub"])
    draw_footer(draw, "OPEN SOURCE · MIT LICENSE", ACCENT_PINK)
    return img

# === Scene 2: #1 RTVC intro ===
def scene2():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥇 #1 REAL-TIME-VOICE-CLONING", ACCENT_YELLOW)
    # Big rank
    rank_font = font(200, bold=True)
    center_text(draw, "#1", rank_font, 200, fill=ACCENT_YELLOW)
    # Title
    title_font = font(56, bold=True)
    center_text(draw, "Real-Time-Voice-Cloning", title_font, 430, fill=TEXT_WHITE)
    center_text(draw, "59,986 ⭐ · 11K forks", font(40), 500, fill=ACCENT_YELLOW)
    # Screenshot TO
    paste_shot(img, f"{SHOTS}/rtvc_01_title.png", max_w=1000, max_h=250, y_start=580, border_color=ACCENT_YELLOW)
    # Feature card
    y = 870
    draw.rounded_rectangle([80, y, W - 80, y + 280], radius=14, outline=ACCENT_YELLOW, width=2, fill=(25, 20, 15))
    draw.text((110, y + 20), "✨ Đặc điểm nổi bật:", font=font(38, bold=True), fill=ACCENT_YELLOW)
    draw.text((110, y + 75), "• Clone giọng trong 5 giây", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 125), "• Generate speech real-time", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 175), "• Transfer Learning based", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 225), "• Python · MIT License", font=font(36), fill=TEXT_WHITE)
    draw_subtitle(draw, ["#1 Real-Time-Voice-Cloning - 60K sao", "Clone giọng chỉ trong 5 giây!"])
    draw_footer(draw, "5-SECOND CLONE · REAL-TIME", ACCENT_YELLOW)
    return img

# === Scene 3: RTVC README ===
def scene3():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥇 RTVC · CODE STRUCTURE", ACCENT_YELLOW)
    # Screenshot TO
    paste_shot(img, f"{SHOTS}/rtvc_03_files.png", max_w=1000, max_h=600, y_start=200, border_color=ACCENT_YELLOW)
    # Architecture card
    y = 850
    draw.rounded_rectangle([80, y, W - 80, y + 320], radius=14, outline=ACCENT_YELLOW, width=2, fill=(25, 20, 15))
    draw.text((110, y + 20), "🏗️ Architecture:", font=font(38, bold=True), fill=ACCENT_YELLOW)
    draw.text((110, y + 80), "• Encoder-Encoder-Decoder", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 130), "• Speaker encoder + Synthesizer", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 180), "• Vocoder (WaveRNN/DeepVoice)", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 230), "• Pre-trained weights available", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 280), "• Runs on CPU (no GPU needed)", font=font(36), fill=ACCENT_GREEN)
    draw_subtitle(draw, ["Architecture: encoder-decoder + vocoder", "Chạy được trên CPU, không cần GPU"])
    draw_footer(draw, "ENCODER · DECODER · VOCODER", ACCENT_YELLOW)
    return img

# === Scene 4: RTVC README detail ===
def scene4():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥇 RTVC · README", ACCENT_YELLOW)
    paste_shot(img, f"{SHOTS}/rtvc_04_readme.png", max_w=1000, max_h=700, y_start=200, border_color=ACCENT_YELLOW)
    # Info card
    y = 930
    draw.rounded_rectangle([80, y, W - 80, y + 240], radius=14, outline=ACCENT_YELLOW, width=2, fill=(25, 20, 15))
    draw.text((110, y + 20), "📦 Cài đặt:", font=font(38, bold=True), fill=ACCENT_YELLOW)
    draw.text((110, y + 75), "git clone github.com/CorentinJ/", font=font(34, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 120), "  Real-Time-Voice-Cloning", font=font(34, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 170), "pip install -r requirements.txt", font=font(34, bold=True), fill=ACCENT_GREEN)
    draw_subtitle(draw, ["Cài đặt đơn giản: clone + pip install", "Download pre-trained weights là chạy được"])
    draw_footer(draw, "EASY SETUP · Python · MIT", ACCENT_YELLOW)
    return img

# === Scene 5: #2 GPT-SoVITS intro ===
def scene5():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥈 #2 GPT-SoVITS", ACCENT_CYAN)
    rank_font = font(200, bold=True)
    center_text(draw, "#2", rank_font, 200, fill=ACCENT_CYAN)
    title_font = font(60, bold=True)
    center_text(draw, "GPT-SoVITS", title_font, 430, fill=TEXT_WHITE)
    center_text(draw, "59,488 ⭐ · 13K forks", font(40), 500, fill=ACCENT_CYAN)
    paste_shot(img, f"{SHOTS}/gptsovits_01_title.png", max_w=1000, max_h=250, y_start=580, border_color=ACCENT_CYAN)
    # Feature card
    y = 870
    draw.rounded_rectangle([80, y, W - 80, y + 280], radius=14, outline=ACCENT_CYAN, width=2, fill=(15, 25, 30))
    draw.text((110, y + 20), "✨ Đặc điểm nổi bật:", font=font(38, bold=True), fill=ACCENT_CYAN)
    draw.text((110, y + 75), "• 1 phút data → train TTS tốt!", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 125), "• Few-shot voice cloning", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 175), "• GPT + SoVITS architecture", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 225), "• WebUI Gradio tích hợp", font=font(36), fill=TEXT_WHITE)
    draw_subtitle(draw, ["#2 GPT-SoVITS - 59K sao", "Chỉ 1 phút data là train được TTS!"])
    draw_footer(draw, "1-MIN DATA · FEW-SHOT CLONE", ACCENT_CYAN)
    return img

# === Scene 6: GPT-SoVITS features ===
def scene6():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥈 GPT-SoVITS · FEATURES", ACCENT_CYAN)
    paste_shot(img, f"{SHOTS}/gptsovits_04_readme.png", max_w=1000, max_h=600, y_start=200, border_color=ACCENT_CYAN)
    # Features
    y = 850
    draw.rounded_rectangle([80, y, W - 80, y + 320], radius=14, outline=ACCENT_CYAN, width=2, fill=(15, 25, 30))
    draw.text((110, y + 20), "🌐 Đa ngôn ngữ:", font=font(38, bold=True), fill=ACCENT_CYAN)
    draw.text((110, y + 80), "• Trung · Anh · Nhật · Hàn · Việt", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 135), "🎙️ Tích hợp:", font=font(38, bold=True), fill=ACCENT_CYAN)
    draw.text((110, y + 190), "• Text-to-Speech", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 235), "• Speech-to-Speech · Voice Conversion", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 285), "• Real-time inference", font=font(36), fill=TEXT_WHITE)
    draw_subtitle(draw, ["Support: Trung, Anh, Nhật, Hàn, Việt", "TTS + STS + Voice Conversion + Real-time"])
    draw_footer(draw, "MULTI-LANG · WEBUI · REAL-TIME", ACCENT_CYAN)
    return img

# === Scene 7: GPT-SoVITS code ===
def scene7():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥈 GPT-SoVITS · CODE", ACCENT_CYAN)
    paste_shot(img, f"{SHOTS}/gptsovits_03_files.png", max_w=1000, max_h=600, y_start=200, border_color=ACCENT_CYAN)
    # Install
    y = 850
    draw.rounded_rectangle([80, y, W - 80, y + 280], radius=14, outline=ACCENT_CYAN, width=2, fill=(15, 25, 30))
    draw.text((110, y + 20), "📦 Cài đặt:", font=font(38, bold=True), fill=ACCENT_CYAN)
    draw.text((110, y + 75), "git clone github.com/RVC-Boss/", font=font(34, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 120), "  GPT-SoVITS", font=font(34, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 170), "pip install -r requirements.txt", font=font(34, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 220), "python webui.py  # Gradio WebUI", font=font(34, bold=True), fill=ACCENT_GREEN)
    draw_subtitle(draw, ["Cài đặt + chạy WebUI Gradio", "Repo RVC-Boss/GPT-SoVITS, Python, MIT"])
    draw_footer(draw, "WEBUI · GRADIO · MIT", ACCENT_CYAN)
    return img

# === Scene 8: #3 OpenVoice intro ===
def scene8():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥉 #3 OPENVOICE", ACCENT_ORANGE)
    rank_font = font(200, bold=True)
    center_text(draw, "#3", rank_font, 200, fill=ACCENT_ORANGE)
    title_font = font(60, bold=True)
    center_text(draw, "OpenVoice", title_font, 430, fill=TEXT_WHITE)
    center_text(draw, "36,873 ⭐ · 3.5K forks", font(40), 500, fill=ACCENT_ORANGE)
    center_text(draw, "by MIT & MyShell", font(36), 550, fill=TEXT_DIM)
    paste_shot(img, f"{SHOTS}/openvoice_01_title.png", max_w=1000, max_h=250, y_start=620, border_color=ACCENT_ORANGE)
    # Feature card
    y = 900
    draw.rounded_rectangle([80, y, W - 80, y + 250], radius=14, outline=ACCENT_ORANGE, width=2, fill=(30, 22, 18))
    draw.text((110, y + 20), "✨ Đặc điểm:", font=font(38, bold=True), fill=ACCENT_ORANGE)
    draw.text((110, y + 75), "• Zero-shot cloning (không train!)", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 125), "• Cross-lingual voice cloning", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 175), "• Granular style control", font=font(36), fill=TEXT_WHITE)
    draw_subtitle(draw, ["#3 OpenVoice - 37K sao", "Zero-shot, cross-lingual, style control"])
    draw_footer(draw, "ZERO-SHOT · CROSS-LINGUAL", ACCENT_ORANGE)
    return img

# === Scene 9: OpenVoice features ===
def scene9():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥉 OPENVOICE · FEATURES", ACCENT_ORANGE)
    paste_shot(img, f"{SHOTS}/openvoice_04_readme.png", max_w=1000, max_h=700, y_start=200, border_color=ACCENT_ORANGE)
    # Features
    y = 930
    draw.rounded_rectangle([80, y, W - 80, y + 240], radius=14, outline=ACCENT_ORANGE, width=2, fill=(30, 22, 18))
    draw.text((110, y + 20), "🎯 Style Control:", font=font(38, bold=True), fill=ACCENT_ORANGE)
    draw.text((110, y + 75), "• Control tone (happy, sad, angry)", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 125), "• Control emotion & accent", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 175), "• Commercial use allowed", font=font(36), fill=ACCENT_GREEN)
    draw_subtitle(draw, ["Control tone, emotion, accent", "Zero-shot - không cần train model"])
    draw_footer(draw, "STYLE CONTROL · COMMERCIAL OK", ACCENT_ORANGE)
    return img

# === Scene 10: OpenVoice code ===
def scene10():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥉 OPENVOICE · CODE", ACCENT_ORANGE)
    paste_shot(img, f"{SHOTS}/openvoice_03_files.png", max_w=1000, max_h=600, y_start=200, border_color=ACCENT_ORANGE)
    # Install
    y = 850
    draw.rounded_rectangle([80, y, W - 80, y + 280], radius=14, outline=ACCENT_ORANGE, width=2, fill=(30, 22, 18))
    draw.text((110, y + 20), "📦 Cài đặt:", font=font(38, bold=True), fill=ACCENT_ORANGE)
    draw.text((110, y + 75), "git clone github.com/myshell-ai/", font=font(34, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 120), "  OpenVoice", font=font(34, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 170), "pip install -r requirements.txt", font=font(34, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 220), "Audio foundation model · MIT", font=font(34, bold=True), fill=ACCENT_ORANGE)
    draw_subtitle(draw, ["Cài đặt: clone + pip install", "Audio foundation model, MIT license"])
    draw_footer(draw, "FOUNDATION MODEL · MIT", ACCENT_ORANGE)
    return img

# === Scene 11: Comparison ===
def scene11():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "📊 SO SÁNH 3 CÔNG CỤ", ACCENT_PURPLE)
    title_font = font(64, bold=True)
    center_text(draw, "So sánh", title_font, 200, fill=TEXT_WHITE)
    # Comparison table
    y = 310
    headers = ["Tool", "Stars", "Đặc điểm"]
    draw.text((100, y), headers[0], font=font(32, bold=True), fill=TEXT_DIM)
    draw.text((350, y), headers[1], font=font(32, bold=True), fill=TEXT_DIM)
    draw.text((600, y), headers[2], font=font(32, bold=True), fill=TEXT_DIM)
    y += 55
    rows = [
        ("🥇 RTVC", "60K", "Đơn giản nhất", ACCENT_YELLOW),
        ("🥈 GPT-SoVITS", "59K", "Chất lượng cao nhất", ACCENT_CYAN),
        ("🥉 OpenVoice", "37K", "Nhanh nhất (zero-shot)", ACCENT_ORANGE),
    ]
    for tool, stars, desc, color in rows:
        draw.rounded_rectangle([80, y, W - 80, y + 140], radius=12, outline=color, width=2, fill=(20, 15, 35))
        draw.text((100, y + 35), tool, font=font(36, bold=True), fill=color)
        draw.text((350, y + 40), stars, font=font(36, bold=True), fill=TEXT_WHITE)
        draw.text((600, y + 40), desc, font=font(32), fill=TEXT_WHITE)
        y += 160
    # Verdict card
    y += 30
    draw.rounded_rectangle([80, y, W - 80, y + 200], radius=14, outline=ACCENT_GREEN, width=3, fill=(20, 30, 25))
    draw.text((110, y + 20), "💡 Tùy use case:", font=font(38, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 80), "• Mới bắt đầu → RTVC", font=font(34), fill=TEXT_WHITE)
    draw.text((110, y + 130), "• Chất lượng cao → GPT-SoVITS", font=font(34), fill=TEXT_WHITE)
    draw.text((110, y + 180), "• Nhanh + zero-shot → OpenVoice", font=font(34), fill=TEXT_WHITE)
    draw_subtitle(draw, ["So sánh: RTVC đơn giản, GPT-SoVITS chất lượng", "OpenVoice nhanh nhất với zero-shot"])
    draw_footer(draw, "CHOOSE YOUR TOOL", ACCENT_PURPLE)
    return img

# === Scene 12: Takeaway ===
def scene12():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "TAKEAWAY", ACCENT_GREEN)
    title_font = font(70, bold=True)
    center_text(draw, "3 công cụ", title_font, 220, fill=TEXT_WHITE)
    center_text(draw, "TTS voice cloning", title_font, 300, fill=ACCENT_GREEN)
    center_text(draw, "open source", title_font, 380, fill=ACCENT_GREEN)
    # Icons
    icon_font = font(120)
    center_text(draw, "🎙️  🔧  🎤", icon_font, 500, fill=TEXT_WHITE)
    # Links card
    y_hash = 700
    draw.rounded_rectangle([80, y_hash, W - 80, y_hash + 400], radius=18, outline=ACCENT_PURPLE, width=3, fill=(18, 12, 28))
    hash_font = font(36, bold=True)
    center_text(draw, "github.com/CorentinJ/", hash_font, y_hash + 30, fill=ACCENT_YELLOW)
    center_text(draw, "  Real-Time-Voice-Cloning", hash_font, y_hash + 75, fill=ACCENT_YELLOW)
    center_text(draw, "github.com/RVC-Boss/GPT-SoVITS", hash_font, y_hash + 130, fill=ACCENT_CYAN)
    center_text(draw, "github.com/myshell-ai/OpenVoice", hash_font, y_hash + 185, fill=ACCENT_ORANGE)
    center_text(draw, "", hash_font, y_hash + 240, fill=TEXT_WHITE)
    center_text(draw, "#TTS #VoiceCloning #OpenSource", hash_font, y_hash + 290, fill=ACCENT_GREEN)
    center_text(draw, "#AI2026 #Python #MIT", hash_font, y_hash + 340, fill=ACCENT_PURPLE)
    draw_subtitle(draw, ["Cả 3 đều open source, MIT, chạy local", "Follow kênh để cập nhật AI tools!"])
    draw_footer(draw, "FOLLOW FOR MORE", ACCENT_GREEN)
    return img

# Render all 12
for i, fn in enumerate([scene1, scene2, scene3, scene4, scene5, scene6, scene7, scene8, scene9, scene10, scene11, scene12], 1):
    img = fn()
    out = os.path.join(OUT_DIR, f"s{i}.png")
    img.save(out, "PNG")
    print(f"  s{i}.png saved")

print(f"\nAll 12 frames in: {OUT_DIR}")
