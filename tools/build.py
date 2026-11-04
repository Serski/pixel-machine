#!/usr/bin/env python3
"""Build the installable app.

Reads source/pixel-machine.html (the editable app) and writes index.html and sw.js
at the top of the repository, with the fonts and the MP4 encoder built in so the
app works offline. Run from anywhere:  python3 tools/build.py
"""
import base64
import hashlib
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
VENDOR = ROOT / "tools" / "vendor"

src = (ROOT / "source" / "pixel-machine.html").read_text()

# Fonts: inline each bundled woff2 file.
def inline_font(match):
    data = (VENDOR / match.group(1)).read_bytes()
    return "url(data:font/woff2;base64," + base64.b64encode(data).decode() + ")"
font_css = re.sub(r"url\((fonts/[^)]+\.woff2)\)", inline_font, (VENDOR / "fonts.css").read_text())
muxer = (VENDOR / "mp4-muxer.min.js").read_text()

# The source page is written for claude.ai, which adds its own <head>. Lift the title and drop the
# lines that load fonts and the encoder from the web, since both are built in here.
title = re.search(r"<title>.*?</title>", src).group(0)
body = src
for pattern in [
    r"<title>.*?</title>\n",
    r'<meta name="claude:viewport-fit-sides"[^>]*>\n',
    r'<link rel="preconnect"[^>]*>\n',
    r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n',
    r'<script async id="muxer-js"[^>]*></script>\n',
]:
    body, n = re.subn(pattern, "", body)
    if not n:
        raise SystemExit(f"build: expected to find {pattern!r} in the source")

# Install button and iPhone tip under the byline.
byline = '<p class="byline">By Argiris Ser</p>'
if body.count(byline) != 1:
    raise SystemExit("build: byline not found in the source")
body = body.replace(byline, byline + """
      <button type="button" class="btn wide" id="install-app" hidden>Install Pixel Machine</button>
      <p class="note" id="install-ios" hidden>To install on iPhone or iPad: tap Share, then Add to Home Screen.</p>""")

install_js = """<script>
// Installable app: offline support and the Install button.
(() => {
  if ("serviceWorker" in navigator && location.protocol !== "file:") {
    window.addEventListener("load", () => { navigator.serviceWorker.register("sw.js").catch(() => {}); });
  }
  const installed = matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
  const btn = document.getElementById("install-app"), ios = document.getElementById("install-ios");
  let deferred = null;
  window.addEventListener("beforeinstallprompt", e => { e.preventDefault(); deferred = e; btn.hidden = false; });
  btn.addEventListener("click", async () => {
    if (!deferred) return;
    deferred.prompt();
    try { await deferred.userChoice; } catch (e) { /* ignore */ }
    deferred = null;
    btn.hidden = true;
  });
  window.addEventListener("appinstalled", () => { btn.hidden = true; });
  const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  if (isIOS && !installed && location.protocol !== "file:") ios.hidden = false;
})();
</script>"""

index = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title}
<meta name="author" content="Argiris Ser">
<meta name="description" content="Pixel Machine by Argiris Ser: stepped tone fields built from square pixels, still, moving, reacting to music, or full screen.">
<meta name="theme-color" content="#111518">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Pixel Machine">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>
:root {{ color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
body {{ margin: 0; font: 14px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
img {{ max-width: 100%; }}
{font_css}
</style>
<script>
{muxer}
</script>
</head>
<body>
{body}
{install_js}
</body>
</html>
"""
(ROOT / "index.html").write_text(index)

version = "pixel-machine-" + hashlib.sha256(index.encode()).hexdigest()[:10]
(ROOT / "sw.js").write_text((ROOT / "tools" / "sw.template.js").read_text().replace("__VERSION__", version))
print(f"Built index.html ({len(index) // 1024} KB) and sw.js ({version}).")
