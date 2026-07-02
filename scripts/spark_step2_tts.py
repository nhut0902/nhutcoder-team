#!/home/z/.venv/bin/python3
"""Step 2: Generate 2-min Vietnamese TTS narration about Gemini Spark. Upload to sandbox."""
import os, subprocess, json, time
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SBX_ID = open("/tmp/spark_sandbox_id.txt").read().strip()
print(f"=== Connect to sandbox {SBX_ID} ===", flush=True)
sbx = Sandbox.connect(SBX_ID)
sbx.set_timeout(60 * 30)

# 8 scenes ~15s each = 120s
VOICE = "vi-VN-NamMinhNeural"
scenes = [
    {"id": "s1", "text": "Chào các bạn! Hôm nay là ngày 2 tháng 7 năm 2026, và Google vừa tung ra bản cập nhật lớn cho Gemini Spark - trợ lý AI 24/7 mới nhất của họ. Cùng mình tìm hiểu nhé!"},
    {"id": "s2", "text": "Gemini Spark là gì? Đây là AI agent cá nhân hoạt động 24/7 trên cloud Google. Sử dụng Gemini 3.5 kết hợp Antigravity harness, Spark tự động quản lý tác vụ ngay cả khi thiết bị của bạn offline."},
    {"id": "s3", "text": "Bản cập nhật ngày 2 tháng 7 năm 2026 mang đến tính năng beta trên macOS desktop app. Spark có thể tương tác trực tiếp với file local, tự sắp xếp thư mục downloads, tạo spreadsheet từ invoice."},
    {"id": "s4", "text": "Tính năng real-time topic tracking mới theo dõi tin tức, tài chính và social media theo thời gian thực. Spark còn tích hợp với Google Tasks, Keep, Canva, Dropbox, Instacart, OpenTable và Zillow Rentals."},
    {"id": "s5", "text": "Đặc biệt, Google bổ sung hỗ trợ custom MCP connections. Bạn có thể tạo AI workflow cá nhân hóa, kết nối Spark với bất kỳ dịch vụ nào tương thích Model Context Protocol."},
    {"id": "s6", "text": "Về giá, Gemini Spark đi kèm gói Google AI Ultra với giá 99 đô la 99 cent mỗi tháng. Hiện tại chỉ dành cho người dùng 18 tuổi trở lên tại Mỹ, sử dụng tiếng Anh."},
    {"id": "s7", "text": "So sánh với ChatGPT và Claude, Spark nổi bật ở khả năng chạy 24/7 trên cloud, không cần thiết bị bật. Antigravity harness giúp Spark thực hiện multi-step actions phức tạp một cách tự chủ."},
    {"id": "s8", "text": "Tóm lại, Gemini Spark là bước tiến quan trọng của Google trong cuộc đua AI agent. Nếu bạn cần trợ lý AI luôn sẵn sàng làm việc thay mình, Spark đáng cân nhắc. Follow kênh để cập nhật AI mới nhất nhé!"},
]

OUT_DIR = "/home/z/my-project/download/spark_audio"
os.makedirs(OUT_DIR, exist_ok=True)

def get_duration(path):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1", path], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except: return 0.0

durations = {}
print(f"=== Generating {len(scenes)} TTS chunks ===", flush=True)
for s in scenes:
    out = os.path.join(OUT_DIR, f"{s['id']}.mp3")
    for attempt in range(5):
        if os.path.exists(out): os.remove(out)
        r = subprocess.run(["/home/z/.venv/bin/edge-tts","--voice",VOICE,"--text",s["text"],"--write-media",out], capture_output=True, text=True)
        size = os.path.getsize(out) if os.path.exists(out) else 0
        if size > 1000: break
        print(f"  {s['id']} attempt {attempt+1} retry...", flush=True)
        time.sleep(2)
    dur = get_duration(out)
    durations[s["id"]] = dur
    print(f"  {s['id']}: {dur:.2f}s", flush=True)

total = sum(durations.values())
print(f"\nTotal TTS: {total:.2f}s ({total/60:.2f} min)", flush=True)

# Concat all into one MP3
inputs = [os.path.join(OUT_DIR, f"{s['id']}.mp3") for s in scenes]
filter_str = "".join(f"[{i}:a]" for i in range(len(inputs))) + f"concat=n={len(inputs)}:v=0:a=1[out]"
full_mp3 = os.path.join(OUT_DIR, "narration.mp3")
r = subprocess.run(["ffmpeg","-y"] + [arg for inp in inputs for arg in ("-i", inp)] + ["-filter_complex", filter_str, "-map", "[out]", "-b:a", "64k", full_mp3], capture_output=True, text=True)
if r.returncode != 0:
    print("concat err:", r.stderr[-500:])
else:
    print(f"Full narration: {full_mp3} ({get_duration(full_mp3):.2f}s)", flush=True)

# Upload narration to sandbox
print(f"\n=== Upload narration to sandbox ===", flush=True)
with open(full_mp3, "rb") as f:
    audio_bytes = f.read()
print(f"Audio size: {len(audio_bytes)} bytes", flush=True)
sbx.files.write("/home/user/spark_project/narration.mp3", audio_bytes)
print("Uploaded to /home/user/spark_project/narration.mp3", flush=True)

# Upload Gemini Spark image
print(f"\n=== Upload Gemini Spark image ===", flush=True)
img_path = "/home/z/my-project/download/gemini_spark/gemini_spark_pcmag.png"
with open(img_path, "rb") as f:
    img_bytes = f.read()
print(f"Image size: {len(img_bytes)} bytes", flush=True)
sbx.files.write("/home/user/spark_project/gemini_spark.png", img_bytes)
print("Uploaded to /home/user/spark_project/gemini_spark.png", flush=True)

# Save durations
with open("/tmp/spark_durations.json", "w") as f:
    json.dump({"durations": durations, "total": total}, f)
print(f"\nDurations saved.", flush=True)
print(f"Sandbox: {SBX_ID}", flush=True)
