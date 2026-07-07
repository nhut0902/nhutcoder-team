#!/home/z/.venv/bin/python3
"""Generate VieNeu TTS with ADAM cloned voice for Gemini 3.5 Pro comparison video.
12 scenes ~15s each = ~180s (3 min). One scene at a time via arg."""
import os, sys, time, wave, subprocess, json
import numpy as np
from vieneu import Vieneu

OUT_DIR = "/home/z/my-project/download/gemini35_video_audio"
os.makedirs(OUT_DIR, exist_ok=True)
REF = "/home/z/my-project/download/voice_profiles/adam_firm_ref.wav"

SCENES = {
    "s1": "Chào các bạn! Hôm nay mình sẽ giới thiệu Gemini 3.5 Pro - model flagship mới nhất của Google DeepMind. Context window hai triệu token, lớn nhất thị trường!",
    "s2": "Gemini 3.5 Pro được công bố ngày mười chín tháng năm năm hai nghìn hai mươi sáu. Hiện đang ở giai đoạn limited preview trên Vertex AI. GA dự kiến tháng bảy.",
    "s3": "Thông số nổi bật: context window hai triệu token, gấp đôi Claude Fable 5 và gấp mười lần GPT-5.6. Deep Think Mode cho reasoning phức tạp. Multimodal đầy đủ.",
    "s4": "Deep Think Mode là tính năng mới. Opt-in reasoning mode cho scientific, mathematical, coding problems. Trade latency cho accuracy. thinkingLevel từ minimal đến high.",
    "s5": "Về giá, ước tính khoảng mười lăm đô la mỗi triệu token input. Đắt gấp tám đến mười lần Gemini 3.5 Flash. Reasoning tokens tính vào context budget.",
    "s6": "So sánh top model hiện nay. GPT-5.6 Sol Ultra dẫn đầu coding với Terminal-Bench chín mươi một phẩy chín phần trăm. Nhưng đang restricted preview.",
    "s7": "Claude Fable 5 là model production-grade tốt nhất cho agentic workflows. Context một triệu token. Đang bị suspend do export control nhưng sắp return.",
    "s8": "Gemini 3.5 Pro là price-performance leader. Hai triệu token context làm nó vua của RAG và large-scale data processing. Deep Think cho science.",
    "s9": "Kimi K2.7 Code là model open-source mạnh. Một nghìn tỷ tham số MoE, giảm ba mươi phần trăm thinking tokens. Phù hợp cho coding agent.",
    "s10": "Bảng tổng kết: Gemini 3.5 Pro thắng về context. GPT-5.6 Sol thắng về coding. Claude Fable 5 thắng về agentic. Kimi K2.7 thắng về efficiency.",
    "s11": "Khi nào dùng model nào? RAG với tài liệu dài chọn Gemini 3.5 Pro. Coding phức tạp chọn GPT-5.6 hoặc Kimi K2.7. Agentic production chọn Claude Fable 5.",
    "s12": "Gemini 3.5 Pro là bước tiến quan trọng của Google. Hai triệu token context mở ra khả năng mới cho AI. Follow kênh để cập nhật AI mới nhất!",
}

if len(sys.argv) > 1:
    sid = sys.argv[1]
    scenes_to_gen = {sid: SCENES[sid]}
else:
    scenes_to_gen = SCENES

tts = Vieneu()
for sid, text in scenes_to_gen.items():
    out = os.path.join(OUT_DIR, f"{sid}.wav")
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print(f"{sid}: exists, skip", flush=True)
        continue
    print(f"Generating {sid}...", flush=True)
    audio = tts.infer(text, ref_audio=REF, voice=None, style="tu_nhien", denoise=True)
    audio_int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(out, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(tts.sample_rate)
        wf.writeframes(audio_int16.tobytes())
    print(f"{sid}: {len(audio)/tts.sample_rate:.2f}s", flush=True)

# Check if all done
all_done = all(os.path.exists(os.path.join(OUT_DIR, f"{s}.wav")) and os.path.getsize(os.path.join(OUT_DIR, f"{s}.wav")) > 1000 for s in SCENES)
if all_done:
    scenes = sorted(SCENES.keys())
    durations = {}
    for s in scenes:
        p = os.path.join(OUT_DIR, f"{s}.wav")
        r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1", p], capture_output=True, text=True)
        durations[s] = float(r.stdout.strip())
    total = sum(durations.values())
    print(f"\nTotal: {total:.2f}s ({total/60:.2f} min)", flush=True)
    inputs = [os.path.join(OUT_DIR, f"{s}.wav") for s in scenes]
    filter_str = "".join(f"[{i}:a]" for i in range(len(inputs))) + f"concat=n={len(inputs)}:v=0:a=1[out]"
    full_wav = os.path.join(OUT_DIR, "narration_full.wav")
    subprocess.run(["ffmpeg","-y"] + [arg for inp in inputs for arg in ("-i", inp)] + ["-filter_complex", filter_str, "-map", "[out]", "-ar", "48000", "-ac", "1", full_wav], capture_output=True, check=True)
    narration_mp3 = os.path.join(OUT_DIR, "narration.mp3")
    subprocess.run(["ffmpeg","-y","-i", full_wav, "-b:a", "96k", narration_mp3], capture_output=True, check=True)
    print(f"MP3: {os.path.getsize(narration_mp3)}B", flush=True)
    with open("/tmp/gemini35_video_durations.json", "w") as f:
        json.dump({"durations": durations, "total": total}, f)
    print("Done!", flush=True)
