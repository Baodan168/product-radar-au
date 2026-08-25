#!/usr/bin/env python3
"""
Season Engine — AU seasonal event prediction for product sourcing.

Built-in calendar of Australian consumer events (Jan-Dec) with:
- Event dates and recommended product categories
- Sourcing deadlines (air freight: -45 days, sea freight: -75 days)
- Seasonal search keyword generation

Usage:
    python3 season_engine.py                  # upcoming events (90 days)
    python3 season_engine.py --days 120       # next 120 days
    python3 season_engine.py --keywords       # current seasonal keywords
    python3 season_engine.py --json           # JSON output
"""
import json, sys
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).parent
CONFIG = json.loads((BASE / "config.json").read_text())

# ── AU Seasonal Events Calendar ───────────────────────────────────
# Each event: name, month, day (approx), categories, year_override for floating dates
# Fixed dates use (month, day). Floating dates use best-guess for current year.
# For floating events, we store the typical month/week range and pick a plausible date.

# AU_EVENTS 表已移除 — 统一由 `festival_engine` 管理的 `data/au_festivals_data.js` 提供完整节日数据。
# 如需查看事件列表，运行 `python3 -c "from festival_engine import load_festivals; import json; print(json.dumps(load_festivals(), indent=2, ensure_ascii=False))"`


def _build_event_date(event, reference_year):
    """Build a datetime for the event in the reference year.
    
    For events that have passed this year, rolls to next year.
    """
    month = event["month"]
    day = event["day"]

    # Handle month overflow (e.g., month=13 for events that need next-year wrap)
    try:
        dt = datetime(reference_year, month, day)
    except ValueError:
        # Invalid day (e.g., Feb 30), fall back to last day of month
        if month == 2:
            dt = datetime(reference_year, 2, 28)
        elif month in (4, 6, 9, 11):
            dt = datetime(reference_year, month, 30)
        else:
            dt = datetime(reference_year, month, 31)

    return dt


