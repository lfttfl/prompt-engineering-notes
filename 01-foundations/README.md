# 模块 1 · 基础认知与 Prompt 结构

> **难度**：⭐ 入门
> **建议周次**：第 1 周（约 6–8 小时）
> **前置**：无
> **产出能力**：能写出结构清晰、指令明确的 Prompt

---

## 🎯 本模块目标

搞懂两件事：
1. **LLM 到底在干什么？**（原理）
2. **一条好的 Prompt 长什么样？**（结构）

学完后，你写的 Prompt 输出会明显更稳定、更贴近预期。

---

## 💼 应用场景

| 场景 | 典型用法 |
|---|---|
| 日常写作 | 润色邮件、起标题、翻译 |
| 销售工作 | 起草客户邮件、产品介绍文案 |
| 数据工作 | 简单文本清洗、分类 |
| 学习辅助 | 知识点解释、案例生成 |

---

## 📚 核心知识点

### 1. LLM 的本质：下一个 token 预测器

LLM 不是"理解"你的问题，而是基于你输入的文本，计算下一个最可能出现的词（token）。

**推论**：
- Prompt 越具体，"下一个词"的概率分布越集中 → 输出越可预测
- 含糊的指令 = 让模型在大量可能性中随机猜 → 输出不稳定

### 2. Token 与上下文窗口

- **Token**：模型的基本处理单位。英文约 1 token ≈ 0.75 词，中文约 1 token ≈ 1–2 字
- **上下文窗口**：模型一次能"看到"的总 token 数
  - GPT-4o：128K
  - Claude Sonnet 4.6：200K（1M 可选）
  - Gemini 2.5 Pro：1M+
- **成本**：按 input + output token 计费，长 Prompt = 贵

### 3. Prompt 四件套结构

| 组件 | 作用 | 示例 |
|---|---|---|
| `Role` 角色 | 定调专业性 | "你是一个有 10 年经验的电气工程师" |
| `Task` 任务 | 明确要做什么 | "阅读以下招标文件，提取关键信息" |
| `Context` 上下文 | 补充背景 | "本次招标是 10kV 配电项目，预算 500 万" |
| `Format` 格式 | 规定输出样式 | "以 JSON 输出，字段包括……；用中文" |

---

## 🛠 学习步骤（步骤 + 原理 + 示例）

### Step 1：原理理解（1 小时）

任选其一：
- [Anthropic Prompt Engineering Overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- 吴恩达《ChatGPT Prompt Engineering for Developers》（免费，1 小时看完）

### Step 2：四件套实操（2 小时）

选 5 个你日常会遇到的任务（例如"写报价邮件"），每个任务写两版 Prompt：
- **烂版**：只说"帮我写一封报价邮件"
- **好版**：四件套齐全

对比输出差异，感受结构化的威力。

### Step 3：Token 意识训练（1 小时）

- 用 Python 库 `tiktoken` 数一下你常用 Prompt 的 token 量
- 或用 [OpenAI Tokenizer](https://platform.openai.com/tokenizer) 在线查

```python
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4o")
print(len(enc.encode("你的 Prompt 文本")))
```

### Step 4：实战项目（2–3 小时）

见下方。

---

## 💻 Prompt 示例对比

### ❌ 烂版

```
写一封给客户的报价邮件
```

输出：泛泛而谈，每次都不一样。

### ✅ 好版

```xml
<role>
你是某电气设备公司的资深销售，有 10 年配电设备销售经验。
</role>

<task>
根据以下信息起草一封给客户的正式报价邮件。
</task>

<context>
客户：华东某新能源公司采购部 张经理
产品：10kV 环网柜 ×5 台，单价 8.5 万
交付：60 天内
付款：30% 预付，60% 发货前，10% 质保金
</context>

<format>
- 中文、正式商务语气
- 包含：问候语、报价明细表、交付条款、付款条款、结束语
- 邮件长度 300–500 字
</format>
```

---

## 🏗 实战项目：报价邮件生成器

**要求**：做一个 Prompt 模板，输入 `{客户名称}` `{产品清单}` `{特殊要求}`，输出一封完整报价邮件。

**验收标准**：
- [ ] 换 3 个不同客户输入，输出格式稳定
- [ ] 术语专业，无明显"AI 味"
- [ ] 能处理"客户砍价"这类追加问题的连续对话

---

## ✅ 本模块自检清单

- [ ] 能用自己的话解释"LLM 是 token 预测器"
- [ ] 写 Prompt 时会本能地包含 Role / Task / Context / Format
- [ ] 知道自己常用 Prompt 大概多少 token
- [ ] 完成报价邮件生成器实战

---

## 📎 推荐资源

- [Anthropic Prompt Engineering Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Learn Prompting（中文）](https://learnprompting.org/zh-Hans/docs/intro)

---

## 📝 我的笔记

<!-- 在这里记录学习心得、踩过的坑、好用的 Prompt 片段 -->
