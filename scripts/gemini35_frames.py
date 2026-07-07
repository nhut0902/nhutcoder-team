#!/home/z/.venv/bin/python3
"""Render 12 PIL frames for Gemini 3.5 Pro comparison video.
Uses 4 original images + 4 blog screenshots + comparison tables + icons."""
import os, json
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/z/my-project/download/gemini35_frames"
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

def paste_shot(img, path, max_w, max_h, y_start, border_color=(100, 160, 255)):
    shot = Image.open(path).convert("RGB")
    sw, sh = shot.size
    scale = min(max_w / sw, max_h / sh)
    new_w = int(sw * scale)
    new_h = int(sh * scale)
    shot_resized = shot.resize((new_w, new_h), Image.LANCZOS)
    x = (W - new_w) // 2
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x-6, y_start-6, x+new_w+6, y_start+new_h+6], radius=14, fill=(10, 15, 30), outline=border_color, width=4)
    img.paste(shot_resized, (x, y_start))

# Google blue/teal theme
BG_TOP = (8, 20, 40)
BG_BOTTOM = (4, 10, 22)
ACCENT_BLUE = (66, 133, 244)
ACCENT_GREEN = (52, 168, 83)
ACCENT_YELLOW = (251, 188, 4)
ACCENT_RED = (234, 67, 53)
ACCENT_CYAN = (0, 200, 220)
ACCENT_PURPLE = (155, 110, 220)
ACCENT_ORANGE = (255, 140, 50)
TEXT_WHITE = (245, 245, 250)
TEXT_DIM = (160, 165, 180)

IMGS = "/home/z/my-project/download/gemini35_imgs"
BLOG = "/home/z/my-project/download/gemini35_blog_shots"

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

def draw_card(draw, y, icon, title, desc, color):
    draw.rounded_rectangle([80, y, W - 80, y + 150], radius=14, outline=color, width=2, fill=(15, 22, 40))
    draw.text((110, y + 30), icon, font=font(56), fill=TEXT_WHITE)
    draw.text((200, y + 25), title, font=font(42, bold=True), fill=color)
    draw.text((200, y + 80), desc, font=font(34), fill=TEXT_DIM)

# === Scene 1: Hook ===
def scene1():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🚀 GEMINI 3.5 PRO", ACCENT_BLUE)
    center_text(draw, "✨", font(180), 200, fill=TEXT_WHITE)
    title_font = font(120, bold=True)
    center_text(draw, "Gemini", title_font, 400, fill=ACCENT_BLUE)
    center_text(draw, "3.5 Pro", title_font, 520, fill=ACCENT_GREEN)
    sub_font = font(48, bold=True)
    center_text(draw, "2M Token Context", sub_font, 660, fill=ACCENT_YELLOW)
    center_text(draw, "Deep Think Mode", sub_font, 720, fill=ACCENT_CYAN)
    center_text(draw, "by Google DeepMind", font(38), 790, fill=TEXT_DIM)
    # Stats card
    y = 880
    draw.rounded_rectangle([80, y, W - 80, y + 320], radius=20, outline=ACCENT_BLUE, width=3, fill=(10, 18, 35))
    stat_font = font(80, bold=True)
    desc_font = font(34)
    draw.text((130, y + 20), "2M tokens", font=stat_font, fill=ACCENT_YELLOW)
    draw.text((130, y + 110), "context window (largest!)", font=desc_font, fill=TEXT_WHITE)
    draw.text((130, y + 170), "Deep Think", font=stat_font, fill=ACCENT_GREEN)
    draw.text((130, y + 260), "reasoning mode", font=desc_font, fill=TEXT_WHITE)
    draw_subtitle(draw, ["Gemini 3.5 Pro - flagship mới nhất Google", "2M token context, Deep Think Mode"])
    draw_footer(draw, "GOOGLE DEEPMIND · 2M CONTEXT", ACCENT_BLUE)
    return img

