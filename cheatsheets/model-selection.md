# 🤖 模型选型速查

> 不同任务用不同模型。本表截至 2026 年 4 月,会过时,请结合当前定价复核。

---

## 🏆 任务 × 模型推荐

| 任务类型 | 首选 | 备选 | 经济型 |
|---|---|---|---|
| **复杂推理 / 长思考** | Claude Opus 4.x | GPT-o1/o3 | Gemini 2.5 Pro |
| **长文档分析(>50K)** | Claude Sonnet 4.x(200K) / 1M 上下文 | Gemini 2.5 Pro(1M+) | - |
| **中文写作** | Claude / GPT | DeepSeek | Qwen |
| **代码生成** | Claude Sonnet 4.x | GPT-4.x | DeepSeek Coder |
| **结构化数据提取** | Claude Sonnet / GPT-4o | Haiku / GPT-4o mini | Gemini Flash |
| **简单分类 / 情感** | Claude Haiku | GPT-4o mini | Qwen-Turbo |
| **Agent / 工具调用** | Claude Sonnet 4.x | GPT-4.x | - |
| **多模态(图片)** | Claude / GPT-4.x / Gemini | - | - |
| **超高并发 / 成本敏感** | Haiku / GPT-4o mini | Gemini Flash | 开源自部署 |

---

## 💰 成本梯队(量级参考)

| 档位 | 代表模型 | 输入价格(美元 / 1M tokens) |
|---|---|---|
| 旗舰 | Claude Opus 4.x / GPT-o 系 | $15–30 |
| 主力 | Claude Sonnet 4.x / GPT-4.x | $3–5 |
| 经济 | Claude Haiku 4.x / GPT-4o mini | $0.25–1 |
| 开源自部署 | Qwen / DeepSeek / Llama | 运营成本(电+卡) |

**原则**:先用主力模型把 Prompt 调到 90 分 → 再尝试换小模型降本 → 掉 5 分以内就换,超过就升回。

---

## 🎯 按场景分配(Felix 专属参考)

| 你的使用场景 | 推荐 |
|---|---|
| 日常写邮件/报价/邮件改写 | Claude Sonnet(稳,中文好) |
| 批量简历/标书提取 | Claude Haiku(便宜 + 结构化好) |
| 股票/基金深度分析 | Claude Opus(推理强) |
| 客服机器人 | Claude Haiku + Prompt Caching |
| Python 学习辅助 | Claude Sonnet(代码解释好) |
| 服务器脚本生成 / 运维助手 | Claude Sonnet(代码生成+推理) |
| 本地/私有部署(合规要求高) | Qwen 72B / DeepSeek / Llama 系 |

---

## 🔀 不同模型的"脾气"

### Claude(Anthropic)
- ✅ XML 标签解析最稳
- ✅ 长上下文表现好(Needle-in-a-haystack)
- ✅ 指令跟随严格,不爱自由发挥
- ⚠️ 对"拒答"更敏感,有时过于谨慎

### GPT(OpenAI)
- ✅ Tool Use 生态成熟(Assistants API)
- ✅ JSON mode / Structured Outputs 健壮
- ✅ 生态工具最丰富
- ⚠️ 复杂指令有时"偷工减料"

### Gemini(Google)
- ✅ 超长上下文(1M+)
- ✅ 多模态一体化强
- ✅ 价格有竞争力(Flash 系列)
- ⚠️ 中文和细微指令遵循略弱

### 国产(DeepSeek / Qwen)
- ✅ 中文表现优秀
- ✅ 便宜 / 可私有部署
- ✅ 数学/代码能力不错
- ⚠️ 高阶 Agent 场景、复杂推理仍落后旗舰

---

## ⚡ 延迟与吞吐参考

| 场景 | 推荐 | 理由 |
|---|---|---|
| 实时客服(< 2s 首字) | Haiku / GPT-4o mini | Streaming 快 |
| 批处理(离线) | 主力模型 + Batch API | 批处理 50% 折扣 |
| 需要"思考"的任务 | Opus / o1 | 允许更长响应时间 |
| 嵌入式设备 | 本地小模型 / 蒸馏 | 无网络依赖 |

---

## 🧭 决策流程

```
任务是否需要深度推理?
├─ 是 → Claude Opus / GPT-o 系
└─ 否 → 继续
        ↓
任务是否涉及长文档(>50K)?
├─ 是 → Claude Sonnet 200K / Gemini 2.5
└─ 否 → 继续
        ↓
任务是否高并发 / 成本敏感?
├─ 是 → Haiku / GPT-4o mini
└─ 否 → 继续
        ↓
任务涉及 Tool Use / Agent?
├─ 是 → Claude Sonnet / GPT-4.x
└─ 否 → 主力模型中任一
```

---

## ⚠️ 常见误区

- "用最贵的模型最好" — 不,小模型 + 好 Prompt 往往胜过大模型 + 烂 Prompt
- "换个模型就能解决" — 90% 的效果问题是 Prompt 问题(见 [debugging.md](./debugging.md))
- "中文一定用国产" — 当前 Claude / GPT 的中文已经非常好,不是决定因素
