# 🚀 Prompt Engineering Notes · 提示词工程 3 个月系统学习

> 一份面向**工程化落地**的提示词工程学习笔记 + 即用模板 + 可运行 Demo。
> 目标:3 个月内能独立为复杂任务设计 Prompt,并做出一个真实可用的 Agent。

---

## 🎯 学习目标

**12 周内达成**:
- ✅ 为复杂任务独立设计结构化 Prompt
- ✅ 处理长文档、多轮对话、知识库问答
- ✅ 构建带工具调用的 Agent
- ✅ 建立 Eval 评估与回归测试工作流
- ✅ 识别并防御常见 Prompt 攻击
- 🎓 做出一个能真实使用的"销售 Agent"作为毕业作品

**总时长预算**:82 小时(每周 ≈ 7 小时)

---

## 📂 仓库结构

```
prompt-engineering-notes/
│
├── 📚 核心教程(每模块:README + 可运行 demo.py)
│   ├── 01-foundations/         M1 基础认知 + demo_quote_email.py
│   ├── 02-instruction/         M2 指令工程 + demo_bid_extractor.py
│   ├── 03-reasoning/           M3 推理思维链 + demo_stock_analysis.py
│   ├── 04-structured-output/   M4 结构化输出 + demo_resume_parser.py
│   ├── 05-context-memory/      M5 上下文记忆 + demo_rag.py
│   ├── 06-agent-tools/         M6 Agent 工具 + demo_agent.py
│   ├── 07-evaluation/          M7 评估优化 + demo_eval.py
│   └── 08-security/            M8 安全防御 + demo_red_team.py
│
├── 🎓 毕业综合项目
│   └── 99-capstone/            销售 Agent(整合 M1-M8)
│
├── 📦 工具箱
│   ├── templates/              即拿即用 Prompt 模板(10+ 场景)
│   └── cheatsheets/            速查表(XML/咒语/调试/模型选型)
│
└── 📎 工程
    ├── resources.md            参考资源汇总
    ├── CHANGELOG.md            更新日志
    ├── requirements.txt        Python 依赖
    └── .gitignore, LICENSE
```

---

## 🗺 总路线图

| # | 模块 | 难度 | 周次 | 教程 | Demo |
|---|---|---|---|---|---|
| 1 | 基础认知与 Prompt 结构 | ⭐ | W1 | [📘](./01-foundations/) | [💻](./01-foundations/demo_quote_email.py) |
| 2 | 核心技法:指令工程 | ⭐⭐ | W2-3 | [📘](./02-instruction/) | [💻](./02-instruction/demo_bid_extractor.py) |
| 3 | 推理与思维链进阶 | ⭐⭐⭐ | W4-5 | [📘](./03-reasoning/) | [💻](./03-reasoning/demo_stock_analysis.py) |
| 4 | 结构化输出与约束控制 | ⭐⭐⭐ | W6 | [📘](./04-structured-output/) | [💻](./04-structured-output/demo_resume_parser.py) |
| 5 | 上下文与记忆管理 | ⭐⭐⭐ | W7-8 | [📘](./05-context-memory/) | [💻](./05-context-memory/demo_rag.py) |
| 6 | Agent 与工具调用 | ⭐⭐⭐⭐ | W9-10 | [📘](./06-agent-tools/) | [💻](./06-agent-tools/demo_agent.py) |
| 7 | 评估与迭代优化 | ⭐⭐⭐⭐ | W11 | [📘](./07-evaluation/) | [💻](./07-evaluation/demo_eval.py) |
| 8 | 安全与对抗防御 | ⭐⭐⭐ | W12 | [📘](./08-security/) | [💻](./08-security/demo_red_team.py) |
| 🎓 | **毕业作品:销售 Agent** | ⭐⭐⭐⭐⭐ | W13+ | [📘 Capstone](./99-capstone/) | [💻](./99-capstone/starter.py) |

---

## 📖 学习路径(三选一)

| 路径 | 适合 | 节奏 |
|---|---|---|
| **🎯 A · 系统学习** | 想做 AI 产品 | 12 周按顺序 + 每模块实战 + 毕业 Capstone |
| **⚡ B · 速成实用** | 日常工作用 | M1 + M2 + M4 + M8(≈ 4 周) |
| **🔧 C · 工具使用** | 当参考用 | 直接用 [templates/](./templates/) + [cheatsheets/](./cheatsheets/) |

---

## 📅 12 周日历(细化到天)

### W1 · 基础认知与 Prompt 结构
| 天 | 任务 |
|---|---|
| Day 1 | 看 Anthropic Prompt Engineering 文档(1h) |
| Day 2 | 理解 Token,用 tiktoken 数自己 Prompt 的 token(1h) |
| Day 3 | 写 3 个"烂 vs 好"Prompt 对比练习(2h) |
| Day 4-5 | 跑通 `demo_quote_email.py`,改成自己的场景 |
| Day 6-7 | 复盘 + 在 01-foundations/README 底部写笔记 |

