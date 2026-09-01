#!/usr/bin/env python3
"""月度 rejected 分析报告 — 2026-08-26 新增 cron, 2026-09-01 重构

数据源: data/channels/*-rejected.json（仓库根，非 scripts/data/）

2026-09-01 修复:
1. DATA_DIR 路径错误（scripts/data/channels → data/channels），此前报告恒为 0 条
2. 禁选词截断 bug：正则 '禁选:\\s*(.+?)(?:\\s|\\()' 把 'cat food' 截成 'cat'
3. 误杀判定改为用当前 scanner.is_forbidden 真实重判（旧逻辑查自家硬编码豁免表副本，
   key 与 scanner.py 不一致且把 cat litter/dog treat 等正确拦截标成"疑似误杀"）

输出: data/reports/rejected_analysis_YYYY-MM-DD.md
"""
import json
import re
import sys
import datetime
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).parent
DATA_DIR = BASE.parent / "data" / "channels"
sys.path.insert(0, str(BASE.parent))
from scanner import is_forbidden  # noqa: E402


def collect_rejected(days=30):
    """收集最近 N 天的 rejected 数据（文件名含日期，天然按天去重来源）"""
    rejected = []
    for f in sorted(DATA_DIR.glob("*-rejected.json")):
        try:
            for r in json.load(open(f)):
                r["_date"] = f.name[:10]
                rejected.append(r)
        except Exception:
            pass
    return rejected


def analyze(rejected):
    """分析 rejected 数据。误杀判定 = 用当前 scanner 重判，真放行才算误杀"""
    kw_counts = Counter()          # 禁选词 → 命中次数（含跨天重复）
    kw_products = defaultdict(set)  # 禁选词 → 去重产品名
    type_counts = Counter()        # 拦截类型分布
    misfires = {}                  # name → {kw, date, count} 当前scanner会放行的历史拦截
    suspect_incomplete = 0         # 截断名不可判定（触发词不在可见名内）
    suspect_by_kw = Counter()      # 存疑条目的关键词分布

    for r in rejected:
        name = r.get("name", "")
        reason = r.get("reason", "")

        # 拦截类型分布
        if "多件套装" in reason:
            type_counts["多件套装(≥5件)"] += 1
        elif reason.startswith("禁选:"):
            type_counts["禁选词"] += 1
        elif reason.startswith("大牌:"):
            type_counts["大牌"] += 1
        elif "红海" in reason:
            type_counts["评论过多(红海)"] += 1
        elif "无验证" in reason:
            type_counts["评论过少"] += 1
        elif "评分" in reason:
            type_counts["评分低"] += 1
        elif "不在区间" in reason:
            type_counts["价格区间外"] += 1
        elif "利润率" in reason:
            type_counts["利润率<20%"] += 1
        elif reason.startswith("oversize:"):
            type_counts["oversize(超大体积)"] += 1
        elif "体积" in reason or "重量" in reason or "包装尺寸" in reason:
            type_counts["体积/重量/尺寸超标"] += 1
        else:
            type_counts["其他"] += 1

        # 禁选词完整统计（reason 形如 "禁选: cat food"）
        if reason.startswith("禁选:"):
            kw = reason[3:].strip()
            if kw:
                kw_counts[kw] += 1
                kw_products[kw].add(name)

        # 误杀重判：只对禁选词拦截做（当前 scanner 放行 = 历史误杀/规则已放宽）
        # 注：2026-09-01 前 rejected.json 的 name 截断到 60 字符。若触发词/token
        # 不在可见名内，重判放行可能是截断假象 → 计入存疑，不算可靠误杀
        if reason.startswith("禁选:") and name:
            kw = reason[3:].strip()
            nl = name.lower().replace(" ", "")
            if kw.startswith("多件套装"):
                m = re.search(r"(\d+)pcs", kw)
                token_ok = bool(m) and bool(re.search(
                    rf"{m.group(1)}\s*-?\s*(pack|pcs|piece|件|个|片|套)", name.lower()))
            elif kw.startswith(("体积", "重量", "包装尺寸")):
                m = re.search(r"([\d.]+\s*[kKmM]?[lLgG]|[\dx*×]+cm)", kw)
                token_ok = bool(m) and m.group(1).replace(" ", "").lower() in nl
            elif kw.startswith("oversize"):
                token_ok = False  # 触发标记词不在 reason 里，无法验证，保守计入存疑
            else:
                token_ok = kw.replace(" ", "").lower() in nl
            if not token_ok:
                suspect_incomplete += 1  # 触发词不可见，判定不可靠，单列
                suspect_by_kw[kw.split(" (")[0]] += 1
                continue
            try:
                ok, _now = is_forbidden(name)
            except Exception:
                ok = True  # 判定失败按仍拦截处理，不误报
            if not ok:
                if name not in misfires:
                    misfires[name] = {"kw": kw, "date": r["_date"], "count": 0}
                misfires[name]["count"] += 1

    return {
        "total": len(rejected),
        "kw_counts": kw_counts,
        "kw_products": kw_products,
        "type_counts": type_counts,
        "misfires": misfires,
        "suspect_incomplete": suspect_incomplete,
        "suspect_by_kw": suspect_by_kw,
    }


