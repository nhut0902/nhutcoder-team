#!/home/z/.venv/bin/python3
"""Test VieNeu-TTS with Vietnamese text. First run downloads model weights."""
import os, sys, time, wave

print("=== Testing VieNeu-TTS Vietnamese ===", flush=True)

TEST_TEXT = "Chào các bạn! Hôm nay mình sẽ so sánh VieNeu TTS với edge TTS cho tiếng Việt. Cuộc đua AI chưa bao giờ nóng đến thế!"

OUT_DIR = "/home/z/my-project/download/vieneu_test"
os.makedirs(OUT_DIR, exist_ok=True)

try:
    from vieneu import Vieneu
    print("✓ vieneu imported OK", flush=True)
    
    print("\n=== Init Vieneu (will download model weights on first run) ===", flush=True)
    t0 = time.time()
    # Default uses v3 Turbo with ONNX on CPU
    tts = Vieneu()
    print(f"✓ Vieneu ready in {time.time()-t0:.1f}s", flush=True)
    
    print(f"\n=== Generate speech ===", flush=True)
    print(f"Text: {TEST_TEXT}", flush=True)
    t0 = time.time()
    
    # Generate - returns audio samples (numpy array)
    audio = tts(TEST_TEXT)
    t_gen = time.time() - t0
    print(f"✓ Generated in {t_gen:.1f}s", flush=True)
    print(f"  Type: {type(audio)}", flush=True)
    if hasattr(audio, '__len__'):
        print(f"  Length: {len(audio)} samples", flush=True)
    
    # Save as WAV
    out_path = f"{OUT_DIR}/vieneu_test.wav"
    
    # Try different save methods
    if hasattr(tts, 'save'):
        tts.save(audio, out_path)
        print(f"  Saved via tts.save(): {out_path} ({os.path.getsize(out_path)} bytes)", flush=True)
    else:
        # Manual save with wave
        import numpy as np
        if not isinstance(audio, np.ndarray):
            audio = np.array(audio)
        # Convert to int16
        audio_int16 = (audio * 32767).astype(np.int16)
        with wave.open(out_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            # Sample rate is typically 24000 or 48000 for VieNeu v3 Turbo
            sr = 48000 if hasattr(tts, 'sample_rate') and tts.sample_rate == 48000 else 24000
            wf.setframerate(sr)
            wf.writeframes(audio_int16.tobytes())
        print(f"  Saved as WAV: {out_path} ({os.path.getsize(out_path)} bytes, sr={sr})", flush=True)

except Exception as e:
    print(f"ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
