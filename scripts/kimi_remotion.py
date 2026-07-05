#!/home/z/.venv/bin/python3
"""Create Remotion project + composition for Kimi K2.7 video. Then render MP4.
Remotion 4.0.484 + Headless Shell already installed."""
import os, json, time
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SBX_ID = "i1icx11jg9lvyzjlwic06"
print(f"=== Connect to sandbox {SBX_ID} ===", flush=True)
sbx = Sandbox.connect(SBX_ID)
sbx.set_timeout(60 * 30)
PATHFIX = "export PATH=/usr/bin:$PATH && "

# Load durations
with open("/tmp/kimi_durations.json") as f:
    durations_data = json.load(f)
durations = durations_data["durations"]
total_dur = durations_data["total"]
print(f"Total duration: {total_dur:.2f}s", flush=True)

# Compute scene start times (in frames at 30fps)
FPS = 30
scenes_list = ["s1","s2","s3","s4","s5","s6","s7","s8"]
scene_starts = {}  # in seconds
scene_durations = {}  # in seconds
cum = 0
for s in scenes_list:
    scene_starts[s] = cum
    scene_durations[s] = durations[s]
    cum += durations[s]
total_frames = int(total_dur * FPS)
print(f"Total frames: {total_frames} at {FPS}fps", flush=True)

# Init Remotion project structure
print("\n=== Init Remotion project ===", flush=True)
sbx.commands.run("mkdir -p /home/user/kimi_project/src", timeout=15)

# Create package.json
package_json = """{
  "name": "kimi-k27-video",
  "version": "1.0.0",
  "description": "Kimi K2.7 Code video",
  "scripts": {
    "build": "remotion render src/index.ts KimiVideo out/kimi.mp4",
    "render": "remotion render src/index.ts KimiVideo out/kimi.mp4 --codec h264 --crf 23"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "remotion": "^4.0.484",
    "@remotion/cli": "^4.0.484",
    "@remotion/react": "^4.0.484",
    "@remotion/ffmpeg": "^4.0.484"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "typescript": "^5.0.0"
  }
}
"""
sbx.files.write("/home/user/kimi_project/package.json", package_json)
print("  package.json written", flush=True)

# Create tsconfig.json
tsconfig = """{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "node",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
"""
sbx.files.write("/home/user/kimi_project/tsconfig.json", tsconfig)
print("  tsconfig.json written", flush=True)

# Install Remotion dependencies locally
print("\n=== Install Remotion deps (npm install) ===", flush=True)
r = sbx.commands.run(PATHFIX + "cd /home/user/kimi_project && npm install --no-audit --no-fund 2>&1 | tail -5", timeout=300)
print(r.stdout, flush=True)

