import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS, SAFE, TYPE } from "./typography";
import { TimelineScene } from "./types";

const fontStack = '"Manrope", "Noto Sans", "DejaVu Sans", system-ui, sans-serif';

/**
 * Branded final card — the generative/branded 20 % of the mix, drawn entirely in
 * Remotion from tokens (no generated imagery, no stock, no invented contact data).
 */
export const BrandClose: React.FC<{ scene: TimelineScene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const rule = interpolate(frame, [10, 10 + 24], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const wordmark = interpolate(frame, [0, 18], [0.94, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const wordmarkOpacity = interpolate(frame, [0, 16], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const ctaOpacity = interpolate(frame, [Math.round(1.1 * fps), Math.round(1.1 * fps) + 16], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(
    frame,
    [Math.max(durationInFrames - 20, 0), durationInFrames - 1],
    [1, 0.86],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.ink, opacity: fadeOut, overflow: "hidden" }}>
      {/* Material texture: layered gradients keep the card premium without any asset. */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(90% 60% at 22% 18%, rgba(200,161,90,0.20) 0%, rgba(0,0,0,0) 58%)," +
            "radial-gradient(70% 70% at 82% 88%, rgba(88,64,38,0.42) 0%, rgba(0,0,0,0) 60%)," +
            "linear-gradient(160deg, #12100E 0%, #1B1714 55%, #0C0B0A 100%)",
        }}
      />
      <AbsoluteFill
        style={{
          opacity: 0.16,
          backgroundImage:
            "repeating-linear-gradient(94deg, rgba(255,255,255,0.10) 0px, rgba(255,255,255,0.10) 1px, rgba(0,0,0,0) 1px, rgba(0,0,0,0) 5px)",
        }}
      />
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          paddingLeft: SAFE.marginX,
          paddingRight: SAFE.marginX,
        }}
      >
        <div
          style={{
            fontFamily: fontStack,
            fontWeight: 800,
            fontSize: TYPE.brand,
            letterSpacing: 6,
            color: COLORS.paper,
            opacity: wordmarkOpacity,
            transform: `scale(${wordmark})`,
          }}
        >
          SALAMAT MEBEL
        </div>
        <div
          style={{
            marginTop: 34,
            width: 460 * rule,
            height: 4,
            background: COLORS.brass,
          }}
        />
        <div
          style={{
            marginTop: 40,
            fontFamily: fontStack,
            fontWeight: 500,
            fontSize: TYPE.subtitle,
            color: "rgba(244,239,230,0.94)",
            opacity: ctaOpacity,
            textAlign: "center",
            maxWidth: 1300,
          }}
        >
          мебель, созданная под ваше пространство
        </div>
      </AbsoluteFill>
      {scene.audio ? null : null}
    </AbsoluteFill>
  );
};
