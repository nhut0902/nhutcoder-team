import {Composition, staticFile, AbsoluteFill, Audio, Sequence, Img, useCurrentFrame, interpolate, Easing, registerRoot} from 'remotion';
import React from 'react';

const FPS = 30;
const W = 1080;
const H = 1920;
const TOTAL_DURATION = __TOTAL_FRAMES__;

const Background: React.FC = () => (
  <AbsoluteFill style={{background: 'linear-gradient(135deg, #0a0e1a 0%, #1a1a3e 50%, #2d1b69 100%)'}}>
    <div style={{position: 'absolute', top: '-100px', left: '-100px', width: 400, height: 400, borderRadius: '50%', background: '#4285f4', filter: 'blur(60px)', opacity: 0.4}} />
    <div style={{position: 'absolute', bottom: '-150px', right: '-150px', width: 500, height: 500, borderRadius: '50%', background: '#9b72cb', filter: 'blur(60px)', opacity: 0.4}} />
  </AbsoluteFill>
);

const HeaderLabel: React.FC<{text: string; color: string}> = ({text, color}) => (
  <div style={{position: 'absolute', top: 90, left: '50%', transform: 'translateX(-50%)', padding: '12px 30px', border: `3px solid ${color}`, borderRadius: 8, color: color, fontSize: 34, fontWeight: 700}}>
    {text}
  </div>
);

const FooterLabel: React.FC<{text: string; color: string}> = ({text, color}) => (
  <div style={{position: 'absolute', bottom: 70, left: '50%', transform: 'translateX(-50%)', padding: '10px 20px', border: `2px solid ${color}`, borderRadius: 6, color: color, fontSize: 28, fontWeight: 700}}>
    {text}
  </div>
);

const Subtitle: React.FC<{lines: string[]}> = ({lines}) => (
  <div style={{position: 'absolute', bottom: 180, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
    {lines.map((line, i) => (
      <div key={i} style={{color: '#f5f5fa', fontSize: 38, fontWeight: 500, textAlign: 'center', marginBottom: 10}}>
        {line}
      </div>
    ))}
  </div>
);

const useEntrance = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp', extrapolateLeft: 'clamp'});
  const translateY = interpolate(frame, [0, 10], [30, 0], {extrapolateRight: 'clamp', extrapolateLeft: 'clamp', easing: Easing.out(Easing.ease)});
  return {opacity, transform: `translateY(${translateY}px)`};
};

const Scene1: React.FC = () => {
  const entr = useEntrance();
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 60}}>
      <HeaderLabel text="🔥 RELEASE 12/6/2026" color="#ff8c32" />
      <div style={{fontSize: 200, marginBottom: 40, marginTop: 100}}>🚀</div>
      <div style={{fontSize: 160, fontWeight: 900, color: '#4285f4', textAlign: 'center', lineHeight: 1, marginBottom: 30, letterSpacing: -3}}>Kimi K2.7</div>
      <div style={{fontSize: 56, fontWeight: 700, color: '#9b72cb', marginBottom: 30}}>Code</div>
      <div style={{fontSize: 44, color: '#cbd5e1', textAlign: 'center'}}>by Moonshot AI · Open-weights</div>
      <Subtitle lines={['Kimi K2.7 Code - mô hình AI coding mới nhất', 'của Moonshot AI, ra mắt 12/6/2026']} />
      <FooterLabel text="OPEN-WEIGHTS · MoE" color="#4285f4" />
    </AbsoluteFill>
  );
};

const Scene2: React.FC = () => {
  const entr = useEntrance();
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
        <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, width: '100%', background: 'rgba(30,41,59,0.7)', border: `2px solid ${s.color}`, borderRadius: 18, padding: '24px 32px', marginBottom: 16}}>
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

