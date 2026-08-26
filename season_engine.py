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
    """[已废弃] 旧内联事件表辅助函数。表已移除，保留空实现仅为兼容历史引用。"""
    raise NotImplementedError("AU_EVENTS 表已移除，节日数据统一由 festival_engine 提供")


def get_upcoming_events(days_ahead=90):
    """Get upcoming AU seasonal events within the specified window.

    数据统一来自 festival_engine（data/au_festivals_data.js），输出 schema 与旧版一致：
    event_name/date/days_until/recommended_categories/sourcing_deadline_{air,rail,sea}/
    sourcing_urgency(OK|URGENT|AIR_ONLY|RAIL_OR_AIR|OVERDUE)/notes

    Args:
        days_ahead: how many days ahead to look (default 90)

    Returns:
        list of dicts 按 days_until 升序
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    cutoff = today + timedelta(days=days_ahead)

    try:
        from festival_engine import load_festivals, get_deadlines
        festivals = load_festivals()
    except Exception as e:
        print(f"  ⚠️ festival_engine load failed: {e}", file=sys.stderr)
        return []

    if not festivals:
        # load_festivals 返回空列表 = 所有数据源都读不到（见其 docstring），不能当作「没有节日」
        print("  ⚠️ 无可用节日数据源", file=sys.stderr)
        return []

    upcoming = []
    for f in festivals:
        f_date_str = f.get("date", "")
        if not f_date_str:
            continue
        try:
            f_date = datetime.strptime(f_date_str, "%Y-%m-%d")
        except ValueError:
            continue
        if f_date < today or f_date > cutoff:
            continue

        deadlines = get_deadlines(f)
        days_until = (f_date - today).days

        air_days = deadlines.get("air", {}).get("days_from_today", 999)
        rail_days = deadlines.get("truck", {}).get("days_from_today", 999)
        sea_days = deadlines.get("sea", {}).get("days_from_today", 999)

        # Status — best available option（与旧版内联表逻辑一致）
        if air_days < 0:
            sourcing_urgency = "OVERDUE"      # 全部方式过期
        elif rail_days < 0:
            sourcing_urgency = "AIR_ONLY"     # 仅剩空运
        elif sea_days < 0:
            sourcing_urgency = "RAIL_OR_AIR"  # 海运过期
        elif air_days <= 7:
            sourcing_urgency = "URGENT"       # 空运截止临近
        else:
            sourcing_urgency = "OK"

        upcoming.append({
            "event_name": f"{f.get('icon', '📅')} {f.get('name', '')}".strip(),
            "date": f_date_str,
            "days_until": days_until,
            "recommended_categories": [p.get("category", "") for p in f.get("products", [])[:4]],
            "sourcing_deadline_air": deadlines.get("air", {}).get("date", ""),
            "sourcing_deadline_rail": deadlines.get("truck", {}).get("date", ""),
            "sourcing_deadline_sea": deadlines.get("sea", {}).get("date", ""),
            "sourcing_urgency": sourcing_urgency,
            "notes": f"Importance: {f.get('importance', 'B')} | {len(f.get('products', []))} SKUs",
        })

    upcoming.sort(key=lambda x: x["days_until"])
    return upcoming


def get_seasonal_keywords():
    """Return search keywords relevant to the current season.

    Based on the current month and upcoming events in the next 30 days.
    Returns list of keyword strings suitable for Amazon AU / AnySearch.
    """
    today = datetime.now()
    month = today.month

    # Seasonal keyword map — 南半球季节 ⭐️ 澳洲：12-2月夏 / 3-5月秋 / 6-8月冬 / 9-11月春
    # 父亲节9月(第一个周日)、母亲节5月、Back to School 1月底(Term 1)、圣诞=盛夏海滩BBQ、EOFY 6月30
    # 关键词提前量对齐空运截止（节日前~45天开始扫描相关品类）
    seasonal = {
        1: ["back to school stationery", "lunch box", "desk organiser",
            "beach accessories", "summer toys"],
        2: ["valentine gift ideas", "romantic gift", "beach accessories",
            "outdoor water play", "summer picnic"],
        3: ["easter decoration", "autumn garden tools", "party supplies",
            "home decor", "kitchen gadgets"],
        4: ["autumn decor", "garden accessories", "easter decoration",
            "warm home textiles", "cleaning supplies"],
        5: ["mothers day gift", "autumn garden tools", "winter warmers",
            "candles", "home comfort"],
        6: ["winter warmers", "blanket throw", "indoor games",
            "hot water bottle cover", "eofy storage solutions"],
        7: ["fathers day gift", "winter indoor activities",
            "school holiday toys", "puzzle board game", "car care winter"],
        8: ["fathers day gift", "spring cleaning tools", "garden tools",
            "bbq accessories prep", "pet grooming shedding"],
        9: ["fathers day gift", "spring garden", "pet hair remover",
            "outdoor dining", "bbq grill mat"],
        10: ["spring garden", "outdoor living", "halloween decoration",
             "bbq accessories", "picnic items"],
        11: ["christmas gifts", "stocking fillers", "summer outdoor toys",
             "black friday deals", "beach accessories"],
        12: ["christmas gifts", "stocking fillers", "beach accessories",
             "bbq tools", "post-christmas storage organiser"],
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
