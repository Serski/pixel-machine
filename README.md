# Pixel Machine

**By Argiris Ser**

Pixel Machine is an interactive generative work that grows stepped fields of square pixels,
from light edges to a dark core, from a 20 × 20 study up to 5000 × 5000 squares.
The fields can stay still, flow and breathe, react to music and to touch, or run full screen
as an installation.

**Open it:** https://serski.github.io/pixel-machine/

## Install it as an app

Open the link above, then:

- **Computer (Chrome or Edge):** click **Install Pixel Machine** in the panel, or the install icon in the address bar.
- **Mac (Safari):** File menu, then **Add to Dock**.
- **iPhone or iPad (Safari):** tap **Share**, then **Add to Home Screen**.
- **Android (Chrome):** tap **Install Pixel Machine**, or the browser menu, then **Install app**.

Once installed it opens in its own window and works offline.

## What it does

- Grids from 20 to 5000 squares along the long side, in square, portrait, story, wide, panorama and banner formats
- Palettes sampled from the original studies, plus custom hues
- Movement: flow, morph, drift, breathe, ripple, swirl, wave and shimmer, in any combination
- Music: load a song and the work pulses, sends rings out on the beat, surges and sparkles with it
- Touch and mouse play: ripple, swirl, push and ink
- Exhibition mode: full screen, controls hidden, the screen kept awake
- Saves PNGs and MP4 videos (slow motion to time-lapse, up to 4K, with the song's sound)

## Updating the app

`source/pixel-machine.html` is the editable app. After changing it, rebuild and commit:

```bash
python3 tools/build.py
```

The build writes `index.html` and `sw.js`. GitHub Pages publishes them a minute after each push,
and installed copies update the next time they are opened online.

## Files

- `index.html`, `manifest.webmanifest`, `sw.js`, `icons/`: the published app
- `source/pixel-machine.html`: the editable source
- `tools/build.py`: builds the app from the source
- `tools/vendor/`: bundled fonts and the MP4 encoder ([licenses](tools/vendor/LICENSES.md))

© 2026 Argiris Ser. All rights reserved. Bundled fonts and libraries keep their own licenses.
