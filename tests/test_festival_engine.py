"""节日引擎回归：AU 节日库加载、物流倒计时、紧迫度。

节日库是选品决策的时间骨架（海运 63 天倒计时），改错一天 = 错过一季。
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from festival_engine import (
    LOGISTICS_MODES,
    get_deadlines,
    get_urgency,
    load_festivals,
)


@pytest.fixture(scope="module")
def festivals():
    fs = load_festivals()
    assert fs, "节日库加载失败：data/au_festivals_data.js 不可读或为空"
    return fs


def test_festival_library_size(festivals):
    # 与 CLAUDE.md 声称的规模一致（40 事件 136 SKU）
    assert len(festivals) >= 35
    sku_count = sum(len(f.get("products", [])) for f in festivals)
    assert sku_count >= 120


def test_festival_dates_parseable_and_au_specific(festivals):
    names = " ".join(f.get("name", "") for f in festivals)
    for f in festivals:
        datetime.strptime(f["date"], "%Y-%m-%d")  # 日期格式统一
    # AU 专属节点必须在场（UK 库没有的）
    joined = names.lower()
    for must in ("eofy", "返校", "父亲节"):
        assert must in joined or any(must in (f.get("name") or "").lower() for f in festivals)


def test_deadlines_ordering_sea_longest():
    f = {"date": (datetime.now() + timedelta(days=200)).strftime("%Y-%m-%d")}
    d = get_deadlines(f)
    assert d["sea"]["days_from_today"] < d["truck"]["days_from_today"] < d["air"]["days_from_today"]
    # 海运提前期 = 63 天（leadTime）+14 缓冲口径
    assert LOGISTICS_MODES["sea"]["leadTime"] == 63


def test_urgency_lifecycle():
    far = {"date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")}
    assert get_urgency(far, "sea") == "plan"
    past = {"date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")}
    assert get_urgency(past, "sea") == "past"
    tomorrow = {"date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")}
    assert get_urgency(tomorrow, "sea") == "urgent"  # 海运窗口(63+14天)早已关闭
