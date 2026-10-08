import React from "react";
import { Composition } from "remotion";
import timelineJson from "./generated/timeline.json";
import { SalamatPromo } from "./Promo";
import { Timeline } from "./types";

const timeline = timelineJson as unknown as Timeline;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="SalamatPromo"
        component={SalamatPromo}
        durationInFrames={timeline.totalFrames}
        fps={timeline.fps}
        width={timeline.width}
        height={timeline.height}
        defaultProps={{ showCaptions: true, showAudio: true }}
      />
      {/* Caption-free master for the revision loop and for a text-light variant. */}
      <Composition
        id="SalamatPromoNoCaptions"
        component={SalamatPromo}
        durationInFrames={timeline.totalFrames}
        fps={timeline.fps}
        width={timeline.width}
        height={timeline.height}
        defaultProps={{ showCaptions: false, showAudio: true }}
      />
    </>
  );
};
