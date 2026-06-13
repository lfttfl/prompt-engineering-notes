# Changelog

本文档记录本仓库的所有重要变更。
遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式。

---

## [0.3.0] - 2026-06-13 · 技术内容升级

### Fixed
- M1：修正 tiktoken → Anthropic SDK Token Counter（tiktoken 不适用于 Claude）
- M1：修复 "学习步骤" 标题重复、章节编号跳号问题
- M3：修正 Self-Consistency 温度建议（0.5–0.7，非越高越好）
- M3：修正 Extended Thinking 表格描述（移除错误的 `betas` 参数说明）
- M6：修复代码示例中未定义的 `my_weather_api` 函数
- README：Day 2 日历任务修正为 Anthropic SDK（原 tiktoken）
- README：环境准备改用 `cp .env.example .env`

### Added
- M1：新增 API 消息结构（system vs user）说明
- M1：新增 temperature 参数专节
- M2：新增 few-shot 示例顺序影响说明
- M3：新增 Extended Thinking API 专节（含代码示例和适用场景对比）
- M4：新增 Pydantic 结构化输出集成示例
- M5：新增 Voyage AI / BGE-m3 等 Embedding 模型推荐；新增缓存命中验证代码
- M6：新增并行工具调用章节（含 ThreadPoolExecutor 示例）
- M7：新增 Batch API 批量评估示例（降本 50%）
- Capstone：`starter.py` 新增完整异常处理
- `.env.example`：新增 API Key 配置模板
- `99-capstone/data/`：新增 customers.json、inventory.json 样本数据

### Changed
- README：学习路径 B 更新为 M1+M2+M4+M6+M8（补充 Agent 模块）
- README：仓库结构图补充 `.env.example` 和 `99-capstone/data/`
- README：版本记录新增 v0.3
- resources.md：Token 工具列表调整顺序，Anthropic 优先，tiktoken 标注仅适用 OpenAI

---

## [0.2.0] - 2026-04-22 · 工具箱化升级

### Added
- 8 个模块全部配可运行的 Python Demo（使用 Anthropic SDK）
- `templates/` 通用 Prompt 模板库,含销售邮件/信息提取/投资分析/客服/代码解释等 10+ 场景
- `cheatsheets/` 速查表:XML 标签、常用咒语、调试 checklist、模型选型
- `99-capstone/` 毕业综合项目:销售 Agent（整合 3 个月所学）
- 工程标配:`.gitignore`、`requirements.txt`、`LICENSE`（MIT）
- 根 README 增加"每日学习计划"粒度

### Changed
- 根 README 导航结构更新,增加 templates / cheatsheets / capstone 入口

---

## [0.1.0] - 2026-04-22 · 首个完整版本

### Added
- 仓库初始化
- 8 个核心模块学习教程（理论 + 步骤 + Prompt 示例 + 实战项目 + 自检清单）
  - 模块 1:基础认知与 Prompt 结构
  - 模块 2:核心技法（Few-shot / CoT / Role / XML）
  - 模块 3:推理与思维链进阶（ToT / Self-Consistency / Step-back）
  - 模块 4:结构化输出与约束控制
  - 模块 5:上下文与记忆管理（RAG / Prompt Caching）
  - 模块 6:Agent 与工具调用（Function Calling / ReAct）
  - 模块 7:评估与迭代优化（Eval / LLM-as-Judge）
  - 模块 8:安全与对抗防御（Prompt Injection）
- 根 README 总路线图
- `resources.md` 参考资源汇总
