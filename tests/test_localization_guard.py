"""本地化守卫：现役代码不允许 UK/北半球残留。

规则与豁免集中定义在 tools/site_check.py，此处只保证"守卫本身在 CI 里被执行"。
如果该测试失败：按输出里的 file:line 清理残留，或（确属合理场景）在
site_check.PATTERNS 中补充豁免说明后再调整正则。
"""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "tools"))

from site_check import run_checks


def test_no_uk_residue_in_active_code():
    findings = run_checks()
    assert not findings, "发现非 AU 残留：\n" + "\n".join(
        f"  [{f['rule']}] {f['file']}:{f['line']} → {f['match']}（{f['hint']}）"
        for f in findings
    )
