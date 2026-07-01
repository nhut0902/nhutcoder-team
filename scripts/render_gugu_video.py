"""Render MP4 from 5 Gugu AI images + mixed audio. 9:16 vertical for TikTok."""
import os, subprocess, json

FRAMES_DIR = "/home/z/my-project/download/gugu_ai_images"
AUDIO = "/home/z/my-project/download/gugu_video_audio/mixed.mp3"
OUT_MP4 = "/home/z/my-project/download/gugu-video.mp4"

# 5 images, each ~12s = 60s total
DURATION_PER_IMG = 12.0

images = sorted([f for f in os.listdir(FRAMES_DIR) if f.endswith(('.png','.jpg','.jpeg'))])
print(f"Images: {len(images)}")
for img in images:
    print(f"  - {img}")

# Get audio duration
r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1", AUDIO], capture_output=True, text=True)
audio_dur = float(r.stdout.strip())
print(f"\nAudio duration: {audio_dur:.2f}s")

# Build concat list (image2 demuxer with duration per image)
list_file = "/tmp/gugu_video_concat.txt"
with open(list_file, "w") as f:
    for img in images:
        f.write(f"file '{FRAMES_DIR}/{img}'\n")
        f.write(f"duration {DURATION_PER_IMG:.3f}\n")
    # Repeat last image (ffmpeg quirk)
    f.write(f"file '{FRAMES_DIR}/{images[-1]}'\n")

print(f"\nConcat list: {list_file}")

# First, get image dimensions to determine scaling
sample_img = os.path.join(FRAMES_DIR, images[0])
r = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height", f"file:{sample_img}"], capture_output=True, text=True)
print(f"Sample image: {r.stdout}")

# Render MP4 9:16 (1080x1920) - scale + pad images to fit
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", list_file,
    "-i", AUDIO,
    "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1",
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

# Verify output
r = subprocess.run(
    ["ffprobe","-v","error","-show_entries","format=duration,size:stream=width,height,codec_name","-of","default=noprint_wrappers=1", OUT_MP4],
    capture_output=True, text=True,
)
print(f"\n=== Output ===")
print(f"File: {OUT_MP4}")
print(r.stdout)
print(f"Size: {os.path.getsize(OUT_MP4) / 1024 / 1024:.2f} MB")