# Create Remotion entry point - index.ts
# This defines the root composition with audio + 8 scenes
# Use staticFile() to load narration.mp3 and screenshots from public/
index_ts = """import {Composition, staticFile, AbsoluteFill, Audio, Sequence, Img, useCurrentFrame, interpolate, Easing} from 'remotion';
import React from 'react';

const FPS = 30;
const W = 1080;
const H = 1920;

// Scene durations in frames
const SCENES = [
  {id: 's1', start: 0, duration: """ + str(int(durations['s1'] * FPS)) + """},
  {id: 's2', start: """ + str(int(scene_starts['s2'] * FPS)) + """, duration: """ + str(int(durations['s2'] * FPS)) + """},
  {id: 's3', start: """ + str(int(scene_starts['s3'] * FPS)) + """, duration: """ + str(int(durations['s3'] * FPS)) + """},
  {id: 's4', start: """ + str(int(scene_starts['s4'] * FPS)) + """, duration: """ + str(int(durations['s4'] * FPS)) + """},
  {id: 's5', start: """ + str(int(scene_starts['s5'] * FPS)) + """, duration: """ + str(int(durations['s5'] * FPS)) + """},
  {id: 's6', start: """ + str(int(scene_starts['s6'] * FPS)) + """, duration: """ + str(int(durations['s6'] * FPS)) + """},
  {id: 's7', start: """ + str(int(scene_starts['s7'] * FPS)) + """, duration: """ + str(int(durations['s7'] * FPS)) + """},
  {id: 's8', start: """ + str(int(scene_starts['s8'] * FPS)) + """, duration: """ + str(int(durations['s8'] * FPS)) + """},
];

const TOTAL_DURATION = """ + str(total_frames) + """;

// Helper: dark gradient background
const Background: React.FC = () => (
  <AbsoluteFill style={{
    background: 'linear-gradient(135deg, #0a0e1a 0%, #1a1a3e 50%, #2d1b69 100%)',
  }}>
    {/* Decorative orbs */}
    <div style={{
      position: 'absolute', top: '-100px', left: '-100px',
      width: '400px', height: '400px', borderRadius: '50%',
      background: '#4285f4', filter: 'blur(60px)', opacity: 0.4,
    }} />
    <div style={{
      position: 'absolute', bottom: '-150px', right: '-150px',
      width: '500px', height: '500px', borderRadius: '50%',
      background: '#9b72cb', filter: 'blur(60px)', opacity: 0.4,
    }} />
  </AbsoluteFill>
);

// Helper: header label (boxed)
const HeaderLabel: React.FC<{text: string; color: string}> = ({text, color}) => (
  <div style={{
    position: 'absolute', top: 90, left: '50%', transform: 'translateX(-50%)',
    padding: '12px 30px', border: `3px solid ${color}`, borderRadius: 8,
    color: color, fontSize: 34, fontWeight: 700, letterSpacing: 1,
  }}>
    {text}
  </div>
);

// Helper: footer label (boxed)
const FooterLabel: React.FC<{text: string; color: string}> = ({text, color}) => (
  <div style={{
    position: 'absolute', bottom: 70, left: '50%', transform: 'translateX(-50%)',
    padding: '10px 20px', border: `2px solid ${color}`, borderRadius: 6,
    color: color, fontSize: 28, fontWeight: 700,
  }}>
    {text}
  </div>
);

// Helper: Vietnamese subtitle at bottom
const Subtitle: React.FC<{lines: string[]}> = ({lines}) => (
  <div style={{
    position: 'absolute', bottom: 180, left: 0, right: 0,
    display: 'flex', flexDirection: 'column', alignItems: 'center',
  }}>
    {lines.map((line, i) => (
      <div key={i} style={{
        color: '#f5f5fa', fontSize: 38, fontWeight: 500,
        textAlign: 'center', marginBottom: 10, lineHeight: 1.3,
      }}>
        {line}
      </div>
    ))}
  </div>
);

// Helper: animated entrance (fade + slide up)
const useEntrance = (startFrame: number, durationInFrames: number) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;
  const opacity = interpolate(localFrame, [0, 10], [0, 1], {extrapolateRight: 'clamp', extrapolateLeft: 'clamp'});
  const translateY = interpolate(localFrame, [0, 10], [30, 0], {extrapolateRight: 'clamp', extrapolateLeft: 'clamp', easing: Easing.out(Easing.ease)});
  return {opacity, transform: `translateY(${translateY}px)`};
};

// === Scene 1: Hook ===
const Scene1: React.FC = () => {
  const entr = useEntrance(0, 30);
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 60}}>
      <HeaderLabel text="🔥 RELEASE 12/6/2026" color="#ff8c32" />
      <div style={{fontSize: 200, marginBottom: 40, marginTop: 100}}>🚀</div>
      <div style={{
        fontSize: 160, fontWeight: 900, color: '#4285f4', textAlign: 'center',
        lineHeight: 1, marginBottom: 30, letterSpacing: -3,
      }}>Kimi K2.7</div>
      <div style={{fontSize: 56, fontWeight: 700, color: '#9b72cb', textAlign: 'center', marginBottom: 30}}>
        Code
      </div>
      <div style={{fontSize: 44, color: '#cbd5e1', textAlign: 'center'}}>
        by Moonshot AI · Open-weights
      </div>
      <Subtitle lines={['Kimi K2.7 Code - mô hình AI coding mới nhất', 'của Moonshot AI, ra mắt 12/6/2026']} />
      <FooterLabel text="OPEN-WEIGHTS · MoE" color="#4285f4" />
    </AbsoluteFill>
  );
};

// === Scene 2: Specs ===
const Scene2: React.FC = () => {
  const entr = useEntrance(0, 30);
  const specs = [
    {icon: '📊', title: '1T params', desc: '32B active MoE', color: '#fac850'},
    {icon: '📚', title: '256K context', desc: 'long-context window', color: '#4285f4'},
    {icon: '⚡', title: '-30% thinking', desc: 'vs K2.6', color: '#50c878'},
    {icon: '📜', title: 'MIT modified', desc: 'commercial use OK', color: '#9b72dc'},
  ];
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="THÔNG SỐ KỸ THUẬT" color="#fac850" />
      <div style={{fontSize: 72, fontWeight: 800, color: '#fff', marginTop: 130, marginBottom: 50}}>Specs</div>
      {specs.map((s, i) => (
        <div key={i} style={{
          display: 'flex', alignItems: 'center', gap: 24, width: '100%',
          background: 'rgba(30,41,59,0.7)', border: `2px solid ${s.color}`,
          borderRadius: 18, padding: '24px 32px', marginBottom: 16,
        }}>
          <div style={{fontSize: 56}}>{s.icon}</div>
          <div>
            <div style={{fontSize: 50, fontWeight: 700, color: s.color}}>{s.title}</div>
            <div style={{fontSize: 34, color: '#a0a0b4'}}>{s.desc}</div>
          </div>
        </div>
      ))}
      <Subtitle lines={['1T params MoE (32B active), 256K context', 'Giảm 30% thinking tokens vs K2.6']} />
      <FooterLabel text="MoE · LONG CONTEXT" color="#fac850" />
    </AbsoluteFill>
  );
};

// === Scene 3: Thinking efficiency ===
const Scene3: React.FC = () => {
  const entr = useEntrance(0, 30);
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="THINKING EFFICIENCY" color="#50c878" />
      <div style={{fontSize: 200, marginBottom: 40, marginTop: 130}}>⚡</div>
      <div style={{fontSize: 100, fontWeight: 900, color: '#50c878', marginBottom: 30}}>-30%</div>
      <div style={{fontSize: 48, fontWeight: 700, color: '#fff', textAlign: 'center', marginBottom: 20}}>
        thinking tokens
      </div>
      <div style={{fontSize: 38, color: '#cbd5e1', textAlign: 'center', marginBottom: 40}}>
        so với Kimi K2.6
      </div>
      <div style={{
        background: 'rgba(30,41,59,0.7)', border: '2px solid #4285f4',
        borderRadius: 18, padding: '30px 40px', width: '100%',
      }}>
        <div style={{fontSize: 34, color: '#a0a0b4', marginBottom: 12}}>Forces thinking mode</div>
        <div style={{fontSize: 36, color: '#fff'}}>✓ Tối ưu long-horizon SWE</div>
      </div>
      <Subtitle lines={['Giảm 30% thinking tokens so với K2.6', 'Forces thinking mode cho mọi task']} />
      <FooterLabel text="EFFICIENT REASONING" color="#50c878" />
    </AbsoluteFill>
  );
};

// === Scene 4: Benchmarks ===
const Scene4: React.FC = () => {
  const entr = useEntrance(0, 30);
  const benchmarks = [
    {name: 'Kimi Code Bench v2', gain: '+21.8%', color: '#fac850'},
    {name: 'Program Bench', gain: '+11.0%', color: '#4285f4'},
    {name: 'MLS Bench Lite', gain: '+31.5%', color: '#50c878'},
    {name: 'MCP Mark Verified', gain: '+11.4%', color: '#9b72dc'},
    {name: 'Kimi Claw 24/7 Bench', gain: '+9.3%', color: '#ff8c32'},
  ];
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="BENCHMARK vs K2.6" color="#f05a46" />
      <div style={{fontSize: 70, fontWeight: 800, color: '#fff', marginTop: 130, marginBottom: 40}}>Cải thiện</div>
      {benchmarks.map((b, i) => (
        <div key={i} style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%',
          background: 'rgba(30,41,59,0.7)', border: `2px solid ${b.color}`,
          borderRadius: 14, padding: '20px 30px', marginBottom: 12,
        }}>
          <div style={{fontSize: 36, color: '#fff'}}>{b.name}</div>
          <div style={{fontSize: 42, fontWeight: 800, color: b.color}}>{b.gain}</div>
        </div>
      ))}
      <Subtitle lines={['Benchmark tăng vọt so với K2.6', 'Code Bench +21.8%, MLS Bench +31.5%']} />
      <FooterLabel text="SIGNIFICANT GAINS" color="#f05a46" />
    </AbsoluteFill>
  );
};

// === Scene 5: HuggingFace screenshot ===
const Scene5: React.FC = () => {
  const entr = useEntrance(0, 30);
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="HUGGINGFACE" color="#9b72dc" />
      <div style={{fontSize: 56, fontWeight: 800, color: '#9b72dc', marginTop: 130, marginBottom: 30}}>
        moonshotai/Kimi-K2.7-Code
      </div>
      <Img src={staticFile('01_hf_title.png')} style={{
        width: 950, height: 'auto', borderRadius: 24,
        border: '4px solid rgba(155,114,220,0.5)',
        boxShadow: '0 20px 60px rgba(155,114,220,0.4)',
        marginBottom: 30,
      }} />
      <div style={{
        background: 'rgba(30,41,59,0.7)', border: '2px solid #9b72dc',
        borderRadius: 18, padding: '24px 32px', width: '100%',
      }}>
        <div style={{fontSize: 38, fontWeight: 700, color: '#9b72dc', marginBottom: 10}}>Modified MIT</div>
        <div style={{fontSize: 32, color: '#cbd5e1'}}>✓ Commercial use OK</div>
      </div>
      <Subtitle lines={['Model trên HuggingFace: moonshotai/Kimi-K2.7-Code', 'License: Modified MIT (commercial OK)']} />
      <FooterLabel text="HF · OPEN-WEIGHTS" color="#9b72dc" />
    </AbsoluteFill>
  );
};

// === Scene 6: GitHub screenshot ===
const Scene6: React.FC = () => {
  const entr = useEntrance(0, 30);
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="GITHUB REPO" color="#4285f4" />
      <div style={{fontSize: 56, fontWeight: 800, color: '#4285f4', marginTop: 130, marginBottom: 20}}>
        MoonshotAI/Kimi-K2
      </div>
      <div style={{fontSize: 36, color: '#cbd5e1', marginBottom: 30}}>
        10,800+ stars · 900+ forks
      </div>
      <Img src={staticFile('03_gh_title.png')} style={{
        width: 950, height: 'auto', borderRadius: 24,
        border: '4px solid rgba(66,133,244,0.5)',
        boxShadow: '0 20px 60px rgba(66,133,244,0.4)',
        marginBottom: 30,
      }} />
      <div style={{
        background: 'rgba(30,41,59,0.7)', border: '2px solid #4285f4',
        borderRadius: 18, padding: '20px 30px', width: '100%',
      }}>
        <div style={{fontSize: 32, color: '#cbd5e1'}}>Part of Kimi K2 ecosystem</div>
      </div>
      <Subtitle lines={['GitHub: MoonshotAI/Kimi-K2 (10.8K stars)', 'Repository chính thức của Moonshot AI']} />
      <FooterLabel text="GITHUB · OPEN SOURCE" color="#4285f4" />
    </AbsoluteFill>
  );
};

// === Scene 7: Use cases ===
const Scene7: React.FC = () => {
  const entr = useEntrance(0, 30);
  const cases = [
    {icon: '🔧', text: 'Complex SWE', color: '#4285f4'},
    {icon: '📋', text: 'Long-horizon agentic', color: '#9b72dc'},
    {icon: '💻', text: 'Multi-step coding', color: '#50c878'},
    {icon: '🔄', text: 'CI/CD integration', color: '#fac850'},
  ];
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="USE CASES" color="#4285f4" />
      <div style={{fontSize: 72, fontWeight: 800, color: '#fff', marginTop: 130, marginBottom: 50}}>Ứng dụng</div>
      {cases.map((c, i) => (
        <div key={i} style={{
          display: 'flex', alignItems: 'center', gap: 24, width: '100%',
          background: 'rgba(30,41,59,0.7)', border: `2px solid ${c.color}`,
          borderRadius: 14, padding: '24px 32px', marginBottom: 16,
        }}>
          <div style={{fontSize: 56}}>{c.icon}</div>
          <div style={{fontSize: 42, fontWeight: 700, color: c.color}}>{c.text}</div>
        </div>
      ))}
      <Subtitle lines={['Use cases: complex SWE, long-horizon agentic', 'Multi-step coding, CI/CD integration']} />
      <FooterLabel text="AGENTIC CODING" color="#4285f4" />
    </AbsoluteFill>
  );
};

// === Scene 8: Takeaway ===
const Scene8: React.FC = () => {
  const entr = useEntrance(0, 30);
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="TAKEAWAY" color="#50c878" />
      <div style={{fontSize: 200, marginBottom: 40, marginTop: 130}}>🎯</div>
      <div style={{fontSize: 80, fontWeight: 900, color: '#50c878', textAlign: 'center', marginBottom: 30, lineHeight: 1.1}}>
        Lựa chọn<br/>tuyệt vời
      </div>
      <div style={{fontSize: 38, color: '#cbd5e1', textAlign: 'center', marginBottom: 40}}>
        cho AI coding agent mạnh + tiết kiệm
      </div>
      <div style={{
        background: 'rgba(20,20,30,0.8)', border: '3px solid #4285f4',
        borderRadius: 18, padding: '30px 40px', width: '100%',
      }}>
        <div style={{fontSize: 36, fontWeight: 700, color: '#4285f4', marginBottom: 12, textAlign: 'center'}}>
          huggingface.co/moonshotai
        </div>
        <div style={{fontSize: 32, fontWeight: 700, color: '#50c878', textAlign: 'center'}}>
          #KimiK27 #MoonshotAI #OpenSource
        </div>
      </div>
      <Subtitle lines={['Kimi K2.7 Code - AI coding agent mạnh + tiết kiệm', 'Follow kênh để cập nhật AI mới nhất!']} />
      <FooterLabel text="FOLLOW FOR MORE" color="#50c878" />
    </AbsoluteFill>
  );
};

// Scene components map
const SCENE_COMPONENTS: Record<string, React.FC> = {
  s1: Scene1, s2: Scene2, s3: Scene3, s4: Scene4,
  s5: Scene5, s6: Scene6, s7: Scene7, s8: Scene8,
};

// Root composition
export const KimiVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#0a0e1a'}}>
      <Background />
      {/* Audio narration */}
      <Audio src={staticFile('narration.mp3')} />
      {/* Scenes */}
      {SCENES.map((scene) => {
        const Comp = SCENE_COMPONENTS[scene.id];
        return (
          <Sequence key={scene.id} from={scene.start} durationInFrames={scene.duration}>
            <Comp />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

// Register composition
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="KimiVideo"
        component={KimiVideo}
        durationInFrames={TOTAL_DURATION}
        fps={FPS}
        width={W}
        height={H}
      />
    </>
  );
};
"""
sbx.files.write("/home/user/kimi_project/src/index.tsx", index_ts)
print("  src/index.tsx written", flush=True)

