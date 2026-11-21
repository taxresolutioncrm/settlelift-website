from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,xml.etree.ElementTree as ET
import re
root=Path(__file__).resolve().parents[1]/'public'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.h1=0;self.ids=set();self.links=[];self.canon=[];self.titles=[];self.description=[];self.robots=[];self.in_title=False;self.in_schema=False;self.schemas=[];self.schema='';self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if 'id' in a:assert a['id'] not in self.ids,('Duplicate ID',a['id']);self.ids.add(a['id'])
  if tag=='title':self.in_title=True
  if tag=='script' and a.get('type')=='application/ld+json':self.in_schema=True;self.schema=''
  if tag=='link' and a.get('rel')=='canonical':self.canon.append(a.get('href'))
  if tag=='meta' and a.get('name')=='description':self.description.append(a.get('content',''))
  if tag=='meta' and a.get('name')=='robots':self.robots.append(a.get('content',''))
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
 def handle_data(self,s):
  if self.in_title:self.titles.append(s)
  if self.in_schema:self.schema+=s
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
  if t=='script' and self.in_schema:self.schemas.append(json.loads(self.schema));self.in_schema=False
tracking=(root/'site.js').read_text()
assert tracking.count('ze2d5b2ixy')==2, 'SettleLift Clarity project must have exactly one loader, plus its comment'
assert 'https://www.clarity.ms/tag/' in tracking
pages={p:Page(p.read_text()) for p in root.rglob('*.html')}
assert len(pages)==27,len(pages)
seen_titles=set();seen_canon=set()
for path,page in pages.items():
 assert page.h1==1,(path,page.h1)
 assert len(page.canon)==1,(path,'canonical')
 assert page.canon[0] not in seen_canon;seen_canon.add(page.canon[0])
 title=''.join(page.titles);assert title and title not in seen_titles,(path,title);seen_titles.add(title)
 assert len(page.description)==1 and page.description[0],path
 assert page.schemas,path
 assert 'noindex' not in ','.join(page.robots),path
 assert '/editorial.css?v=20261112-product' in path.read_text(),path
 assert ('/energy.css?v=20261112-map-final' if path==root/'index.html' else '/energy.css?v=20261112-connected') in path.read_text(),path
 assert path.read_text().count('GTM-W4MBL7WQ')==1,(path,'GTM duplicate or missing')
 assert 'window.dataLayer=window.dataLayer||[]' in path.read_text(),(path,'dataLayer missing')
 if path!=root/'index.html':
  assert 'sl-interior' in path.read_text() and 'sl-page-hero' in path.read_text() and 'sl-page-visual' in path.read_text(),path
 assert 'siteLanguage' in path.read_text(),path
 assert path.read_text().count('/site.js?v=20261115-clarity')==1,(path,'shared Clarity script version missing or duplicated')
 for value in page.links:
  u=urlsplit(value)
  if u.scheme or u.netloc:continue
  target=(root/unquote(u.path).lstrip('/')) if u.path.startswith('/') else path.parent/unquote(u.path)
  if not u.path:target=path
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(path,value,target)
  if u.fragment and target.suffix=='.html':assert unquote(u.fragment) in pages[target.resolve() if target.resolve() in pages else target].ids,(path,value)
