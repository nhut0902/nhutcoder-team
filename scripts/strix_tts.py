#!/home/z/.venv/bin/python3
"""Generate Vietnamese TTS narration for 6 scenes about Strix repo."""
import os, subprocess, json, time

OUT_DIR = "/home/z/my-project/download/strix_audio"
os.makedirs(OUT_DIR, exist_ok=True)
VOICE = "vi-VN-NamMinhNeural"

scenes = [
    {"id": "s1", "text": "Hôm nay ngày 3 tháng 7 năm 2026, repo trending số 1 GitHub là Strix - công cụ pentest bằng AI mã nguồn mở. Tăng hơn hai nghìn sao chỉ trong 24 giờ!"},
    {"id": "s2", "text": "Repo usestrix/strix hiện có ba mươi lăm nghìn bốn trăm sao và ba nghìn sáu trăm fork. Viết bằng Python, chủ đề về bảo mật, AI hacking và red teaming."},
    {"id": "s3", "text": "Cấu trúc repo rất chuyên nghiệp. Các file chính mới cập nhật bao gồm migration sang uv, SARIF emitter cho CI, và bump lên phiên bản 1.0.0."},
    {"id": "s4", "text": "README giới thiệu Strix là công cụ pentest AI mã nguồn mở. Sử dụng autonomous AI hackers để tìm và sửa lỗ hổng ứng dụng một cách tự động."},
    {"id": "s5", "text": "Tính năng nổi bật gồm HTTP interception proxy, browser exploitation tự động, terminal execution, custom Python exploit runtime, và static code analysis với vulnerability knowledge base."},
    {"id": "s6", "text": "Strix tích hợp GitHub Actions để quét mỗi pull request và chặn code không an toàn. Một công cụ tuyệt vời cho bug bounty và CTF. Follow kênh để cập nhật AI mới nhất!"},
]

def get_duration(path):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1", path], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except: return 0.0

durations = {}
print(f"=== Generating {len(scenes)} TTS chunks ===")
for s in scenes:
    out = os.path.join(OUT_DIR, f"{s['id']}.mp3")
    for attempt in range(5):
        if os.path.exists(out): os.remove(out)
        r = subprocess.run(["/home/z/.venv/bin/edge-tts","--voice",VOICE,"--text",s["text"],"--write-media",out], capture_output=True, text=True)
        size = os.path.getsize(out) if os.path.exists(out) else 0
        if size > 1000: break
        print(f"  {s['id']} retry {attempt+1}...", flush=True)
        time.sleep(2)
    dur = get_duration(out)
    durations[s["id"]] = dur
    print(f"  {s['id']}: {dur:.2f}s", flush=True)

total = sum(durations.values())
print(f"\nTotal: {total:.2f}s ({total/60:.2f} min)")

# Concat all
inputs = [os.path.join(OUT_DIR, f"{s['id']}.mp3") for s in scenes]
filter_str = "".join(f"[{i}:a]" for i in range(len(inputs))) + f"concat=n={len(inputs)}:v=0:a=1[out]"
full_mp3 = os.path.join(OUT_DIR, "narration.mp3")
r = subprocess.run(["ffmpeg","-y"] + [arg for inp in inputs for arg in ("-i", inp)] + ["-filter_complex", filter_str, "-map", "[out]", "-b:a", "64k", full_mp3], capture_output=True, text=True)
if r.returncode != 0:
    print("concat err:", r.stderr[-500:])
else:
    print(f"Full: {full_mp3} ({get_duration(full_mp3):.2f}s)")

with open("/tmp/strix_durations.json", "w") as f:
    json.dump({"durations": durations, "total": total}, f)
print("Durations saved.")
