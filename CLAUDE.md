# Product Radar AU — Amazon AU 选品运营 OA

## 一句话定位

Amazon 澳洲站的选品与运营门户（英国站 product-radar 的姊妹系统），独立仓库独立数据，共享 oa-theme.css 设计系统。服务澳洲站产品开发助理的日常选品决策。

## 怎么跑起来

```bash
cd /home/lee/product-radar-au
bash cron_scan.sh              # 扫描+过滤+评分+生成HTML+推送GitHub
python3 generate_platform.py   # 生成选品平台 HTML
python3 generate_portal.py     # 生成门户页面
python3 github_api_push.py "msg"  # 推送到 GitHub Pages

# 本地预览
python3 -m http.server 8081    # 访问 http://localhost:8081/output/
```

## 与UK版的关键差异（改代码前必读）

| 维度 | UK版 | AU版 |
|------|------|------|
| 站点 | amazon.co.uk | amazon.com.au |
| 货币 | £ (GBP) | A$ (AUD)，价格带 12.99-25.99 |
| 成本模型 | VAT 16.7% + FBA £1.46 | **GST 10%** + FBA A$4.2（见 config.json cost_structure） |
| 季节 | 北半球 | **南半球反转**：12-2月夏，6-8月冬（run_scan_v2/scoring_engine 已改） |
| 母亲节 | 3月 | **5月**；父亲节 6月 → **9月** |
| Back to School | 8-9月 | **1月底**（Term 1，最大文具节点） |
| 圣诞场景 | 冬季室内 | **盛夏海滩/BBQ主题** |
| EOFY | 无 | **6月30日财年末** B2B采购潮 |
| 节日库 | uk-festival-planner(65事件) | `data/au_festivals_data.js`（37事件130 SKU，自建） |
| 抓取源文件 | sources/amazon_uk.py | `sources/amazon_au.py`（已改名） |
| 部署 | Baodan168/product-radar | `Baodan168/product-radar-au` |

## 关键文件

| 文件 | 作用 |
|------|------|
| `config.json` | 主配置（AUD价格带/GST成本结构/禁售词173词继承UK） |
| `run_scan_v2.py` | 扫描引擎（南半球季节逻辑） |
| `scanner.py` | 过滤规则（is_forbidden 返回 False 非元组） |
| `calc_profit.py` | AU利润计算器（GST版） |
| `festival_engine.py` | 节日引擎（读 data/au_festivals_data.js） |
| `season_engine.py` | 季节引擎（AU_EVENTS 表+南半球判断） |
| `github_api_push.py` | GitHub API 部署（REPO=product-radar-au） |
| `cron_scan.sh` | 定时扫描入口（850s预算） |
| `oa/config.py` | 门户板块配置（无跨境雷达板块） |
| `tests/` | pytest 回归 |

## 操作禁忌

- ❌ **改数据不直接改HTML** — 改数据源JSON，重新生成
- ❌ **节日SKU必须过红线** — 无液体/膏体/body care/电器灯具/电子件；新增SKU对照 au_festivals_data.js 头部注释自检
- ❌ **季节关键词别照抄UK** — 南半球反季，任何「7月=夏季」假设都是bug
- ✅ **价格带调整先跑 calc_profit.py 校准利润率≥20%**
- ✅ **部署产物用 github_api_push.py，源码用 git push HTTPS+PAT**

## 市场预期管理

澳洲2600万人口，市场容量约为英国的1/10。单次扫描通过筛选的产品数显著少于UK属正常现象（几个到十几个），不是系统故障。

## 当前状态

- P1-P5 全量建设完成（2026-08-25），待Lee审核后启用cron
- cron计划：06:30/19:30扫描、07:40发现、周六18:00周报/18:15反馈学习（错开UK槽位+澳洲凌晨风控窗口）
- 待办：看板同步Cloudflare Worker（可选二期）
