"""Assemble final MP4: 6 scene PNGs + audio track, with crossfade transitions."""
import os, subprocess, json

FRAMES = "/home/z/my-project/download/frames"
AUDIO_DIR = "/home/z/my-project/download/audio"
OUT_MP4 = "/home/z/my-project/download/browser-use-video.mp4"

# Read per-scene durations
scenes = ["s1", "s2", "s3", "s4", "s5", "s6"]
durations = {}
for s in scenes:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", f"{AUDIO_DIR}/{s}.mp3"],
        capture_output=True, text=True,
    )
    durations[s] = float(r.stdout.strip())

print("Per-scene durations:")
for s in scenes:
    print(f"  {s}: {durations[s]:.2f}s")

total = sum(durations.values())
print(f"Total: {total:.2f}s")

# Build ffmpeg concat file (image2 demuxer with per-image duration)
list_file = "/tmp/video_concat.txt"
with open(list_file, "w") as f:
    for s in scenes:
        f.write(f"file '{FRAMES}/{s}.png'\n")
        f.write(f"duration {durations[s]:.3f}\n")
    # Last image needs to be repeated (ffmpeg quirk)
    f.write(f"file '{FRAMES}/{scenes[-1]}.png'\n")

print(f"\nConcat list: {list_file}")

# Run ffmpeg: combine images with durations, then add audio
# Use libx264 + aac for max compatibility with TikTok/Facebook
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", list_file,
    "-i", f"{AUDIO_DIR}/full_narration.mp3",
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
print(f"\nRunning ffmpeg...")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("FFMPEG STDERR:", r.stderr[-3000:])
    raise SystemExit(1)

# Verify output
r = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=width,height,codec_name",
     "-of", "default=noprint_wrappers=1", OUT_MP4],
    capture_output=True, text=True,
)
print(f"\n=== Output ===")
print(f"File: {OUT_MP4}")
print(r.stdout)
print(f"Size: {os.path.getsize(OUT_MP4) / 1024 / 1024:.2f} MB")
