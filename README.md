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

**Make**

- Grids from 20 to 5000 squares along the long side, in square, portrait, story, wide, panorama and banner formats
- Palettes sampled from the original studies, plus custom hues
- Movement: flow, morph, drift, breathe, ripple, swirl, wave and shimmer, in any combination
- Music: load a song and the work pulses, sends rings out on the beat, surges and sparkles with it
- Touch and mouse play: ripple, swirl, push and ink
- Exhibition mode: full screen, controls hidden, the screen kept awake
- Growth: the study builds itself square by square, from the core, scattered or row by row, once or on a loop
- Space: load a LiDAR scan of a room or a place and rebuild it in pixel cubes, covering its surfaces or filling its air, then walk around it in AR

**Interact**
- Camera: visitors' movement darkens, lightens, pushes or ripples the field
- Listen to the room: the microphone hears voices, clapping or a live band
- Live performance: MIDI knobs (map any slider), keys and pads fire rings, keyboard shortcuts, and an output window for a projector or second screen

Camera and microphone are processed on the device. Nothing is recorded, saved or sent.

**Show and save**
- Saves PNGs and MP4 videos (slow motion to time-lapse, up to 4K, with the song's sound), and USDZ files for AR from Space
- Print: A4 to A1 and square or poster sizes in cm, border, signature line, 150 or 300 dpi PNG, plus PDF and SVG vector files with one layer per tone
- TV: a TV link, 4K screensaver images and seamless TV loop videos

## On a TV or as a screensaver

- **Any smart TV with a browser:** open https://serski.github.io/pixel-machine/?tv. It starts full screen and changes by itself. On the remote, OK makes a new study, left and right change the palette, up and down change the speed.
- **Google TV and Chromecast:** in the app, save the 4K screensaver images, add them to a Google Photos album, then pick that album in Ambient mode.
- **Samsung The Frame:** send the images to Art Mode with the SmartThings app.
- **Apple TV:** add the images to a shared photo album and choose it as the screen saver.
- **Any TV with USB:** use "Set up a TV loop video", render it, copy the MP4 to a USB stick and play it on repeat.
- **Casting:** open the app in Chrome and cast the tab, or use AirPlay from a Mac, iPhone or iPad.

## Scan a place with an iPhone (Space)

Websites can't use the iPhone's LiDAR scanner directly, so the scan is made in a scanner app and loaded into Pixel Machine.

1. **Scan.** On an iPhone or iPad Pro with LiDAR, scan the room with a free app such as **Scaniverse** or **3d Scanner App**. Walk slowly and cover the floor, the walls and the ceiling.
2. **Export.** Share the scan as **GLB** (best), **OBJ** or **PLY**, and save it to Files.
3. **Load.** In Pixel Machine, open **Space**, press **Load a scan** and pick the file, or drop it on the work on a computer. **Try a sample room** shows how it works without a scan.
4. **Shape it.**
   - **Cover the surfaces** tiles the floor, walls and furniture with pixel cubes.
   - **Fill the air** fills the room with a cloud of cubes, dense and dark at the core and thinning out toward the pale edges.
   - Pixel size, spread, density and the core's position set the look. Every movement, palette, growth order and music reaction works in 3D too.
5. **Look around.** Drag to turn the space and pinch or scroll to zoom. **Inside** puts you in the room at eye height. A quick tap sends a pulse through the pixels.
6. **Save.** PNG and MP4 saving work as usual. **View in AR** (iPhone and iPad) or **Save USDZ for AR** places the pixels in the real room at true size, so you can walk through them.

The scan never leaves the device. If a scan lies on its side, switch **Up direction** to Z. Scans in centimetres or millimetres are scaled to metres automatically.

## Live performance setup

1. Open the app on your laptop and press **Open output window** in Live performance.
2. Drag the new window to the projector or second screen, click it, and press **F** for full screen.
3. Keep playing from the laptop: everything you change appears on the output.
4. To use a MIDI controller (Chrome or Edge), press **Connect**, turn on **Map knobs**, click a slider and turn a knob. Keys and pads send rings out from the core.

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