locs={x.text for x in ET.parse(root/'sitemap.xml').iter() if x.tag.endswith('}loc')}
assert locs==seen_canon,('Sitemap mismatch',locs^seen_canon)
home=(root/'index.html').read_text()
assert 'sl-editorial-home' in home and 'settlelift-client-workspace.jpg' in home
assert all(x in home for x in ['sl-network','sl-tour-workbench','sl-bento','sl-launch-board'])
assert (root/'energy.css').stat().st_size<100000
assert all(value in home for value in ['SAMPLE DATA','/login/'])
assert 'IN DEVELOPMENT' not in home and 'EN DESARROLLO' not in home
assert 'development preview' not in home
# Premium redesign invariants (GitHub Actions intentionally not invoked for this release).
assert '/premium.css?v=20261121-platform-proof' in (root/'platform/index.html').read_text(), 'Platform preview release cache key missing'
assert all('/premium.css?v=20261121-product-proof' in p.read_text() for p in pages if p!=root/'platform/index.html'), 'All remaining pages must use product gallery stylesheet'
assert home.count('images.unsplash.com/')>=3, 'Hero and people section need licensed real photography'
assert 'sl-premium-analytics' in home and 'sl-analytics-dashboard' in home, 'Premium analytics illustration missing'
assert 'sl-insights-priorities' in home and 'sl-insights-legend' in home, 'Operational analytics must use the expanded chart and priorities'
assert 'PEOPLE-CENTERED OPERATIONS' not in home, 'Outdated floating photography badge remains'
implementation=(root/'implementation/index.html').read_text()
assert 'sl-implementation-board' in implementation and 'sl-implementation-steps' in implementation, 'Implementation page must show the complete rollout board'
assert 'sl-page-launch' not in implementation, 'Old tilted implementation mockup must not return'
assert 'Fictional values demonstrate reporting design' in home, 'Illustrative graph must never claim production metrics'
assert 'sl-bento-handoff' in home and 'sl-handoff-preview' in home, 'Team workflow card missing'
assert 'sl-report-mini' not in home, 'Duplicate reporting mini dashboard must not return'
assert home.count('sl-analytics-dashboard') == 1, 'Only one reporting dashboard belongs on homepage'
assert 'href="/workflows/tasks-calendar/" class="sl-bento-card sl-bento-handoff"' in home, 'Team workflow card must open the tasks and calendar page'
assert '<section id="workspace" class="sl-product"><div class="sl-container sl-workspace-showcase">' in home, 'Malformed CRM showcase section'
assert '<section id="workspace" class="sl-product"<' not in home, 'Broken HTML tag must not return'
assert 'sl-screen-link' in home and 'max-width:500px' in home and 'max-width:500px!important' in (root/'premium.css').read_text(), 'CRM preview must stay contained and readable'
photo_sources={}
for path in pages:
 for photo in re.findall(r'images\.unsplash\.com/(photo-[\w-]+)',path.read_text()):
  photo_sources.setdefault(photo,[]).append(path.relative_to(root).as_posix())
assert len(photo_sources)>=18, ('Expected unique photos across product pages',len(photo_sources))
# Context-specific photography is a release invariant, not just a unique URL count.
expected_page_photos={
 'features/client-portal/index.html':'photo-1758611974982-ca55f12b3378',
 'features/communications/index.html':'photo-1712159018726-4564d92f3ec2',
 'features/creditor-management/index.html':'photo-1762427354051-a9bdb181ae3b',
 'features/documents-signatures/index.html':'photo-1764231467852-b609a742e082',
 'features/funding-planning/index.html':'photo-1772588627327-1eeddcf73c11',
 'features/intake-enrollment/index.html':'photo-1774205884989-37f0f2271503',
 'features/negotiations/index.html':'photo-1714079761488-e0c9b9ac4138',
 'features/reporting/index.html':'photo-1758691736542-c437fea2c673',
 'features/multi-office/index.html':'photo-1760346546839-aced24accdff',
 'workflows/tasks-calendar/index.html':'photo-1435527173128-983b87201f4d',
 'platform/index.html':'photo-1768483538267-fce52de424d5',
}
for page_rel,photo_id in expected_page_photos.items():
 text=(root/page_rel).read_text()
 assert photo_id in text,(page_rel,'Incorrect page-specific photo')
 assert text.count('images.unsplash.com/photo-')==1,(page_rel,'Unexpected repeated page photography')
 assert 'alt="' in text,(page_rel,'Missing meaningful photo description')

assert all(len(used_by)==1 for used_by in photo_sources.values()), ('Photo reused across unrelated pages',[(p,locations) for p,locations in photo_sources.items() if len(locations)>1])
assert sum(1 for p in pages if 'sl-interior-photo-panel' in p.read_text())>=15, 'Each major feature page needs a distinct image'
assert (root/'premium.css').stat().st_size>8500, 'Missing premium responsive layout'
assert (root.parent/'PHOTO_SOURCES.md').exists(), 'Photographic license/source record missing'

