#!/home/z/.venv/bin/python3
"""Generate TTS with Adam cloned voice for 2-min video about the viral cooking video.
8 scenes based on Riff-generated content."""
import os, sys, time, wave, subprocess, json
import numpy as np
from vieneu import Vieneu

OUT_DIR = "/home/z/my-project/download/cook_video_audio"
os.makedirs(OUT_DIR, exist_ok=True)
REF = "/home/z/my-project/download/voice_profiles/adam_firm_ref.wav"

SCENES = {
    "s1": "Chào các bạn! Hôm nay mình sẽ review một video viral trên YouTube: Bầu Huy Trực Tiếp Vào Bếp Chuẩn Bị Cơm Trưa Cho Bầu Ni. Từ kênh Thiện Tiên Vlog.",
    "s2": "Video kể về Bầu Huy, một người chồng trực tiếp vào bếp nấu cơm trưa cho vợ đang mang thai. Rửa rau, nấu cơm, bày biện món ăn. Đơn giản nhưng ấm áp.",
    "s3": "Điều làm video viral: tính chân thực. Không công thức cầu kỳ, không drama. Chỉ là một người đàn ông làm những việc cần thiết để chăm sóc vợ.",
    "s4": "Video tạo ra cuộc trò chuyện về domestic care, về lao động chăm sóc vô hình trong gia đình. Những việc nhỏ nhưng quan trọng, đặc biệt khi vợ đang mang thai.",
    "s5": "Bình luận đầy ắp người xem chia sẻ trải nghiệm riêng. Nhiều người nói loại chăm sóc này thường vô hình, ngay cả trong tình yêu. Khác ca ngợi người chồng.",
    "s6": "Bài học cho content creator: tính chân thực và gần gũi mạnh hơn sự hoàn hảo. Biến khoảnh khắc thật life thành content cần công cụ giúp streamline quy trình.",
    "s7": "Nếu bạn là content creator muốn biến cuộc sống thường ngày thành nội dung, có nhiều AI tools giúp tối ưu workflow. Từ TTS, video editing, đến social media posting.",
    "s8": "Video này là minh chứng: tình yêu không phải lúc nào cũng ở cử chỉ lớn. Đôi khi, nó nằm trong bát cơm bạn nấu cho người partner. Follow kênh để cập nhật AI tools!",
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

# Check all done
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
    with open("/tmp/cook_durations.json", "w") as f:
        json.dump({"durations": durations, "total": total}, f)
    print("Done!", flush=True)
