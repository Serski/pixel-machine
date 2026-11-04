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

# "Get the app" button at the end of the title block.
brand = re.search(r'<header class="brand">.*?</header>', body, re.S)
if not brand:
    raise SystemExit("build: title block not found in the source")
brand_html = brand.group(0).replace("</header>", """  <button type="button" class="btn primary wide install-btn" id="install-app" hidden>
        <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 8.5v7M8.5 12h7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
        <span id="install-label">Install Pixel Machine</span>
      </button>
    </header>""")
body = body[:brand.start()] + brand_html + body[brand.end():]

install_css = """
.install-btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; margin-top: 12px; }
.install-btn svg { width: 18px; height: 18px; flex: none; }
#install-help { border: 1px solid var(--line); background: var(--bg); color: var(--ink); padding: 20px; width: calc(100% - 32px); max-width: 420px; border-radius: 6px; box-shadow: var(--shadow); font-family: var(--f-body); }
#install-help::backdrop { background: rgba(8, 10, 12, .5); }
#install-help h2 { margin: 0 0 14px; font: 800 19px/1.2 var(--f-display); letter-spacing: .01em; }
#install-help ol { margin: 0; padding-left: 22px; display: grid; gap: 12px; }
#install-help li { line-height: 1.5; padding-left: 2px; }
#install-help .ico { display: inline-grid; place-items: center; width: 28px; height: 28px; margin: -4px 2px; border: 1px solid var(--line); border-radius: 7px; background: var(--chip); color: var(--accent); vertical-align: middle; }
#install-help .ico svg { width: 17px; height: 17px; }
#install-help .install-link { display: block; margin-top: 6px; padding: 8px 10px; border: 1px solid var(--line); background: var(--chip); font: 13px/1.3 var(--f-mono); word-break: break-all; user-select: all; -webkit-user-select: all; }
#install-help .note { margin-top: 14px; }
#install-help .install-actions { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; margin-top: 18px; }
@media (max-width: 560px) {
  #install-help { margin: auto 0 0; width: 100%; max-width: none; border-radius: 14px 14px 0 0; border-width: 1px 0 0; padding-bottom: calc(20px + env(safe-area-inset-bottom, 0px)); }
  #install-help .install-actions .btn { flex: 1; }
}
"""