# Render
print(f"\n=== Render video ({total_dur:.2f}s, {FPS}fps) ===", flush=True)
try:
    r = sbx.commands.run(
        f"cd /home/user/kimi_project && "
        f"nohup bash -c '{PATHFIX} remotion render src/index.tsx KimiVideo out/kimi.mp4 --codec h264 --crf 23 --concurrency 1 > /tmp/render.log 2>&1' "
        f"</dev/null > /dev/null 2>&1 & disown; echo PID=$!",
        timeout=20,
    )
    print(r.stdout, flush=True)
except Exception as e:
    print(f"render start err: {e}", flush=True)

# Poll (max 12 min)
print("\n=== Poll render (max 12 min) ===", flush=True)
start_poll = time.time()
done = False
while time.time() - start_poll < 720:
    time.sleep(30)
    try:
        sbx = Sandbox.connect(SBX_ID)
        sbx.set_timeout(60 * 30)
        r = sbx.commands.run(
            "ls /home/user/kimi_project/out/*.mp4 2>/dev/null && echo MP4_FOUND || echo NO_MP4; "
            "ps aux | grep remotion | grep -v grep | wc -l; "
            "tail -1 /tmp/render.log 2>&1 | head -c 200",
            timeout=15,
        )
        elapsed = int(time.time() - start_poll)
        out = r.stdout.strip().replace('\n', ' | ')[:250]
        print(f"[{elapsed}s] {out}", flush=True)
        if 'MP4_FOUND' in r.stdout:
            r2 = sbx.commands.run(
                "ls -la /home/user/kimi_project/out/*.mp4 && "
                "ffprobe -v error -show_entries format=duration,size:stream=width,height /home/user/kimi_project/out/kimi.mp4 2>&1",
                timeout=15,
            )
            print("MP4 READY:", r2.stdout, flush=True)
            done = True
            break
    except Exception as e:
        print(f"poll err: {e}", flush=True)

if not done:
    print("Render did not finish. Last log:", flush=True)
    try:
        sbx = Sandbox.connect(SBX_ID)
        r = sbx.commands.run('tail -30 /tmp/render.log 2>&1', timeout=15)
        print(r.stdout, flush=True)
    except: pass

print(f"\nSandbox: {SBX_ID}", flush=True)
