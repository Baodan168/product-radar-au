"""评分引擎回归：信号分类（含 Ozbargain 兼容旧数据）、信号置信度、评分主流程。"""
import sys
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from scoring_engine import (
    _classify_signal_sources,
    _get_signal_confidence,
    _has_demand_signal,
    score_all_products,
)


def test_classify_internal_vs_external():
    p = {"channel": "new_releases", "sources": ["TikTok趋势", "Ozbargain折扣"]}
    internal, external, ext_count = _classify_signal_sources(p)
    assert "新品榜" in internal
    assert "TikTok" in external and "Ozbargain" in external
    assert ext_count == 2


def test_classify_ozbargain_legacy_hotukdeals_tag():
    # 2026-08-29 前（UK 残留时期）入库的历史数据带 HotUKDeals热帖 标签，仍应计数
    p = {"channel": "bsr", "sources": ["HotUKDeals热帖"]}
    _, external, ext_count = _classify_signal_sources(p)
    assert "Ozbargain" in external
    assert ext_count == 1


def test_signal_confidence_levels():
    assert _get_signal_confidence(["新品榜"], 3)[0] == "strong"
    assert _get_signal_confidence(["新品榜"], 2)[0] == "medium"
    assert _get_signal_confidence(["新品榜"], 1)[0] == "weak"
    assert _get_signal_confidence(["新品榜"], 0)[1] == "⚪ 仅Amazon"
    assert _get_signal_confidence([], 0)[1] == "⚪ 无信号"


def test_demand_signal_requires_external():
    assert _has_demand_signal({"channel": "new_releases", "sources": []}) is False
    assert _has_demand_signal({"channel": "bsr", "sources": ["Temu热销"]}) is True


def test_score_all_products_smoke():
    products = [{
        "asin": "B0SCORE0001", "name": "Silicone Basting Brush", "category": "Kitchen",
        "price": 12.99, "reviews": 25, "rating": 4.6, "profit_margin": 0.4,
        "channel": "new_releases", "sources": ["TikTok趋势", "Ozbargain折扣", "Reddit需求"],
    }]
    out = score_all_products(products, trend_data=None, history=None)
    assert out[0]["score"] > 0
    assert "score_breakdown" in out[0] and out[0]["stars"] >= 3
    # 新品榜 + 多外部信号 → 分数应高于仅有 Amazon 内部信号的同款
    lonely = dict(out[0], asin="B0SCORE0002", sources=[])
    out2 = score_all_products([lonely])
    assert out2[0]["score"] < out[0]["score"]


def test_score_all_products_empty():
    assert score_all_products([]) == []
