# Watch Video (PWA launcher)

A one-purpose installable web app: tapping its home-screen icon opens a specific
YouTube video directly in the YouTube app on Android (not the browser).

## Files
- `index.html` — redirects to the video via an Android `intent://` URL, which
  hands off straight to the YouTube app (falls back to the web URL if the app
  isn't installed).
- `manifest.json` — makes the page installable ("Add to Home Screen").
- `icon-192.png` / `icon-512.png` — app icon.

## Change the video
Edit the two constants near the top of the `<script>` in `index.html`:

```js
var VIDEO_ID = "2LMqOdCHQWw";
var START_SECONDS = 9;
```

## Host it (needs HTTPS for install to work)
Easiest free option — GitHub Pages:

```bash
cd youtube-launcher-pwa
git init
git add .
git commit -m "youtube launcher pwa"
gh repo create youtube-launcher-pwa --public --source=. --push
gh api repos/:owner/youtube-launcher-pwa/pages -X POST -f "source[branch]=main" -f "source[path]=/"
```

Or just drag the folder onto https://app.netlify.com/drop for an instant HTTPS URL.

## Install on your phone
1. Open the hosted URL in Chrome on Android.
2. Tap the ⋮ menu → **Add to Home screen** (Chrome may show an **Install** prompt instead).
3. Launch it from the home screen icon — it goes straight into the YouTube app.
