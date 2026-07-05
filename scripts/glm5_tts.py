#!/home/z/.venv/bin/python3
"""Generate VieNeu TTS narration for GLM-5 video. Upload to sandbox."""
import os, time, wave
import numpy as np
from e2b import Sandbox
from vieneu import Vieneu

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SBX_ID = open("/tmp/glm5_sandbox_id.txt").read().strip()
print(f"=== Connect to sandbox {SBX_ID} ===", flush=True)
sbx = Sandbox.connect(SBX_ID)
sbx.set_timeout(60 * 30)

# 8 scenes ~15s each = 120s (2 min)
scenes = [
    {"id": "s1", "text": "Chào các bạn! Hôm nay ngày 5 tháng 7 năm 2026, Z.ai vừa mở mã nguồn GLM-5 - mô hình AI mới nhất cho agentic engineering. Cùng mình tìm hiểu nhé!"},
    {"id": "s2", "text": "Repo zai-org GLM-5 hiện có hơn sáu nghìn sao và bảy trăm fork. Tagline: From Vibe Coding to Agentic Engineering - từ code cảm hứng đến kỹ thuật agent."},
    {"id": "s3", "text": "Thông số kỹ thuật: bảy trăm bốn mươi bốn tỷ tham số tổng, bốn mươi tỷ active. Pre-train với hai mươi tám phẩy năm nghìn tỷ token. Context window hai trăm nghìn token."},
    {"id": "s4", "text": "GLM-5 tích hợp DeepSeek Sparse Attention, giúp giảm chi phí mà vẫn giữ fidelity cho long-context. Sử dụng slime infrastructure cho asynchronous reinforcement learning."},
    {"id": "s5", "text": "Benchmark: xếp hạng nhất trên Vending Bench 2 với balance bốn nghìn bốn trăm ba mươi hai đô la. State-of-the-art cho các model open-source về reasoning, coding và agentic tasks."},
    {"id": "s6", "text": "Đặc biệt, GLM-5 cho phép kiểm soát thinking budget qua tham số reasoning_effort. Mặc định là max, có thể giảm xuống để trade-off giữa chất lượng và tốc độ."},
    {"id": "s7", "text": "Use cases: complex systems engineering, long-horizon agentic tasks, coding, reasoning. Phù hợp cho developer muốn build AI agent xử lý task phức tạp nhiều bước."},
    {"id": "s8", "text": "Tóm lại, GLM-5 là bước tiến quan trọng của Z.ai trong cuộc đua open-source AI. Truy cập github.com/zai-org/glm-5 để trải nghiệm. Follow kênh để cập nhật AI mới nhất!"},
]

OUT_DIR = "/home/z/my-project/download/glm5_audio"
os.makedirs(OUT_DIR, exist_ok=True)

# Init Vieneu (downloads weights first time)
print("=== Init Vieneu TTS ===", flush=True)
t0 = time.time()
tts = Vieneu()
print(f"✓ Vieneu ready in {time.time()-t0:.1f}s, sample_rate={tts.sample_rate}Hz", flush=True)

# Use "Gia Bảo" voice (male, mượt mà) - good for tech narration
VOICE = "Gia Bảo"
print(f"Voice: {VOICE}", flush=True)

# Generate per-scene
durations = {}
print(f"\n=== Generate {len(scenes)} scenes ===", flush=True)
for s in scenes:
    out = os.path.join(OUT_DIR, f"{s['id']}.wav")
    t0 = time.time()
    audio = tts.infer(s["text"], voice=VOICE, emotion="natural")
    t_gen = time.time() - t0
    # Save as WAV
    audio_int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(out, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(tts.sample_rate)
        wf.writeframes(audio_int16.tobytes())
    dur = len(audio) / tts.sample_rate
    durations[s["id"]] = dur
    print(f"  {s['id']}: {dur:.2f}s audio, gen {t_gen:.1f}s ({os.path.getsize(out)}B)", flush=True)

total = sum(durations.values())
print(f"\nTotal: {total:.2f}s ({total/60:.2f} min)", flush=True)

# Concat all into one WAV
print("\n=== Concat all scenes ===", flush=True)
import subprocess
inputs = [os.path.join(OUT_DIR, f"{s['id']}.wav") for s in scenes]
filter_str = "".join(f"[{i}:a]" for i in range(len(inputs))) + f"concat=n={len(inputs)}:v=0:a=1[out]"
full_wav = os.path.join(OUT_DIR, "narration_full.wav")
r = subprocess.run(["ffmpeg","-y"] + [arg for inp in inputs for arg in ("-i", inp)] + ["-filter_complex", filter_str, "-map", "[out]", "-ar", "48000", "-ac", "1", full_wav], capture_output=True, text=True)
if r.returncode != 0:
    print("concat err:", r.stderr[-500:])
else:
    print(f"Full: {full_wav} ({os.path.getsize(full_wav)}B)", flush=True)

# Convert to MP3 (smaller, HyperFrames-friendly)
narration_mp3 = os.path.join(OUT_DIR, "narration.mp3")
subprocess.run(["ffmpeg","-y","-i", full_wav, "-b:a", "96k", narration_mp3], capture_output=True, check=True)
print(f"MP3: {narration_mp3} ({os.path.getsize(narration_mp3)}B)", flush=True)

# Upload narration to sandbox
print(f"\n=== Upload narration to sandbox ===", flush=True)
with open(narration_mp3, "rb") as f:
    audio_bytes = f.read()
print(f"Audio size: {len(audio_bytes)} bytes", flush=True)
sbx.commands.run("mkdir -p /home/user/glm5_project/renders", timeout=15)
sbx.files.write("/home/user/glm5_project/narration.mp3", audio_bytes)
print("Uploaded to /home/user/glm5_project/narration.mp3", flush=True)

# Save durations
import json
with open("/tmp/glm5_durations.json", "w") as f:
    json.dump({"durations": durations, "total": total}, f)
print(f"\nDurations saved. Sandbox: {SBX_ID}", flush=True)