# === Scene 2: Original image 1 ===
def scene2():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "OFFICIAL ANNOUNCEMENT", ACCENT_GREEN)
    title_font = font(56, bold=True)
    center_text(draw, "Announced: 19/5/2026", title_font, 200, fill=TEXT_WHITE)
    center_text(draw, "GA: July 2026", font(42), 270, fill=ACCENT_GREEN)
    # Original image
    paste_shot(img, f"{IMGS}/gemini35_google_deepmind.jpg", max_w=1000, max_h=500, y_start=340, border_color=ACCENT_GREEN)
    # Info card
    y = 900
    draw.rounded_rectangle([80, y, W - 80, y + 280], radius=14, outline=ACCENT_GREEN, width=2, fill=(10, 20, 15))
    draw.text((110, y + 20), "📋 Thông tin:", font=font(38, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 80), "• Vertex AI Enterprise Preview", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 130), "• Model ID: gemini-3.5-pro-preview-06", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 180), "• Multimodal: text + image + video + audio", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 230), "• thinkingLevel: minimal → high", font=font(36), fill=TEXT_WHITE)
    draw_subtitle(draw, ["Công bố 19/5/2026, GA July 2026", "Vertex AI Enterprise Preview"])
    draw_footer(draw, "VERTEX AI · PREVIEW", ACCENT_GREEN)
    return img

# === Scene 3: Specs ===
def scene3():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "THÔNG SỐ KỸ THUẬT", ACCENT_YELLOW)
    title_font = font(68, bold=True)
    center_text(draw, "Specs", title_font, 220, fill=TEXT_WHITE)
    specs = [
        ("🧠", "2M tokens", "context window (largest!)", ACCENT_YELLOW),
        ("🔬", "Deep Think", "opt-in reasoning mode", ACCENT_GREEN),
        ("📊", "Multimodal", "text + image + video + audio", ACCENT_BLUE),
        ("⚙️", "thinkingLevel", "minimal → low → medium → high", ACCENT_PURPLE),
        ("💰", "~$15/1M", "input tokens (est.)", ACCENT_ORANGE),
    ]
    y = 340
    for icon, title, desc, color in specs:
        draw_card(draw, y, icon, title, desc, color)
        y += 170
    draw_subtitle(draw, ["2M context, Deep Think, Multimodal", "thinkingLevel: minimal → high"])
    draw_footer(draw, "2M · DEEP THINK · MULTIMODAL", ACCENT_YELLOW)
    return img

# === Scene 4: Deep Think ===
def scene4():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "DEEP THINK MODE", ACCENT_PURPLE)
    title_font = font(68, bold=True)
    center_text(draw, "Deep Think", title_font, 220, fill=ACCENT_PURPLE)
    center_text(draw, "🔬", font(180), 320, fill=TEXT_WHITE)
    # Description card
    y = 560
    draw.rounded_rectangle([80, y, W - 80, y + 420], radius=18, outline=ACCENT_PURPLE, width=3, fill=(18, 12, 30))
    draw.text((110, y + 20), "Tính năng:", font=font(38, bold=True), fill=ACCENT_PURPLE)
    draw.text((110, y + 80), "• Opt-in reasoning mode", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 135), "• Cho scientific, math, coding", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 190), "• Trade latency → accuracy", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 245), "• thinkingLevel config:", font=font(36), fill=ACCENT_GREEN)
    draw.text((110, y + 300), "  minimal · low · medium · high", font=font(36, bold=True), fill=ACCENT_YELLOW)
    draw.text((110, y + 360), "• Reasoning tokens = output rate", font=font(34), fill=TEXT_DIM)
    draw_subtitle(draw, ["Deep Think: reasoning mode cho science + math", "thinkingLevel: minimal → high"])
    draw_footer(draw, "REASONING · LATENCY ↔ ACCURACY", ACCENT_PURPLE)
    return img

