#!/home/z/.venv/bin/python3
"""Test VieNeu-TTS with multiple Vietnamese voices. Save WAVs for comparison."""
import os, time, wave
import numpy as np
from vieneu import Vieneu

print("=== Init Vieneu ===", flush=True)
t0 = time.time()
tts = Vieneu()
print(f"✓ Ready in {time.time()-t0:.1f}s, sample_rate={tts.sample_rate}Hz", flush=True)

OUT_DIR = "/home/z/my-project/download/vieneu_test"
os.makedirs(OUT_DIR, exist_ok=True)

TEST_TEXT = "Chào các bạn! Hôm nay mình sẽ so sánh VieNeu TTS với edge TTS cho tiếng Việt. Cuộc đua AI chưa bao giờ nóng đến thế!"
print(f"\nText: {TEST_TEXT}", flush=True)

# Test 4 voices: 2 male + 2 female
voices_to_test = [
    ("Gia Bảo", "nam_mượt"),
    ("Thái Sơn", "nam_chắc"),
    ("Ngọc Lan", "nữ_dịu"),
    ("Trúc Ly", "nữ_trẻ"),
]

for voice, label in voices_to_test:
    print(f"\n=== Voice: {voice} ({label}) ===", flush=True)
    t0 = time.time()
    try:
        audio = tts.infer(TEST_TEXT, voice=voice, emotion="natural")
        t_gen = time.time() - t0
        print(f"  ✓ Generated in {t_gen:.1f}s, {len(audio)} samples, {len(audio)/tts.sample_rate:.2f}s audio", flush=True)
        # Save as WAV
        out_path = f"{OUT_DIR}/vieneu_{label}_{voice.replace(' ', '_')}.wav"
        audio_int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
        with wave.open(out_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(tts.sample_rate)
            wf.writeframes(audio_int16.tobytes())
        print(f"  Saved: {out_path} ({os.path.getsize(out_path)} bytes)", flush=True)
    except Exception as e:
        print(f"  ✗ Failed: {e}", flush=True)

print(f"\n=== Done. Files in {OUT_DIR} ===", flush=True)
for f in sorted(os.listdir(OUT_DIR)):
    p = os.path.join(OUT_DIR, f)
    print(f"  {f} ({os.path.getsize(p)} bytes)")
