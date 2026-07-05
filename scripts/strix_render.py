#!/home/z/.venv/bin/python3
"""Render final MP4 with smooth crossfade + zoom animation + TTS narration + background music."""
import os, subprocess, json

FRAMES = "/home/z/my-project/download/strix_frames"
NARRATION = "/home/z/my-project/download/strix_audio/narration.mp3"
OUT_MP4 = "/home/z/my-project/download/strix-video.mp4"

with open("/tmp/strix_durations.json") as f:
    d = json.load(f)
    durations = d["durations"]
    total = d["total"]

scenes = [f"s{i}" for i in range(1, 7)]
print(f"Per-scene durations:")
for s in scenes:
    print(f"  {s}: {durations[s]:.2f}s")
print(f"Total: {total:.2f}s")

# === Generate background music (royalty-free synth) ===
print("\n=== Generate background music ===")
BG_MUSIC = "/home/z/my-project/download/strix_audio/bg_music.mp3"
bg_dur = int(total + 5)
r = subprocess.run([
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", "sine=frequency=110:duration=" + str(bg_dur),
    "-f", "lavfi", "-i", "sine=frequency=164.81:duration=" + str(bg_dur),
    "-f", "lavfi", "-i", "sine=frequency=220:duration=" + str(bg_dur),
    "-filter_complex",
    "[0:a]volume=0.18,tremolo=f=0.3:d=0.4[a1];"
    "[1:a]volume=0.12,tremolo=f=0.25:d=0.4[a2];"
    "[2:a]volume=0.10,tremolo=f=0.2:d=0.4[a3];"
    "[a1][a2][a3]amix=inputs=3:duration=longest:weights=1 1 1,"
    "aecho=0.7:0.5:60|120:0.3|0.2,"
    f"afade=t=in:st=0:d=2,afade=t=out:st={total-3}:d=3",
    "-t", str(bg_dur), "-b:a", "96k", BG_MUSIC,
], capture_output=True, text=True)
if r.returncode == 0:
    print(f"  BG music: {BG_MUSIC}")
else:
    print(f"  BG err: {r.stderr[-300:]}")

# === Mix narration + bg music ===
print("\n=== Mix narration + bg music ===")
MIXED = "/home/z/my-project/download/strix_audio/mixed.mp3"
r = subprocess.run([
    "ffmpeg", "-y",
    "-i", NARRATION,
    "-i", BG_MUSIC,
    "-filter_complex",
    f"[1:a]volume=0.20[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0:weights=1 0.6",
    "-b:a", "96k", MIXED,
], capture_output=True, text=True)
if r.returncode == 0:
    print(f"  Mixed: {MIXED}")
else:
    print(f"  Mix err: {r.stderr[-300:]}")

# === Render video with smooth crossfade + zoom ===
# Use xfade filter for crossfade between scenes (0.5s overlap each)
# Plus subtle zoom (Ken Burns effect) on each scene
print("\n=== Render video with crossfade + zoom ===")

# Build complex filter:
# For each scene, apply zoompan (subtle zoom in)
# Then xfade between scenes
crossfade_dur = 0.5
inputs = []
filter_parts = []
prev_label = None

for i, s in enumerate(scenes):
    inputs.extend(["-i", f"{FRAMES}/{s}.png"])
    scene_dur = durations[s]
    # zoompan: subtle zoom from 1.0 to 1.05 over the scene duration
    # fps 30, total frames = scene_dur * 30
    total_frames = int(scene_dur * 30)
    zoom_filter = (
        f"[{i}:v]"
        f"scale=1080:1920:force_original_aspect_ratio=decrease,"
        f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,"
        f"setsar=1,"
        f"zoompan=z='min(zoom+0.0008,1.05)':d={total_frames}:s=1080x1920:fps=30,"
        f"trim=duration={scene_dur:.3f},setpts=PTS-STARTPTS,"
        f"fps=30,format=yuv420p"
        f"[v{i}]"
    )
    filter_parts.append(zoom_filter)

# Now apply xfade chain
for i, s in enumerate(scenes):
    if i == 0:
        # First scene stays as v0
        prev_label = "v0"
    else:
        # xfade prev + v{i}
        # offset = sum of (prev durations) - crossfade_dur * (number of prev xfades)
        # For each xfade: duration consumed = prev_dur - crossfade_dur
        offset = sum(durations[scenes[j]] for j in range(i)) - crossfade_dur * i
        new_label = f"x{i}"
        filter_parts.append(
            f"[{prev_label}][v{i}]xfade=transition=fade:duration={crossfade_dur}:offset={offset:.3f}[{new_label}]"
        )
        prev_label = new_label

# Final label
filter_parts.append(f"[{prev_label}]format=yuv420p[vout]")

filter_complex = ";".join(filter_parts)

cmd = [
    "ffmpeg", "-y",
    *inputs,
    "-i", MIXED,
    "-filter_complex", filter_complex,
    "-map", "[vout]",
    "-map", f"{len(scenes)}:a",  # audio is last input
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

print(f"Running ffmpeg (this may take 2-3 min)...")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("FFMPEG STDERR:", r.stderr[-3000:])
    raise SystemExit(1)

# Verify output
r = subprocess.run(
    ["ffprobe","-v","error","-show_entries","format=duration,size:stream=width,height,codec_name,r_frame_rate","-of","default=noprint_wrappers=1", OUT_MP4],
    capture_output=True, text=True,
)
print(f"\n=== Output ===")
print(f"File: {OUT_MP4}")
print(r.stdout)
print(f"Size: {os.path.getsize(OUT_MP4) / 1024 / 1024:.2f} MB")
