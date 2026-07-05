#!/home/z/.venv/bin/python3
"""Render final GLM-5 MP4: 8 PIL frames + VieNeu narration + subtle bg music.
NO animation - just clean concat with subtle fade. TikTok/Reels optimized."""
import os, subprocess, json

FRAMES = "/home/z/my-project/download/glm5_frames"
NARRATION = "/home/z/my-project/download/glm5_audio/narration.mp3"
OUT_MP4 = "/home/z/my-project/download/glm5-video-v2.mp4"

with open("/tmp/glm5_durations.json") as f:
    d = json.load(f)
    durations = d["durations"]
    total = d["total"]

scenes = [f"s{i}" for i in range(1, 9)]
print(f"Per-scene durations:")
for s in scenes:
    print(f"  {s}: {durations[s]:.2f}s")
print(f"Total: {total:.2f}s")

# === Generate subtle bg music ===
print("\n=== Generate bg music ===")
BG_MUSIC = "/home/z/my-project/download/glm5_audio/bg_music.mp3"
bg_dur = int(total + 3)
subprocess.run([
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", f"sine=frequency=130.81:duration={bg_dur}",
    "-f", "lavfi", "-i", f"sine=frequency=196:duration={bg_dur}",
    "-filter_complex",
    "[0:a]volume=0.10,tremolo=f=0.2:d=0.4[a1];"
    "[1:a]volume=0.07,tremolo=f=0.15:d=0.4[a2];"
    "[a1][a2]amix=inputs=2:duration=longest:weights=1 1,"
    f"afade=t=in:st=0:d=2,afade=t=out:st={total-3}:d=3",
    "-t", str(bg_dur), "-b:a", "96k", BG_MUSIC,
], capture_output=True, check=True)
print(f"  BG music: {BG_MUSIC}")

# === Mix narration + bg ===
print("\n=== Mix narration + bg music ===")
MIXED = "/home/z/my-project/download/glm5_audio/mixed.mp3"
subprocess.run([
    "ffmpeg", "-y",
    "-i", NARRATION,
    "-i", BG_MUSIC,
    "-filter_complex",
    "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0:weights=1 0.5",
    "-b:a", "96k", MIXED,
], capture_output=True, check=True)
print(f"  Mixed: {MIXED}")

# === Build concat list ===
list_file = "/tmp/glm5_concat.txt"
with open(list_file, "w") as f:
    for s in scenes:
        f.write(f"file '{FRAMES}/{s}.png'\n")
        f.write(f"duration {durations[s]:.3f}\n")
    f.write(f"file '{FRAMES}/{scenes[-1]}.png'\n")

print(f"\nConcat list: {list_file}")

# === Render: concat frames + audio, 24fps, fade in/out, optimized ===
fade_out_start = max(0, total - 1.5)
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", list_file,
    "-i", MIXED,
    "-vf", f"fade=t=in:st=0:d=0.4,fade=t=out:st={fade_out_start:.2f}:d=1.5",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "24",
    "-preset", "slow",
    "-crf", "23",
    "-c:a", "aac",
    "-b:a", "128k",
    "-ar", "44100",
    "-shortest",
    "-movflags", "+faststart",
    OUT_MP4,
]
print(f"\nRendering...")
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