### W2-W3 · 核心技法
| 阶段 | 任务 |
|---|---|
| W2 前 | Zero-shot vs Few-shot 对比实验(3h) |
| W2 后 | CoT + Role 消融实验(4h) |
| W3 前 | 把所有 Prompt 改造为 XML 结构(2h) |
| W3 后 | 跑通 `demo_bid_extractor.py`,换成真实标书(2h) |

### W4-W5 · 推理与思维链
| 阶段 | 任务 |
|---|---|
| W4 前 | `<thinking>` 标签 + Self-Consistency(3h) |
| W4 后 | Tree of Thoughts 实验(3h) |
| W5 前 | Step-back 应用到客户沟通(4h) |
| W5 后 | 跑通 `demo_stock_analysis.py`,改成你关注的股票 |

### W6 · 结构化输出
| 天 | 任务 |
|---|---|
| Day 1-2 | JSON Schema + Tool Use 实操(4h) |
| Day 3-4 | 失败 retry 机制 + 兜底(2h) |
| Day 5-7 | 跑通 `demo_resume_parser.py`,扩展到 10 份真实简历 |

### W7-W8 · 上下文与记忆
| 阶段 | 任务 |
|---|---|
| W7 前 | Prompt Caching 成本实测(3h) |
| W7 后 | 跑通 `demo_rag.py`,扩展到多份文档(4h) |
| W8 前 | 对话 Running Summary 压缩(3h) |
| W8 后 | 实战:标书问答助手 MVP(2h) |

### W9-W10 · Agent 与工具调用
| 阶段 | 任务 |
|---|---|
| W9 前 | Tool Use Hello World(2h) |
| W9 后 | ReAct 模式实操(3h) |
| W10 前 | 跑通 `demo_agent.py`,加 Planning + 错误恢复(4h) |
| W10 后 | 接一个真实 API(如股票行情 / 天气)替代 mock(3h) |

### W11 · 评估
| 天 | 任务 |
|---|---|
| Day 1-2 | 构建 Eval 集 30 条(2h) |
| Day 3-4 | 基于 `demo_eval.py` 扩展 Rule-based 评估(2h) |
| Day 5-6 | LLM-as-Judge + 位置互换消偏(3h) |
| Day 7 | 给前面任一模块 Prompt 做 v1→v3 回归(3h) |

### W12 · 安全
| 天 | 任务 |
|---|---|
| Day 1 | 复现 5 种 Prompt Injection(1h) |
| Day 2-3 | 加固前面某个 Agent(3h) |
| Day 4-5 | 跑 `demo_red_team.py`,记录穿透率(3h) |
| Day 6-7 | 毕业自评 + 决定是否启动 Capstone |

### 🎓 W13+ · 毕业作品(可选,4 周)
→ 进入 [99-capstone/](./99-capstone/)

---

## ⚙️ 环境准备

```bash
# 克隆项目
git clone git@github.com:lfttfl/prompt-engineering-notes.git
cd prompt-engineering-notes

# 安装依赖
python -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\Scripts\activate           # Windows
pip install -r requirements.txt

# 配置 API Key(创建 .env 文件)
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 验证
python 01-foundations/demo_quote_email.py
```

---

## 🎓 毕业标准

| 组别 | 适合人群 | 毕业条件 |
|---|---|---|
| **A · 工程师向** | 想做 AI 产品 | 完成 8 模块 + 至少 5 个 Demo 跑通 + 毕业 Capstone |
| **B · 业务向** | 日常工作用 | 完成 M1-M5 + M8 + 3 个与本职工作相关的实战 |
| **C · 速成向** | 面试前突击 | 完成 M1-M4 + M8 + 能独立写出覆盖 5 种场景的 Prompt |

---

## 📌 进度跟踪

- [ ] M1:基础认知与 Prompt 结构
- [ ] M2:核心技法:指令工程
- [ ] M3:推理与思维链进阶
- [ ] M4:结构化输出与约束控制
- [ ] M5:上下文与记忆管理
- [ ] M6:Agent 与工具调用
- [ ] M7:评估与迭代优化
- [ ] M8:安全与对抗防御
- [ ] 🎓 Capstone:销售 Agent

---

## 📎 快速链接

- 🎓 [毕业项目 Capstone](./99-capstone/) — 销售 Agent
- 📦 [Prompt 模板库](./templates/) — 10+ 场景的即用模板
- ⚡ [速查表](./cheatsheets/) — XML 标签 / 咒语 / 调试 / 模型选型
- 📖 [参考资源](./resources.md) — 官方文档 / 课程 / 论文
- 📝 [更新日志](./CHANGELOG.md)

---

## 📅 版本记录

- **v0.2 (2026-04-22)** — 工具箱升级:templates、cheatsheets、8 个 Python Demo、Capstone、工程标配文件
- **v0.1 (2026-04-22)** — 初始版本:8 模块完整教程

---

*Built with ☕ by Felix · 持续更新中*
