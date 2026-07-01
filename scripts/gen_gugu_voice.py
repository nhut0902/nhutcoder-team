"""Generate 1-minute Vietnamese TTS narration about Sakana Fugu vs GPT-5.6 vs Claude Fable 5."""
import os, subprocess, json, time

OUT_DIR = "/home/z/my-project/download/gugu_video_audio"
os.makedirs(OUT_DIR, exist_ok=True)
VOICE = "vi-VN-NamMinhNeural"

# 6 scenes ~10s each = 60s total (shortened)
scenes = [
    {"id": "s1", "text": "So sánh ba ông lớn AI 2026: Sakana Fugu, GPT-5.6 Sol, và Claude Fable 5. Cuộc đua chưa bao giờ nóng đến thế!"},
    {"id": "s2", "text": "Sakana Fugu của Nhật Bản, ra mắt 22 tháng 6 năm 2026. Đây là hệ thống multi-agent, điều phối nhiều model qua một API."},
    {"id": "s3", "text": "Terminal-Bench 2.1: GPT-5.6 Sol Ultra dẫn đầu 91.9 phần trăm. GPT-5.6 Sol 88.8. Claude Fable 5 đạt 83.4. Fugu Ultra 82.1."},
    {"id": "s4", "text": "SWE-Bench Pro coding: Claude Fable 5 thắng 80.3, hơn Fugu Ultra 73.7. Nhưng LiveCodeBench: Fugu Ultra dẫn 93.2, Claude 89.8."},
    {"id": "s5", "text": "Giá mỗi triệu token: GPT-5.6 Sol và Fugu Ultra đều 5 đô input, 30 đô output. Claude Fable 5 đắt nhất 10 đô la. Luna rẻ nhất 1 đô la."},
    {"id": "s6", "text": "Kết luận: không ai thắng tuyệt đối. Coding chọn Claude, đa tác vụ chọn Fugu, giá rẻ chọn GPT-5.6. Follow kênh nhé!"},
]

def get_duration(path):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1", path], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except: return 0.0

durations = {}
print(f"=== Generating {len(scenes)} chunks with {VOICE} ===")
for s in scenes:
    out = os.path.join(OUT_DIR, f"{s['id']}.mp3")
    for attempt in range(5):
        if os.path.exists(out): os.remove(out)
        r = subprocess.run(["/home/z/.venv/bin/edge-tts","--voice",VOICE,"--text",s["text"],"--write-media",out], capture_output=True, text=True)
        size = os.path.getsize(out) if os.path.exists(out) else 0
        if size > 1000: break
        print(f"  {s['id']} attempt {attempt+1} failed ({size}B), retry...")
        time.sleep(2)
    dur = get_duration(out)
    durations[s["id"]] = dur
    print(f"  {s['id']}: {dur:.2f}s")

total = sum(durations.values())
print(f"\nTotal: {total:.2f}s ({total/60:.2f} min)")

with open(os.path.join(OUT_DIR, "durations.json"), "w") as f:
    json.dump({"durations": durations, "total": total, "scenes": scenes}, f, ensure_ascii=False, indent=2)

# Concat
inputs = [os.path.join(OUT_DIR, f"{s['id']}.mp3") for s in scenes]
filter_str = "".join(f"[{i}:a]" for i in range(len(inputs))) + f"concat=n={len(inputs)}:v=0:a=1[out]"
full_mp3 = os.path.join(OUT_DIR, "full_narration.mp3")
r = subprocess.run(["ffmpeg","-y"] + [arg for inp in inputs for arg in ("-i", inp)] + ["-filter_complex", filter_str, "-map", "[out]", "-b:a", "64k", full_mp3], capture_output=True, text=True)
if r.returncode != 0:
    print("concat err:", r.stderr[-500:])
else:
    print(f"Full: {full_mp3} ({get_duration(full_mp3):.2f}s)")
