import {Config} from '@remotion/cli/config';

// Chromium is supplied per run via --browser-executable (Arena sandbox has no system Chrome).
Config.setVideoImageFormat('jpeg');
