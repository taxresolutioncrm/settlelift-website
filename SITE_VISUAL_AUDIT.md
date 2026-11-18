# SettleLift visual QA closeout — November 18, 2026

## Scope / protocol
Source-scoped review of 27 public HTML pages, marketing styles and reusable assets, from main release `c11d9b78536fc31158c3a4b143cb57096f06ae34`.
Work was performed on the isolated `develop/compact-preview-professional-report` branch. No GitHub Actions runs or repeated production deployments were requested. This change is designed for **one Cloudflare-connected main release**.

## Confirmed defects from screenshots and code
1. Repeated the same photographer image IDs on multiple feature pages, regardless of subject matter.
2. Oversized `settlelift-client-workspace.jpg` displayed close to full marketing content width.
3. Elementary horizontal sample workload bars presented as if they were sophisticated analytics.
4. Malformed homepage markup: `<section id="workspace" class="sl-product"<div ...` missing `>`.
5. QA script had no image uniqueness assertion; could not prevent repeated photographs.

## Corrections implemented
- Replaced the repeated images on **15 distinct interior pages** with 15 unique photographs and specific headline/caption/alt text for each page. Homepage keeps its **three additional, separate photographs**.
- Brought the CRM screenshot to a controlled **760px maximum** on desktop in a framed container. Original screenshot file and its link remain intact; mobile layout shrinks with viewport.
- Rebuilt the small reporting feature into a polished miniature analytics card: three KPIs, meaningful labels, six-week trend chart with axes, explanatory source/illustrative status. The larger analytics dashboard remains intact.
- Repaired the malformed `#workspace` HTML element.
- Strengthened `scripts/verify-site.py` checks to ensure chart treatment, image uniqueness, 15 individual interior photo panels, preview sizing and markup integrity.
- Preserved distinct headings, canonical pages, GTM, Clarity script version, all internal links, bilingual attributes, CTA routing, marketing domain and existing CRM asset.

## Source inspection results
| Area | Coverage | Current result |
|---|---:|---|
| HTML page inventory | 27/27 | Inspected via repository source |
| Premium stylesheet links | 27/27 | Present |
| Unique main heading | 27/27 | One h1 per page |
| Homepage photos | 3 | Three unique IDs |
| Interior photography | 15 | Fifteen distinct IDs, no intentional duplication |
| Other informational pages | 9 | Text-led resources, FAQ, login, security, and policy pages rather than repeated filler photos |
| CRM screenshot | 1 preserved asset | Capped CSS frame |
| Reporting card | 1 | Replaced with new line-chart SVG |
| SEO / instrumentation | All original page sources | No intentional modifications |
| Browser visual comparison | Desktop/mobile | **Not tested in authenticated/cloud browser** |
| Cloudflare deployment | Production | **Not verified** |

## Acceptance gates
- Run `python scripts/verify-site.py` in the real website checkout (local, not GitHub Actions) before final closeout. Static source inspection was completed, but a local execution is not represented as passed unless actually run.
- Confirm the site on 1440px desktop, 1024px tablet and 375px mobile.
- Check external CDN images and crop quality in a live browser.
- Check hero, all 15 photograph pages, mobile navigation, screenshot scaling and both analytics panels.
- Confirm Cloudflare is serving the new main commit, no broken links or console exceptions.
- Do **not** call any demo graph live financial results or verified settlement rates.

## Photo source register
See `PHOTO_SOURCES.md`. No synthetic-person images were generated and no photographed subject is represented as an actual SettleLift customer or employee.

## 2026-11-18 structural follow-up
A subsequent desktop screenshot showed the top marketing composition visually tiny next to the CRM screenshot. Source review identified another design defect: the old opening layout stacked the hero copy and the photograph strip rather than treating them as a cohesive two-column product hero. CSS URLs were reused across the previous releases, risking stale browser styling.

Updated `premium.css` with a new desktop hero layout using an explicit wide `1320px` container, two proportional columns, large headline, deliberate CTA placement, and a single impactful human photograph. The second photograph is suppressed in the hero to avoid the 'two tiny cards' treatment. Tablet and mobile layouts were addressed separately. Added a new heading before the CRM screenshot, a strict 720px maximum for its frame in both CSS and inline HTML attributes, and lazy loading. All 27 pages now request `premium.css?v=20261118-layout-v2` to invalidate earlier cached CSS.

Static source checks confirmed 27/27 pages retain one H1, the GTM tag and updated stylesheet reference. No claim is made that a real browser has passed visual QA or that Cloudflare has deployed the commit; these must be checked on production using desktop and mobile viewports.

No authenticated CRM data, production settlement metrics or proprietary branding assets were changed.
