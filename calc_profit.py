#!/usr/bin/env python3
"""统一利润计算(AU版) — 选品雷达和选品发现共用
用法: python3 calc_profit.py <price_aud> [category]
输出: JSON格式的利润明细
成本结构来自 config.json cost_structure（GST 10% / 佣金13-15% / FBA A$4.2起）
"""
import json, sys
from pathlib import Path

CONFIG = json.loads((Path(__file__).parent / 'config.json').read_text(encoding='utf-8'))

def calc_profit(price_aud, category="general", sourcing_aud=None):
    """Calculate profit for a given AUD price.

    Args:
        price_aud: Amazon AU selling price in AUD
        category: product category (affects commission rate)
        sourcing_aud: actual sourcing cost in AUD (if None, uses config default)
    """
    c = CONFIG["cost_structure"]
    comm_rate = c["commission_rate"]
    cat_lower = category.lower()
    if "home" in cat_lower or "kitchen" in cat_lower:
        comm_rate = c["commission_home"]
    elif "pet" in cat_lower:
        comm_rate = c["commission_pets"]

    # 2026-08-26 Lee调整：不计广告、退货、GST（运营端消化，雷达只看硬成本）
    commission = price_aud * comm_rate
    fba = c["fba_small_standard"]
    sourcing = sourcing_aud if sourcing_aud is not None else c.get("sourcing_cost", 1.30)

    total_cost = commission + fba + sourcing
    net_profit = price_aud - total_cost
    margin = net_profit / price_aud if price_aud > 0 else 0

    return {
        "net_profit": round(net_profit, 2),
        "margin": round(margin, 3),
        "margin_pct": f"{margin*100:.1f}%",
        "breakdown": {
            "commission": round(commission, 2),
            "fba": fba,
            "sourcing": round(sourcing, 2),
            "total_cost": round(total_cost, 2),
        }
    }


if __name__ == "__main__":
    price = float(sys.argv[1]) if len(sys.argv) > 1 else 18.00
    category = sys.argv[2] if len(sys.argv) > 2 else "general"
    result = calc_profit(price, category)
    print(json.dumps(result, ensure_ascii=False, indent=2))
