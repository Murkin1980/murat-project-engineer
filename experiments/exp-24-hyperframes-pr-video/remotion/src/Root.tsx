import React from 'react';
import {Composition} from 'remotion';
import {Scene, sceneDurationInFrames} from './Scene';
import {storyboard} from './data';

export const RemotionRoot: React.FC = () => {
	const fps = storyboard.presentation.fps;
	return (
		<Composition
			id="E01S005"
			component={Scene}
			durationInFrames={sceneDurationInFrames()}
			fps={fps}
			width={storyboard.presentation.width}
			height={storyboard.presentation.height}
		/>
	);
};
