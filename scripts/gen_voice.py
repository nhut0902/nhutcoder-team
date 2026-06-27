"""Generate Vietnamese male voice narration using edge-tts CLI."""
import os, subprocess, json

OUT_DIR = "/home/z/my-project/download/audio"
os.makedirs(OUT_DIR, exist_ok=True)

VOICE = "vi-VN-NamMinhNeural"

scenes = [
    {"id": "s1", "text": "Chào mừng các bạn đến với Browser Use, thư viện Python mã nguồn mở giúp các tác nhân AI tự động hóa trình duyệt web một cách dễ dàng."},
    {"id": "s2", "text": "Với hơn một trăm nghìn sao trên GitHub và hơn mười một nghìn lượt fork, Browser Use hiện là công cụ hàng đầu cho việc điều khiển trình duyệt bằng AI."},
    {"id": "s3", "text": "Cài đặt cực kỳ đơn giản. Bạn chỉ cần mở terminal và chạy pip install browser-use. Thế là xong."},
    {"id": "s4", "text": "Các tính năng nổi bật bao gồm điều khiển AI agent, tự động click chuột, gõ văn bản, cuộn trang và trích xuất dữ liệu từ bất kỳ trang web nào."},
    {"id": "s5", "text": "Browser Use được xây dựng trên Playwright và tương thích với mọi mô hình ngôn ngữ lớn. Truy cập github.com/browser-use để bắt đầu ngay hôm nay. Đừng quên theo dõi kênh nhé!"},
]

def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip())

durations = {}
print(f"=== Generating {len(scenes)} chunks with {VOICE} ===")
for s in scenes:
    out = os.path.join(OUT_DIR, f"{s['id']}.mp3")
    r = subprocess.run(
        ["edge-tts", "--voice", VOICE, "--text", s["text"], "--write-media", out],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"FAILED {s['id']}: {r.stderr}")
        continue
    dur = get_duration(out)
    durations[s["id"]] = dur
    print(f"  {s['id']}: {dur:.2f}s")

total = sum(durations.values())
print(f"\nTotal: {total:.2f}s")

with open(os.path.join(OUT_DIR, "durations.json"), "w") as f:
    json.dump({"durations": durations, "total": total, "scenes": scenes}, f, ensure_ascii=False, indent=2)

# Concat
list_file = os.path.join(OUT_DIR, "concat.txt")
with open(list_file, "w") as f:
    for s in scenes:
        f.write(f"file '{s['id']}.mp3'\n")

full_mp3 = os.path.join(OUT_DIR, "full_narration.mp3")
subprocess.run(
    ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", full_mp3],
    check=True, capture_output=True,
)
print(f"Full: {full_mp3} ({get_duration(full_mp3):.2f}s)")
