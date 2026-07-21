import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "NhutCoder Team";
export const size = { width: 180, height: 180 };
export const contentType = "image/png";

export default function AppleIcon() {
  return new ImageResponse(
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#06080d",
        borderRadius: 40,
        position: "relative",
      }}
    >
      <svg width="100" height="100" viewBox="0 0 32 32" fill="none">
        <path
          d="M8 22V10l12 12V10"
          stroke="url(#aig)"
          strokeWidth="2.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx="24.5" cy="9" r="1.8" fill="#b9f7a4" />
        <defs>
          <linearGradient
            id="aig"
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
    </div>,
    { ...size }
  );
}
