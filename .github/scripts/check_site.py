#!/usr/bin/env python3
"""Smoke-test generated GitHub Pages routes, navigation, archive and sitemap."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import sys
import xml.etree.ElementTree as ET

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
HOST = "zhaoshangwei.github.io"

REQUIRED = [
    "index.html", "about/index.html", "about.html",
    "research/index.html", "projects/index.html", "writing/index.html",
    "life/index.html", "en/index.html", "en/about/index.html",
    "en/research/index.html", "en/projects/index.html",
    "en/writing/index.html", "en/life/index.html",
    "projects/wafer-scheduling/index.html",
    "projects/process-optimization/index.html",
    "projects/production-scheduling/index.html",
    "projects/photo-archive/index.html",
    "en/projects/wafer-scheduling/index.html",
    "en/projects/process-optimization/index.html",
    "en/projects/production-scheduling/index.html",
    "en/projects/photo-archive/index.html",
    "archives/index.html", "tags/index.html", "404.html", "offline.html",
    "sitemap.xml", "robots.txt", "feed.xml",
    "img/portfolio/scheduling.svg", "img/portfolio/control.svg",
    "img/portfolio/archive.svg", "js/writing-search.js",
    "js/portfolio-toc.js", "css/portfolio.css",
]
missing = [p for p in REQUIRED if not (SITE / p).is_file()]
if missing:
    raise SystemExit("Missing required generated files:\n  " + "\n  ".join(missing))
if (SITE / "WEBSITE_GUIDE/index.html").exists():
    raise SystemExit("Internal maintenance guide should not be published as a website page")

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.desktop_nav = []
        self.mobile_nav = []
        self._nav = None
        self._anchor = None
        self._anchor_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "nav":
            classes = attrs.get("class", "").split()
            label = attrs.get("aria-label", "")
            if "desktop" in classes:
                self._nav = "desktop"
                self.desktop_nav.append([])
            elif "移动端导航" in label or "Mobile navigation" in label:
                self._nav = "mobile"
                self.mobile_nav.append([])
        if tag in ("a", "link", "img", "script", "source", "iframe", "form"):
            for key in ("href", "src", "action"):
                value = attrs.get(key)
                if value:
                    self.links.append(value)
        if tag == "a" and self._nav:
            self._anchor = True
            self._anchor_text = []

    def handle_data(self, data):
        if self._anchor:
            self._anchor_text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._anchor:
            label = "".join(self._anchor_text).strip()
            if label and self._nav:
                bucket = self.desktop_nav if self._nav == "desktop" else self.mobile_nav
                bucket[-1].append(label)
            self._anchor = None
            self._anchor_text = []
        if tag == "nav":
            self._nav = None

def page_url(rel):
    rel = rel.as_posix()
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    if rel == "index.html":
        return "/"
    return "/" + rel

def output_exists(path):
    path = unquote(path or "/")
    if not path.startswith("/"):
        path = "/" + path
    rel = path.lstrip("/")
    if path.endswith("/"):
        return (SITE / rel / "index.html").is_file()
    exact = SITE / rel
    if exact.is_file():
        return True
    if not Path(rel).suffix:
        return (SITE / rel / "index.html").is_file() or (SITE / (rel + ".html")).is_file()
    return False

def is_internal_url(target, current):
    parts = urlsplit(urljoin("https://" + HOST + current, target))
    if parts.scheme not in ("http", "https"):
        return None
    if parts.netloc and parts.hostname not in (HOST, "www." + HOST):
        return None
    return parts.path or "/"

CORE = [Path(p) for p in REQUIRED if p.endswith(".html")]
# Add all main pages explicitly; ignore links inside old archived article bodies,
# whose historical third-party references are not part of the new navigation QA.
CORE = [Path(p) for p in [
    "index.html", "about/index.html", "about.html",
    "research/index.html", "projects/index.html", "writing/index.html",
    "life/index.html", "en/index.html", "en/about/index.html",
    "en/research/index.html", "en/projects/index.html",
    "en/writing/index.html", "en/life/index.html",
    "projects/wafer-scheduling/index.html",
    "projects/process-optimization/index.html",
    "projects/production-scheduling/index.html",
    "projects/photo-archive/index.html",
    "en/projects/wafer-scheduling/index.html",
    "en/projects/process-optimization/index.html",
    "en/projects/production-scheduling/index.html",
    "en/projects/photo-archive/index.html",
    "archives/index.html", "tags/index.html", "404.html", "offline.html",
]]
broken = []
parsed = {}
for rel in CORE:
    file = SITE / rel
    parser = PageParser()
    parser.feed(file.read_text(encoding="utf-8"))
    parsed[rel.as_posix()] = parser
    base_url = page_url(rel)
    for target in parser.links:
        path = is_internal_url(target, base_url)
        if path is not None and not output_exists(path):
            broken.append(f"{rel.as_posix()} -> {target} (resolved {path})")
if broken:
    raise SystemExit("Broken internal links/assets:\n  " + "\n  ".join(broken[:80]))

zh = parsed["index.html"]
en = parsed["en/index.html"]
expected_zh = ["首页", "关于", "研究", "项目", "写作", "生活"]
expected_en = ["Home", "About", "Research", "Projects", "Writing", "Life"]
if not zh.desktop_nav or zh.desktop_nav[0] != expected_zh:
    raise SystemExit(f"Chinese desktop navigation mismatch: {zh.desktop_nav}")
if not zh.mobile_nav or zh.mobile_nav[0][:6] != expected_zh or zh.mobile_nav[0][6:] != ["English Version ↗"]:
    raise SystemExit(f"Chinese mobile navigation mismatch: {zh.mobile_nav}")
if not en.desktop_nav or en.desktop_nav[0] != expected_en:
    raise SystemExit(f"English desktop navigation mismatch: {en.desktop_nav}")
if not en.mobile_nav or en.mobile_nav[0][:6] != expected_en or en.mobile_nav[0][6:] != ["中文版 ↗"]:
    raise SystemExit(f"English mobile navigation mismatch: {en.mobile_nav}")

zh_html = (SITE / "index.html").read_text(encoding="utf-8")
en_html = (SITE / "en/index.html").read_text(encoding="utf-8")
if 'hreflang="en"' not in zh_html or 'hreflang="zh"' not in en_html:
    raise SystemExit("Missing reciprocal language metadata")
if 'http-equiv="refresh"' not in (SITE / "about.html").read_text(encoding="utf-8"):
    raise SystemExit("Legacy /about.html redirect is missing")

# Ensure the article archive has entries and the first article route resolves.
writing_parser = PageParser()
writing_parser.feed((SITE / "writing/index.html").read_text(encoding="utf-8"))
if not any("离散线性系统的模型预测控制" in (SITE / "writing/index.html").read_text(encoding="utf-8") for _ in [0]):
    raise SystemExit("Expected legacy article is missing from the writing archive")
post_pages = []
for html_file in SITE.rglob("*.html"):
    try:
        contents = html_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if 'class="reading-header"' in contents and 'id="post-content"' in contents:
        post_pages.append(html_file)
if not post_pages:
    raise SystemExit("No historical article pages were generated")
post_parser = PageParser()
post_parser.feed(post_pages[0].read_text(encoding="utf-8"))
if not any("/writing/" in link for link in post_parser.links):
    raise SystemExit("Historical article does not link back to the writing archive")

# Parse sitemap as XML and verify representative bilingual routes.
sitemap = ET.parse(SITE / "sitemap.xml")
locs = {node.text for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
for route in [
    "https://zhaoshangwei.github.io/",
    "https://zhaoshangwei.github.io/en/",
    "https://zhaoshangwei.github.io/projects/wafer-scheduling/",
    "https://zhaoshangwei.github.io/en/projects/wafer-scheduling/",
]:
    if route not in locs:
        raise SystemExit("Missing sitemap URL: " + route)

# Regression checks for social previews, mobile semantics and archived math.
for rel in ["index.html", "en/index.html", "projects/wafer-scheduling/index.html"]:
    html = (SITE / rel).read_text(encoding="utf-8")
    if 'property="og:image"' not in html or '/img/34999732.jpg' not in html:
        raise SystemExit(f"Missing social preview image metadata: {rel}")
    if 'name="twitter:image"' not in html:
        raise SystemExit(f"Missing Twitter image metadata: {rel}")
    if 'aria-current="page"' not in html:
        raise SystemExit(f"Missing current-page navigation semantics: {rel}")
if not (SITE / "img/34999732.jpg").is_file():
    raise SystemExit("Social preview asset is missing")
for post_file in post_pages:
    html = post_file.read_text(encoding="utf-8")
    if "mathjax@3/es5/tex-chtml.js" not in html:
        raise SystemExit(f"Archived article missing MathJax: {post_file.relative_to(SITE)}")

print(f"Site QA passed: {len(REQUIRED)} required files, {len(CORE)} page routes, bilingual navigation, legacy URL, article archive and XML sitemap.")
