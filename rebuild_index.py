#!/usr/bin/env python3
"""Regenerate archive index pages from dated briefing files YYYY/YYYY-MM-DD.html."""
from pathlib import Path
import math
import re
import html
import datetime
import shutil

ROOT = Path(__file__).resolve().parent
WEEKDAY = "一二三四五六日"
PER_PAGE = 14  # ~12–16 entries per page

CSS = """
    :root {
      --bg: #f3f5f8;
      --bg-accent: #e8eef6;
      --paper: #ffffff;
      --ink: #1a1f2e;
      --muted: #5a6478;
      --line: #d8dee9;
      --line-soft: #e8edf4;
      --accent: #3b6d9a;
      --accent-soft: rgba(59, 109, 154, 0.12);
      --link: #2a5f8f;
      --link-hover: #1a4068;
      --nav-bg: rgba(255, 255, 255, 0.86);
      --shadow: 0 1px 2px rgba(26, 31, 46, 0.04), 0 4px 16px rgba(26, 31, 46, 0.04);
      --radius: 12px;
      --sans: "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Hiragino Sans GB",
               "Noto Sans SC", "Microsoft YaHei", sans-serif;
      --serif: "Songti SC", "Noto Serif SC", "Source Han Serif SC",
               "Noto Serif CJK SC", Georgia, serif;
    }
    * { box-sizing: border-box; }
    html { font-size: 16.5px; scroll-behavior: smooth; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      font-family: var(--serif);
      line-height: 1.7;
      background:
        linear-gradient(180deg, var(--bg-accent) 0%, transparent 280px),
        linear-gradient(90deg, rgba(59, 109, 154, 0.03) 1px, transparent 1px),
        linear-gradient(rgba(59, 109, 154, 0.03) 1px, transparent 1px),
        var(--bg);
      background-size: auto, 28px 28px, 28px 28px, auto;
      background-attachment: fixed;
    }
    .topnav {
      position: sticky;
      top: 0;
      z-index: 40;
      isolation: isolate;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      background: var(--nav-bg);
      border-bottom: 1px solid var(--line-soft);
    }
    .topnav::after {
      content: "";
      position: absolute;
      left: 0;
      right: 0;
      bottom: -1px;
      height: 1px;
      background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(59, 109, 154, 0.18) 20%,
        rgba(59, 109, 154, 0.52) 50%,
        rgba(59, 109, 154, 0.18) 80%,
        transparent 100%
      );
      opacity: 0.5;
      pointer-events: none;
    }
    .topnav-inner {
      width: min(1040px, calc(100% - 2.5rem));
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      padding: 0.72rem 0;
      font-family: var(--sans);
    }
    .brand {
      font-weight: 700;
      font-size: 0.95rem;
      letter-spacing: 0.04em;
      color: var(--ink);
      text-decoration: none;
    }
    .brand:hover { color: var(--link); }
    .nav-links {
      display: flex;
      align-items: center;
      gap: 0.15rem;
      list-style: none;
      margin: 0;
      padding: 0;
    }
    .nav-links a {
      display: inline-block;
      padding: 0.35rem 0.7rem;
      border-radius: 999px;
      color: var(--muted);
      text-decoration: none;
      font-size: 0.84rem;
      transition: color 0.15s ease, background 0.15s ease;
    }
    .nav-links a:hover,
    .nav-links a[aria-current="page"] {
      color: var(--ink);
      background: var(--accent-soft);
    }
    .wrap {
      width: min(1040px, calc(100% - 2.5rem));
      margin: 0 auto;
      padding: 2rem 0 3.5rem;
    }
    header.mast {
      margin-bottom: 2rem;
      padding: 0.4rem 0 1.5rem;
      border-bottom: 1px solid var(--line);
      position: relative;
    }
    header.mast::after {
      content: "";
      position: absolute;
      left: 0;
      bottom: -1px;
      width: 4.5rem;
      height: 2px;
      background: var(--accent);
      border-radius: 2px;
    }
    h1 {
      font-family: var(--sans);
      font-size: clamp(1.75rem, 4vw, 2.15rem);
      line-height: 1.25;
      margin: 0 0 0.5rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--ink);
    }
    .meta {
      font-family: var(--sans);
      font-size: 0.88rem;
      color: var(--muted);
      margin: 0;
      max-width: 36em;
    }
    .month-group {
      margin: 0 0 1.75rem;
    }
    .month-group:last-child { margin-bottom: 0.5rem; }
    .month-label {
      font-family: var(--sans);
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.12em;
      color: var(--accent);
      margin: 0 0 0.75rem;
      padding-left: 0.15rem;
    }
    .archive {
      list-style: none;
      padding: 0;
      margin: 0;
      display: grid;
      grid-template-columns: 1fr;
      gap: 0.85rem;
    }
    @media (min-width: 780px) {
      .archive { grid-template-columns: 1fr 1fr; }
    }
    .archive li { margin: 0; }
    .archive a.card {
      display: block;
      position: relative;
      text-decoration: none;
      color: var(--ink);
      background: var(--paper);
      border: 1px solid var(--line-soft);
      border-radius: var(--radius);
      padding: 1.1rem 1.2rem 1.15rem;
      box-shadow: var(--shadow);
      transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
      height: 100%;
    }
    .archive a.card::before {
      content: "";
      position: absolute;
      left: 0;
      top: 1rem;
      bottom: 1rem;
      width: 2px;
      border-radius: 0 2px 2px 0;
      background: var(--accent);
      opacity: 0;
      transform: scaleY(0);
      transform-origin: center;
      transition: opacity 0.2s ease, transform 0.2s ease;
      pointer-events: none;
    }
    .archive a.card:hover {
      border-color: #b8c5d8;
      box-shadow: 0 2px 4px rgba(26, 31, 46, 0.05), 0 8px 24px rgba(26, 31, 46, 0.07);
      transform: translateY(-1px);
      color: var(--ink);
    }
    .archive a.card:hover::before,
    .archive a.card:focus-visible::before {
      opacity: 0.9;
      transform: scaleY(1);
    }
    .archive .when {
      font-family: var(--sans);
      font-size: 0.76rem;
      letter-spacing: 0.04em;
      color: var(--muted);
      margin: 0 0 0.35rem;
    }
    .archive .title {
      font-family: var(--sans);
      font-size: 1.08rem;
      font-weight: 650;
      margin: 0 0 0.4rem;
      letter-spacing: -0.01em;
      line-height: 1.35;
    }
    .archive .blurb {
      margin: 0;
      color: var(--muted);
      font-size: 0.92rem;
      line-height: 1.65;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .pager {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
      margin-top: 2.25rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--line-soft);
      font-family: var(--sans);
    }
    .pager a,
    .pager span {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 2.2rem;
      height: 2.2rem;
      padding: 0 0.65rem;
      border-radius: 8px;
      font-size: 0.86rem;
      text-decoration: none;
      color: var(--muted);
      border: 1px solid transparent;
      transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
    }
    .pager a:hover {
      color: var(--ink);
      background: var(--paper);
      border-color: var(--line);
    }
    .pager .current {
      color: #fff;
      background: var(--accent);
      border-color: var(--accent);
      font-weight: 600;
    }
    .pager .disabled {
      opacity: 0.35;
      pointer-events: none;
    }
    .pager .nav-btn {
      color: var(--ink);
      border-color: var(--line);
      background: var(--paper);
    }
    .pager .nav-btn:hover {
      border-color: var(--accent);
      color: var(--accent);
    }
    .site-footer {
      margin-top: 2.5rem;
      padding-top: 1.1rem;
      border-top: 1px solid var(--line-soft);
      color: var(--muted);
      font-size: 0.8rem;
      font-family: var(--sans);
      text-align: center;
    }
    .site-footer p { margin: 0; }
    @media (prefers-reduced-motion: no-preference) {
      @keyframes archive-fade-rise {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
      }
      @keyframes nav-line-shimmer {
        0%, 100% { background-position: 0% 50%; opacity: 0.28; }
        50% { background-position: 100% 50%; opacity: 0.52; }
      }
      header.mast {
        animation: archive-fade-rise 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
      }
      .month-group {
        animation: archive-fade-rise 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
      }
      .month-group:nth-child(1) { animation-delay: 0.12s; }
      .month-group:nth-child(2) { animation-delay: 0.2s; }
      .month-group:nth-child(3) { animation-delay: 0.28s; }
      .month-group:nth-child(n + 4) { animation-delay: 0.36s; }
      .archive li {
        animation: archive-fade-rise 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
      }
      .archive li:nth-child(1) { animation-delay: 0.22s; }
      .archive li:nth-child(2) { animation-delay: 0.27s; }
      .archive li:nth-child(3) { animation-delay: 0.32s; }
      .archive li:nth-child(4) { animation-delay: 0.37s; }
      .archive li:nth-child(5) { animation-delay: 0.42s; }
      .archive li:nth-child(6) { animation-delay: 0.47s; }
      .archive li:nth-child(7) { animation-delay: 0.52s; }
      .archive li:nth-child(8) { animation-delay: 0.57s; }
      .archive li:nth-child(n + 9) { animation-delay: 0.62s; }
      .topnav::after {
        background-size: 200% 100%;
        animation: nav-line-shimmer 10s ease-in-out infinite;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      .topnav::after,
      header.mast,
      .month-group,
      .archive li {
        animation: none !important;
      }
    }
    @media (max-width: 520px) {
      .topnav-inner { width: calc(100% - 1.5rem); }
      .wrap { width: calc(100% - 1.5rem); padding-top: 1.5rem; }
      .nav-links a { padding: 0.3rem 0.5rem; font-size: 0.8rem; }
      .archive a.card { padding: 1rem; }
    }
"""


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
    """Group entries by month and render HTML sections."""
    sections = []
    current_key = None
    items = []

    def flush():
        nonlocal items, current_key
        if not items:
            return
        month_label = items[0]["month_label"]
        cards = []
        for e in items:
            blurb_src = e["lede"]
            blurb = html.escape(blurb_src[:220] + ("…" if len(blurb_src) > 220 else ""))
            cards.append(
                "        <li>\n"
                f'          <a class="card" href="{e["href"]}">\n'
                f'            <p class="when">{e["label"]} · {e["dow"]}</p>\n'
                f'            <p class="title">{e["label"]} 简报</p>\n'
                f'            <p class="blurb">{blurb}</p>\n'
                "          </a>\n"
                "        </li>"
            )
        sections.append(
            f'      <section class="month-group" aria-label="{month_label}">\n'
            f'        <h2 class="month-label">{month_label}</h2>\n'
            f'        <ol class="archive">\n'
            + "\n".join(cards)
            + "\n        </ol>\n"
            "      </section>"
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
        return "/index.html"
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
    home_current = ' aria-current="page"' if page_num == 1 else ""
    archive_current = ' aria-current="page"' if page_num > 1 else ""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="每日简报归档：工作日更新，覆盖 AI、科学、科技业界与抗衰论文。">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <style>
{CSS}
  </style>
</head>
<body>
  <nav class="topnav" aria-label="主导航">
    <div class="topnav-inner">
      <a class="brand" href="/index.html">每日简报</a>
      <ul class="nav-links">
        <li><a href="/index.html"{home_current}>首页</a></li>
        <li><a href="{html.escape(newest_href)}">最新一期</a></li>
        <li><a href="/index.html"{archive_current}>归档</a></li>
      </ul>
    </div>
  </nav>
  <div class="wrap">
    <header class="mast">
      <h1>每日简报</h1>
      <p class="meta">工作日 08:00 更新 · 亚洲/上海 · AI、科学、科技业界、抗衰论文</p>
    </header>
{cards_html}
{pager_html}
    <footer class="site-footer">
      <p>每日简报 · 按日期归档</p>
    </footer>
  </div>
</body>
</html>
"""


def main():
    entries = collect_entries()
    total = len(entries)
    total_pages = max(1, math.ceil(total / PER_PAGE)) if total else 1
    newest_href = entries[0]["href"] if entries else "/index.html"

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


if __name__ == "__main__":
    main()
