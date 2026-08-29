#!/usr/bin/env python3
"""Google Trends Australia demand signal fetcher - extracts trending keywords"""
import json, subprocess, re, sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE))

from constants import get_au_season

ANYSEARCH = str(Path.home() / ".hermes/skills/search/anysearch/scripts/anysearch_cli.py")


def _run_anysearch(query, domain="web", max_results=5):
    try:
        result = subprocess.run(
            ["python3", ANYSEARCH, "search", query,
             "--domain", domain, "--max_results", str(max_results), "--zone", "intl"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception as e:
        print(f"  AnySearch error: {e}", file=sys.stderr)
    return ""


def fetch_demand_signals():
    """Fetch Google Trends Australia rising product categories.

    季节/年份动态生成（2026-08-29 修复：原查询硬编码错季词+固定年份，  # site-check: allow
    南半球 8 月实为冬季，抓回来的是错季信号；且跨年即过期）。
    """
    now = datetime.now()
    season = get_au_season(now.month)
    year = now.year

    queries = [
        f"Google Trends Australia trending products rising {season} {year}",
        f"Australia consumer trending products {season} {year} popular",
        f"trending products Australia {season} {year} what people buying",
    ]

    signals = []
    for q in queries:
        print(f"  Google Trends: {q[:50]}...", file=sys.stderr)
        text = _run_anysearch(q, domain="ecommerce")
        if text:
            signals.append(text)

    combined = "\n".join(signals)
    print(f"  Google Trends signals: {len(combined)} chars", file=sys.stderr)
    return combined


# 全年通用品类词（与季节无关的需求）
_SHARED_TREND_WORDS = [
    'storage', 'organizer', 'organisation', 'cleaning', 'kitchen', 'bathroom',
    'fitness', 'yoga', 'exercise', 'sport', 'cycling',
    'festival', 'party', 'decoration', 'led', 'solar',
    'phone holder', 'car accessory', 'phone mount',
    'pet', 'gift',
]

# 南半球夏季热词（12-2月；春季提前布局）
_SUMMER_TREND_WORDS = [
    'garden', 'outdoor', 'bbq', 'camping', 'travel', 'beach', 'picnic',
    'summer', 'cooling', 'water bottle', 'sunglasses', 'sun',
    'pool', 'inflatable', 'swim', 'towel',
    'barbecue', 'grill', 'patio', 'fence',
    'hose', 'sprinkler', 'lawn', 'mower',
    'tent', 'sleeping bag', 'backpack',
]

# 南半球冬季热词（6-8月；秋季提前布局）
_WINTER_TREND_WORDS = [
    'winter', 'warm', 'heating', 'thermal', 'fleece', 'wool', 'knit',
    'blanket', 'throw', 'cushion', 'puzzle', 'board game', 'indoor',
    'hot water bottle', 'insulated', 'soup', 'socks', 'slipper',
]


def extract_trending_keywords(signals_text, season=None):
    """Extract trending product keywords from Google Trends signals.

    词表按南半球季节切换：夏季/春季→夏季词表，冬季/秋季→冬季词表
    （零售商提前一个季节备货，故春季看夏季、秋季看冬季）。
    """
    if not signals_text:
        return []

    if season is None:
        season = get_au_season()
    if season in ("summer", "spring"):
        trend_words = _SHARED_TREND_WORDS + _SUMMER_TREND_WORDS
    else:
        trend_words = _SHARED_TREND_WORDS + _WINTER_TREND_WORDS

    keywords = []
    text_lower = signals_text.lower()
    for word in trend_words:
        if word in text_lower:
            keywords.append(word)

    return list(set(keywords))[:20]
