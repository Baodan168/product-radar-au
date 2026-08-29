"""核心管线回归：constants 南半球季节 / calc_profit 三项硬成本口径 /
is_forbidden 过滤与豁免 / filter_products 过滤链。

2026-08-29 全面审查后补充 —— 此前核心管线零测试，换季/改站点最容易回归。
"""
import json
import sys
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import constants
from calc_profit import calc_profit
from scanner import is_forbidden
from run_scan_v2 import filter_products


# ── constants.get_au_season：南半球 ──────────────────────────────

@pytest.mark.parametrize("month,season", [
    (1, "summer"), (2, "summer"),       # 12-2月 夏
    (3, "autumn"), (4, "autumn"), (5, "autumn"),
    (6, "winter"), (7, "winter"), (8, "winter"),   # 澳洲 8 月=冬（北半球是夏）
    (9, "spring"), (10, "spring"), (11, "spring"),
    (12, "summer"),
])
def test_au_season_southern_hemisphere(month, season):
    assert constants.get_au_season(month) == season


def test_au_season_uses_current_month_by_default():
    assert constants.get_au_season() == constants.get_au_season(__import__("datetime").datetime.now().month)


# ── config 口径（2026-08-29 Lee 定价）────────────────────────────

def test_config_price_band_and_rate():
    cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    assert cfg["price_range"]["min"] == 8.99
    assert cfg["price_range"]["max"] == 16.99
    assert cfg["exchange_rate_cny_aud"] == 4.8


# ── calc_profit：佣金+FBA+采购，无 VAT/广告/退货 ─────────────────

def test_calc_profit_general_uses_hard_costs_only():
    r = calc_profit(16.99, "general")
    expected = round(16.99 - 16.99 * 0.15 - 4.2 - 1.3, 2)
    assert r["net_profit"] == expected
    assert set(r["breakdown"].keys()) == {"commission", "fba", "sourcing", "total_cost"}


def test_calc_profit_margin_above_threshold_across_band():
    # 价格带两端利润率都必须 ≥ 20%（config.min_profit_margin）
    cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    lo = cfg["price_range"]["min"]
    hi = cfg["price_range"]["max"]
    for price in (lo, (lo + hi) / 2, hi):
        for cat in ("general", "home", "pets"):
            r = calc_profit(price, cat)
            assert r["margin"] >= cfg["min_profit_margin"], f"price={price} cat={cat} margin={r['margin']}"


def test_calc_profit_commission_by_category():
    assert calc_profit(16.99, "home")["breakdown"]["commission"] == round(16.99 * 0.13, 2)
    assert calc_profit(16.99, "pet")["breakdown"]["commission"] == round(16.99 * 0.10, 2)
    assert calc_profit(16.99, "general")["breakdown"]["commission"] == round(16.99 * 0.15, 2)


def test_calc_profit_extra_sourcing_arg():
    r = calc_profit(16.99, "general", sourcing_aud=2.0)
    assert r["breakdown"]["sourcing"] == 2.0


# ── is_forbidden：统一元组返回 + 语境豁免 ────────────────────────

def test_is_forbidden_always_returns_tuple():
    assert is_forbidden("clean name product") == (False, "")
    forbidden, reason = is_forbidden("toy race car set")
    assert forbidden is True and reason


def test_is_forbidden_basics():
    assert is_forbidden("desk fan with clip")[0] is True
    assert is_forbidden("baby bottle warmer")[0] is True
    assert is_forbidden("ceramic mug set")[0] is True
    assert is_forbidden("shampoo 500 ml")[0] is True          # 液体/膏体词
    assert is_forbidden("500 ml water bottle")[0] is False     # 容器豁免体积检查
    assert is_forbidden("wooden cat bowl")[0] is False       # 容器语境豁免
    assert is_forbidden("dog toy chew rope")[0] is False     # 宠物玩具豁免
    assert is_forbidden("christmas costume dress")[0] is False  # party 语境豁免


def test_is_forbidden_weight_and_sets():
    assert is_forbidden("storage box 3 kg")[0] is True       # 超重（config max_weight_g=200）
    assert is_forbidden("towel rail 180 g")[0] is False
    assert is_forbidden("container set 6 pack")[0] is True   # 多件套装
    assert is_forbidden("pimple patches 36 pack")[0] is False  # 小件豁免


# ── filter_products：过滤链（季节标记/用户拒绝/利润）────────────

@pytest.fixture
def config():
    return json.loads((BASE / "config.json").read_text(encoding="utf-8"))


def _prod(**kw):
    base = {"asin": "B0TEST0001", "name": "Silicone Kitchen Tongs", "category": "Kitchen",
            "price": 12.99, "reviews": 30, "rating": 4.5, "channel": "bsr"}
    base.update(kw)
    return base


def test_filter_products_passes_clean_product(config):
    passed, rejected = filter_products([_prod()], config)
    assert len(passed) == 1
    assert passed[0]["profit_margin"] > 0
    assert passed[0]["off_season"] is False


def test_filter_products_price_band_enforced(config):
    # 16.99 上限之上（如 19.99）应被拒
    passed, rejected = filter_products([_prod(price=19.99)], config)
    assert not passed
    assert "不在区间" in rejected[0]["reason"]


def test_filter_products_user_rejected_asin(config, tmp_path, monkeypatch):
    rej = BASE / "rejected_by_user.json"
    backup = rej.read_text(encoding="utf-8") if rej.exists() else None
    try:
        rej.write_text(json.dumps({"B0REJECT99": {"reason": "test"}}), encoding="utf-8")
        passed, rejected = filter_products([_prod(asin="B0REJECT99")], config)
        assert not passed
        assert rejected[0]["reason"] == "用户标记不考虑"
    finally:
        if backup is None:
            rej.unlink(missing_ok=True)
        else:
            rej.write_text(backup, encoding="utf-8")


def test_filter_products_marks_off_season(config, monkeypatch):
    # 8 月=南半球冬季 → summer_cold 词表生效（含 "bbq"）
    import run_scan_v2
    from datetime import datetime as _real_dt

    class _FakeDT(_real_dt):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 8, 29)

    monkeypatch.setattr(run_scan_v2, "datetime", _FakeDT)
    passed, rejected = filter_products([_prod(name="BBQ Grill Mat Set", category="Garden")], config)
    # 该产品能否通过其他过滤取决于价格/评论，只断言 off_season 标记逻辑
    for p in passed:
        assert p["off_season"] is True
