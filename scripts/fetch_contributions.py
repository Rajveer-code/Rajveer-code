#!/usr/bin/env python3
"""Fetch a real GitHub contribution calendar with no token and no API.

GitHub serves the calendar as public HTML at
    https://github.com/users/<username>/contributions
— the same fragment the profile page renders. We scrape the day cells and
per-day tool-tips, then write data/contributions.json (raw days + derived
stats) for render_heatmap_svg.py to draw.
"""
import datetime as dt
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USERNAME", "Rajveer-code")
OUT = "data/contributions.json"
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_html():
    headers = {
        "User-Agent": "Mozilla/5.0 (profile-art contribution fetcher)",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
    }
    # Prefer certifi's CA bundle — some Python installs (miniconda, minimal
    # CI images) can't find a local issuer cert otherwise.
    try:
        import certifi
        verify = certifi.where()
    except ImportError:
        verify = True
    r = requests.get(URL, headers=headers, timeout=30, verify=verify)
    r.raise_for_status()
    return r.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")

    # id -> count, from the per-day tool-tips ("N contributions on ...")
    counts = {}
    for tip in soup.find_all("tool-tip"):
        tid = tip.get("for")
        if not tid:
            continue
        text = tip.get_text(" ", strip=True)
        if text.lower().startswith("no contribution"):
            counts[tid] = 0
        else:
            mo = re.search(r"([\d,]+)", text)
            counts[tid] = int(mo.group(1).replace(",", "")) if mo else 0

    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        cells = soup.find_all(attrs={"data-date": True})

    days = []
    for c in cells:
        date = c.get("data-date")
        if not date:
            continue
        level = int(c.get("data-level", 0) or 0)
        cid = c.get("id")
        count = c.get("data-count")
        if count is not None:
            count = int(count)
        elif cid in counts:
            count = counts[cid]
        else:
            count = 0
        days.append({"date": date, "count": count, "level": level})

    if not days:
        raise RuntimeError("no contribution cells parsed — page layout changed?")

    days.sort(key=lambda d: d["date"])
    return days


def grid_positions(days):
    """Sunday-aligned column/row for each day, GitHub-style."""
    first = dt.date.fromisoformat(days[0]["date"])
    # back up to the Sunday on/before the first date  (Sun=6 in weekday())
    start = first - dt.timedelta(days=(first.weekday() + 1) % 7)
    for d in days:
        delta = (dt.date.fromisoformat(d["date"]) - start).days
        d["col"] = delta // 7
        d["row"] = delta % 7


def derive_stats(days):
    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"])

    # longest streak of consecutive active days
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)

    # current streak from the end; today (last cell) may legitimately be 0
    rev = list(reversed(days))
    start = 1 if rev and rev[0]["count"] == 0 else 0
    current = 0
    for d in rev[start:]:
        if d["count"] > 0:
            current += 1
        else:
            break

    return {
        "total_last_year": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
    }


def main():
    try:
        days = parse(fetch_html())
    except Exception as e:  # network/layout failure -> keep any existing file
        print(f"fetch failed: {e}", file=sys.stderr)
        if os.path.exists(OUT):
            print("keeping existing", OUT)
            return
        raise
    grid_positions(days)
    stats = derive_stats(days)
    data = {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "username": USERNAME,
        "weeks": max(d["col"] for d in days) + 1,
        **stats,
        "days": days,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    print(f"wrote {OUT}: {len(days)} days, {stats['total_last_year']} contributions, "
          f"streak {stats['current_streak']}/{stats['longest_streak']}")


if __name__ == "__main__":
    main()
