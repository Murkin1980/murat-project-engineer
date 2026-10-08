export type TimelineScene = {
  id: string;
  order: number;
  block: string;
  startSeconds: number;
  durationSeconds: number;
  startFrame: number;
  durationFrames: number;
  title: string | null;
  subtitle: string | null;
  label: string | null;
  captionLines: string[];
  audio: string | null;
  motion: "push-in" | "push-out" | "drift-left" | "drift-right" | "hold";
  asset: {
    file: string | null;
    kind: "REAL_FOOTAGE" | "GENERATIVE";
    provider: string;
    providerKind: string;
    status: string;
    focalPoint: [number, number];
  } | null;
  brand: boolean;
  durationSource: string;
};

export type Timeline = {
  version: number;
  generatedAt: string;
  fps: number;
  width: number;
  height: number;
  totalSeconds: number;
  totalFrames: number;
  audioMix: string | null;
  musicGainDb: number;
  scenes: TimelineScene[];
};
