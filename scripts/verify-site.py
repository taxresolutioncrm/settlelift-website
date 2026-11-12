from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,xml.etree.ElementTree as ET
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
 assert 'siteLanguage' in path.read_text(),path
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
assert all(s in home for s in ['SAMPLE DATA','IN DEVELOPMENT','shared backend are pending','/login/'])
assert 'crm-buyer-checklist' in (root/'resources/choosing-debt-settlement-crm/index.html').read_text()
assert (root/'assets/settlelift-client-workspace.jpg').stat().st_size<250000
print('PASS: 27 unique pages, metadata/schema/sitemap preserved, all local links/assets/anchors valid, shared styles and language controls present; sample status and lightweight product image verified.')
