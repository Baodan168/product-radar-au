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


# Seasonal keyword map — 南半球季节 ⭐️ 澳洲：12-2月夏 / 3-5月秋 / 6-8月冬 / 9-11月春
# 父亲节9月(第一个周日)、母亲节5月、Back to School 1月底(Term 1)、圣诞=盛夏海滩BBQ、EOFY 6月30
# 关键词提前量对齐空运截止（节日前~45天开始扫描相关品类）
# 2026-08-28 提升为模块常量：festival_engine 的季节面板复用同一份月度词表，避免双份维护
# 2026-08-28 全面升级：基于 Amazon AU bestseller + Australia Post 电商报告 + Kmart 热点
# 每月关键词从5个扩展到8-10个，覆盖 AU 实际热销品类（宠物/BBQ/泳池/校园）
# 气候标注：N=北方(QLD/NT,全年暖), S=南方(VIC/TAS,分明四季), ALL=全国通用
MONTHLY_SEASONAL_KEYWORDS = {
        1: [  # 盛夏 + 开学季
            "back to school stationery", "lunch box organiser", "school bag accessories",
            "beach accessories", "portable neck fan", "pool maintenance",
            "summer picnic", "outdoor tableware"],
        2: [  # 盛夏尾 + 情人节
            "valentine gift ideas", "beach accessories", "pool cleaning tools",
            "outdoor water play", "summer picnic", "pet cooling mat",
            "portable fan", "bbq tableware"],
        3: [  # 入秋 + 复活节准备
            "easter decoration", "easter basket", "autumn garden tools",
            "party supplies", "home decor", "kitchen gadgets",
            "garden pruning tools", "pool cover"],
        4: [  # 秋季 + ANZAC Day
            "autumn decor", "garden accessories", "easter decoration",
            "anzac day commemorative", "warm home textiles", "cleaning supplies",
            "outdoor heating", "garden tools"],
        5: [  # 深秋 + 母亲节
            "mothers day gift", "mothers day personalized", "autumn garden tools",
            "winter warmers", "candles", "home comfort",
            "indoor heating", "warm bedding"],
        6: [  # 入冬 + EOFY
            "winter warmers", "thermal gloves", "heated blanket",
            "indoor games", "hot water bottle cover", "eofy storage solutions",
            "winter accessories", "door draft stopper"],
        7: [  # 深冬 + 学校假期
            "winter indoor activities", "heated blanket", "school holiday toys",
            "puzzle board game", "car care winter", "thermal accessories",
            "winter warmers", "indoor heating"],
        8: [  # 冬尾 + 父亲节准备
            "fathers day gift", "spring cleaning tools", "garden tools",
            "bbq accessories prep", "pet grooming shedding", "winter warmers",
            "thermal gloves", "door draft stopper"],
        9: [  # 入春 + 父亲节
            "fathers day gift", "spring garden", "pet hair remover",
            "pet cooling mat", "outdoor dining", "bbq grill mat",
            "bbq cleaner brush", "pool maintenance kit"],
        10: [  # 春季 + 万圣节
            "spring garden", "outdoor living", "halloween decoration",
            "bbq accessories", "picnic items", "pet cooling mat",
            "pool cleaning tools", "garden tools"],
        11: [  # 春尾 + Click Frenzy + 圣诞准备
            "christmas gifts", "stocking fillers", "summer outdoor toys",
            "black friday deals", "beach accessories", "click frenzy deals",
            "pool accessories", "portable neck fan"],
        12: [  # 盛夏 + 圣诞
            "christmas gifts", "stocking fillers", "beach accessories",
            "bbq tools", "post-christmas storage organiser", "pool maintenance",
            "portable neck fan", "outdoor tableware"],
    }


def get_seasonal_keywords():
    """Return search keywords relevant to the current season.

    Based on the current month and upcoming events in the next 30 days.
    Returns list of keyword strings suitable for Amazon AU / AnySearch.
    """
    today = datetime.now()
    month = today.month

    keywords = list(MONTHLY_SEASONAL_KEYWORDS.get(month, ["kitchen accessories", "home gadgets"]))

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


# ── 季节品 47 天空运倒计时（2026-08-28）──
# 季节品不像节日有固定日期，按"季节首日"前 47 天开始预警
# 返回每个季节的空运截止日 + 倒计时天数 + 紧急度
SEASON_AIR_FREIGHT_LEAD = 47  # 空运备货提前天数

# 区域气候标签：N=北方(QLD/NT全年暖), S=南方(VIC/TAS四季分明), ALL=全国
SEASON_REGION_TAGS = {
    "spring": {"months": (9, 10, 11), "north": "延后1月(10-12月才真春)", "south": "9-11月标准春"},
    "summer": {"months": (12, 1, 2), "north": "全年皆夏(QLD/NT)", "south": "12-2月标准夏"},
    "autumn": {"months": (3, 4, 5), "north": "3-5月微凉", "south": "3-5月标准秋"},
    "winter": {"months": (6, 7, 8), "north": "6-8月温和(15-25°C)", "south": "6-8月寒冷(5-15°C)"},
}


def get_seasonal_sourcing_alert():
    """返回当前季节的备货倒计时信息。
    
    按季节首日计算：如果当前在季节内，算下一个季节的倒计时；
    如果在季节交替前47天内，当前季节品已进入"最后空运窗口"。
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    month = today.month
    
    # 南半球季节映射
    _season_map = {9: "spring", 10: "spring", 11: "spring",
                   12: "summer", 1: "summer", 2: "summer",
                   3: "autumn", 4: "autumn", 5: "autumn",
                   6: "winter", 7: "winter", 8: "winter"}
    _season_months = {"spring": (9, 10, 11), "summer": (12, 1, 2),
                      "autumn": (3, 4, 5), "winter": (6, 7, 8)}
    _season_order = ["spring", "summer", "autumn", "winter"]
    
    cur_season = _season_map.get(month)
    if cur_season:
        cur_idx = _season_order.index(cur_season)
        next_season = _season_order[(cur_idx + 1) % 4]
    else:
        next_season = "spring"
    
    next_months = _season_months[next_season]
    next_month_1st = next_months[0]
    
    # 计算下一季节首日
    if next_month_1st == 1 and month >= 11:
        year = today.year + 1
    elif next_month_1st > month:
        year = today.year
    else:
        year = today.year + 1
    
    season_start = datetime(year, next_month_1st, 1)
    air_deadline = season_start - timedelta(days=SEASON_AIR_FREIGHT_LEAD)
    days_to_deadline = (air_deadline - today).days
    
    if days_to_deadline < 0:
        urgency = "OVERDUE"
    elif days_to_deadline <= 7:
        urgency = "URGENT"
    elif days_to_deadline <= 21:
        urgency = "AIR_ONLY"
    elif days_to_deadline <= 47:
        urgency = "PLAN"
    else:
        urgency = "OK"
    
    return {
        "next_season": next_season,
        "season_start": season_start.strftime("%Y-%m-%d"),
        "air_deadline": air_deadline.strftime("%Y-%m-%d"),
        "days_to_deadline": days_to_deadline,
        "urgency": urgency,
        "current_month_keywords": MONTHLY_SEASONAL_KEYWORDS.get(month, []),
    }


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
