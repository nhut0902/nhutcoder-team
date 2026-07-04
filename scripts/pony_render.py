#!/home/z/.venv/bin/python3
"""Render final MP4 - NO animation. Just concat frames + narration audio.
Optimized for TikTok/Reels: H264, AAC, 30fps, faststart, vertical 1080x1920."""
import os, subprocess, json

FRAMES = "/home/z/my-project/download/pony_frames"
NARRATION = "/home/z/my-project/download/pony_audio/narration.mp3"
OUT_MP4 = "/home/z/my-project/download/pony-video.mp4"

with open("/tmp/pony_durations.json") as f:
    d = json.load(f)
    durations = d["durations"]
    total = d["total"]

scenes = [f"s{i}" for i in range(1, 7)]
print(f"Per-scene durations:")
for s in scenes:
    print(f"  {s}: {durations[s]:.2f}s")
print(f"Total: {total:.2f}s")

# === Mix narration + bg music (very subtle, 15% volume) ===
print("\n=== Generate subtle bg music + mix with narration ===")
BG_MUSIC = "/home/z/my-project/download/pony_audio/bg_music.mp3"
bg_dur = int(total + 3)
subprocess.run([
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", f"sine=frequency=146.83:duration={bg_dur}",
    "-f", "lavfi", "-i", f"sine=frequency=196:duration={bg_dur}",
    "-filter_complex",
    "[0:a]volume=0.10,tremolo=f=0.2:d=0.4[a1];"
    "[1:a]volume=0.07,tremolo=f=0.15:d=0.4[a2];"
    "[a1][a2]amix=inputs=2:duration=longest:weights=1 1,"
    f"afade=t=in:st=0:d=2,afade=t=out:st={total-3}:d=3",
    "-t", str(bg_dur), "-b:a", "96k", BG_MUSIC,
], capture_output=True, check=True)

MIXED = "/home/z/my-project/download/pony_audio/mixed.mp3"
subprocess.run([
    "ffmpeg", "-y",
    "-i", NARRATION,
    "-i", BG_MUSIC,
    "-filter_complex",
    "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0:weights=1 0.5",
    "-b:a", "96k", MIXED,
], capture_output=True, check=True)
print(f"  Mixed audio: {MIXED}")

# === Build concat list (image2 demuxer with duration per image) ===
list_file = "/tmp/pony_concat.txt"
with open(list_file, "w") as f:
    for s in scenes:
        f.write(f"file '{FRAMES}/{s}.png'\n")
        f.write(f"duration {durations[s]:.3f}\n")
    f.write(f"file '{FRAMES}/{scenes[-1]}.png'\n")  # repeat last (ffmpeg quirk)

print(f"\nConcat list: {list_file}")

# === Render video - NO animation, just concat frames + audio ===
# TikTok/Reels optimized: H264, AAC 128k, 30fps, yuv420p, +faststart
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", list_file,
    "-i", MIXED,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-preset", "slow",
    "-crf", "23",
    "-c:a", "aac",
    "-b:a", "128k",
    "-ar", "44100",
    "-shortest",
    "-movflags", "+faststart",
    OUT_MP4,
]
print(f"\nRendering (this may take 1-2 min)...")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("FFMPEG STDERR:", r.stderr[-2000:])
    raise SystemExit(1)

# Verify
r = subprocess.run(
    ["ffprobe","-v","error","-show_entries","format=duration,size:stream=width,height,codec_name,r_frame_rate","-of","default=noprint_wrappers=1", OUT_MP4],
    capture_output=True, text=True,
)
print(f"\n=== Output ===")
print(f"File: {OUT_MP4}")
print(r.stdout)
print(f"Size: {os.path.getsize(OUT_MP4) / 1024 / 1024:.2f} MB")
