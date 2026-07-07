#!/home/z/.venv/bin/python3
"""Generate VieNeu TTS with ADAM cloned voice for Top 3 TTS tools video. 12 scenes ~15s each = ~180s."""
import os, sys, time, wave, subprocess, json
import numpy as np
from vieneu import Vieneu

OUT_DIR = "/home/z/my-project/download/tts3_audio"
os.makedirs(OUT_DIR, exist_ok=True)
REF = "/home/z/my-project/download/voice_profiles/adam_firm_ref.wav"

SCENES = {
    "s1": "Chào các bạn! Hôm nay mình sẽ giới thiệu top 3 công cụ TTS voice cloning mã nguồn mở hot nhất 2026. Nếu bạn muốn clone giọng nói bằng AI, đây là 3 công cụ bạn không thể bỏ qua!",
    "s2": "Top một: Real-Time-Voice-Cloning, gần sáu mươi nghìn sao trên GitHub. Clone giọng chỉ trong năm giây, generate speech theo thời gian thực. Dựa trên Transfer Learning từ mẫu giọng reference.",
    "s3": "Real-Time-Voice-Cloning sử dụng encoder-encoder-decoder architecture. Cài đặt: clone repo, pip install, download pre-trained weights. Support nhiều ngôn ngữ, chạy được cả trên CPU.",
    "s4": "Repo CorentinJ Real-Time-Voice-Cloning, viết bằng Python, license MIT. Đơn giản, dễ dùng, phù hợp cho người mới bắt đầu với voice cloning.",
    "s5": "Top hai: GPT-SoVITS, cũng gần sáu mươi nghìn sao. Chỉ cần một phút voice data là train được TTS model tốt! Few-shot voice cloning cực mạnh.",
    "s6": "GPT-SoVITS kết hợp GPT và SoVITS cho chất lượng clone cao nhất. Support đa ngôn ngữ: Trung, Anh, Nhật, Hàn, Việt. Có WebUI Gradio dễ sử dụng.",
    "s7": "Repo RVC-Boss GPT-SoVITS, viết bằng Python, license MIT. Tích hợp nhiều features: text-to-speech, speech-to-speech, voice conversion, và real-time inference.",
    "s8": "Top ba: OpenVoice, gần ba mươi bảy nghìn sao. Instant voice cloning bởi MIT và MyShell. Zero-shot, cross-lingual, granular style control.",
    "s9": "OpenVoice cho phép clone giọng mà không cần train, chỉ cần một đoạn reference ngắn. Control tone, emotion, accent. Support cross-lingual cloning.",
    "s10": "Repo myshell-ai OpenVoice, viết bằng Python, license MIT. Audio foundation model, commercial use allowed. Dùng cho production-ready applications.",
    "s11": "So sánh: Real-Time-Voice-Cloning đơn giản nhất, GPT-SoVITS chất lượng cao nhất, OpenVoice nhanh nhất với zero-shot. Tùy use case mà chọn công cụ phù hợp.",
    "s12": "Cả ba công cụ đều open source, MIT license, chạy local. Truy cập GitHub để trải nghiệm. Follow kênh để cập nhật AI tools mới nhất!",
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
    with open("/tmp/tts3_durations.json", "w") as f:
        json.dump({"durations": durations, "total": total}, f)
    print("Done!", flush=True)
