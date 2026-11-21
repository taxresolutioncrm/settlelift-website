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

## November 21, 2026 — unified design release

Branch: `design/settlelift-sitewide-finish-20261121`.

### Structural/design changes
- Removed the historical stack of overlapping late-stage `premium.css` overrides and replaced it with a single coordinated design layer, preserving the original component foundations and SettleLift colors.
- Established shared desktop, tablet, and mobile spacing, header/CTA treatment, product imagery sizing, interior page proportions, editorial cards, reporting visualization and implementation workflow styling.
- Homepage: added a three-workflow navigation band; enlarged the *contained* sample CRM preview to a readable 500px maximum and linked directly to the source illustrative image for closer inspection. Kept the screenshot beside explanatory copy, not as a full-width page takeover.
- Interior feature pages: added contextual demo and workflow links, preserved unique photography and improved image crop/height consistency.
- Existing CRM detail crops are distinct views of one **illustrative** screenshot, **not** separately captured real authenticated screens. No production metrics or claims of completed integrations were introduced.
- Implementation: preserved the four-step rollout board and normalized its container with other site sections.
- Reporting: retained grouped activity bars, follow-up priority breakout and explicit fictional-data disclosure.
- Versioned the consolidated stylesheet across all 27 public HTML pages to prevent stale CSS.

### Source QA performed
- Checked all 27 HTML pages for a unique H1, nonempty descriptions, canonical tags, stylesheet version, balanced section tags and no duplicate IDs.
- Confirmed all 27 pages use `premium.css?v=20261121-sitewide-finish`.
- Checked the homepage screenshot source link, 500px HTML/CSS cap, balanced sections, hero workflow band, analytics labels and sample-data disclosure.
- Checked the Implementation board replaced the tilted legacy mockup.
- Checked the official CRM login URL remains `https://app.settlelift.com`.
- Checked CSS opening/closing braces are balanced and both desktop and mobile breakpoint rules remain.
- Preserved the original sitemap, marketing paths, SEO metadata, tracking, contact flow, assets and branding.

### Not verified; do not claim complete
- No full authenticated Cloudflare browser pass, viewport screenshots, external photo rendering/crop QA, computed-style testing, Lighthouse measurements, or Cloudflare deployment confirmation were available in the source-only environment.
- The feature pages do not yet show unique authenticated CRM screenshots. That requires approved captures from each real CRM feature screen using synthetic data.
- Real-time behaviors such as contact/demo delivery and product-specific integrations were not independently exercised in this marketing-site-only release.
- Production readiness remains conditional on desktop (1440px), tablet (1024px) and mobile (375px) visual QA and a successful Cloudflare Pages production deployment.

## November 21 follow-up — eliminate redundant analytics showcase
The homepage previously presented a six-week reporting chart inside the fourth feature card and then an expanded operations reporting chart immediately below it. The duplicated KPIs (24, 16, 08) and back-to-back charts created redundant page storytelling. Replaced the fourth feature card with a **case-linked task handoff** example and a route to `/workflows/tasks-calendar/`; retained exactly one operational analytics dashboard in the dedicated Reporting section. Removed 24 obsolete mini-dashboard CSS rules rather than layering another override. Updated the homepage CSS cache key and regression checks to reject reintroducing the duplicate. The feature example uses synthetic case data and is not represented as a live task view.

Verified in source: balanced HTML sections; single analytics dashboard; no old mini-report markup or CSS; updated bilingual handoff labels; link to the existing tasks/calendar page; balanced CSS braces; unique homepage IDs. Live viewport rendering and Cloudflare production deployment remain unverified.

## November 21, 2026 — product-first site release

- The homepage now contains **two CRM visuals total**: the existing client workspace sample screenshot and one contained, illustrative negotiations concept linking to its feature page. Documents, tasks and reporting visuals are intentionally placed on their dedicated pages, not crowded onto the homepage.
- Added ten separate lightweight SVG workflow concepts, covering intake, negotiations, creditors, funding, client portal, documents, communications, reporting, multi-office access and tasks/calendar. Each contains synthetic example data and the explicit label **not a live CRM capture**.
- Embedded a matching, differently composed workflow preview on each of ten corresponding marketing pages. Added four previews to the Platform page.
- Preserved the existing genuine uploaded illustrative CRM image rather than replacing it with an image-generation output and claiming it is real. New SVG concepts must not be described as captured operational screens.
- Added a balanced two-column, single-preview product section on the homepage; responsive feature visuals, navigation and demo CTA. All 27 HTML pages synchronized to `premium.css?v=20261121-product-proof`.
- Source checks: 27 one-H1 pages, 27 stylesheet versions, homepage sections balanced, 10 asset wrappers and active sidebar states checked, CSS braces balanced, sample-data disclosures present. Regression gates updated for product view files and screenshot truthfulness.

**Remaining limitation:** Authenticated screenshots of actual functioning SettleLift CRM sections could not be collected from the source repository or unauthenticated website in this work. The illustrations show layout concepts, not verified running features. Cloudflare deployment and real browser visual validation are not confirmed.

## Homepage visual density correction — November 21
Per product owner feedback, the homepage is restricted to two CRM visuals at most: client summary plus one negotiations concept. The four-item showcase was removed. The separate documents, tasks, reporting, creditor, funding, portal, communications, intake and office visual previews remain distributed across dedicated pages, with their illustrative nature disclosed. Regression checks enforce the homepage limit.
