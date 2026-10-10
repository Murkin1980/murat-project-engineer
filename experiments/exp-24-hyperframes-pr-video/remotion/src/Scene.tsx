import React from 'react';
import {AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Beat, manifest, storyboard} from './data';

const FONT = 'Arial, Helvetica, sans-serif';
// Caption: 56px at 1280 width => ~15.8px effective at a 360px player (see mobile QA).
const CAPTION_FONT_PX = 56;

// Derived presentation timing: beat start = cumulative sum of preceding durations.
const starts = (() => {
	let acc = 0;
	return storyboard.beats.map((b) => {
		const s = acc;
		acc += b.duration_s;
		return s;
	});
})();

export const sceneDurationInFrames = () => {
	const total = storyboard.beats.reduce((a, b) => a + b.duration_s, 0);
	return Math.round(total * storyboard.presentation.fps);
};

const assetFor = (beat: Beat): string => {
	const entry = manifest.entries.find((e) => e.beat_id === beat.beat_id && e.asset_slot === beat.asset_slot);
	if (!entry) {
		throw new Error(`No manifest entry for ${beat.beat_id}/${beat.asset_slot}`);
	}
	return entry.asset_path;
};

const BeatView: React.FC<{beat: Beat}> = ({beat}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const fade = storyboard.presentation.transition.duration_s;
	const opacity = interpolate(t, [0, fade], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

	const capIn = beat.cues.find((c) => c.kind === 'caption_in');
	const capOut = beat.cues.find((c) => c.kind === 'caption_out');
	const showCaption =
		beat.caption !== null && capIn !== undefined && capOut !== undefined && t >= capIn.at_s && t < capOut.at_s;
	const capOpacity = interpolate(t, [0, fade], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

	return (
		<AbsoluteFill style={{opacity, backgroundColor: '#111'}}>
			<Img
				src={staticFile(assetFor(beat))}
				style={{width: '100%', height: '100%', objectFit: 'cover'}}
			/>
			{showCaption ? (
				<div
					style={{
						position: 'absolute',
						left: 60,
						right: 60,
						bottom: 56,
						padding: '18px 28px',
						background: 'rgba(0,0,0,0.62)',
						borderRadius: 10,
						color: '#ffffff',
						fontFamily: FONT,
						fontWeight: 700,
						fontSize: CAPTION_FONT_PX,
						lineHeight: 1.2,
						textAlign: 'center',
						opacity: capOpacity,
					}}
				>
					{beat.caption}
				</div>
			) : null}
		</AbsoluteFill>
	);
};

export const Scene: React.FC = () => {
	const fps = storyboard.presentation.fps;
	return (
		<AbsoluteFill style={{backgroundColor: '#000'}}>
			{storyboard.beats.map((beat, i) => (
				<Sequence
					key={beat.beat_id}
					from={Math.round(starts[i] * fps)}
					durationInFrames={Math.round(beat.duration_s * fps)}
					name={beat.beat_id}
				>
					<BeatView beat={beat} />
				</Sequence>
			))}
		</AbsoluteFill>
	);
};
