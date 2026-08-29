"""Shared constants for product-radar-au — single source of truth.

AU 专属口径（改动前先确认 Lee）：
- 货币 A$ (AUD)；CNY→AUD 汇率唯一来源 config.json 的 exchange_rate_cny_aud
- 利润模型只算 佣金+FBA+采购 三项硬成本（GST/广告/退货由运营端消化，2026-08-26 Lee 口径）
- 南半球季节：12-2月夏 / 3-5月秋 / 6-8月冬 / 9-11月春
"""

# Event keywords for filtering, limiting, and tagging
# Used by: run_scan_v2.py, scoring_engine.py, generate_platform.py

EVENT_KEYWORDS_SET = {
    'world cup', 'euro 2024', 'euro 2025', 'euro 2026',
    'olympic', 'olympics', 'jubilee', 'coronation',
    'christmas', 'halloween', 'easter', 'valentine',
    "mother's day", "father's day", 'black friday', 'prime day',
}

# Map keywords to event type groups (for limiting per-event counts)
# Used by: run_scan_v2.limit_event_products
EVENT_KEYWORDS_MAP = {
    'world cup': 'world_cup',
    'euro 2024': 'euro', 'euro 2025': 'euro', 'euro 2026': 'euro',
    'olympic': 'olympics', 'olympics': 'olympics',
    'jubilee': 'royal', 'coronation': 'royal',
    'christmas': 'christmas', 'halloween': 'halloween',
    'easter': 'easter', 'valentine': 'valentine',
    "mother's day": 'mothers_day', "father's day": 'fathers_day',
    'black friday': 'black_friday', 'prime day': 'prime_day',
}

# 简单成员判断（信号打标 / 事件过密降权），含子串词根
# Used by: run_scan_v2.assign_channel_tags, scoring_engine.score_all_products
EVENT_TAG_KEYWORDS = {
    'world cup', 'euro', 'olympic', 'olympics', 'jubilee', 'coronation',
    'christmas', 'halloween', 'easter', 'valentine',
}


def get_au_season(month=None):
    """南半球季节（AU）：12-2月夏 / 3-5月秋 / 6-8月冬 / 9-11月春。

    所有季节相关逻辑（过滤降权、趋势查询、评分）都必须走这里，
    禁止任何模块自己写 "7月=夏季" 的北半球假设。
    """
    from datetime import datetime as _dt
    m = month if month is not None else _dt.now().month
    if m in (12, 1, 2):
        return "summer"
    if m in (3, 4, 5):
        return "autumn"
    if m in (6, 7, 8):
        return "winter"
    return "spring"
