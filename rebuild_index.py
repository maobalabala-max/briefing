#!/usr/bin/env python3
"""Regenerate index.html from dated briefing files YYYY/YYYY-MM-DD.html."""
from pathlib import Path
import re, html, datetime

ROOT = Path(__file__).resolve().parent
WEEKDAY = "一二三四五六日"

CSS = """    :root {
      --bg: #f4f1ea;
      --paper: #fcfaf6;
      --ink: #1c1915;
      --muted: #5c564c;
      --line: #e4ddd2;
      --accent: #8b4513;
      --link: #1f4e79;
      --link-hover: #0d2f4f;
    }
    * { box-sizing: border-box; }
    html { font-size: 17px; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: "Iowan Old Style", "Palatino Linotype", Palatino, "Songti SC", "Noto Serif SC", "Source Han Serif SC", "Noto Serif CJK SC", Georgia, serif;
      line-height: 1.7;
    }
    .wrap {
      width: min(1080px, calc(100% - 3rem));
      max-width: 1080px;
      margin: 0 auto;
      padding: 2.2rem 0 4rem;
    }
    header.mast {
      border-bottom: 2px solid var(--ink);
      padding-bottom: 1.35rem;
      margin-bottom: 1.75rem;
    }
    .kicker {
      letter-spacing: 0.18em;
      text-transform: uppercase;
      font-size: 0.72rem;
      color: var(--muted);
      font-family: "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Noto Sans SC", sans-serif;
      margin: 0 0 0.45rem;
    }
    .kicker a { color: inherit; text-decoration: none; }
    h1 {
      font-size: 2.05rem;
      line-height: 1.2;
      margin: 0 0 0.55rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }
    .meta {
      font-family: "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Noto Sans SC", sans-serif;
      font-size: 0.86rem;
      color: var(--muted);
      margin: 0;
    }
    a { color: var(--link); }
    a:hover { color: var(--link-hover); }
    .archive { list-style: none; padding: 0; margin: 0; }
    .archive {
      display: grid;
      grid-template-columns: 1fr;
      gap: 0.85rem;
    }
    @media (min-width: 840px) {
      .archive { grid-template-columns: 1fr 1fr; }
    }
    .archive li { margin: 0; }
    .archive a {
      display: block;
      text-decoration: none;
      color: var(--ink);
      background: var(--paper);
      border: 1px solid var(--line);
      padding: 1.05rem 1.15rem;
    }
    .archive a:hover { border-color: var(--ink); }
    .archive .when {
      font-family: "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Noto Sans SC", sans-serif;
      font-size: 0.78rem;
      letter-spacing: 0.06em;
      color: var(--muted);
      margin: 0 0 0.28rem;
    }
    .archive .title {
      font-size: 1.18rem;
      font-weight: 700;
      margin: 0 0 0.35rem;
    }
    .archive .blurb {
      margin: 0;
      color: var(--muted);
      font-size: 0.95rem;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    footer {
      margin-top: 2.4rem;
      padding-top: 1rem;
      border-top: 1px solid var(--line);
      color: var(--muted);
      font-size: 0.82rem;
      font-family: "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Noto Sans SC", sans-serif;
    }
"""

def main():
    entries = []
    for path in sorted(ROOT.glob("[0-9][0-9][0-9][0-9]/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].html"), reverse=True):
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
            "label": f"{dt.year}年{dt.month}月{dt.day}日",
            "dow": f"周{WEEKDAY[dt.weekday()]}",
            "lede": lede,
        })
    items = []
    for e in entries:
        blurb = html.escape(e["lede"][:220] + ("…" if len(e["lede"]) > 220 else ""))
        items.append(
            "      <li>\n"
            f'        <a href="{e["href"]}">\n'
            f'          <p class="when">{e["label"]} · {e["dow"]}</p>\n'
            f'          <p class="title">{e["label"]} 简报</p>\n'
            f'          <p class="blurb">{blurb}</p>\n'
            "        </a>\n"
            "      </li>"
        )
    joined = "\n".join(items)
    html_out = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>每日简报</title>
  <style>
{CSS}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="mast">
      <h1>每日简报</h1>
      <p class="meta">工作日 08:00 更新 · 亚洲/上海 · AI、科学、科技业界、抗衰论文</p>
    </header>
    <ol class="archive">
{joined}
    </ol>
    <footer>
      <p>按日期归档，地址形如 /2026/2026-08-27.html</p>
    </footer>
  </div>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html_out, encoding="utf-8")
    print(f"wrote index.html with {len(entries)} entries")

if __name__ == "__main__":
    main()
