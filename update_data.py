#!/usr/bin/env python3
"""
Scraper de classificacions del Tour de França 2026
Font: ProCyclingStats (procyclingstats.com)
S'executa automàticament cada hora via GitHub Actions
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

BASE = "https://www.procyclingstats.com"
RACE = "race/tour-de-france/2026"

CLASSIFICATION_URLS = {
    "gc":       f"{BASE}/{RACE}/gc",
    "mountain": f"{BASE}/{RACE}/kom",
    "sprint":   f"{BASE}/{RACE}/points",
}

STAGES_URL = f"{BASE}/{RACE}/stages"


def scrape_classification(url, limit=20):
    """Scrapes a classification page and returns top N riders."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        table = soup.find("table", {"class": lambda c: c and "results" in c})
        if not table:
            table = soup.find("table")
        if not table:
            print(f"  No table found at {url}")
            return []

        rows = table.find_all("tr")[1:]  # skip header
        for row in rows[:limit]:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue
            pos_text = cols[0].get_text(strip=True)
            try:
                pos = int(pos_text)
            except ValueError:
                continue

            # Find rider name (usually in an <a> tag)
            rider_name = ""
            for col in cols:
                a = col.find("a", href=lambda h: h and "/rider/" in h)
                if a:
                    rider_name = a.get_text(strip=True)
                    break

            # Find team
            team_name = ""
            for col in cols:
                a = col.find("a", href=lambda h: h and "/team/" in h)
                if a:
                    team_name = a.get_text(strip=True)
                    break

            # Find time/points (last numeric column)
            value = ""
            for col in reversed(cols):
                t = col.get_text(strip=True)
                if t and t not in [rider_name, team_name, str(pos)]:
                    value = t
                    break

            if rider_name:
                results.append({
                    "pos": pos,
                    "name": rider_name,
                    "team": team_name,
                    "value": value
                })

        return results

    except Exception as e:
        print(f"  Error scraping {url}: {e}")
        return []


def scrape_stage_winners(limit=21):
    """Scrapes stage winners from the stages overview page."""
    try:
        r = requests.get(STAGES_URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        winners = []
        table = soup.find("table")
        if not table:
            return []

        rows = table.find_all("tr")[1:]
        for row in rows[:limit]:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            stage_num = cols[0].get_text(strip=True)
            date = cols[1].get_text(strip=True) if len(cols) > 1 else ""
            stage_name = cols[2].get_text(strip=True) if len(cols) > 2 else ""

            winner_name = ""
            winner_team = ""
            for col in cols:
                a = col.find("a", href=lambda h: h and "/rider/" in h)
                if a:
                    winner_name = a.get_text(strip=True)
                    break
            for col in cols:
                a = col.find("a", href=lambda h: h and "/team/" in h)
                if a:
                    winner_team = a.get_text(strip=True)
                    break

            if winner_name:
                winners.append({
                    "stage": stage_num,
                    "date": date,
                    "name": stage_name,
                    "winner": winner_name,
                    "team": winner_team
                })

        return winners

    except Exception as e:
        print(f"  Error scraping stages: {e}")
        return []


def get_current_stage(stage_winners):
    """Infer current stage from number of completed stages."""
    return len(stage_winners)


def main():
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}] Actualitzant classificacions...")

    data = {
        "updated_at": datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC"),
        "current_stage": 0,
        "gc": [],
        "mountain": [],
        "sprint": [],
        "stage_winners": []
    }

    print("  → Classificació General (GC)...")
    data["gc"] = scrape_classification(CLASSIFICATION_URLS["gc"])
    print(f"     {len(data['gc'])} corredors")

    print("  → Classificació Muntanya...")
    data["mountain"] = scrape_classification(CLASSIFICATION_URLS["mountain"])
    print(f"     {len(data['mountain'])} corredors")

    print("  → Classificació Sprint...")
    data["sprint"] = scrape_classification(CLASSIFICATION_URLS["sprint"])
    print(f"     {len(data['sprint'])} corredors")

    print("  → Guanyadors d'etapa...")
    data["stage_winners"] = scrape_stage_winners()
    data["current_stage"] = get_current_stage(data["stage_winners"])
    print(f"     {len(data['stage_winners'])} etapes completades")

    out_path = os.path.join(os.path.dirname(__file__), "data", "classifications.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  Desat a {out_path}")
    print("  Fet!")


if __name__ == "__main__":
    main()
