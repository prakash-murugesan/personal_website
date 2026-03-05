# Prakash Murugesan · Personal Website

Static portfolio site for Prakash Murugesan, focused on multimodal research engineering work.

## Getting started

```bash
# Serve locally
python3 -m http.server 8000
# Then open http://localhost:8000 in your browser.
```

## Deploying to GitHub Pages

1. Push the `index.html` and `styles.css` files to the `main` branch of a public repo.
2. Enable GitHub Pages on that repo (Settings → Pages → Deploy from branch → `main` / `/ (root)`).
3. Point your custom domain (e.g., prakashmurugesan.com) to GitHub Pages following [GitHub's DNS docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

The site is fully static, so no build step is required.

## Preview in Codex

If you see **"Not Found"** for a previously shared preview image, that usually means the old `browser:/...` artifact link expired.

To get a fresh preview in this Codex session:

```bash
python3 -m http.server 8000
```

Then request a new screenshot render in-chat.

## Preview in GitHub

`browser:/...` links are session-local and do not render on GitHub. Use local serving (`python3 -m http.server 8000`) or deploy to GitHub Pages for a persistent URL.