# === Scene 5: Pricing blog screenshot ===
def scene5():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "PRICING", ACCENT_ORANGE)
    title_font = font(60, bold=True)
    center_text(draw, "Google AI Pricing", title_font, 200, fill=TEXT_WHITE)
    # Blog screenshot
    paste_shot(img, f"{BLOG}/04_pricing.png", max_w=1000, max_h=650, y_start=300, border_color=ACCENT_ORANGE)
    # Price card
    y = 980
    draw.rounded_rectangle([80, y, W - 80, y + 200], radius=14, outline=ACCENT_ORANGE, width=2, fill=(30, 22, 18))
    draw.text((110, y + 20), "💰 Ước tính:", font=font(38, bold=True), fill=ACCENT_ORANGE)
    draw.text((110, y + 80), "~$15/1M input tokens", font=font(40, bold=True), fill=ACCENT_YELLOW)
    draw.text((110, y + 140), "8-10x Gemini 3.5 Flash", font=font(34), fill=TEXT_DIM)
    draw_subtitle(draw, ["~$15/1M tokens, đắt 8-10x Flash", "Reasoning tokens billed at output rate"])
    draw_footer(draw, "PRICING · ESTIMATED", ACCENT_ORANGE)
    return img

# === Scene 6: Comparison blog screenshot ===
def scene6():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "VS OTHER MODELS", ACCENT_RED)
    title_font = font(56, bold=True)
    center_text(draw, "Gemini 3.5 Pro vs", title_font, 200, fill=TEXT_WHITE)
    center_text(draw, "GPT-5.6 · Claude · Kimi", title_font, 270, fill=ACCENT_RED)
    # Blog screenshot
    paste_shot(img, f"{BLOG}/01_comparison_blog.png", max_w=1000, max_h=600, y_start=360, border_color=ACCENT_RED)
    # Verdict
    y = 1000
    draw.rounded_rectangle([80, y, W - 80, y + 180], radius=14, outline=ACCENT_GREEN, width=2, fill=(15, 25, 20))
    draw.text((110, y + 20), "💡 Verdict:", font=font(38, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 80), "Gemini 3.5 Pro = price-performance leader", font=font(34), fill=TEXT_WHITE)
    draw.text((110, y + 130), "2M context = vua của RAG", font=font(34), fill=ACCENT_YELLOW)
    draw_subtitle(draw, ["So sánh: Gemini 3.5 Pro vs GPT-5.6 vs Claude", "Price-performance leader, 2M context cho RAG"])
    draw_footer(draw, "COMPARISON · FRONTIER MODELS", ACCENT_RED)
    return img

# === Scene 7: GPT-5.6 ===
def scene7():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥇 GPT-5.6 SOL ULTRA", ACCENT_YELLOW)
    rank_font = font(180, bold=True)
    center_text(draw, "🥇", rank_font, 200, fill=TEXT_WHITE)
    title_font = font(56, bold=True)
    center_text(draw, "GPT-5.6 Sol Ultra", title_font, 420, fill=ACCENT_YELLOW)
    center_text(draw, "Coding Leader", font(42), 490, fill=TEXT_WHITE)
    # Stats card
    y = 570
    draw.rounded_rectangle([80, y, W - 80, y + 380], radius=18, outline=ACCENT_YELLOW, width=3, fill=(25, 20, 15))
    big_font = font(120, bold=True)
    center_text(draw, "91.9%", big_font, y + 30, fill=ACCENT_YELLOW)
    center_text(draw, "Terminal-Bench 2.1", font(42, bold=True), y + 170, fill=TEXT_WHITE)
    draw.text((110, y + 240), "• Coding benchmark leader", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 290), "• Restricted preview only", font=font(36), fill=ACCENT_RED)
    draw.text((110, y + 340), "• $5/$30 per 1M tokens", font=font(36), fill=TEXT_WHITE)
    draw_subtitle(draw, ["GPT-5.6 Sol Ultra: coding leader 91.9%", "Nhưng restricted preview, chưa GA"])
    draw_footer(draw, "CODING LEADER · RESTRICTED", ACCENT_YELLOW)
    return img