# Closeout regression gates: sitewide CSS cache bust and actual hero scaling.
assert '/premium.css?v=20261121-product-proof' in home, 'Homepage stylesheet cache refresh missing'
assert '<section id="workspace" class="sl-product"><div class="sl-container sl-workspace-showcase">' in home, 'CRM section must be structurally valid'
assert 'sl-screen-intro' in home and 'sl-showcase-points' in home and 'sl-workspace-preview' in home, 'Side-by-side CRM composition missing'
assert 'sl-capability-ribbon' in home, 'Workflow capability strip must appear after hero'
assert 'sl-product-proof' in home and 'sl-proof-grid' in home, 'Product gallery missing from homepage'
assert home.count('/assets/product-view-') == 1, 'Homepage must show at most one feature view plus the client workspace image'
assert '/assets/product-view-negotiations.svg' in home, 'Negotiation preview missing from homepage'
assert '<img class="sl-product-screen"' in home, 'Existing client workspace preview missing'
feature_views={
 'features/intake-enrollment/index.html':'intake',
 'features/negotiations/index.html':'negotiations',
 'features/creditor-management/index.html':'creditors',
 'features/funding-planning/index.html':'funding',
 'features/client-portal/index.html':'portal',
 'features/documents-signatures/index.html':'documents',
 'features/communications/index.html':'communications',
 'features/reporting/index.html':'reporting',
 'features/multi-office/index.html':'offices',
 'workflows/tasks-calendar/index.html':'tasks'
}
for rel,view in feature_views.items():
 page_text=(root/rel).read_text()
 assert 'sl-feature-proof' in page_text,(rel,'Feature gallery missing')
 assert '/assets/product-view-'+view+'.svg' in page_text,(rel,'Incorrect or missing product view')
 assert 'illustrative' in page_text.lower(),(rel,'Missing illustrative disclosure')
 svg=(root/'assets'/('product-view-'+view+'.svg')).read_text()
 assert svg.startswith('<svg ') and svg.strip().endswith('</svg>'),(view,'Invalid SVG wrapper')
 assert 'NOT A LIVE CRM CAPTURE' in svg,(view,'Product illustration must not be represented as actual screenshot')
 assert '{e(sub)}' not in svg and 'fill="2"' not in svg,(view,'Unrendered templating in SVG')
platform_html=(root/'platform/index.html').read_text()
assert 'sl-platform-workflow-nav' in platform_html, 'Platform workflow navigation missing'
assert 'sl-platform-proof-grid' not in platform_html, 'Four-up thumbnail gallery must not return'
assert platform_html.count('src="/assets/settlelift-client-workspace.jpg"') == 1, 'Platform must not duplicate the client screenshot'
assert '<nav class="sl-platform-feature-links"' in platform_html, 'Distinct feature links must replace repeated screenshots'
assert '.sl-platform-feature-links' in (root/'premium.css').read_text(), 'Workflow navigation styling missing'

assert 'href="/assets/settlelift-client-workspace.jpg"' in home, 'CRM sample must be inspectable at its full original resolution'
assert '<section class="sl-capability-ribbon"' in home, 'Feature routing strip missing'
for name in ['features/intake-enrollment','features/negotiations','features/creditor-management','features/funding-planning','features/client-portal','features/documents-signatures','features/communications','features/reporting','features/multi-office']:
 feature=(root/name/'index.html').read_text()
 assert 'sl-page-hero-actions' in feature,(name,'Missing clear demo and workflow actions')
 assert 'href="/contact/#demo"' in feature,(name,'Demo routing missing')

for rel in ['features/creditor-management/index.html','features/negotiations/index.html','features/reporting/index.html']:
 sample=(root/rel).read_text()
 assert 'sl-crm-detail' not in sample,(rel,'Repeated client overview crop must not return')
 assert 'sl-feature-proof' in sample,(rel,'Distinct feature view missing')
assert '.sl-crm-detail-crop' not in (root/'premium.css').read_text(),'Orphaned screenshot crop styling must not return'

assert 'max-width:500px' in home, 'Screenshot must have a readable inline cap if CSS is stale'
assert 'SETTLELIFT UNIFIED RELEASE' in (root/'premium.css').read_text(), 'Consolidated design system absent'
assert 'grid-template-columns:minmax(0,1.02fr) minmax(0,.98fr)' in (root/'premium.css').read_text(), 'Desktop hero must use split composition'
assert 'body.sl-editorial-home .sl-opening>.sl-container' in (root/'premium.css').read_text(), 'Page wide hero layout is missing'
login=(root/'login/index.html').read_text()
assert 'https://app.settlelift.com' in login, 'CRM login must open the actual SettleLift app'
assert 'settlelift.rcruz187.chatgpt.site' not in login, 'Legacy preview login forbidden'
assert 'Private development workspace' not in login, 'Obsolete development login heading'
assert 'development workspace' not in login, 'Obsolete development access copy'
assert 'crm-buyer-checklist' in (root/'resources/choosing-debt-settlement-crm/index.html').read_text()
assert (root/'assets/settlelift-client-workspace.jpg').stat().st_size<250000
print('PASS: 27 unique pages, metadata/schema/sitemap preserved, all local links/assets/anchors valid, shared styles and language controls present; illustrative sample status and lightweight product image verified.')
