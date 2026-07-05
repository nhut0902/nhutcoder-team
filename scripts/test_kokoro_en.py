#!/home/z/.venv/bin/python3
"""Test Kokoro TTS with English (no Vietnamese support in Kokoro 0.9.4).
Compare same English text with edge-tts."""
import os, sys, time, subprocess

print("=== Kokoro TTS Test (English) ===", flush=True)

TEST_TEXT_EN = "Hello everyone! Today I'll compare Kokoro TTS with edge-tts. The AI race has never been this hot!"

OUT_DIR = "/home/z/my-project/download/tts_test"
os.makedirs(OUT_DIR, exist_ok=True)

# === Kokoro ===
try:
    from kokoro import KPipeline
    import soundfile as sf
    print("✓ Kokoro imports OK", flush=True)
    
    print("\n=== Init KPipeline (lang_code='a' American English) ===", flush=True)
    t0 = time.time()
    pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
    print(f"✓ Pipeline ready in {time.time()-t0:.1f}s", flush=True)
    
    # List available voices - Kokoro has many English voices
    # Default voice is 'af_heart' (American female)
    # Try multiple voices to find best
    voices = ['af_heart', 'af_bella', 'af_sky', 'am_adam', 'am_michael']
    
    for voice in voices:
        try:
            print(f"\n=== Voice: {voice} ===", flush=True)
            t0 = time.time()
            chunks = list(pipeline(TEST_TEXT_EN, voice=voice))
            t_gen = time.time() - t0
            print(f"  Generated {len(chunks)} chunk(s) in {t_gen:.1f}s", flush=True)
            
            # Concatenate all chunks
            import numpy as np
            all_audio = np.concatenate([audio for _, _, audio in chunks])
            out_path = f"{OUT_DIR}/kokoro_en_{voice}.wav"
            sf.write(out_path, all_audio, 24000)
            print(f"  Saved: {out_path} ({os.path.getsize(out_path)} bytes, {len(all_audio)/24000:.2f}s)", flush=True)
        except Exception as e:
            print(f"  ✗ {voice} failed: {e}", flush=True)
    
except Exception as e:
    print(f"Kokoro ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()

# === edge-tts for comparison (English) ===
print("\n=== Edge-TTS English (for comparison) ===", flush=True)
edge_voices = ['en-US-GuyNeural', 'en-US-AriaNeural']
for v in edge_voices:
    out = f"{OUT_DIR}/edge_en_{v}.mp3"
    r = subprocess.run(["/home/z/.venv/bin/edge-tts", "--voice", v, "--text", TEST_TEXT_EN, "--write-media", out], capture_output=True, text=True)
    if os.path.exists(out):
        # Get duration
        r2 = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1", out], capture_output=True, text=True)
        dur = float(r2.stdout.strip()) if r2.stdout.strip() else 0
        print(f"  {v}: {out} ({os.path.getsize(out)} bytes, {dur:.2f}s)", flush=True)
    else:
        print(f"  {v}: FAILED", flush=True)

print("\n=== Done. Files in:", OUT_DIR, "===", flush=True)
for f in sorted(os.listdir(OUT_DIR)):
    p = os.path.join(OUT_DIR, f)
    print(f"  {f} ({os.path.getsize(p)} bytes)")
