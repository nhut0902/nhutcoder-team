#!/home/z/.venv/bin/python3
"""Generate VieNeu TTS narration with FEMALE voice (Ngọc Lan) for Kimi K2.7 video. Upload to sandbox."""
import os, time, wave, subprocess, json
import numpy as np
from e2b import Sandbox
from vieneu import Vieneu

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SBX_ID = "i1icx11jg9lvyzjlwic06"
print(f"=== Connect to sandbox {SBX_ID} ===", flush=True)
sbx = Sandbox.connect(SBX_ID)
sbx.set_timeout(60 * 30)

# 8 scenes ~15s each = 120s
scenes = [
    {"id": "s1", "text": "Chào các bạn! Hôm nay mình sẽ giới thiệu Kimi K2.7 Code - mô hình AI coding mới nhất của Moonshot AI. Vừa ra mắt ngày 12 tháng 6 năm 2026."},
    {"id": "s2", "text": "Kimi K2.7 là mô hình open-weights với kiến trúc Mixture-of-Experts một nghìn tỷ tham số, 32 tỷ active. Context window 256 nghìn token, license MIT modified."},
    {"id": "s3", "text": "Đặc điểm nổi bật: giảm 30 phần trăm thinking tokens so với K2.6, tối ưu cho long-horizon software engineering. Forces thinking mode cho mọi task."},
    {"id": "s4", "text": "Benchmark so với K2.6: Kimi Code Bench v2 tăng 21.8 phần trăm, Program Bench tăng 11 phần trăm, MLS Bench Lite tăng 31.5 phần trăm, MCP Mark Verified tăng 11.4 phần trăm."},
    {"id": "s5", "text": "Repo chính thức trên HuggingFace: moonshotai/Kimi-K2.7-Code. GitHub MoonshotAI/Kimi-K2 có hơn mười nghìn sao. Modified MIT license cho商用."},
    {"id": "s6", "text": "Use cases chính: complex software engineering, multi-step coding, long-horizon agentic tasks, integration với CI/CD và code review."},
    {"id": "s7", "text": "So sánh với đối thủ: Kimi K2.7 nổi bật về thinking efficiency, context 256K đủ lớn cho codebase lớn, giá cạnh tranh so với Claude và GPT-5."},
    {"id": "s8", "text": "Tóm lại, Kimi K2.7 Code là lựa chọn tuyệt vời cho developer cần AI coding agent mạnh mẽ và tiết kiệm. Truy cập huggingface.co/moonshotai/Kimi-K2.7-Code. Follow kênh nhé!"},
]

OUT_DIR = "/home/z/my-project/download/kimi_audio"
os.makedirs(OUT_DIR, exist_ok=True)

# Init Vieneu
print("=== Init Vieneu TTS ===", flush=True)
t0 = time.time()
tts = Vieneu()
print(f"✓ Vieneu ready in {time.time()-t0:.1f}s, sample_rate={tts.sample_rate}Hz", flush=True)

# Use Ngọc Lan voice (Vietnamese female, dịu dàng)
VOICE = "Ngọc Lan"
print(f"Voice: {VOICE} (Vietnamese female)", flush=True)

# Generate per-scene
durations = {}
print(f"\n=== Generate {len(scenes)} scenes ===", flush=True)
for s in scenes:
    out = os.path.join(OUT_DIR, f"{s['id']}.wav")
    t0 = time.time()
    audio = tts.infer(s["text"], voice=VOICE, emotion="natural")
    t_gen = time.time() - t0
    audio_int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(out, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(tts.sample_rate)
        wf.writeframes(audio_int16.tobytes())
    dur = len(audio) / tts.sample_rate
    durations[s["id"]] = dur
    print(f"  {s['id']}: {dur:.2f}s audio, gen {t_gen:.1f}s ({os.path.getsize(out)}B)", flush=True)

total = sum(durations.values())
print(f"\nTotal: {total:.2f}s ({total/60:.2f} min)", flush=True)

# Concat all
print("\n=== Concat all scenes ===", flush=True)
inputs = [os.path.join(OUT_DIR, f"{s['id']}.wav") for s in scenes]
filter_str = "".join(f"[{i}:a]" for i in range(len(inputs))) + f"concat=n={len(inputs)}:v=0:a=1[out]"
full_wav = os.path.join(OUT_DIR, "narration_full.wav")
r = subprocess.run(["ffmpeg","-y"] + [arg for inp in inputs for arg in ("-i", inp)] + ["-filter_complex", filter_str, "-map", "[out]", "-ar", "48000", "-ac", "1", full_wav], capture_output=True, text=True)
print(f"Full WAV: {os.path.getsize(full_wav)}B", flush=True)

# Convert to MP3
narration_mp3 = os.path.join(OUT_DIR, "narration.mp3")
subprocess.run(["ffmpeg","-y","-i", full_wav, "-b:a", "96k", narration_mp3], capture_output=True, check=True)
print(f"MP3: {os.path.getsize(narration_mp3)}B", flush=True)

# Upload narration to sandbox
print(f"\n=== Upload narration to sandbox ===", flush=True)
with open(narration_mp3, "rb") as f:
    audio_bytes = f.read()
print(f"Audio size: {len(audio_bytes)} bytes", flush=True)
sbx.commands.run("mkdir -p /home/user/kimi_project/public", timeout=15)
sbx.files.write("/home/user/kimi_project/public/narration.mp3", audio_bytes)
print("Uploaded narration.mp3", flush=True)

# Upload screenshots
print(f"\n=== Upload screenshots ===", flush=True)
for f in ['01_hf_title.png', '02_hf_readme.png', '03_gh_title.png', '04_gh_files.png']:
    p = f"/home/z/my-project/download/kimi_shots/{f}"
    with open(p, "rb") as fh:
        sbx.files.write(f"/home/user/kimi_project/public/{f}", fh.read())
    print(f"  Uploaded {f}", flush=True)

# Save durations
with open("/tmp/kimi_durations.json", "w") as f:
    json.dump({"durations": durations, "total": total}, f)
print(f"\nDurations saved. Total: {total:.2f}s", flush=True)
