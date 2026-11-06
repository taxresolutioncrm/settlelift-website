# SettleLift website: GitHub + Cloudflare Pages setup

This package contains the marketing website only. It does not publish the CRM or activate Supabase. It retains noindex while launch work remains. The development buttons link to the roadmap; there are no private-prototype links or disconnected forms.

1. Extract this ZIP. Upload the public folder and this README to the root of a private GitHub repository named settlelift-website. Keep the public folder intact. Do not upload only the ZIP.
2. In Cloudflare, open Workers & Pages and create a Pages project connected to that repository. Choose the Pages flow, not a Worker deployment.
3. Project name: settlelift-website. Production branch: main. Framework: None. Build command: exit 0. Output directory: public. Root directory: leave blank. Environment variables: none.
4. Start the initial deployment and verify the assigned pages.dev address. Test both pages, Spanish, workflow tabs, FAQs, and logo loading.
5. In the Pages project, choose Custom domains > Set up a custom domain > settlelift.com. Follow the domain verification instructions. For the apex domain, the domain must be a zone in the same Cloudflare account and use Cloudflare nameservers. If DNS is currently elsewhere, preserve existing email and verification records when moving it. Do not replace existing mail records with website records.
6. After the apex is active, add www.settlelift.com using the same Custom domains flow. Follow the DNS records provided by Cloudflare. Set the canonical redirect from www to https://settlelift.com using a redirect rule after both hosts are verified.
7. Confirm HTTPS, both languages, logo, workflow tabs, FAQ toggles and /security/ on the custom domain.
8. Keep this as a development website until lead/booking delivery, business contact/privacy details, analytics and final mobile checks are complete. Before search indexing, remove the noindex meta tags and X-Robots-Tag in public/_headers, change robots.txt to allow crawling, and verify canonical URLs and sitemap on the live domain. Do not activate indexing merely because hosting succeeds.

The uploaded package already contains built HTML/CSS/JS and image assets. No npm installation, Supabase key or separate deploy command is needed for Cloudflare Pages. The earlier exporter-command instructions applied to the full source checkout, not this ready-to-upload package.

Changes to the selected production branch can trigger Cloudflare production deployments. Use a separate branch for future review, and follow the existing explicit release protocol.


## Expanded website: 22 pages

This replaces the earlier two-page package. Upload the entire extracted public folder to overwrite existing paths and add all pages. Do not nest it inside another public folder. Cloudflare output remains public; build command remains exit 0.

Pages:
- Home: /
- Access & data: /security/
- Lead intake & enrollment: /features/intake-enrollment/
- Negotiations & settlement offers: /features/negotiations/
- Creditor & collector management: /features/creditor-management/
- Funding & commitment planning: /features/funding-planning/
- Client experience & portal: /features/client-portal/
- Documents, worksheets & signatures: /features/documents-signatures/
- Communication & follow-up: /features/communications/
- Portfolio reporting & oversight: /features/reporting/
- Multi-office teams & access: /features/multi-office/
- The SettleLift platform: /platform/
- Lead management & follow-up: /workflows/lead-management/
- Tasks, appointments & reminders: /workflows/tasks-calendar/
- Data imports & migration review: /workflows/data-imports/
- State availability & company scope: /state-availability/
- Integrations & connection boundaries: /integrations/
- Implementation & launch preparation: /implementation/
- Why SettleLift: /about/
- Build status & release roadmap: /roadmap/
- Debt settlement workflow glossary: /resources/glossary/
- Product questions & answers: /faq/
