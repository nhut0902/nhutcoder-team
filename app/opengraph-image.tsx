import { ImageResponse } from "next/og";
import { SITE } from "@/lib/data";

export const runtime = "edge";
export const alt = `${SITE.name} — ${SITE.tagline}`;
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    <div
      style={{
        height: "100%",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        backgroundColor: "#06080d",
        backgroundImage:
          "radial-gradient(circle at 85% 15%, rgba(132,212,75,0.22), transparent 55%), radial-gradient(circle at 10% 90%, rgba(176,116,255,0.20), transparent 55%)",
        padding: "72px",
        fontFamily: "sans-serif",
        color: "white",
      }}
    >
      {/* Top row: brand + tag */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 20,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: 64,
            height: 64,
            borderRadius: 16,
            border: "1px solid rgba(255,255,255,0.16)",
            backgroundColor: "rgba(255,255,255,0.04)",
          }}
        >
          <svg width="34" height="34" viewBox="0 0 32 32" fill="none">
            <path
              d="M8 22V10l12 12V10"
              stroke="url(#og)"
              strokeWidth="2.6"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <circle cx="24.5" cy="9" r="1.8" fill="#b9f7a4" />
            <defs>
              <linearGradient
                id="og"
                x1="8"
                y1="10"
                x2="24"
                y2="22"
                gradientUnits="userSpaceOnUse"
              >
                <stop stopColor="#b9f7a4" />
                <stop offset="1" stopColor="#b074ff" />
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <div
            style={{
              display: "flex",
              fontSize: 26,
              fontWeight: 600,
              letterSpacing: -0.5,
            }}
          >
            <span>NhutCoder </span>
            <span style={{ color: "#b9f7a4" }}>/</span>
            <span> team</span>
          </div>
          <div
            style={{
              display: "flex",
              fontSize: 16,
              color: "rgba(255,255,255,0.5)",
              marginTop: 4,
            }}
          >
            open source · ai · web · games
          </div>
        </div>
      </div>

      {/* Center: tagline */}
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div
          style={{
            display: "flex",
            fontSize: 84,
            fontWeight: 700,
            lineHeight: 1.02,
            letterSpacing: -3,
          }}
        >
          Building the future with{" "}
          <span
            style={{
              backgroundImage:
                "linear-gradient(100deg, #b9f7a4, #b074ff 70%, #84d44b)",
              backgroundClip: "text",
              color: "transparent",
            }}
          >
            {" "}
            code &amp; AI
          </span>
          .
        </div>
        <div
          style={{
            display: "flex",
            fontSize: 24,
            color: "rgba(255,255,255,0.55)",
            marginTop: 24,
          }}
        >
          Open-source tools · AI products · Games · Web · {SITE.location}
        </div>
      </div>

      {/* Bottom row: meta */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 18,
          color: "rgba(255,255,255,0.55)",
        }}
      >
        <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
          <span>github.com/nhut0902</span>
          <span style={{ opacity: 0.4 }}>·</span>
          <span>Ho Chi Minh City, VN</span>
        </div>
        <div
          style={{
            display: "flex",
            gap: 8,
            alignItems: "center",
            padding: "6px 14px",
            border: "1px solid rgba(185, 247, 164, 0.3)",
            borderRadius: 999,
            backgroundColor: "rgba(185, 247, 164, 0.08)",
            color: "#b9f7a4",
            fontSize: 15,
          }}
        >
          <span
            style={{
              display: "flex",
              width: 8,
              height: 8,
              borderRadius: 999,
              backgroundColor: "#84d44b",
            }}
          />
          open for collaborations
        </div>
      </div>
    </div>,
    { ...size }
  );
}
