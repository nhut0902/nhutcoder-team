"""Render final FireClaw MP4: 8 scene frames + mixed audio (narration + bg music)."""
import os, subprocess, json

FRAMES = "/home/z/my-project/download/fireclaw_frames"
AUDIO_DIR = "/home/z/my-project/download/fireclaw_audio"
OUT_MP4 = "/home/z/my-project/download/fireclaw-video.mp4"

# Per-scene durations from durations.json
with open(f"{AUDIO_DIR}/durations.json") as f:
    d = json.load(f)
durations = d["durations"]
scenes = [f"s{i}" for i in range(1, 9)]

print("Per-scene durations:")
for s in scenes:
    print(f"  {s}: {durations[s]:.2f}s")
total = sum(durations[s] for s in scenes)
print(f"Total: {total:.2f}s ({total/60:.1f} min)")

# Build ffmpeg concat list (image2 demuxer with duration per image)
list_file = "/tmp/fireclaw_concat.txt"
with open(list_file, "w") as f:
    for s in scenes:
        f.write(f"file '{FRAMES}/{s}.png'\n")
        f.write(f"duration {durations[s]:.3f}\n")
    # Last image repeated (ffmpeg quirk)
    f.write(f"file '{FRAMES}/{scenes[-1]}.png'\n")

print(f"\nConcat list: {list_file}")
print(f"Audio: {AUDIO_DIR}/mixed_audio.mp3")

cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", list_file,
    "-i", f"{AUDIO_DIR}/mixed_audio.mp3",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-preset", "medium",
    "-crf", "23",
    "-c:a", "aac",
    "-b:a", "128k",
    "-shortest",
    "-movflags", "+faststart",
    OUT_MP4,
]
print(f"\nRunning ffmpeg (this may take 1-2 min)...")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("FFMPEG STDERR:", r.stderr[-2000:])
    raise SystemExit(1)

# Verify
r = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=width,height,codec_name",
     "-of", "default=noprint_wrappers=1", OUT_MP4],
    capture_output=True, text=True,
)
print(f"\n=== Output ===")
print(f"File: {OUT_MP4}")
print(r.stdout)
print(f"Size: {os.path.getsize(OUT_MP4) / 1024 / 1024:.2f} MB")
