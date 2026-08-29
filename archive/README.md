# archive/ — 已停用模块（2026-08-29 全面审查后归档）

这些模块与现役管线（run_scan_v2 → scoring_engine → generate_platform）无任何引用关系，
且部分仍带 UK 版残留。保留源码备查，**不参与扫描、不参与部署**。
如需恢复某个模块，先完成 AU 本地化（参照 ../tools/site_check.py 自检）再移出。

| 文件 | 原用途 | 归档原因 |
|------|--------|----------|
| signal_fusion.py | 信号融合评分（已 git rm） | 死代码；引用已停用的 VAT/广告/退货成本项，且读不存在的 `COST["vat_rate"]`（config 只有 gst_rate），调用即 KeyError |
| keyword_matcher.py | 关键词-产品匹配 | 唯一调用方是 signal_fusion（已删除） |
| seasonal_trigger.py | 季节触发扫描 | 职责已被 festival_engine + keyword_scanner 取代 |
| image_fetcher.py | 产品图抓取 | 无调用方；平台图直接用 Amazon CDN |
| generate_analysis.py | 旧版单次扫描 HTML | 已被 generate_platform.py 取代；内含 VAT 展示残留 |
| amazon_search.py | 搜索式抓取变体 | 无调用方；搜索路径已由 keyword_scanner + amazon_au._curl_fetch 覆盖 |

**明确不归档**（外部 cron / 手动运营工具，尽管无静态引用）：
selection_report.py（周六18:00周报）、analyze_rejected.py（18:15反馈学习）、
sync_rejected_status.py（看板→rejected 同步）、fix_product.py（人工修数）、
review_analyzer.py（差异化洞察 CLI）、feishu_push.py / discovery_feishu_push.py（飞书推送）。
