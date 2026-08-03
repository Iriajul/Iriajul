"""Scrape the public GitHub contribution calendar (no token required).

Fetches https://github.com/users/<username>/contributions, parses each day's
date / level / count, and writes data/contributions.json.
"""

import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

PROFILE = Path("data/profile.json")
OUT = Path("data/contributions.json")


def get_username() -> str:
    profile = json.loads(PROFILE.read_text())
    return profile["username"]


def fetch_html(username: str) -> str:
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (profile-readme-bot)",
        "X-Requested-With": "XMLHttpRequest",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")

    # Counts live in <tool-tip> elements keyed by each day cell's id.
    counts_by_id: dict[str, int] = {}
    for tip in soup.find_all("tool-tip"):
        target = tip.get("for")
        if not target:
            continue
        m = re.search(r"([\d,]+)\s+contribution", tip.get_text())
        counts_by_id[target] = int(m.group(1).replace(",", "")) if m else 0

    days = []
    for cell in soup.select("td.ContributionCalendar-day"):
        date = cell.get("data-date")
        if not date:
            continue
        level = int(cell.get("data-level", 0))
        count = counts_by_id.get(cell.get("id", ""), 0)
        days.append({"date": date, "level": level, "count": count})

    days.sort(key=lambda d: d["date"])
    return days


def main() -> None:
    username = get_username()
    print(f"Fetching contributions for {username}")
    days = parse(fetch_html(username))
    if not days:
        raise SystemExit("No contribution days parsed; page layout may have changed")

    data = {
        "username": username,
        "total": sum(d["count"] for d in days),
        "days": days,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))
    print(f"Wrote {OUT} ({len(days)} days, {data['total']} contributions)")


if __name__ == "__main__":
    main()
