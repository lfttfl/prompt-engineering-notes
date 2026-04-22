# 🚀 Prompt Engineering Notes · 提示词工程 3 个月系统学习

> 一份面向 **工程化落地** 的提示词工程学习笔记,从零基础到能为复杂任务独立设计 Prompt。

---

## 🎯 学习目标

**12 周内,达成以下能力**:

- ✅ 为复杂任务独立设计结构化 Prompt
- ✅ 能处理长文档、多轮对话、知识库问答
- ✅ 能构建带工具调用的 Agent
- ✅ 建立 Eval 评估与回归测试工作流
- ✅ 能识别并防御常见 Prompt 攻击

**总时长预算**:82 小时(每周 ≈ 7 小时)

---

## 🗺 总路线图

| # | 模块 | 难度 | 周次 | 核心能力 | 对应文档 |
|---|---|---|---|---|---|
| 1 | 基础认知与 Prompt 结构 | ⭐ | W1 | 理解 LLM 工作原理,会写清晰指令 | [01-foundations](./01-foundations/) |
| 2 | 核心技法:指令工程 | ⭐⭐ | W2–W3 | Few-shot / CoT / Role / XML 四板斧 | [02-instruction](./02-instruction/) |
| 3 | 推理与思维链进阶 | ⭐⭐⭐ | W4–W5 | Self-Consistency / ToT / Step-back / ReAct | [03-reasoning](./03-reasoning/) |
| 4 | 结构化输出与约束控制 | ⭐⭐⭐ | W6 | JSON Schema / Tool Use 强制格式 | [04-structured-output](./04-structured-output/) |
| 5 | 上下文与记忆管理 | ⭐⭐⭐ | W7–W8 | Prompt Caching / RAG / 对话压缩 | [05-context-memory](./05-context-memory/) |
| 6 | Agent 与工具调用 | ⭐⭐⭐⭐ | W9–W10 | Function Calling / ReAct Loop / Planning | [06-agent-tools](./06-agent-tools/) |
| 7 | 评估与迭代优化 | ⭐⭐⭐⭐ | W11 | Eval 集 / LLM-as-Judge / 回归测试 | [07-evaluation](./07-evaluation/) |
| 8 | 安全与对抗防御 | ⭐⭐⭐ | W12 | Prompt Injection 防御 / 红队测试 | [08-security](./08-security/) |

> 📎 参考资源汇总见 [resources.md](./resources.md)

---

## 📖 使用方法

### 推荐学习节奏

1. **按顺序学**:后续模块依赖前面的基础,不建议跳过
2. **先看原理 → 再动手实战**:每个模块都有"步骤 + 原理 + 示例"三段式
3. **每个模块必做 1 个实战项目**:不做不算学会
4. **做完每个模块勾选"自检清单"**:不过关就回头复习

### 如何使用本仓库

每个模块文件夹下有:
- `README.md` — 学习笔记(理论 + 步骤 + 示例 + 实战)

学习过程中可以在每份笔记底部的 `📝 我的笔记` 区追加:
- 自己发现的好用 Prompt 片段
- 踩过的坑
- 实战项目的链接或截图

可以另行创建 `examples/` 存 Prompt 示例,`project/` 存实战代码。

---

## 🏗 12 周里程碑(实战项目清单)

| 周 | 实战项目 | 技能点 |
|---|---|---|
| W1 | 报价邮件生成器 | Prompt 四件套 |
| W2–W3 | 招投标关键信息提取器 | Few-shot + CoT + XML |
| W4–W5 | 多视角投资分析助手 | ToT + Step-back |
| W6 | 简历批量结构化入库 | JSON Schema + Tool Use |
| W7–W8 | 标书文档问答助手 | RAG + 引用追溯 |
| W9–W10 | 投资分析 Agent | Function Calling + Planning |
| W11 | 为已有 Prompt 建 Eval 体系 | 回归测试工作流 |
| W12 | Agent 红队加固 | Prompt Injection 防御 |

---

## ⚙️ 环境准备

**最小必备**:

- Python 3.10+
- OpenAI 或 Anthropic API Key(二选一,推荐 Anthropic)
- 一个 Playground 账号(快速调试 Prompt)

**推荐工具**:
```bash
pip install anthropic openai tiktoken chromadb promptfoo
```

---

## 🎓 毕业标准

完成下列任一组合即视为"毕业":

- **A 组(工程师向)**:完成全部 8 个模块 + 至少 5 个实战项目
- **B 组(业务向)**:完成模块 1–5 + 模块 8 + 至少 3 个与本职工作相关的实战

---

## 📌 进度跟踪

在每个模块底部的"自检清单"勾选,或在这里维护总表:

- [ ] 模块 1:基础认知与 Prompt 结构
- [ ] 模块 2:核心技法:指令工程
- [ ] 模块 3:推理与思维链进阶
- [ ] 模块 4:结构化输出与约束控制
- [ ] 模块 5:上下文与记忆管理
- [ ] 模块 6:Agent 与工具调用
- [ ] 模块 7:评估与迭代优化
- [ ] 模块 8:安全与对抗防御

---

## 📅 更新日志

- **2026-04-22** — 仓库初始化,8 个模块教程完整上传

---

*Built with ☕ by Felix · 持续更新中*
