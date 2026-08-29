#!/usr/bin/env python3
"""Product Radar AU - Core utilities
Provides: is_forbidden (keyword/category filter), calc_profit (re-export from calc_profit.py).
Scoring is handled by scoring_engine.py.
"""
import json, os, sys, re
from pathlib import Path

from calc_profit import calc_profit as _calc_profit  # 单一利润实现，禁止在本文件重写

BASE = Path(__file__).parent
CONFIG = json.loads((BASE / "config.json").read_text())


def is_forbidden(name, category=""):
    """Check if product matches forbidden categories."""
    text = (name + " " + category).lower()

    # --- Shared keyword sets ---
    PET_KEYWORDS = {'cat', 'dog', 'pet', 'kitten', 'puppy', 'ferret', 'rabbit', 'hamster', 'catnip', 'silvervine'}
    PARTY_KEYWORDS = {'party', 'decoration', 'costume', 'pirate', 'halloween', 'christmas', 'birthday', 'fancy dress', 'bachelorette', 'wedding'}
    PARTY_EXEMPT_KW = {'kids', 'dress', 'shirt', 'children', 'trousers'}  # clothing keywords exempted when party context

    # 2026-08-26 语境豁免：某些禁选词在特定容器/配件语境下是安全的
    # 数据驱动：rejected 数据命中 'cat'(2次)、'plug'(2次)、'light'(13次)
    # 其中 cat bowls/harness buckles 是容器/配件，不应被 'cat'/'buckle' 拦截
    # 注意：豁免表 key 必须与 CONFIG["forbidden_keywords"] 中的实际条目匹配
    CONTEXT_EXEMPTIONS = {
        # (禁选词, 豁免语境词) → 含豁免语境时跳过该禁选词
        'cat food': ('bowl', 'feeder', 'litter', 'tree', 'nip', 'collar', 'harness'),  # 猫用品≠猫粮
        'plug in': ('night', 'sensor', 'hook', 'adapter'),  # 墙面插件夜灯≠电源线
        'lighting': ('bulb', 'projector', 'switch', 'strand', 'night', 'outdoor'),  # LED灯泡/串灯/夜灯/户外灯≠灯具整机
        'light': ('bulb', 'projector', 'switch', 'strand', 'night', 'outdoor'),  # 同上
        'sensor': ('night', 'light', 'motion'),  # 感应夜灯≠安防设备
        'usb powered': ('hub', 'adapter', 'cable'),  # USB集线器≠电子产品
    }

    has_party = any(kw in text for kw in PARTY_KEYWORDS)

    # --- Special handling: "toy" ---
    has_toy = bool(re.search(r'(?<![a-z])toy(?:s)?(?![a-z])', text))
    if has_toy:
        has_pet = any(re.search(r'(?<![a-z])' + re.escape(kw) + r'(?![a-z])', text) for kw in PET_KEYWORDS)
        if not has_pet and not has_party:
            return True, "toy (非宠物/节日)"

    # --- Oversized bathroom products (too large for FBA small standard) ---
    OVERSIZE_HINTS = {'large capacity', 'extra large', '6 slot', '6 slots', '7 slot', '7 slots',
                      '8 slot', '8 slots', '9 slot', '9 slots', '10 slot', '10 slots',
                      'extra tall', 'super large', 'jumbo'}
    BATHROOM_HINTS = {'toothbrush', 'bathroom', 'shower', 'holder', 'organiser', 'organizer'}
    is_oversize_bathroom = (
        any(kw in text for kw in OVERSIZE_HINTS) and
        any(kw in text for kw in BATHROOM_HINTS)
    )

    # --- Main keyword loop ---
    for kw in CONFIG["forbidden_keywords"]:
        if kw == "toy":
            continue
        # Party exemption: skip clothing keywords for party/costume items
        if kw in PARTY_EXEMPT_KW and has_party:
            continue
        # Context exemption (2026-08-26): 检查是否在安全语境中
        exempt = False
        if kw in CONTEXT_EXEMPTIONS:
            for ctx in CONTEXT_EXEMPTIONS[kw]:
                if ctx in text:
                    exempt = True
                    break
        if exempt:
            continue
        # Oversize bathroom filter
        if kw == "electric" and is_oversize_bathroom:
            return True, f"oversize: {kw} + 体积过大"
        # Word-boundary matching
        pattern = r'(?<![a-z])' + re.escape(kw.strip()) + r'(?![a-z])' if kw.strip().isalpha() else re.escape(kw)
        if re.search(pattern, text):
            return True, kw

    # --- Volume/weight detection ---
    max_ml = 0
    max_l = 0
    max_weight_g = CONFIG.get("max_weight_g", 200)
    max_kg = max_weight_g / 1000
    CONTAINER_KEYWORDS = {'bottle', 'flask', 'tumbler', 'jug', 'carafe', 'pitcher', 'thermos', 'canteen', 'watering can'}
    is_container = any(kw in text for kw in CONTAINER_KEYWORDS)

    # --- Packaging dimension detection ---
    MAX_DIM = CONFIG.get("max_package_dimensions", {"l_cm": 32, "w_cm": 22, "h_cm": 6})
    MAX_L = MAX_DIM["l_cm"]
    MAX_W = MAX_DIM["w_cm"]
    MAX_H = MAX_DIM["h_cm"]
    # Match patterns like "32x22x6cm", "32×22×6 cm", "30 x 20 x 10 cm", "32*22*6cm"
    dim_match = re.search(
        r'(\d+(?:\.\d+)?)\s*[x×*]\s*(\d+(?:\.\d+)?)\s*[x×*]\s*(\d+(?:\.\d+)?)\s*(?:cm|mm)?',
        text
    )
    if dim_match:
        d1, d2, d3 = float(dim_match.group(1)), float(dim_match.group(2)), float(dim_match.group(3))
        # Assume mm values > 200 are likely mm not cm
        if d1 > 200: d1 /= 10
        if d2 > 200: d2 /= 10
        if d3 > 200: d3 /= 10
        dims = sorted([d1, d2, d3], reverse=True)
        if dims[0] > MAX_L or dims[1] > MAX_W or dims[2] > MAX_H:
            return True, f"包装尺寸 {d1:.0f}x{d2:.0f}x{d3:.0f}cm (限{MAX_L}x{MAX_W}x{MAX_H}cm)"

    # --- OVERSIZE HINTS (products likely too large for small standard) ---
    OVERSIZE_KEYWORDS = {
        'large capacity', 'extra large', 'super large', 'jumbo', 'x-large', 'xxl',
        'giant', 'massive', 'oversized', '6 slot', '6 slots', '7 slot', '7 slots',
        '8 slot', '8 slots', '9 slot', '9 slots', '10 slot', '10 slots',
    }
    if any(kw in text for kw in OVERSIZE_KEYWORDS):
        return True, f"oversize: 关键词标记为超大体积"

    # --- Multi-piece kit check (sets with 5+ pieces risk bulky packaging) ---
    # Exclude obviously small items (e.g. pimple patches 36/72 pack, baking mats 2 pack)
    SET_SMALL_EXEMPT = {'patch', 'sheet', 'strip', 'stick', 'bag', 'sachet', 'lining', 'mouse', 'mice', 'feather', 'rattle', 'ball', 'catnip', 'cat'}
    # 覆盖格式: N-Piece / N Piece / N Pack / N pcs / N件 / N Set（数字在前，允许连字符）
    # 注意: "4-in-1"/"N in 1" 是"多合一"非套装，不能误拦（'in' 不在关键词表内，天然安全）
    set_match = re.search(r'(\d+)\s*-?\s*(?:pack|piece|pcs|件|片|个|枚|套|set)[^a-z]', text)
    # 数字在后的格式: "Pack of 6" / "Set of 6"
    if not set_match:
        set_match = re.search(r'\b(?:pack|set)\s+of\s+(\d+)\b', text)
    if set_match:
        qty = int(set_match.group(1))
        if qty >= 5 and not any(s in text for s in SET_SMALL_EXEMPT):
            return True, f"多件套装 {qty}pcs (≥5件, 包装易超标)"

    if not is_container:
        vol_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:l\b|litre|litres|liter|liters)', text)
        if vol_match and float(vol_match.group(1)) > max_l:
            return True, f"体积 {vol_match.group(0)} (>{max_l*1000:.0f}ml)"
        ml_match = re.search(r'(\d+)\s*ml', text)
        if ml_match and int(ml_match.group(1)) > max_ml:
            return True, f"体积 {ml_match.group(0)} (>{max_ml}ml)"

    kg_match = re.search(r'(\d+(?:\.\d+)?)\s*kg', text)
    if kg_match and float(kg_match.group(1)) > max_kg:
        return True, f"重量 {kg_match.group(0)} (>{max_kg*1000:.0f}g)"
    g_match = re.search(r'(\d+)\s*(?:g\b|grams?)', text)
    if g_match and int(g_match.group(1)) > max_weight_g:
        return True, f"重量 {g_match.group(0)} (>{max_weight_g}g)"

    # 统一返回元组 (forbidden, reason)，调用方无需再做 isinstance 判断
    return False, ""


def calc_profit(price_aud, category="general"):
    # 2026-08-29 统一利润口径：实现收敛到 calc_profit.py，这里仅保留兼容转发
    return _calc_profit(price_aud, category)
