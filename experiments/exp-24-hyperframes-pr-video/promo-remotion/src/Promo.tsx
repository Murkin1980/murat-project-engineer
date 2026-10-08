import React from "react";
import {
  AbsoluteFill,
  Audio,
  Composition,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import timelineJson from "./generated/timeline.json";

/**
 * EXP-24 Phase 2 — Salamat Mebel promo. One composition file, Remotion primitives only.
 * Mobile-first sizes (effective 360 px review => px * 0.1875): caption 112, title 144, label 88.
 */

const FONT = '"Manrope", "Noto Sans", "DejaVu Sans", system-ui, sans-serif';
const INK = "#0F0E0C";
const PAPER = "#F4EFE6";
const BRASS = "#C8A15A";
const SAFE_X = 120;
const SAFE_TOP = 96;
const TYPE = { brand: 176, title: 144, subtitle: 84, caption: 112, label: 88 } as const;

type Shot = {
  id: string;
  order: number;
  scriptScene: number;
  scriptTimecode: string;
  startFrame: number;
  durationFrames: number;
  narrationPart: string | null;
  captionLines: string[];
  title: string | null;
  subtitle: string | null;
  label: string | null;
  motion: "push-in" | "push-out" | "drift-left" | "drift-right" | "hold";
  ownerDirected: boolean;
  asset: { file: string | null; query: string; status: string; provider: string } | null;
};

type Timeline = {
  fps: number;
  width: number;
  height: number;
  totalFrames: number;
  totalSeconds: number;
  audioMix: string | null;
  scenes: Shot[];
};

const timeline = timelineJson as unknown as Timeline;

const captionStyle: React.CSSProperties = {
  fontFamily: FONT, fontSize: TYPE.caption, fontWeight: 600, lineHeight: 1.18, color: "#FFFFFF",
  textAlign: "center", maxWidth: 1560, padding: "6px 18px", borderRadius: 10,
  background: "rgba(15,14,12,0.34)", textShadow: "0 2px 14px rgba(0,0,0,0.55)",
};

const grade = (
  <>
    <AbsoluteFill
      style={{
        background:
          "linear-gradient(180deg, rgba(15,14,12,0.42) 0%, rgba(15,14,12,0.06) 26%, rgba(15,14,12,0.16) 62%, rgba(15,14,12,0.72) 100%)",
      }}
    />
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(120% 80% at 50% 45%, rgba(200,161,90,0.10) 0%, rgba(0,0,0,0) 60%)",
        mixBlendMode: "soft-light",
      }}
    />
  </>
);

/** Restrained Ken-Burns motion; direction comes from the manifest, not from taste. */
const useMotion = (shot: Shot, frames: number) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [0, Math.max(frames - 1, 1)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  switch (shot.motion) {
    case "push-out":
      return { scale: 1.095 - 0.075 * t, x: 0 };
    case "drift-left":
      return { scale: 1.08, x: -28 * t };
    case "drift-right":
      return { scale: 1.08, x: 28 * t };
    case "hold":
      return { scale: 1.03, x: 0 };
    default:
      return { scale: 1.02 + 0.075 * t, x: 0 };
  }
};

/**
 * Placeholder while licensed footage is unresolved. It is a text search slate, not
 * media: no imagery, clearly marked unlicensed so no preview can be mistaken for a film.
 */
const SearchSlate: React.FC<{ shot: Shot }> = ({ shot }) => (
  <AbsoluteFill
    style={{
      background:
        "repeating-linear-gradient(135deg, #17150F 0px, #17150F 26px, #1D1A13 26px, #1D1A13 52px)",
      justifyContent: "center",
      alignItems: "center",
      paddingLeft: SAFE_X,
      paddingRight: SAFE_X,
    }}
  >
    <div style={{ fontFamily: FONT, textAlign: "center", maxWidth: 1500 }}>
      <div style={{ fontSize: 72, fontWeight: 700, color: BRASS, letterSpacing: 2 }}>
        STORYBLOCKS · UNLICENSED · PREVIEW ONLY
      </div>
      <div style={{ fontSize: 64, fontWeight: 600, color: PAPER, marginTop: 26 }}>
        {shot.query}
      </div>
      <div style={{ fontSize: 48, fontWeight: 400, color: "rgba(244,239,230,0.62)", marginTop: 18 }}>
        {`scene ${shot.order} · script ${shot.scriptTimecode} · target ${Math.round(
          shot.durationFrames / 30,
        )}s`}
      </div>
    </div>
  </AbsoluteFill>
);

const Footage: React.FC<{ shot: Shot }> = ({ shot }) => {
  const { durationInFrames } = useVideoConfig();
  const { scale, x } = useMotion(shot, durationInFrames);
  if (!shot.asset?.file) {
    return <SearchSlate shot={shot} />;
  }
  return (
    <AbsoluteFill style={{ backgroundColor: INK, overflow: "hidden" }}>
      <Img
        src={staticFile(shot.asset.file)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `translateX(${x}px) scale(${scale})`,
        }}
      />
    </AbsoluteFill>
  );
};

/**
 * Overlay text. Scene 1 (script scene 1) shows the allowlisted wordmark reveal low in frame;
 * every other beat shows its approved on-screen line at the top. No other copy exists.
 */
