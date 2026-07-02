"""Render final MP4: 8 dark card frames + TTS narration. 24fps TikTok-compatible."""
import os, subprocess, json

FRAMES = "/home/z/my-project/download/spark_darkcard_frames"
AUDIO = "/home/z/my-project/download/spark_audio/narration.mp3"
OUT_MP4 = "/home/z/my-project/download/spark-darkcard-video.mp4"

with open("/tmp/spark_durations.json") as f:
    durations = json.load(f)["durations"]
scenes = [f"s{i}" for i in range(1, 9)]

total = sum(durations[s] for s in scenes)
print(f"Total duration: {total:.2f}s ({total/60:.2f} min)")

# Build concat list
list_file = "/tmp/spark_darkcard_concat.txt"
with open(list_file, "w") as f:
    for s in scenes:
        f.write(f"file '{FRAMES}/{s}.png'\n")
        f.write(f"duration {durations[s]:.3f}\n")
    f.write(f"file '{FRAMES}/{scenes[-1]}.png'\n")

print(f"\nConcat list: {list_file}")

# Render with fade in/out
fade_out_start = total - 1.5
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", list_file,
    "-i", AUDIO,
    "-vf", f"fade=t=in:st=0:d=0.4,fade=t=out:st={fade_out_start:.2f}:d=1.5",
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

r = subprocess.run(
    ["ffprobe","-v","error","-show_entries","format=duration,size:stream=width,height,codec_name,r_frame_rate","-of","default=noprint_wrappers=1", OUT_MP4],
    capture_output=True, text=True,
)
print(f"\n=== Output ===")
print(f"File: {OUT_MP4}")
print(r.stdout)
print(f"Size: {os.path.getsize(OUT_MP4) / 1024 / 1024:.2f} MB")
