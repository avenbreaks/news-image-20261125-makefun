// News-image entry for Wednesday 25 November 2026 (Node 22, stdlib only).
// The entry image is the entry.png beside this file; the program copies
// it to /output/entry.png. The image itself is drawn by build_image.py
// in this repository (a Pillow front page of the day's world news, drawn
// from the headlines as reported on 25 November 2026).
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