const Scene3: React.FC = () => {
  const entr = useEntrance();
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="THINKING EFFICIENCY" color="#50c878" />
      <div style={{fontSize: 200, marginBottom: 40, marginTop: 130}}>⚡</div>
      <div style={{fontSize: 100, fontWeight: 900, color: '#50c878', marginBottom: 30}}>-30%</div>
      <div style={{fontSize: 48, fontWeight: 700, color: '#fff', marginBottom: 20}}>thinking tokens</div>
      <div style={{fontSize: 38, color: '#cbd5e1', marginBottom: 40}}>so với Kimi K2.6</div>
      <div style={{background: 'rgba(30,41,59,0.7)', border: '2px solid #4285f4', borderRadius: 18, padding: '30px 40px', width: '100%'}}>
        <div style={{fontSize: 34, color: '#a0a0b4', marginBottom: 12}}>Forces thinking mode</div>
        <div style={{fontSize: 36, color: '#fff'}}>✓ Tối ưu long-horizon SWE</div>
      </div>
      <Subtitle lines={['Giảm 30% thinking tokens so với K2.6', 'Forces thinking mode cho mọi task']} />
      <FooterLabel text="EFFICIENT REASONING" color="#50c878" />
    </AbsoluteFill>
  );
};

const Scene4: React.FC = () => {
  const entr = useEntrance();
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
        <div key={i} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', background: 'rgba(30,41,59,0.7)', border: `2px solid ${b.color}`, borderRadius: 14, padding: '20px 30px', marginBottom: 12}}>
          <div style={{fontSize: 36, color: '#fff'}}>{b.name}</div>
          <div style={{fontSize: 42, fontWeight: 800, color: b.color}}>{b.gain}</div>
        </div>
      ))}
      <Subtitle lines={['Benchmark tăng vọt so với K2.6', 'Code Bench +21.8%, MLS Bench +31.5%']} />
      <FooterLabel text="SIGNIFICANT GAINS" color="#f05a46" />
    </AbsoluteFill>
  );
};

const Scene5: React.FC = () => {
  const entr = useEntrance();
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="HUGGINGFACE" color="#9b72dc" />
      <div style={{fontSize: 46, fontWeight: 800, color: '#9b72dc', marginTop: 130, marginBottom: 30, textAlign: 'center'}}>moonshotai/Kimi-K2.7-Code</div>
      <Img src={staticFile('01_hf_title.png')} style={{width: 950, height: 'auto', borderRadius: 24, border: '4px solid rgba(155,114,220,0.5)', boxShadow: '0 20px 60px rgba(155,114,220,0.4)', marginBottom: 30}} />
      <div style={{background: 'rgba(30,41,59,0.7)', border: '2px solid #9b72dc', borderRadius: 18, padding: '24px 32px', width: '100%'}}>
        <div style={{fontSize: 38, fontWeight: 700, color: '#9b72dc', marginBottom: 10}}>Modified MIT</div>
        <div style={{fontSize: 32, color: '#cbd5e1'}}>✓ Commercial use OK</div>
      </div>
      <Subtitle lines={['Model trên HuggingFace: moonshotai/Kimi-K2.7-Code', 'License: Modified MIT (commercial OK)']} />
      <FooterLabel text="HF · OPEN-WEIGHTS" color="#9b72dc" />
    </AbsoluteFill>
  );
};

const Scene6: React.FC = () => {
  const entr = useEntrance();
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="GITHUB REPO" color="#4285f4" />
      <div style={{fontSize: 50, fontWeight: 800, color: '#4285f4', marginTop: 130, marginBottom: 20}}>MoonshotAI/Kimi-K2</div>
      <div style={{fontSize: 36, color: '#cbd5e1', marginBottom: 30}}>10,800+ stars · 900+ forks</div>
      <Img src={staticFile('03_gh_title.png')} style={{width: 950, height: 'auto', borderRadius: 24, border: '4px solid rgba(66,133,244,0.5)', boxShadow: '0 20px 60px rgba(66,133,244,0.4)', marginBottom: 30}} />
      <div style={{background: 'rgba(30,41,59,0.7)', border: '2px solid #4285f4', borderRadius: 18, padding: '20px 30px', width: '100%'}}>
        <div style={{fontSize: 32, color: '#cbd5e1'}}>Part of Kimi K2 ecosystem</div>
      </div>
      <Subtitle lines={['GitHub: MoonshotAI/Kimi-K2 (10.8K stars)', 'Repository chính thức của Moonshot AI']} />
      <FooterLabel text="GITHUB · OPEN SOURCE" color="#4285f4" />
    </AbsoluteFill>
  );
};