install_js = """<dialog id="install-help" aria-labelledby="install-title">
  <h2 id="install-title">Add Pixel Machine to your Home Screen</h2>
  <ol id="install-steps"></ol>
  <p class="note" id="install-after">It opens full screen, like an app, and works offline.</p>
  <div class="install-actions">
    <button type="button" class="btn" id="install-copy" hidden>Copy the link</button>
    <button type="button" class="btn primary" id="install-close">Got it</button>
  </div>
</dialog>
<script>
// Installable app: offline support, and a "get the app" button that installs where the browser
// allows it and shows the steps where it doesn't (iPhone, iPad, Safari on Mac, in-app browsers).
(() => {
  if ("serviceWorker" in navigator && location.protocol !== "file:") {
    window.addEventListener("load", () => { navigator.serviceWorker.register("sw.js").catch(() => {}); });
  }
  const ua = navigator.userAgent;
  const installed = matchMedia("(display-mode: standalone)").matches || matchMedia("(display-mode: fullscreen)").matches || navigator.standalone === true;
  const isIOS = /iphone|ipad|ipod/i.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  const isAndroid = /android/i.test(ua);
  const inApp = /Instagram|FBAN|FBAV|FB_IAB|FBIOS|Messenger|TikTok|musical_ly|Bytedance|Snapchat|LinkedInApp|Pinterest|Threads|Line\\//i.test(ua);
  const safariVer = +((/Version\\/(\\d+)/.exec(ua) || [])[1] || 0);
  const macSafari = !isIOS && /Macintosh/.test(ua) && /Safari\\//.test(ua) && !/Chrome|Chromium|CriOS|Edg|Firefox|OPR/.test(ua) && safariVer >= 17;
  const btn = document.getElementById("install-app"), label = document.getElementById("install-label");
  const dlg = document.getElementById("install-help"), steps = document.getElementById("install-steps");
  const copyBtn = document.getElementById("install-copy");
  const link = location.origin + location.pathname;
  const SVG = {
    share: '<path d="M12 14.5V3.8M8 7.6l4-3.8 4 3.8M8.7 10.4H7.2a1.7 1.7 0 0 0-1.7 1.7v6.7a1.7 1.7 0 0 0 1.7 1.7h9.6a1.7 1.7 0 0 0 1.7-1.7v-6.7a1.7 1.7 0 0 0-1.7-1.7h-1.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    add: '<rect x="4" y="4" width="16" height="16" rx="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 8.5v7M8.5 12h7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    more: '<circle cx="6" cy="12" r="1.7" fill="currentColor"/><circle cx="12" cy="12" r="1.7" fill="currentColor"/><circle cx="18" cy="12" r="1.7" fill="currentColor"/>',
    menu: '<circle cx="12" cy="6" r="1.7" fill="currentColor"/><circle cx="12" cy="12" r="1.7" fill="currentColor"/><circle cx="12" cy="18" r="1.7" fill="currentColor"/>',
  };
  const ico = k => '<span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">' + SVG[k] + "</svg></span>";
  const linkBox = '<span class="install-link">' + link + "</span>";
  function plan() {
    if (inApp && (isIOS || isAndroid)) {
      const br = isIOS ? "Safari" : "Chrome";
      return { title: "Open Pixel Machine in " + br + " first", copy: true, steps: [
        "This page is open inside another app, which can't add it to your Home Screen. Tap " + ico(isIOS ? "more" : "menu") + " at the top right and choose to open it in " + (isIOS ? "your browser" : "Chrome") + ". Or copy the link and paste it into " + br + ":" + linkBox,
        isIOS ? "In Safari, tap Share " + ico("share") + ", then <b>Add to Home Screen</b> " + ico("add") + "." : "In Chrome, tap " + ico("menu") + ", then <b>Install app</b> or <b>Add to Home screen</b>.",
      ] };
    }
    if (isIOS) {
      const first = /CriOS/.test(ua) ? "Tap the Share button " + ico("share") + " in the address bar. If it isn't there, tap " + ico("more") + " and then <b>Share</b>."
        : /EdgiOS|FxiOS|OPiOS/.test(ua) ? "Open the browser menu and tap <b>Share</b> " + ico("share") + ". If you can't find it, open this page in Safari."
        : "Tap the Share button " + ico("share") + " in Safari's toolbar. If you don't see it, tap " + ico("more") + " first.";
      return { title: "Add Pixel Machine to your Home Screen", steps: [
        first,
        "Tap <b>Add to Home Screen</b> " + ico("add") + ". You may need to scroll down to find it.",
        "If you see <b>Open as Web App</b>, leave it on. Then tap <b>Add</b>.",
      ] };
    }
    if (macSafari) return { title: "Add Pixel Machine to your Dock", after: "It opens in its own window, like an app, and works offline.", steps: [
      "In Safari's menu bar, choose <b>File</b>, then <b>Add to Dock</b>.",
      "Click <b>Add</b>.",
    ] };
    return { title: "Add Pixel Machine to your Home screen", steps: [
      "Open the browser menu " + ico("menu") + ".",
      "Tap <b>Install app</b> or <b>Add to Home screen</b>.",
      "Tap <b>Install</b>.",
    ] };
  }
  function showHelp() {
    const pl = plan();
    document.getElementById("install-title").textContent = pl.title;
    steps.innerHTML = pl.steps.map(t => "<li>" + t + "</li>").join("");
    document.getElementById("install-after").textContent = pl.after || "It opens full screen, like an app, and works offline.";
    copyBtn.hidden = !pl.copy;
    copyBtn.textContent = "Copy the link";
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
  }
  const close = () => { if (dlg.close) dlg.close(); else dlg.removeAttribute("open"); };
  document.getElementById("install-close").addEventListener("click", close);
  dlg.addEventListener("click", e => { if (e.target === dlg) close(); });
  copyBtn.addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(link); copyBtn.textContent = "Link copied"; }
    catch (e) { window.prompt("Copy this link:", link); }
  });
  let deferred = null, mode = null;
  const show = (m, text) => { mode = m; label.textContent = text; btn.hidden = false; };
  window.addEventListener("beforeinstallprompt", e => { e.preventDefault(); deferred = e; show("prompt", "Install Pixel Machine"); });
  btn.addEventListener("click", async () => {
    if (mode === "prompt" && deferred) {
      const ev = deferred;
      deferred = null;
      ev.prompt();
      try { const c = await ev.userChoice; if (c && c.outcome === "accepted") btn.hidden = true; } catch (e) { /* ignore */ }
      if (!btn.hidden && isAndroid) show("help", "Add to Home screen"); else if (!btn.hidden) btn.hidden = true;
      return;
    }
    showHelp();
  });
  window.addEventListener("appinstalled", () => { btn.hidden = true; });
  if (!installed && location.protocol !== "file:") {
    if (isIOS || (inApp && isAndroid)) show("help", "Add to Home Screen");
    else if (macSafari) show("help", "Add to Dock");
    else if (isAndroid) setTimeout(() => { if (!mode) show("help", "Add to Home screen"); }, 3500);
  }
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
{install_css}
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
