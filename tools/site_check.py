#!/usr/bin/env python3
"""AU 本地化自检 —— 复制 UK 框架到新站点或大改之后跑一遍，防残留复发。

用法:
    python3 tools/site_check.py            # 退出码 0=干净 1=有残留
    python3 tools/site_check.py --json     # 机器可读输出

检查范围：现役代码（根目录 *.py、sources/、oa/、templates/、tools/、scripts/、
assets/、tests/ 除外）+ config.json。排除 archive/（有意保留的旧模块）、
output/（生成产物）、data/（运行时数据）。

2026-08-29 全面审查的产物：当年 UK→AU 复制残留散落在 config、前端、注释、
字段名里（amazon.co.uk URL、HotUKDeals 标签、VAT 成本行、£、北半球季节），
每类都修过一次。这个脚本让"下次复制"变成一条命令可验证的事。
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# 扫描目录（相对 BASE）与排除目录
SCAN_DIRS = ['.', 'sources', 'oa', 'templates', 'tools', 'scripts', 'assets']
EXCLUDE_PARTS = {'archive', 'output', 'data', '.git', '__pycache__', '.github', 'logs', 'tests'}
# 规则定义文件本身必然包含全部模式字面量，自我排除
EXCLUDE_FILES = {'tools/site_check.py'}
# 行级豁免标记：确属合理引用（如"替代 UK 版的 HotUKDeals"这类说明文字），
# 在该行行尾或注释里加  site-check: allow
ALLOW_MARK = 'site-check: allow'
SCAN_EXT = {'.py', '.js', '.sh', '.html', '.css'}

# (名称, 正则, 说明)。大小写敏感的按需内联 (?i) 关闭。
PATTERNS = [
    ("UK 域名", r'amazon\.co\.uk', "UK 站点 URL/引用，AU 应为 amazon.com.au"),
    ("HotUKDeals 标签", r'HotUKDeals', "UK 折扣社区标签，AU 对应 Ozbargain"),
    ("英镑符号", r'£', "GBP 符号，AU 应为 A$"),
    ("VAT 字样", r'\bVAT\b|\bvat_rate\b', "VAT 是 UK 税制；AU 是 GST 且已停用不计入利润模型"),
    ("旧汇率键名", r'exchange_rate_cny_gbp', "UK 版汇率键名，AU 应读 exchange_rate_cny_aud"),
    ("UK Reddit 版", r'r/(CasualUK|AskUK|FrugalUK|AmazonUK|UKFrugal)', "UK subreddit，AU 应为 AskAnAustralian/AusFrugal"),
    ("geo=GB", r'"geo"\s*:\s*"GB"|geo=GB', "Google Trends 地区应为 AU"),
    ("硬编码季节查询", r'(summer|winter|spring|autumn)[ _]20\d\d', "趋势查询季节/年份应动态生成（constants.get_au_season）"),
    ("北半球季节映射", r'month in \(6,\s*7,\s*8\)[^\n]*summer|in \(6, 7, 8\): return "summer"', "6-8 月在南半球是冬天"),
]


def iter_files():
    seen = set()
    for d in SCAN_DIRS:
        root = BASE / d
        if not root.exists():
            continue
        for p in root.rglob('*'):
            if not p.is_file() or p.suffix not in SCAN_EXT:
                continue
            if any(part in EXCLUDE_PARTS for part in p.relative_to(BASE).parts):
                continue
            rp = str(p.relative_to(BASE))
            if rp in seen:
                continue
            seen.add(rp)
            yield p, rp


def run_checks(base=BASE):
    findings = []
    for p, rp in iter_files():
        if rp.replace('\\', '/') in EXCLUDE_FILES:
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        lines = text.splitlines()
        for name, pattern, hint in PATTERNS:
            for m in re.finditer(pattern, text):
                line_no = text.count('\n', 0, m.start()) + 1
                line = lines[line_no - 1]
                if ALLOW_MARK in line:
                    continue  # 显式豁免的合理引用
                findings.append({"file": rp, "line": line_no, "rule": name, "match": m.group(0), "context": line.strip()[:100], "hint": hint})
    # config.json 口径断言
    try:
        cfg = json.loads((base / 'config.json').read_text(encoding='utf-8'))
        rate = cfg.get('exchange_rate_cny_aud')
        if rate is None:
            findings.append({"file": "config.json", "line": 0, "rule": "汇率缺失", "match": "exchange_rate_cny_aud", "context": "", "hint": "必须存在（CNY→AUD，唯一来源）"})
        elif not (3.5 <= rate <= 6.0):
            findings.append({"file": "config.json", "line": 0, "rule": "汇率越界", "match": str(rate), "context": "", "hint": "CNY→AUD 合理区间 3.5-6.0，超出可能是 UK 残留值"})
    except (OSError, json.JSONDecodeError):
        findings.append({"file": "config.json", "line": 0, "rule": "配置不可读", "match": "", "context": "", "hint": "config.json 缺失或 JSON 损坏"})
    return findings


def main():
    findings = run_checks()
    if '--json' in sys.argv:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    elif findings:
        print(f'❌ 发现 {len(findings)} 处疑似非 AU 残留：\n')
        for f in findings:
            print(f'  [{f["rule"]}] {f["file"]}:{f["line"]}')
            print(f'    匹配: {f["match"]}  |  {f["context"]}')
            print(f'    建议: {f["hint"]}\n')
    else:
        print('✅ 未发现 UK/北半球残留，AU 本地化检查通过')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
