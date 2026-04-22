# Changelog

本文档记录本仓库的所有重要变更。
遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式。

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
