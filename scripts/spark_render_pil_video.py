"""Render MP4: 8 PIL frames + TTS narration. 24fps for TikTok compatibility. With fade transitions."""
import os, subprocess, json

FRAMES = "/home/z/my-project/download/spark_pil_frames"
AUDIO = "/home/z/my-project/download/spark_audio/narration.mp3"
OUT_MP4 = "/home/z/my-project/download/spark-pil-video.mp4"

# Load durations
with open("/tmp/spark_durations.json") as f:
    durations = json.load(f)["durations"]
scenes = [f"s{i}" for i in range(1, 9)]

# Speed up narration to ~60s total (108s original -> need 1.8x speedup)
# Actually let's use original 108s durations per scene and speed audio separately
# But user wants 2 min or so... Let's use original durations for total ~108s

print("Per-scene durations:")
total = 0
for s in scenes:
    print(f"  {s}: {durations[s]:.2f}s")
    total += durations[s]
print(f"Total: {total:.2f}s ({total/60:.2f} min)")

# Build concat list for image2 demuxer
list_file = "/tmp/spark_pil_concat.txt"
with open(list_file, "w") as f:
    for s in scenes:
        f.write(f"file '{FRAMES}/{s}.png'\n")
        f.write(f"duration {durations[s]:.3f}\n")
    # Repeat last (ffmpeg quirk)
    f.write(f"file '{FRAMES}/{scenes[-1]}.png'\n")

print(f"\nConcat list: {list_file}")

# Render: frames + narration audio, 24fps for TikTok, with xfade between scenes
# Simpler approach: use concat demuxer + add fade-in/out filter globally
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", list_file,
    "-i", AUDIO,
    "-vf", "fade=t=in:st=0:d=0.5,fade=t=out:st=" + str(total - 1) + ":d=1",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "24",
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