# === Scene 8: Claude Fable 5 ===
def scene8():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥈 CLAUDE FABLE 5", ACCENT_PURPLE)
    rank_font = font(180, bold=True)
    center_text(draw, "🥈", rank_font, 200, fill=TEXT_WHITE)
    title_font = font(56, bold=True)
    center_text(draw, "Claude Fable 5", title_font, 420, fill=ACCENT_PURPLE)
    center_text(draw, "Agentic Leader", font(42), 490, fill=TEXT_WHITE)
    # Stats card
    y = 570
    draw.rounded_rectangle([80, y, W - 80, y + 380], radius=18, outline=ACCENT_PURPLE, width=3, fill=(20, 15, 30))
    big_font = font(100, bold=True)
    center_text(draw, "1M tokens", big_font, y + 30, fill=ACCENT_PURPLE)
    center_text(draw, "context window", font(42, bold=True), y + 140, fill=TEXT_WHITE)
    draw.text((110, y + 210), "• Production-grade agentic", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 260), "• $10/$50 per 1M tokens", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 310), "• Suspended → returning soon", font=font(36), fill=ACCENT_ORANGE)
    draw.text((110, y + 360), "• SWE-Bench Pro: 80.3", font=font(36), fill=TEXT_WHITE)
    draw_subtitle(draw, ["Claude Fable 5: agentic leader, 1M context", "Đang suspend, sắp return"])
    draw_footer(draw, "AGENTIC · PRODUCTION-GRADE", ACCENT_PURPLE)
    return img

# === Scene 9: Kimi K2.7 ===
def scene9():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "🥉 KIMI K2.7 CODE", ACCENT_CYAN)
    rank_font = font(180, bold=True)
    center_text(draw, "🥉", rank_font, 200, fill=TEXT_WHITE)
    title_font = font(56, bold=True)
    center_text(draw, "Kimi K2.7 Code", title_font, 420, fill=ACCENT_CYAN)
    center_text(draw, "Efficiency Leader", font(42), 490, fill=TEXT_WHITE)
    # Stats card
    y = 570
    draw.rounded_rectangle([80, y, W - 80, y + 380], radius=18, outline=ACCENT_CYAN, width=3, fill=(15, 22, 30))
    big_font = font(100, bold=True)
    center_text(draw, "-30%", big_font, y + 30, fill=ACCENT_CYAN)
    center_text(draw, "thinking tokens vs K2.6", font(36, bold=True), y + 140, fill=TEXT_WHITE)
    draw.text((110, y + 210), "• 1T params MoE (32B active)", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 260), "• 256K context window", font=font(36), fill=TEXT_WHITE)
    draw.text((110, y + 310), "• Open-source, MIT license", font=font(36), fill=ACCENT_GREEN)
    draw.text((110, y + 360), "• Forces thinking mode", font=font(36), fill=TEXT_WHITE)
    draw_subtitle(draw, ["Kimi K2.7: efficiency leader, -30% thinking", "1T MoE, open-source, MIT"])
    draw_footer(draw, "EFFICIENT · OPEN SOURCE", ACCENT_CYAN)
    return img

# === Scene 10: Comparison table ===
def scene10():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "📊 TỔNG SO SÁNH", ACCENT_BLUE)
    title_font = font(64, bold=True)
    center_text(draw, "So sánh 4 model", title_font, 200, fill=TEXT_WHITE)
    # Table header
    y = 300
    headers = ["Model", "Context", "Điểm mạnh"]
    draw.text((100, y), headers[0], font=font(30, bold=True), fill=TEXT_DIM)
    draw.text((380, y), headers[1], font=font(30, bold=True), fill=TEXT_DIM)
    draw.text((700, y), headers[2], font=font(30, bold=True), fill=TEXT_DIM)
    y += 50
    rows = [
        ("🔵 Gemini 3.5 Pro", "2M", "Context + RAG", ACCENT_BLUE),
        ("🟡 GPT-5.6 Sol", "—", "Coding 91.9%", ACCENT_YELLOW),
        ("🟣 Claude Fable 5", "1M", "Agentic", ACCENT_PURPLE),
        ("🟢 Kimi K2.7", "256K", "Efficient", ACCENT_CYAN),
    ]
    for model, ctx, strength, color in rows:
        draw.rounded_rectangle([80, y, W - 80, y + 140], radius=12, outline=color, width=2, fill=(12, 18, 35))
        draw.text((100, y + 35), model, font=font(34, bold=True), fill=color)
        draw.text((380, y + 40), ctx, font=font(36, bold=True), fill=TEXT_WHITE)
        draw.text((700, y + 40), strength, font=font(32), fill=TEXT_WHITE)
        y += 160
    # Winner card
    y += 20
    draw.rounded_rectangle([80, y, W - 80, y + 200], radius=14, outline=ACCENT_GREEN, width=3, fill=(15, 25, 20))
    draw.text((110, y + 20), "🏆 Mỗi model đều có thế mạnh riêng!", font=font(36, bold=True), fill=ACCENT_GREEN)
    draw.text((110, y + 80), "RAG → Gemini · Coding → GPT-5.6", font=font(32), fill=TEXT_WHITE)
    draw.text((110, y + 130), "Agentic → Claude · Efficient → Kimi", font=font(32), fill=TEXT_WHITE)
    draw_subtitle(draw, ["Gemini 3.5 Pro: context + price leader", "GPT-5.6: coding, Claude: agentic, Kimi: efficient"])
    draw_footer(draw, "CHOOSE YOUR MODEL", ACCENT_BLUE)
    return img