def generate_report(stats, output_path):
    """生成 Markdown 报告"""
    lines = [
        "# 选品雷达 Rejected 分析报告",
        f"\n**生成时间**: {stats.get('generated_at', 'N/A')}",
        f"**分析样本**: {stats['total']} 条 rejected\n",
        "## 一、拦截类型分布",
        "",
        "| 拦截类型 | 次数 |",
        "|---------|-----|",
    ]
    for t, n in stats["type_counts"].most_common():
        lines.append(f"| {t} | {n} |")

    lines.extend([
        "",
        "## 二、禁选词命中 Top 15（完整词）",
        "",
        "| 关键词 | 命中次数 | 去重产品数 | 样本产品 |",
        "|--------|---------|-----------|----------|",
    ])
    for kw, count in stats["kw_counts"].most_common(15):
        prods = stats["kw_products"].get(kw, set())
        sample = sorted(prods)[0][:50] if prods else "-"
        lines.append(f"| {kw} | {count} | {len(prods)} | {sample} |")

    misfires = stats["misfires"]
    lines.extend([
        "",
        "## 三、疑似误杀（当前 scanner 重判会放行）",
        "",
        f"共 {len(misfires)} 个去重产品（另有 {stats.get('suspect_incomplete', 0)} 条因历史数据",
        "名称截断60字符无法可靠重判，已剔除；存疑分布: " + ", ".join(
            f"`{k}`×{v}" for k, v in stats.get("suspect_by_kw", {}).most_common(8)) + "）。",
        "豁免部署(08-26)前的历史拦截，现规则已放行；高频重复出现的模式可考虑新增语境豁免：",
        "",
        "| 历史禁选词 | 首次日期 | 重复次数 | 产品名 |",
        "|-----------|---------|---------|--------|",
    ])
    for name, info in sorted(misfires.items(), key=lambda x: -x[1]["count"])[:15]:
        lines.append(f"| {info['kw']} | {info['date']} | {info['count']} | {name[:50]} |")

    # 豁免建议：按历史禁选词分组误杀
    mf_by_kw = defaultdict(list)
    for name, info in misfires.items():
        mf_by_kw[info["kw"]].append(name)
    lines.extend([
        "",
        "## 四、豁免建议（按误杀模式分组）",
        "",
    ])
    if mf_by_kw:
        for kw, names in sorted(mf_by_kw.items(), key=lambda x: -len(x[1])):
            lines.append(f"- `{kw}` 误杀 {len(names)} 个产品，如: {sorted(names)[0][:45]}")
    else:
        lines.append("暂无新豁免建议（当前规则未发现误杀）")

    lines.extend(["", "---", "*报告由 rejected_analysis.py 自动生成（误杀判定=当前scanner重判）*"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


if __name__ == "__main__":
    rejected = collect_rejected()
    stats = analyze(rejected)
    stats["generated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    report_path = DATA_DIR.parent / "reports" / f"rejected_analysis_{datetime.date.today()}.md"
    report = generate_report(stats, report_path)

    print(f"分析完成: {stats['total']} 条 rejected")
    print(f"报告已保存: {report_path}")
    print("\n" + report[:1500])
