#!/home/z/.venv/bin/python3
"""Test Kokoro TTS with Vietnamese text. First run downloads model weights (~350MB from HuggingFace)."""
import os, sys, time

print("=== Testing Kokoro Vietnamese TTS ===", flush=True)

# Test text (same we'd use for edge-tts comparison)
TEST_TEXT = "Chào các bạn! Hôm nay mình sẽ so sánh Kokoro TTS với edge-tts cho tiếng Việt. Cuộc đua AI chưa bao giờ nóng đến thế!"

OUT_DIR = "/home/z/my-project/download/tts_test"
os.makedirs(OUT_DIR, exist_ok=True)

try:
    from kokoro import KPipeline
    import soundfile as sf
    print("✓ Imports OK", flush=True)
    
    # Kokoro supports Vietnamese with lang_code='v'
    print("\n=== Init KPipeline (lang_code='v') ===", flush=True)
    # First run downloads model weights (~350MB)
    t0 = time.time()
    pipeline = KPipeline(lang_code='v')  # 'v' for Vietnamese
    print(f"✓ Pipeline ready in {time.time()-t0:.1f}s", flush=True)
    
    # Generate speech
    print(f"\n=== Generating speech ===", flush=True)
    print(f"Text: {TEST_TEXT}", flush=True)
    t0 = time.time()
    
    # Vietnamese voice: try 'vf_alpha' (Vietnamese female alpha) or similar
    # Kokoro 0.9.4 has Vietnamese voices with prefix 'v'
    voices_to_try = ['vf_alpha', 'vm_alpha', 'af_heart']  # try VN female, VN male, fallback EN female
    
    for voice in voices_to_try:
        try:
            print(f"\n  Trying voice: {voice}", flush=True)
            chunks = list(pipeline(TEST_TEXT, voice=voice))
            if chunks:
                print(f"  ✓ Generated {len(chunks)} chunk(s) with {voice}", flush=True)
                # Save first chunk
                gs, ps, audio = chunks[0]
                print(f"  Chunk 0: {len(audio)} samples, sample_rate likely 24000", flush=True)
                out_path = f"{OUT_DIR}/kokoro_{voice}.wav"
                sf.write(out_path, audio, 24000)
                print(f"  Saved: {out_path} ({os.path.getsize(out_path)} bytes)", flush=True)
                break
            else:
                print(f"  ✗ No chunks generated for {voice}", flush=True)
        except Exception as e:
            print(f"  ✗ {voice} failed: {e}", flush=True)
            continue
    
    print(f"\n=== Total time: {time.time()-t0:.1f}s ===", flush=True)
    
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
