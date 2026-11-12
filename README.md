# HellixStudio — Independent Art Gallery + Etsy Funnel

A complete, fast, mobile-first static website for **shophellixstudio.com**. Includes a showcase homepage, filterable product catalog, individual wallpaper landing pages, journal/blog, three starter posts, SEO metadata, sitemap, RSS feed, a 404 page, and analytics hooks.

Brand colors are Midnight Indigo `#141B31`, Champagne Gold `#D7B77A`, warm ivory `#F9F5EE`, muted lavender and soft powder blue accents. The exact user-provided HellixStudio emblem is integrated into the site.

The artwork previews in `src/static/images/` come from existing HellixStudio creative assets. The site is a **preview**, not an update to your live domain, until you deploy it.

## What's in the ZIP?

- `site/` — **ready-to-publish website**. Contains the generated HTML, CSS, images, sitemap and blog articles. There is no runtime or build dependency when visitors browse it.
- `content/products.json` — edit product names, descriptions, previews, Etsy links and ordering.
- `content/posts/*.md` — your blog articles. Add Markdown files to publish more.
- `content/settings.json` — optional GA4 tracking ID, shop and channel URLs.
- `src/templates/` — page layouts. `src/static/` — styles, scripts and artwork.
- `scripts/build.py` — regenerates the whole site from the content and layouts.
- `.github/workflows/deploy.yml` — automatic GitHub Pages deployment when you push to `main`.

## Deploy to your existing GitHub Pages website

**Back up your current repository first**; this replaces the currently published homepage when deployed.

1. Unzip the package. Copy all files and folders **inside** `HellixStudio-Website/` into the root of your GitHub repository. (Do not add an extra nested folder.) Preserve the hidden `.github` directory.
2. Commit and push to your `main` branch.
3. In GitHub, open **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Confirm that the workflow **Build and deploy HellixStudio** succeeds under the **Actions** tab.
5. Under **Settings → Pages**, confirm **Custom domain** is `shophellixstudio.com`. The build includes `CNAME`, but you must preserve the domain and DNS settings already in use.
6. Open `https://shophellixstudio.com/` and test each purchase link and product image.

**No GitHub Actions available?** You can instead publish the contents of `site/` directly as the root of a GitHub Pages branch or any static hosting platform. This method does not automatically rebuild Markdown posts; run the builder locally before uploading updates.

## Local preview

Python 3.10+ is required to edit and regenerate content. Use:

```bash
pip install -r requirements.txt
python scripts/build.py
cd site
python -m http.server 8000
```

Open `http://localhost:8000/`. Stop the server with Ctrl+C.

## Add a new product

Edit `content/products.json`. Add an entry with a **unique slug**, product name, description, category, image filename, and real Etsy listing URL. Copy the compressed image into `src/static/images/` and adjust `image` accordingly. Use real screenshots or artwork previews you own. Run `python scripts/build.py` to regenerate pages. Avoid copying full-size purchased JPGs into this public website; showcase compressed previews only.

Existing listing links are based on your previously supplied listing IDs. **Verify the URLs and product inclusions against Etsy before deployment**, particularly any mockups that may show older packaging such as Clear/Tinted modes or a 6-wallpaper set. Replace those previews with your current two-JPG mockups whenever available.

## Publish a new blog article

Create `content/posts/my-new-article.md`:

```md
---
title: A New Little World for Your iPhone
slug: a-new-little-world
excerpt: A brief one-sentence description of the article.
category: Inspiration
date: 2026-11-11
image: glasshouse-art.webp
reading_time: 4 min read
related_product: christmas-wallpaper-bundle
video_url: ""
---

Write your article here using **Markdown**. It supports headings, lists, links, and tables.

## A section heading

Share something genuinely helpful and naturally introduce your product.
```

The `related_product` value must match a slug in `content/products.json`. When you publish a corresponding YouTube video, paste its full YouTube URL into `video_url` to display a Watch on YouTube call-to-action on that article. The YouTube channel URL in settings is intentionally blank until you confirm the exact channel link.

Run `python scripts/build.py` to preview locally, or push changes to GitHub to trigger automatic deployment.

## Google Analytics 4

Tracking is **off by default**. If you choose to enable it, enter your `G-XXXXXXXXXX` measurement ID in `content/settings.json` under `ga4_measurement_id`. Outbound Etsy clicks fire a GA4 event called `etsy_outbound`, with parameters `product_slug`, `site_location`, and `link_url`. Validate the events in GA4 DebugView/Realtime. The website does not know whether a click becomes an Etsy sale.

Before enabling Google Analytics, update the privacy notice and any consent mechanisms appropriate to the jurisdictions you serve. This template does **not** implement a consent management platform.

## Important quality checks

- Product details and current digital file counts should be checked against the live Etsy listings. The preview images come from previous HellixStudio creative assets and may include outdated text baked into the artwork.
- All source images used here are web-compressed previews, not high-resolution digital product downloads.
- The supplied original navy-and-gold HellixStudio emblem is included in the header and footer as optimized web assets (see `src/static/images/hellix-logo.webp`).
- Blog articles are starter posts written for this website; revise any claims and publish dates as needed.
- Existing video links were not guessed. You can attach your real YouTube videos when published.
- The website and checkout are separate. Etsy handles transactions and delivery.

## Optional enhancements

Connect Google Search Console, add Pinterest-rich original images, place buyer-intent posts into an editorial calendar, and consider a Git-backed editor if Markdown becomes cumbersome.

## Quick interactive preview (without publishing)

**Windows:** Double-click `Preview Website.bat`. It opens http://localhost:8000 and serves the entire website. You need Python 3 installed. Close the terminal to stop the preview.

**macOS:** Run `Preview Website.command` in Terminal (or `cd site && python3 -m http.server 8000`).

This is a local, interactive browser preview, not a public link. It uses the exact pages, logo, and artwork in the ZIP. It does not modify your currently published domain.
