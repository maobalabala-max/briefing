#!/usr/bin/env python3
"""Regenerate archive index pages from dated briefing files YYYY/YYYY-MM-DD.html.

Styling comes from /assets/briefing.css (v2 design, shared with daily pages); helpers in tools/briefing_common.py.
Ends by running build_site_meta.py (og tags, feed.xml, sitemap.xml, robots.txt)."""
from pathlib import Path
import math
import re
import html
import datetime
import shutil

ROOT = Path(__file__).resolve().parent
WEEKDAY = "一二三四五六日"
PER_PAGE = 14  # ~12–16 entries per page

import sys as _sys
_sys.dont_write_bytecode = True
_sys.path.insert(0, str(ROOT / "tools"))
from briefing_common import HEAD_ICONS, bar_html, css_href  # noqa: E402  (shared v2 design helpers)


def collect_entries():
    entries = []
    for path in sorted(
        ROOT.glob("[0-9][0-9][0-9][0-9]/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].html"),
        reverse=True,
    ):
        date_s = path.stem
        dt = datetime.date.fromisoformat(date_s)
        text = path.read_text(encoding="utf-8")
        lede_m = re.search(r'<p class="lede">(.*?)</p>', text, re.S)
        lede = re.sub("<[^>]+>", "", lede_m.group(1) if lede_m else "")
        lede = html.unescape(re.sub(r"\s+", " ", lede)).strip()
        year = path.parent.name
        entries.append({
            "href": f"/{year}/{path.name}",
            "iso": date_s,
            "dt": dt,
            "label": f"{dt.year}年{dt.month}月{dt.day}日",
            "dow": f"周{WEEKDAY[dt.weekday()]}",
            "month_key": (dt.year, dt.month),
            "month_label": f"{dt.year}年{dt.month}月",
            "lede": lede,
        })
    return entries


def render_cards(page_entries):
    """Group entries by month and render the v2 archive list (shared /assets/briefing.css)."""
    sections = []
    current_key = None
    items = []

    def flush():
        nonlocal items
        if not items:
            return
        lis = []
        for e in items:
            blurb_src = e["lede"]
            blurb = html.escape(blurb_src[:220] + ("…" if len(blurb_src) > 220 else ""))
            lis.append(
                f'        <li><a href="{e["href"]}"><span class="d">{e["dt"].month}月{e["dt"].day}日'
                f'<span>{e["dow"]}</span></span><span class="b">{blurb}</span></a></li>'
            )
        sections.append(
            f'    <section class="month" aria-label="{items[0]["month_label"]}">\n'
            f'      <h2>{items[0]["month_label"]}</h2>\n      <ol class="entries">\n'
            + "\n".join(lis)
            + "\n      </ol>\n    </section>"
        )
        items = []

    for e in page_entries:
        if e["month_key"] != current_key:
            flush()
            current_key = e["month_key"]
        items.append(e)
    flush()
    return "\n".join(sections)


def page_href(page_num):
    if page_num <= 1:
        return "/"
    return f"/page/{page_num}.html"


def render_pager(page_num, total_pages):
    if total_pages <= 1:
        return ""

    parts = []
    # Prev
    if page_num > 1:
        parts.append(
            f'<a class="nav-btn" href="{page_href(page_num - 1)}" rel="prev">上一页</a>'
        )
    else:
        parts.append('<span class="nav-btn disabled" aria-disabled="true">上一页</span>')

    # Page numbers (show all if small; else window)
    window = 7
    if total_pages <= window:
        page_range = range(1, total_pages + 1)
    else:
        start = max(1, page_num - 2)
        end = min(total_pages, start + window - 1)
        start = max(1, end - window + 1)
        page_range = range(start, end + 1)
        if start > 1:
            parts.append(f'<a href="{page_href(1)}">1</a>')
            if start > 2:
                parts.append('<span aria-hidden="true">…</span>')

    for p in page_range:
        if p == page_num:
            parts.append(f'<span class="current" aria-current="page">{p}</span>')
        else:
            parts.append(f'<a href="{page_href(p)}">{p}</a>')

    if total_pages > window:
        end = page_range[-1] if page_range else 0
        if end < total_pages:
            if end < total_pages - 1:
                parts.append('<span aria-hidden="true">…</span>')
            parts.append(f'<a href="{page_href(total_pages)}">{total_pages}</a>')

    # Next
    if page_num < total_pages:
        parts.append(
            f'<a class="nav-btn" href="{page_href(page_num + 1)}" rel="next">下一页</a>'
        )
    else:
        parts.append('<span class="nav-btn disabled" aria-disabled="true">下一页</span>')

    return (
        '    <nav class="pager" aria-label="分页">\n'
        + "      "
        + "\n      ".join(parts)
        + "\n    </nav>"
    )


def render_page(page_num, total_pages, page_entries, newest_href):
    title = "每日简报" if page_num == 1 else f"每日简报 · 第 {page_num} 页"
    cards_html = render_cards(page_entries)
    pager_html = render_pager(page_num, total_pages)
    links = [("最新一期", newest_href, False), ("AI 日报", "/ai/", False), ("订阅", "/feed.xml", False)]
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="每日简报归档：覆盖 AI、科学、科技业界与抗衰论文。">
  <meta name="color-scheme" content="light dark">
  {HEAD_ICONS}
  <link rel="stylesheet" href="{css_href(ROOT)}">
</head>
<body class="idx">
{bar_html("", links, brand=True)}
<div class="page">
  <main>
    <header class="mast">
      <h1><a class="home" href="/">每日简报</a></h1>
      <p class="sub">AI、科学、科技业界、抗衰论文 · <a href="/ai/">AI 前沿情报日报</a></p>
    </header>
{cards_html}
{pager_html}
    <footer><p class="pn"><span>每日简报 · 按日期归档</span><a href="/feed.xml">订阅（Atom）</a></p></footer>
  </main>
</div>
</body>
</html>
"""


def main():
    entries = collect_entries()
    total = len(entries)
    total_pages = max(1, math.ceil(total / PER_PAGE)) if total else 1
    newest_href = entries[0]["href"] if entries else "/"

    # Clean old page/ directory if present, then recreate when needed
    page_dir = ROOT / "page"
    if page_dir.exists():
        shutil.rmtree(page_dir)

    written = []
    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * PER_PAGE
        chunk = entries[start : start + PER_PAGE]
        html_out = render_page(page_num, total_pages, chunk, newest_href)
        if page_num == 1:
            out_path = ROOT / "index.html"
        else:
            page_dir.mkdir(parents=True, exist_ok=True)
            out_path = page_dir / f"{page_num}.html"
        out_path.write_text(html_out, encoding="utf-8")
        written.append(str(out_path.relative_to(ROOT)))

    print(f"wrote {len(written)} page(s) with {total} entries ({PER_PAGE}/page):")
    for w in written:
        print(f"  {w}")

    # SEO/social tags on all pages + feed.xml / sitemap.xml / robots.txt (idempotent)
    import sys
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(ROOT))
    import build_site_meta
    build_site_meta.main()


if __name__ == "__main__":
    main()
