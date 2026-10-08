import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS, SAFE, TYPE } from "./typography";
import { TimelineScene } from "./types";

const fontStack =
  '"Manrope", "Noto Sans", "DejaVu Sans", system-ui, -apple-system, sans-serif';

/** Ken-Burns on the still: slow, restrained, never decorative. */
const useMotion = (scene: TimelineScene, durationInFrames: number) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [0, Math.max(durationInFrames - 1, 1)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  switch (scene.motion) {
    case "push-in":
      return { scale: 1.02 + 0.075 * t, x: 0, y: 0 };
    case "push-out":
      return { scale: 1.095 - 0.075 * t, x: 0, y: 0 };
    case "drift-left":
      return { scale: 1.08, x: -28 * t, y: 0 };
    case "drift-right":
      return { scale: 1.08, x: 28 * t, y: 0 };
    default:
      return { scale: 1.05 + 0.015 * t, x: 0, y: 0 };
  }
};

const SceneImage: React.FC<{ scene: TimelineScene }> = ({ scene }) => {
  const { durationInFrames } = useVideoConfig();
  const { scale, x, y } = useMotion(scene, durationInFrames);
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.ink, overflow: "hidden" }}>
      {scene.asset?.file ? (
        <Img
          src={staticFile(scene.asset.file)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `translate(${x}px, ${y}px) scale(${scale})`,
            transformOrigin: "50% 50%",
          }}
        />
      ) : (
        <AbsoluteFill style={{ backgroundColor: COLORS.graphite }} />
      )}
    </AbsoluteFill>
  );
};

/** Warm grade + vignette so generated and (later) licensed footage share one look. */
const Grade: React.FC<{ strong?: boolean }> = ({ strong }) => (
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
        mixBlendMode: "soft-light" as const,
      }}
    />
    {strong ? (
      <AbsoluteFill style={{ background: "rgba(15,14,12,0.55)" }} />
    ) : null}
  </>
);

const Label: React.FC<{ text: string; index: number }> = ({ text, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const appear = Math.round((0.35 + index * 0.12) * fps);
  const opacity = interpolate(frame, [appear, appear + 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const shift = interpolate(frame, [appear, appear + 14], [18, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div
      style={{
        position: "absolute",
        left: SAFE.marginX,
        top: SAFE.marginTop,
        opacity,
        transform: `translateY(${shift}px)`,
        display: "flex",
        alignItems: "center",
        gap: 22,
      }}
    >
      <div style={{ width: 46, height: 4, background: COLORS.brass }} />
      <div
        style={{
          fontFamily: fontStack,
          fontWeight: 700,
          fontSize: TYPE.label,
          letterSpacing: 1.5,
          color: COLORS.paper,
          textTransform: "uppercase",
        }}
      >
        {text}
      </div>
    </div>
  );
};

const Title: React.FC<{ scene: TimelineScene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const delay = scene.label ? Math.round(0.9 * fps) : Math.round(0.35 * fps);
  const opacity = interpolate(frame, [delay, delay + 14], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const y = interpolate(frame, [delay, delay + 18], [26, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const showSubtitle = Boolean(scene.subtitle) && frame > delay + fps;
  return (
    <div
      style={{
        position: "absolute",
        left: SAFE.marginX,
        right: SAFE.marginX,
        top: SAFE.marginTop + 150,
        opacity,
        transform: `translateY(${y}px)`,
      }}
    >
      {scene.title ? (
        <div
          style={{
            fontFamily: fontStack,
            fontWeight: 800,
            fontSize: TYPE.title,
            lineHeight: 1.06,
            color: COLORS.paper,
            letterSpacing: -1.5,
            textShadow: "0 4px 28px rgba(0,0,0,0.45)",
            maxWidth: 1320,
          }}
        >
          {scene.title}
        </div>
      ) : null}
      {scene.subtitle ? (
        <div
          style={{
            marginTop: 22,
            fontFamily: fontStack,
            fontWeight: 500,
            fontSize: TYPE.subtitle,
            color: "rgba(244,239,230,0.92)",
            opacity: showSubtitle ? 1 : 0,
            maxWidth: 1180,
          }}
        >
          {scene.subtitle}
        </div>
      ) : null}
    </div>
  );
};

const Captions: React.FC<{ lines: string[] }> = ({ lines }) => {
  if (lines.length === 0) {
    return null;
  }
  return (
    <div
      style={{
        position: "absolute",
        left: SAFE.marginX,
        right: SAFE.marginX,
        top: SAFE.captionBandTop,
        height: SAFE.captionBandBottom - SAFE.captionBandTop,
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-end",
        alignItems: "center",
        gap: 6,
      }}
    >
      {lines.map((line, index) => (
        <div
          key={`${index}-${line}`}
          style={{
            fontFamily: fontStack,
            fontWeight: 600,
            fontSize: TYPE.caption,
            lineHeight: 1.18,
            color: "#FFFFFF",
            textAlign: "center",
            maxWidth: 1560,
            padding: "6px 18px",
            borderRadius: 10,
            background: "rgba(15,14,12,0.34)",
            textShadow: "0 2px 14px rgba(0,0,0,0.55)",
          }}
        >
          {line}
        </div>
      ))}
    </div>
  );
};

export const Scene: React.FC<{ scene: TimelineScene; showCaptions: boolean }> = ({
  scene,
  showCaptions,
}) => {
  const { durationInFrames, fps } = useVideoConfig();
  const frame = useCurrentFrame();
  const fade = Math.round(0.45 * fps);
  const opacity = interpolate(
    frame,
    [0, fade, Math.max(durationInFrames - fade, fade + 1), durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  return (
    <AbsoluteFill style={{ opacity }}>
      <SceneImage scene={scene} />
      <Grade />
      {scene.label ? <Label text={scene.label} index={1} /> : null}
      <Title scene={scene} />
      {showCaptions ? <Captions lines={scene.captionLines} /> : null}
    </AbsoluteFill>
  );
};

export const activeSceneAt = (scenes: TimelineScene[], frame: number): TimelineScene | null => {
  let current: TimelineScene | null = null;
  for (const scene of scenes) {
    if (frame >= scene.startFrame && frame < scene.startFrame + scene.durationFrames) {
      current = scene;
      break;
    }
  }
  return current;
};