# === Scene 11: Use case guide ===
def scene11():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "💡 KHI NÀO DÙNG GÌ?", ACCENT_GREEN)
    title_font = font(64, bold=True)
    center_text(draw, "Choose Your Model", title_font, 200, fill=TEXT_WHITE)
    cases = [
        ("📚", "RAG + tài liệu dài", "→ Gemini 3.5 Pro (2M ctx)", ACCENT_BLUE),
        ("💻", "Coding phức tạp", "→ GPT-5.6 Sol (91.9%)", ACCENT_YELLOW),
        ("🤖", "Agentic production", "→ Claude Fable 5", ACCENT_PURPLE),
        ("⚡", "Coding efficient", "→ Kimi K2.7 (-30%)", ACCENT_CYAN),
        ("🔬", "Science + reasoning", "→ Gemini Deep Think", ACCENT_GREEN),
    ]
    y = 320
    for icon, title, desc, color in cases:
        draw_card(draw, y, icon, title, desc, color)
        y += 170
    draw_subtitle(draw, ["RAG→Gemini, Coding→GPT, Agentic→Claude", "Efficient→Kimi, Science→Deep Think"])
    draw_footer(draw, "USE CASE GUIDE", ACCENT_GREEN)
    return img

# === Scene 12: Takeaway ===
def scene12():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, BG_TOP, BG_BOTTOM)
    draw_header(draw, "TAKEAWAY", ACCENT_BLUE)
    title_font = font(70, bold=True)
    lines = ["Gemini 3.5 Pro", "bước tiến", "của Google"]
    y = 230
    for i, line in enumerate(lines):
        color = ACCENT_BLUE if i == 0 else TEXT_WHITE
        center_text(draw, line, title_font, y, fill=color)
        y += 90
    sub_font = font(40)
    center_text(draw, "2M context mở ra khả năng mới", sub_font, y + 10, fill=TEXT_DIM)
    # Hash card
    y_hash = y + 100
    draw.rounded_rectangle([80, y_hash, W - 80, y_hash + 280], radius=18, outline=ACCENT_BLUE, width=3, fill=(10, 15, 30))
    hash_font = font(40, bold=True)
    center_text(draw, "ai.google.dev/gemini-api", hash_font, y_hash + 40, fill=ACCENT_BLUE)
    center_text(draw, "#Gemini35Pro #Google #DeepThink", hash_font, y_hash + 110, fill=ACCENT_GREEN)
    center_text(draw, "#2MContext #AI2026 #Gemini", hash_font, y_hash + 180, fill=ACCENT_YELLOW)
    draw_subtitle(draw, ["Gemini 3.5 Pro - 2M context, Deep Think", "Follow kênh để cập nhật AI!"])
    draw_footer(draw, "FOLLOW FOR MORE", ACCENT_BLUE)
    return img

# Render all 12
for i, fn in enumerate([scene1, scene2, scene3, scene4, scene5, scene6, scene7, scene8, scene9, scene10, scene11, scene12], 1):
    img = fn()
    out = os.path.join(OUT_DIR, f"s{i}.png")
    img.save(out, "PNG")
    print(f"  s{i}.png saved")

print(f"\nAll 12 frames in: {OUT_DIR}")
