#!/usr/bin/env python3
"""月度 rejected 分析报告 — 2026-08-26 新增 cron

从近30天 rejected.json 中统计：
1. 禁选词命中 Top 20
2. 疑似误杀（安全语境命中）
3. 建议豁免词清单

输出: data/reports/rejected_analysis_YYYY-MM-DD.md
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).parent
DATA_DIR = BASE / "data" / "channels"

def collect_rejected(days=30):
    """收集最近 N 天的 rejected 数据"""
    rejected = []
    # 按时间排序取最近文件
    files = sorted(DATA_DIR.glob("*-rejected.json"))
    for f in files[-50:]:  # 最多取50个文件
        try:
            d = json.load(open(f))
            rejected.extend(d)
        except Exception:
            pass
    return rejected


def analyze(rejected):
    """分析 rejected 数据，返回统计结果"""
    kw_counts = Counter()
    kw_samples = defaultdict(list)
    context_hits = []  # 可能误杀的样本

    # 语境豁免表（与 scanner.py 一致）
    CONTEXT_EXEMPTIONS = {
        'cat': ('bowl', 'feeder', 'litter', 'tree', 'nip', 'collar', 'harness'),
        'plug': ('hook', 'adapter', 'hanger', 'in night'),
        'light': ('bulb', 'projector', 'hook', 'holder', 'switch'),
        'battery': ('powered',),
    }

    for r in rejected:
        name = r.get('name', '')
        reason = r.get('reason', '')

        # 统计禁选词
        m = re.search(r'禁选:\s*(.+?)(?:\s|\()', reason)
        if m:
            kw = m.group(1).strip().lower()
            kw_counts[kw] += 1
            kw_samples[kw].append(name[:60])

        # 检查语境豁免命中（潜在误杀）
        for kw, contexts in CONTEXT_EXEMPTIONS.items():
            if kw in reason.lower():
                for ctx in contexts:
                    if ctx in name.lower():
                        context_hits.append({
                            'kw': kw,
                            'ctx': ctx,
                            'name': name,
                            'reason': reason
                        })
                        break

    return {
        'total': len(rejected),
        'kw_counts': kw_counts,
        'kw_samples': kw_samples,
        'context_hits': context_hits,
    }


def generate_report(stats, output_path):
    """生成 Markdown 报告"""
    lines = [
        "# 选品雷达 Rejected 分析报告",
        f"\n**生成时间**: {stats.get('generated_at', 'N/A')}",
        f"**分析样本**: {stats['total']} 条 rejected\n",
        "## 一、禁选词命中 Top 20",
        "",
        "| 关键词 | 命中次数 | 样本产品 |",
        "|--------|---------|----------|",
    ]

    for kw, count in stats['kw_counts'].most_common(20):
        samples = stats['kw_samples'].get(kw, [])[:1]
        sample = samples[0] if samples else "-"
        lines.append(f"| {kw} | {count} | {sample} |")

    lines.extend([
        "",
        "## 二、疑似误杀（语境豁免命中）",
        "",
        "以下产品在安全语境中命中禁选词，建议加入豁免表：",
        "",
        "| 禁选词 | 豁免语境 | 产品名 |",
        "|--------|---------|--------|",
    ])

    for hit in stats.get('context_hits', [])[:15]:
        lines.append(f"| {hit['kw']} | {hit['ctx']} | {hit['name'][:50]} |")

    lines.extend([
        "",
        "## 三、建议豁免词",
        "",
        "基于数据分析，建议添加以下语境豁免：",
        "",
    ])

    # 统计哪些豁免已生效
    already_exempt = set()
    for hit in stats.get('context_hits', []):
        already_exempt.add(f"{hit['kw']}:{hit['ctx']}")

    if already_exempt:
        lines.append("已生效的豁免：")
        for e in sorted(already_exempt):
            lines.append(f"- `{e}`")
    else:
        lines.append("暂无新豁免建议（或已有豁免覆盖了所有误杀）")

    lines.append("")
    lines.append("---")
    lines.append("*报告由 rejected_analysis.py 自动生成*")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


if __name__ == "__main__":
    import datetime
    rejected = collect_rejected()
    stats = analyze(rejected)
    stats['generated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    report_path = DATA_DIR.parent / "reports" / f"rejected_analysis_{datetime.date.today()}.md"
    report = generate_report(stats, report_path)

    print(f"分析完成: {stats['total']} 条 rejected")
    print(f"报告已保存: {report_path}")
    print("\n" + report[:1000])
