// Entry for the make.fun news-image bounty of Wednesday 25 November
// 2026. Node 22, standard library only.
//
// The deliverable is entry.png next to this file; the script copies it
// into the output directory the grader provides. build_image.py in this
// repository draws that picture with Pillow: a newspaper front page
// built from the headlines reported on 25 November 2026.
//
// Try it outside the grader with:
//   python3 build_image.py
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const src = new URL("./entry.png", import.meta.url);
const dest = join(process.env.MAKEFUN_OUTPUT_DIR ?? "/output", "entry.png");
copyFileSync(src, dest);
