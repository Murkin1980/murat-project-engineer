// Frozen contracts consumed directly by the composition (no copy, no new schema).
import storyboardJson from '../../cp13/EDITORIAL_STORYBOARD.json';
import manifestJson from '../../cp13/MEDIA_MANIFEST.json';

export type Cue = {cue_id: string; kind: 'caption_in' | 'caption_out'; at_s: number};
export type Beat = {
	beat_id: string;
	order: number;
	caption: string | null;
	duration_s: number;
	asset_slot: string;
	cues: Cue[];
};
export type Storyboard = {
	presentation: {fps: number; width: number; height: number; transition: {duration_s: number}};
	beats: Beat[];
};
export type ManifestEntry = {beat_id: string; asset_slot: string; asset_path: string; approval_state: string};
export type Manifest = {entries: ManifestEntry[]};

export const storyboard = storyboardJson as unknown as Storyboard;
export const manifest = manifestJson as unknown as Manifest;
