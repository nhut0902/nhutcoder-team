"""Generate 2-minute Vietnamese narration about FireClaw - 8 scenes."""
import os, subprocess, json, time

OUT_DIR = "/home/z/my-project/download/fireclaw_audio"
os.makedirs(OUT_DIR, exist_ok=True)

VOICE = "vi-VN-NamMinhNeural"

# 8 scenes, ~15s each = 120s total (2 minutes)
scenes = [
    {"id": "s1", "text": "Chào mừng các bạn đến với video hôm nay. Hôm nay mình sẽ giới thiệu một công cụ cực kỳ quan trọng cho bất kỳ ai đang xây dựng AI Agent, đó là FireClaw - bức tường lửa bảo vệ bộ não của AI agent khỏi các cuộc tấn công prompt injection."},
    {"id": "s2", "text": "Vậy Prompt Injection là gì? Đây là kỹ thuật tấn công mà hacker giấu mã độc hoặc lệnh nguy hiểm bên trong nội dung web mà AI agent đang đọc. Khi agent xử lý nội dung này, nó có thể bị thao túng, làm sai lệch hành vi và rò rỉ dữ liệu."},
    {"id": "s3", "text": "FireClaw là một proxy bảo mật mã nguồn mở do nhóm raiph-ai phát triển. Nó đóng vai trò như một lớp lọc trung gian giữa AI agent của bạn và internet, đảm bảo mọi nội dung agent nhận được đều sạch và an toàn."},
    {"id": "s4", "text": "FireClaw hoạt động qua một pipeline bốn giai đoạn. Giai đoạn đầu là Fetching, tải nội dung web từ nguồn. Tiếp theo là Sanitizing, loại bỏ mã độc, script, style ẩn và các thủ thuật mã hóa."},
    {"id": "s5", "text": "Giai đoạn ba là Summarizing, tóm tắt nội dung để agent chỉ nhận thông tin cần thiết. Cuối cùng là Scanning, quét toàn bộ bằng nguồn threat intelligence cộng đồng để phát hiện các mẫu tấn công đã biết."},
    {"id": "s6", "text": "Các tính năng nổi bật bao gồm hệ thống canary token theo dõi kẻ tấn công cố gắng rút trộm dữ liệu, audit logging đầy đủ để phục hồi lại bất kỳ request nào, và rate limiting giúp quản lý tài nguyên hiệu quả."},
    {"id": "s7", "text": "FireClaw hoàn toàn miễn phí và mã nguồn mở trên GitHub. Bạn chỉ cần clone repository, cấu hình domain trust tiers theo nhu cầu, và tích hợp vào workflow AI agent hiện tại. Phù hợp cho cả cá nhân lẫn doanh nghiệp."},
    {"id": "s8", "text": "Trong thời đại AI agent ngày càng phổ biến, bảo mật không còn là tùy chọn. FireClaw là lớp phòng thủ đầu tiên mà mọi developer nên có. Truy cập github.com/raiph-ai/fireclaw để bắt đầu. Cảm ơn các bạn đã theo dõi, hãy like và subscribe nhé!"},
]

def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except:
        return 0.0

durations = {}
print(f"=== Generating {len(scenes)} chunks with {VOICE} ===")
for s in scenes:
    out = os.path.join(OUT_DIR, f"{s['id']}.mp3")
    # Retry up to 5 times for edge-tts flakiness
    for attempt in range(5):
        if os.path.exists(out):
            os.remove(out)
        r = subprocess.run(
            ["edge-tts", "--voice", VOICE, "--text", s["text"], "--write-media", out],
            capture_output=True, text=True,
        )
        size = os.path.getsize(out) if os.path.exists(out) else 0
        if size > 1000:
            break
        print(f"  {s['id']} attempt {attempt+1} failed ({size}B), retry...")
        time.sleep(2)
    
    dur = get_duration(out)
    durations[s["id"]] = dur
    print(f"  {s['id']}: {dur:.2f}s ({os.path.getsize(out)}B)")

total = sum(durations.values())
print(f"\nTotal: {total:.2f}s ({total/60:.1f} min)")

with open(os.path.join(OUT_DIR, "durations.json"), "w") as f:
    json.dump({"durations": durations, "total": total, "scenes": scenes}, f, ensure_ascii=False, indent=2)

# Concat all into single MP3 with re-encode for safety
inputs = [os.path.join(OUT_DIR, f"{s['id']}.mp3") for s in scenes]
filter_str = "".join(f"[{i}:a]" for i in range(len(inputs))) + f"concat=n={len(inputs)}:v=0:a=1[out]"
full_mp3 = os.path.join(OUT_DIR, "full_narration.mp3")
cmd = ["ffmpeg", "-y"] + [arg for inp in inputs for arg in ("-i", inp)] + [
    "-filter_complex", filter_str, "-map", "[out]",
    "-b:a", "64k", full_mp3,
]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("concat err:", r.stderr[-500:])
else:
    print(f"Full: {full_mp3} ({get_duration(full_mp3):.2f}s)")