def get_upcoming_events(days_ahead=90):
    """Get upcoming AU seasonal events within the specified window.

    Args:
        days_ahead: how many days ahead to look (default 90)

    Returns:
        list of dicts: [{
            event_name, date, days_until, recommended_categories,
            sourcing_deadline_air, sourcing_deadline_sea, notes
        }]
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    cutoff = today + timedelta(days=days_ahead)

    upcoming = []

    for event in AU_EVENTS:
        # Try current year, then next year
        for year_offset in range(2):
            event_date = _build_event_date(event, today.year + year_offset)

            if event_date < today:
                continue
            if event_date > cutoff:
                break

            days_until = (event_date - today).days

            # Sourcing deadlines (aligned with uk-festival-planner + festival_engine.py)
            # Air: production(3)+transit(13)=16d, Truck: 3+30=33d, Sea: 3+60=63d
            # Buffer: +14d (FBA receiving + safety)
            air_deadline = event_date - timedelta(days=16 + 14)
            rail_deadline = event_date - timedelta(days=33 + 14)
            sea_deadline = event_date - timedelta(days=63 + 14)

            # Status — best available option
            if air_deadline < today:
                sourcing_urgency = "OVERDUE"  # All options expired
            elif rail_deadline < today:
                sourcing_urgency = "AIR_ONLY"  # Only air freight viable
            elif sea_deadline < today:
                sourcing_urgency = "RAIL_OR_AIR"  # Sea missed, rail still OK
            elif (air_deadline - today).days <= 7:
                sourcing_urgency = "URGENT"  # Air deadline approaching
            else:
                sourcing_urgency = "OK"

            upcoming.append({
                "event_name": event["event_name"],
                "date": event_date.strftime("%Y-%m-%d"),
                "days_until": days_until,
                "recommended_categories": event["recommended_categories"],
                "sourcing_deadline_air": air_deadline.strftime("%Y-%m-%d"),
                "sourcing_deadline_rail": rail_deadline.strftime("%Y-%m-%d"),
                "sourcing_deadline_sea": sea_deadline.strftime("%Y-%m-%d"),
                "sourcing_urgency": sourcing_urgency,
                "notes": event.get("notes", ""),
            })
            break  # Don't add the same event for next year

    upcoming.sort(key=lambda x: x["days_until"])
    
    # Merge Festival Planner events (primary source, more complete)
    try:
        from festival_engine import load_festivals, get_deadlines
        festivals = load_festivals()
        existing_dates = {(e["date"], e["event_name"]) for e in upcoming}
        
        for f in festivals:
            f_date_str = f.get("date", "")
            if not f_date_str:
                continue
            f_date = datetime.strptime(f_date_str, "%Y-%m-%d")
            if f_date < today or f_date > cutoff:
                continue
            
            # Skip if already in upcoming (from UK_EVENTS)
            if (f_date_str, f.get("name", "")) in existing_dates:
                continue
            
            deadlines = get_deadlines(f)
            days_until = (f_date - today).days
            
            # Determine urgency from sea deadline
            sea_days = deadlines.get("sea", {}).get("days_from_today", 999)
            if sea_days < 0:
                sourcing_urgency = "OVERDUE"
            elif sea_days <= 7:
                sourcing_urgency = "URGENT"
            else:
                sourcing_urgency = "OK"
            
            upcoming.append({
                "event_name": f"{f.get('icon', '📅')} {f.get('name', '')}",
                "date": f_date_str,
                "days_until": days_until,
                "recommended_categories": [p.get("category", "") for p in f.get("products", [])[:3]],
                "sourcing_deadline_air": deadlines.get("air", {}).get("date", ""),
                "sourcing_deadline_rail": deadlines.get("truck", {}).get("date", ""),
                "sourcing_deadline_sea": deadlines.get("sea", {}).get("date", ""),
                "sourcing_urgency": sourcing_urgency,
                "notes": f"Importance: {f.get('importance', 'B')} | {len(f.get('products', []))} SKUs",
                "source": "festival_planner",
            })
        
        upcoming.sort(key=lambda x: x["days_until"])
    except Exception as e:
        print(f"  ⚠️ Festival Planner merge failed: {e}", file=sys.stderr)
    
    # AU_EVENTS 表已移除 — 统一由 `festival_engine` 管理的 `data/au_festivals_data.js` 提供完整节日数据。
    # 如需查看事件列表，运行 `python3 -c "from festival_engine import load_festivals; import json; print(json.dumps(load_festivals(), indent=2, ensure_ascii=False))"`
    return []  # get_upcoming_events() now delegated to festival_engine; this block is kept for compatibility but unused


def get_seasonal_keywords():
    """Return search keywords relevant to the current season.

    Based on the current month and upcoming events in the next 30 days.
    Returns list of keyword strings suitable for Amazon AU / AnySearch.
    """
    today = datetime.now()
    month = today.month

    # Seasonal keyword map
    seasonal = {
        1: ["storage organiser", "desk accessories", "meal prep containers",
            "cleaning tools", "kitchen gadgets new year"],
        2: ["valentine gift ideas", "romantic gift", "travel accessories",
            "decorative items", "gift packaging"],
        3: ["spring cleaning tools", "garden tools", "kitchen gadgets",
            "home decor", "storage solutions", "mothers day gift"],
        4: ["garden accessories", "easter decoration", "outdoor tools",
            "kitchen gadgets", "party supplies", "cleaning supplies"],
        5: ["garden tools", "BBQ accessories", "garden decor",
            "plant pots", "picnic items", "outdoor cushions"],
        6: ["travel accessories", "car cleaning", "outdoor gadgets",
            "water bottle", "picnic set", "camping accessories",
            "fathers day gift"],
        7: ["outdoor accessories", "BBQ tools", "travel gadgets",
            "car accessories", "camping gear", "beach accessories",
            "prime day deals"],
        8: ["travel accessories", "back to school stationery", "lunch box",
            "desk organiser", "storage", "outdoor cooling"],
        9: ["kitchen gadgets", "autumn decor", "desk accessories",
            "storage organiser", "candles", "university essentials"],
        10: ["halloween decoration", "autumn garden tools", "party supplies",
             "candles", "bird feeder", "bird accessories"],
        11: ["christmas decoration", "gift ideas", "tinsel garlands",
             "party supplies", "kitchen gadgets", "blanket throw",
             "black friday deals"],
        12: ["christmas gifts", "party supplies", "storage organiser",
             "kitchen gadgets", "travel accessories", "home decor"],
    }

    keywords = seasonal.get(month, ["kitchen accessories", "home gadgets"])

    # Add upcoming event keywords
    upcoming = get_upcoming_events(days_ahead=30)
    for event in upcoming:
        for cat in event["recommended_categories"]:
            if cat not in keywords and cat != "everything — best sellers":
                keywords.append(cat.lower())

    # Deduplicate, preserving order
    seen = set()
    unique = []
    for kw in keywords:
        kw_lower = kw.lower().strip()
        if kw_lower not in seen:
            seen.add(kw_lower)
            unique.append(kw)

    return unique


if __name__ == "__main__":
    output_json = "--json" in sys.argv

    # Parse --days N
    days = 90
    for i, arg in enumerate(sys.argv):
        if arg == "--days" and i + 1 < len(sys.argv):
            try:
                days = int(sys.argv[i + 1])
            except ValueError:
                pass

    if "--keywords" in sys.argv:
        keywords = get_seasonal_keywords()
        if output_json:
            print(json.dumps(keywords, indent=2))
        else:
            print("=== Current Seasonal Keywords ===")
            for i, kw in enumerate(keywords, 1):
                print(f"  {i}. {kw}")
            print(f"\n  Total: {len(keywords)} keywords")
    else:
        events = get_upcoming_events(days_ahead=days)

        if output_json:
            print(json.dumps(events, indent=2, ensure_ascii=False))
        else:
            print(f"=== Upcoming AU Events (next {days} days) ===\n")
            if not events:
                print("  No events found in this window.")
            for e in events:
                urgency_icon = {
                    "OK": "✅", "URGENT": "⚠️", "AIR_ONLY": "🟡", "OVERDUE": "🔴"
                }.get(e["sourcing_urgency"], "")
                print(f"  {e['date']}  ({e['days_until']}d away)  {e['event_name']}  {urgency_icon}")
                print(f"    Categories: {', '.join(e['recommended_categories'][:4])}")
                print(f"    Sourcing: air={e['sourcing_deadline_air']} sea={e['sourcing_deadline_sea']} "
                      f"[{e['sourcing_urgency']}]")
                if e.get("notes"):
                    print(f"    Note: {e['notes']}")
                print()

            print(f"\n--- Current Seasonal Keywords ---")
            for kw in get_seasonal_keywords()[:10]:
                print(f"  • {kw}")
