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
| 货币 | £ (GBP) | A$ (AUD)，价格带 8.99-16.99（2026-08-29 Lee 调整） |
| 成本模型 | VAT 16.7% + FBA £1.46 | 佣金13-15% + FBA A$4.2 + 采购（**不计广告/退货/GST**，Lee口径2026-08）。**唯一实现 calc_profit.py，scanner 只转发** |
| 汇率 | CNY→GBP | **CNY→AUD = 4.8**（config.json `exchange_rate_cny_aud` 唯一来源，2026-08-29 Lee 定） |
| 折扣社区 | HotUKDeals | **Ozbargain**（anysearch_trends 查询组/评分权重/前端标签均已改，旧数据标签仍兼容） |
| 季节 | 北半球 | **南半球反转**：12-2月夏，6-8月冬。**唯一实现 constants.get_au_season()，禁止各模块自写月份映射** |
| 母亲节 | 3月 | **5月**；父亲节 6月 → **9月** |
| Back to School | 8-9月 | **1月底**（Term 1，最大文具节点） |
| 圣诞场景 | 冬季室内 | **盛夏海滩/BBQ主题** |
| EOFY | 无 | **6月30日财年末** B2B采购潮 |
| 节日库 | uk-festival-planner(65事件) | `data/au_festivals_data.js`（40事件136 SKU，价格带已对齐 8.99-16.99） |
| 抓取源文件 | sources/amazon_uk.py | `sources/amazon_au.py`（已改名） |
| 部署 | Baodan168/product-radar | `Baodan168/product-radar-au` |

## 关键文件

| 文件 | 作用 |
|------|------|
| `config.json` | 主配置（AUD价格带 8.99-16.99 / 汇率4.8 / 三项硬成本结构 / 禁售词173词继承UK）。sources 段仅作文档，代码不读 |
| `constants.py` | 单一事实源：南半球季节 get_au_season / EVENT_KEYWORDS / 事件词表 |
| `run_scan_v2.py` | 扫描引擎（过滤/限流/去重编排） |
| `scanner.py` | 过滤规则（is_forbidden 统一返回元组）；calc_profit 从 calc_profit.py 转发 |
| `calc_profit.py` | **利润计算唯一实现**（佣金+FBA+采购，gst/ad/return 已停用不计入） |
| `festival_engine.py` | 节日引擎（读 data/au_festivals_data.js；解析先 json.loads 后 node 兜底） |
| `season_engine.py` | 季节引擎（数据统一来自 festival_engine） |
| `github_api_push.py` | GitHub API 部署（只推 output/ + data/discovery；不再推 raw/rejected/trends/history，启动时一次性清理远程历史数据文件） |
| `tools/site_check.py` | **AU 本地化守卫**：`python3 tools/site_check.py`，UK/北半球残留一行命令查清；合理引用行尾加 `site-check: allow` |
| `cron_scan.sh` | 定时扫描入口（850s预算） |
| `oa/config.py` | 门户板块配置（无跨境雷达板块） |
| `tests/` | pytest 回归（核心管线/评分/节日/本地化守卫已覆盖） |
| `archive/` | 已停用模块（signal_fusion/keyword_matcher/seasonal_trigger/image_fetcher/generate_analysis/amazon_search），不参与扫描与部署 |

## 操作禁忌

- ❌ **改数据不直接改HTML** — 改数据源JSON，重新生成
- ❌ **节日SKU必须过红线** — 无液体/膏体/body care/电器灯具/电子件；新增SKU对照 au_festivals_data.js 头部注释自检
- ❌ **季节关键词别照抄UK** — 南半球反季，任何「7月=夏季」假设都是bug；季节一律调 `constants.get_au_season()`
- ❌ **别复制 UK 死代码到新站点** — 先跑 `python3 tools/site_check.py` 再提交
- ✅ **价格带调整先跑 calc_profit.py 校准利润率≥20%**（8.99 下限 general 23.8%，仍达标）
- ✅ **部署产物用 github_api_push.py，源码用 git push HTTPS+PAT**

## 市场预期管理

澳洲2600万人口，市场容量约为英国的1/10。单次扫描通过筛选的产品数显著少于UK属正常现象（几个到十几个），不是系统故障。

## 当前状态

- P1-P5 全量建设完成（2026-08-25）；**2026-08-29 全面优化落地**：利润口径统一（calc_profit.py 唯一实现）、南半球季节收敛 constants、Ozbargain 替代 HotUKDeals、价格带 8.99-16.99、汇率 4.8、死代码归档 archive/、部署瘦身（远程不再堆 raw JSON）、补核心管线 pytest + CI（.github/workflows/tests.yml）
- cron计划：06:30/19:30扫描、**07:10 AU发现生成（LLM agent任务fdd33551ccc3，写入data/discovery/{date}.json）**、07:40发现推送、周六18:00周报/18:15反馈学习（错开UK槽位+澳洲凌晨风控窗口）
- 待办：git 历史里已有的 raw JSON blob 如需彻底清除要走 BFG/filter-repo（会重写历史，需 Lee 决定）；看板同步Cloudflare Worker（可选二期）