const Overlay: React.FC<{ shot: Shot }> = ({ shot }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opening = shot.scriptScene === 1;
  if (opening ? !shot.title : !shot.subtitle && !shot.title) return null;
  const delay = Math.round((opening ? 3.6 : 0.8) * fps);
  const opacity = interpolate(frame, [delay, delay + 16], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  if (opening) {
    return (
      <div
        style={{
          position: "absolute", left: SAFE_X, bottom: 210, opacity, fontFamily: FONT,
          fontSize: TYPE.brand, fontWeight: 800, letterSpacing: 4, color: PAPER,
          textShadow: "0 4px 30px rgba(0,0,0,0.5)",
        }}
      >
        {shot.title}
      </div>
    );
  }
  return (
    <div
      style={{
        position: "absolute", left: SAFE_X, right: SAFE_X, top: SAFE_TOP + 150, opacity,
        fontFamily: FONT,
      }}
    >
      {shot.subtitle ? (
        <div
          style={{
            fontSize: TYPE.title, fontWeight: 800, lineHeight: 1.06, color: PAPER,
            textShadow: "0 4px 28px rgba(0,0,0,0.45)", maxWidth: 1420,
          }}
        >
          {shot.subtitle}
        </div>
      ) : null}
    </div>
  );
};

const Captions: React.FC<{ lines: string[] }> = ({ lines }) => {
  if (!lines.length) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: SAFE_X,
        right: SAFE_X,
        bottom: 72,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 6,
      }}
    >
      {lines.map((line) => (
        <div key={line} style={captionStyle}>
          {line}
        </div>
      ))}
    </div>
  );
};

const ShotView: React.FC<{ shot: Shot; captions: boolean }> = ({ shot, captions }) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();
  const fade = Math.round(0.45 * fps);
  const opacity = interpolate(
    frame,
    [0, fade, Math.max(durationInFrames - fade, fade + 1), durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  return (
    <AbsoluteFill style={{ opacity }}>
      <Footage shot={shot} />
      {shot.asset?.file ? grade : null}
      <Overlay shot={shot} />
      {captions ? <Captions lines={shot.captionLines} /> : null}
    </AbsoluteFill>
  );
};

/** Allowlisted branded graphic 2/2: closing end card with the neutral CTA (script scene 9). */
const EndCard: React.FC<{ shot: Shot; captions: boolean }> = ({ shot, captions }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const rule = interpolate(frame, [10, 34], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const cta = interpolate(frame, [Math.round(1.1 * fps), Math.round(1.1 * fps) + 16], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill
      style={{
        backgroundColor: INK,
        opacity: interpolate(
          frame,
          [Math.max(durationInFrames - 20, 0), durationInFrames - 1],
          [1, 0.86],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        ),
        justifyContent: "center",
        alignItems: "center",
        paddingLeft: SAFE_X,
        paddingRight: SAFE_X,
      }}
    >
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(90% 60% at 22% 18%, rgba(200,161,90,0.20) 0%, rgba(0,0,0,0) 58%), " +
            "linear-gradient(160deg, #12100E 0%, #1B1714 55%, #0C0B0A 100%)",
        }}
      />
      <div
        style={{
          fontFamily: FONT,
          fontSize: TYPE.brand,
          fontWeight: 800,
          letterSpacing: 6,
          color: PAPER,
          textAlign: "center",
        }}
      >
        {shot.title}
      </div>
      <div style={{ marginTop: 34, width: 460 * rule, height: 4, background: BRASS }} />
      <div
        style={{
          marginTop: 40,
          fontFamily: FONT,
          fontSize: TYPE.subtitle,
          fontWeight: 500,
          color: "rgba(244,239,230,0.94)",
          opacity: cta,
          textAlign: "center",
        }}
      >
        {shot.subtitle}
      </div>
      {captions ? <Captions lines={shot.captionLines} /> : null}
    </AbsoluteFill>
  );
};

export const Promo: React.FC<{ captions?: boolean }> = ({ captions = true }) => {
  const frame = useCurrentFrame();
  const fade = Math.min(frame / 20, (timeline.totalFrames - frame) / 20, 1);
  return (
    <AbsoluteFill style={{ backgroundColor: INK, opacity: fade }}>
      {timeline.scenes.map((shot) => {
        const isEnd = shot.scriptScene === 9;
        return (
          <AbsoluteFill
            key={shot.id}
            style={{
              visibility:
                frame >= shot.startFrame && frame < shot.startFrame + shot.durationFrames
                  ? "visible"
                  : "hidden",
            }}
          >
            {isEnd ? (
              <EndCard shot={shot} captions={captions} />
            ) : (
              <ShotView shot={shot} captions={captions} />
            )}
          </AbsoluteFill>
        );
      })}
      {timeline.audioMix ? <Audio src={staticFile(timeline.audioMix)} volume={1} /> : null}
    </AbsoluteFill>
  );
};

export const Root: React.FC = () => (
  <>
    <Composition
      id="SalamatPromo"
      component={Promo}
      durationInFrames={timeline.totalFrames}
      fps={timeline.fps}
      width={timeline.width}
      height={timeline.height}
      defaultProps={{ captions: true }}
    />
    <Composition
      id="SalamatPromoNoCaptions"
      component={Promo}
      durationInFrames={timeline.totalFrames}
      fps={timeline.fps}
      width={timeline.width}
      height={timeline.height}
      defaultProps={{ captions: false }}
    />
  </>
);
