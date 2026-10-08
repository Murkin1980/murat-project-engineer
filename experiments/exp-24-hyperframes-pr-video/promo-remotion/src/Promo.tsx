import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame } from "remotion";
import timelineJson from "./generated/timeline.json";
import { Timeline, TimelineScene } from "./types";
import { BrandClose } from "./BrandClose";
import { Scene } from "./Scene";

const timeline = timelineJson as unknown as Timeline;

export const SCENES: TimelineScene[] = timeline.scenes;

export const SalamatPromo: React.FC<{ showCaptions?: boolean; showAudio?: boolean }> = ({
  showCaptions = true,
  showAudio = true,
}) => {
  const frame = useCurrentFrame();
  const fadeIn = Math.min(frame / 20, 1);
  const fadeOut = Math.min((timeline.totalFrames - frame) / 20, 1);
  return (
    <AbsoluteFill style={{ backgroundColor: "#0F0E0C", opacity: Math.min(fadeIn, fadeOut) }}>
      {timeline.scenes.map((scene) => (
        <Sequence
          key={scene.id}
          from={scene.startFrame}
          durationInFrames={scene.durationFrames}
          name={`${scene.order}. ${scene.id}`}
        >
          {scene.brand ? <BrandClose scene={scene} /> : <Scene scene={scene} showCaptions={showCaptions} />}
        </Sequence>
      ))}
      {showAudio && timeline.audioMix ? (
        <Audio src={staticFile(timeline.audioMix)} volume={1} />
      ) : null}
    </AbsoluteFill>
  );
};