const Scene7: React.FC = () => {
  const entr = useEntrance();
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
        <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, width: '100%', background: 'rgba(30,41,59,0.7)', border: `2px solid ${c.color}`, borderRadius: 14, padding: '24px 32px', marginBottom: 16}}>
          <div style={{fontSize: 56}}>{c.icon}</div>
          <div style={{fontSize: 42, fontWeight: 700, color: c.color}}>{c.text}</div>
        </div>
      ))}
      <Subtitle lines={['Use cases: complex SWE, long-horizon agentic', 'Multi-step coding, CI/CD integration']} />
      <FooterLabel text="AGENTIC CODING" color="#4285f4" />
    </AbsoluteFill>
  );
};

const Scene8: React.FC = () => {
  const entr = useEntrance();
  return (
    <AbsoluteFill style={{...entr, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 60}}>
      <HeaderLabel text="TAKEAWAY" color="#50c878" />
      <div style={{fontSize: 200, marginBottom: 40, marginTop: 130}}>🎯</div>
      <div style={{fontSize: 80, fontWeight: 900, color: '#50c878', textAlign: 'center', marginBottom: 30, lineHeight: 1.1}}>Lựa chọn<br/>tuyệt vời</div>
      <div style={{fontSize: 38, color: '#cbd5e1', textAlign: 'center', marginBottom: 40}}>cho AI coding agent mạnh + tiết kiệm</div>
      <div style={{background: 'rgba(20,20,30,0.8)', border: '3px solid #4285f4', borderRadius: 18, padding: '30px 40px', width: '100%'}}>
        <div style={{fontSize: 32, fontWeight: 700, color: '#4285f4', marginBottom: 12, textAlign: 'center'}}>huggingface.co/moonshotai</div>
        <div style={{fontSize: 30, fontWeight: 700, color: '#50c878', textAlign: 'center'}}>#KimiK27 #MoonshotAI #OpenSource</div>
      </div>
      <Subtitle lines={['Kimi K2.7 Code - AI coding agent mạnh + tiết kiệm', 'Follow kênh để cập nhật AI mới nhất!']} />
      <FooterLabel text="FOLLOW FOR MORE" color="#50c878" />
    </AbsoluteFill>
  );
};

const SCENES = [
  {id: 's1', start: 0, duration: __DUR_S1__, comp: Scene1},
  {id: 's2', start: __START_S2__, duration: __DUR_S2__, comp: Scene2},
  {id: 's3', start: __START_S3__, duration: __DUR_S3__, comp: Scene3},
  {id: 's4', start: __START_S4__, duration: __DUR_S4__, comp: Scene4},
  {id: 's5', start: __START_S5__, duration: __DUR_S5__, comp: Scene5},
  {id: 's6', start: __START_S6__, duration: __DUR_S6__, comp: Scene6},
  {id: 's7', start: __START_S7__, duration: __DUR_S7__, comp: Scene7},
  {id: 's8', start: __START_S8__, duration: __DUR_S8__, comp: Scene8},
];

const KimiVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#0a0e1a'}}>
      <Background />
      <Audio src={staticFile('narration.mp3')} />
      {SCENES.map((scene) => {
        const Comp = scene.comp;
        return (
          <Sequence key={scene.id} from={scene.start} durationInFrames={scene.duration}>
            <Comp />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

const RemotionRoot: React.FC = () => {
  return (
    <Composition id="KimiVideo" component={KimiVideo} durationInFrames={TOTAL_DURATION} fps={FPS} width={W} height={H} />
  );
};

registerRoot(RemotionRoot);
