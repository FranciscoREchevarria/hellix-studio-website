#!/usr/bin/env python3
"""Generate a deployable, SEO-friendly, zero-runtime-dependency static site."""
from __future__ import annotations
import json
import shutil
from pathlib import Path
from datetime import date
from html import escape
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
import yaml
import mistune
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'site'
CONTENT = ROOT / 'content'
PUBLIC = ROOT / 'src' / 'static'
URL = 'https://shophellixstudio.com'
NOW = date.today().isoformat()
PRODUCTS = json.loads((CONTENT / 'products.json').read_text(encoding='utf-8'))
SETTINGS = json.loads((CONTENT / 'settings.json').read_text(encoding='utf-8'))
PRODUCTS.sort(key=lambda p:p.get('order', 100))
BY_SLUG = {p['slug']: p for p in PRODUCTS}


def parse_post(path: Path) -> dict:
    source = path.read_text(encoding='utf-8')
    if not source.startswith('---\n'):
        raise ValueError(f'{path} must begin with YAML frontmatter')
    _, front, body = source.split('---\n', 2)
    record = yaml.safe_load(front)
    if not isinstance(record, dict) or not record.get('title') or not record.get('slug'):
        raise ValueError(f'Invalid article metadata: {path}')
    record['date'] = str(record['date'])
    dt = date.fromisoformat(record['date'])
    record['pretty_date'] = f'{dt.strftime("%B")} {dt.day}, {dt.year}'
    record['html'] = mistune.create_markdown(escape=True, plugins=['table'])(body)
    return record

POSTS = sorted([parse_post(p) for p in (CONTENT/'posts').glob('*.md')], key=lambda x:x['date'], reverse=True)
ENV = Environment(loader=FileSystemLoader(ROOT/'src'/'templates'), autoescape=select_autoescape(['html']))
PAGES: list[str] = []

def structured(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False).replace('<', '\\u003c')


def build_page(template: str, path: str, title: str, description: str, **data) -> None:
    if not path.startswith('/') or not path.endswith('/') and path != '/404.html':
        raise ValueError(path)
    target = (OUTPUT / '404.html') if path == '/404.html' else (OUTPUT / path.lstrip('/') / 'index.html')
    target.parent.mkdir(parents=True, exist_ok=True)
    params = dict(path=path, title=title, description=description, nav='', year=date.today().year,
                  products=PRODUCTS, articles=POSTS, ga4_id=SETTINGS.get('ga4_measurement_id',''),
                  og_image='og-cover.jpg',jsonld='',is_article=False)
    params.update(data)
    target.write_text(ENV.get_template(template).render(**params), encoding='utf-8')
    if path != '/404.html': PAGES.append(path)
    print('Built', path)


def build() -> None:
    if OUTPUT.exists(): shutil.rmtree(OUTPUT)
    shutil.copytree(PUBLIC, OUTPUT)
    (OUTPUT/'.nojekyll').touch()
    (OUTPUT/'CNAME').write_text('shophellixstudio.com\n',encoding='utf-8')
    organization={'@context':'https://schema.org','@type':'Organization','name':'HellixStudio','url':URL,'sameAs':[SETTINGS['shop_url']]}
    build_page('index.html','/','HellixStudio | Little Worlds for Your Screen',
               'Explore dreamy iPhone wallpapers inspired by cozy Christmas, enchanted gardens, and magical little worlds. Discover the art and shop on Etsy.',nav='home',jsonld=structured(organization))
    build_page('collections.html','/collections/','iPhone Wallpapers & Collections | HellixStudio',
               'Discover coordinated iPhone wallpapers by HellixStudio. Browse seasonal favorites, storybook art, and cozy library scenes.',nav='collections')
    for p in PRODUCTS:
        data={'@context':'https://schema.org','@type':'CreativeWork','name':p['name'],
              'description':p['description'],'creator':{'@type':'Organization','name':'HellixStudio'},
              'image': f'{URL}/images/{p["image"]}','url': f'{URL}/wallpapers/{p["slug"]}/'}
        build_page('product.html',f'/wallpapers/{p["slug"]}/',f'{p["name"]} | HellixStudio',
                   p['description'],nav='collections',product=p,related=[x for x in PRODUCTS if x['slug']!=p['slug']][:3],
                   og_image=p['image'],jsonld=structured(data))
    build_page('journal.html','/journal/','The Journal | Wallpaper Ideas & Studio Notes | HellixStudio',
               'Read iPhone wallpaper inspiration, setup guides and behind-the-scenes stories about digital illustration and GIMP editing.',nav='journal')
    for p in POSTS:
        related_product = BY_SLUG.get(p.get('related_product'))
        if related_product is None:
            raise ValueError(f'Article {p["slug"]}: related_product must match a known slug')
        data={'@context':'https://schema.org','@type':'BlogPosting','headline':p['title'],
              'description':p['excerpt'],'datePublished':p['date'],'dateModified':p['date'],
              'author':{'@type':'Organization','name':'HellixStudio'},
              'publisher':{'@type':'Organization','name':'HellixStudio'},
              'image':f'{URL}/images/{p["image"]}', 'mainEntityOfPage':f'{URL}/journal/{p["slug"]}/'}
        build_page('article.html',f'/journal/{p["slug"]}/',f'{p["title"]} | HellixStudio Journal',
                   p['excerpt'],nav='journal',post=p,related_product=related_product,
                   related_articles=[x for x in POSTS if x['slug']!=p['slug']][:2],og_image=p['image'],jsonld=structured(data),is_article=True)
    build_page('about.html','/about/','About the Art | HellixStudio',
               'Get to know HellixStudio, an independent creative brand making magical, nostalgic and painterly iPhone wallpaper art.',nav='about')
    build_page('privacy.html','/privacy/','Privacy Notice | HellixStudio',
               'Read about privacy and external shopping links on the HellixStudio website.')
    build_page('notfound.html','/404.html','Page Not Found | HellixStudio','The page you requested could not be found.')

    (OUTPUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {URL}/sitemap.xml\n',encoding='utf-8')
    urlset=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for path in PAGES:
        entry=ET.SubElement(urlset,'url'); ET.SubElement(entry,'loc').text=URL+path
        ET.SubElement(entry,'lastmod').text=NOW
    ET.indent(urlset,space='  ')
    ET.ElementTree(urlset).write(OUTPUT/'sitemap.xml',encoding='utf-8',xml_declaration=True)

    rss=ET.Element('rss',version='2.0');channel=ET.SubElement(rss,'channel')
    for tag,val in [('title','HellixStudio Journal'),('link',URL+'/journal/'),('description','Wallpaper inspiration, setup guides, and studio notes')]:
        ET.SubElement(channel,tag).text=val
    for p in POSTS:
        item=ET.SubElement(channel,'item')
        for tag,val in [('title',p['title']),('link',URL+'/journal/'+p['slug']+'/'),('guid',URL+'/journal/'+p['slug']+'/'),('description',p['excerpt'])]:
            ET.SubElement(item,tag).text=val
    ET.indent(rss,space='  '); ET.ElementTree(rss).write(OUTPUT/'feed.xml',encoding='utf-8',xml_declaration=True)
    print(f'Completed {len(PAGES)} static pages in {OUTPUT}')

if __name__=='__main__': build()
