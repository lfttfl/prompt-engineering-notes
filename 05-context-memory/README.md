# 模块 5 · 上下文与记忆管理

> **难度**：⭐⭐⭐ 中级
> **建议周次**：第 7–8 周（约 12 小时）
> **前置**：模块 1–4
> **产出能力**：处理长文档、多轮对话、知识库问答

---

## 🎯 本模块目标

从"单次对话"迈向"**系统级应用**"。

解决三个关键问题：
1. 文档几万字塞不进 Prompt 怎么办？
2. 多轮对话历史越来越长，成本飙升怎么办？
3. 知识库问答怎么让答案可信、有引用？

---

## 💼 应用场景

| 场景 | 技术组合 |
|---|---|
| 长合同 / 标书分析 | Long context + 结构化摘要 |
| 客服多轮对话 | Summarization + Prompt Caching |
| 企业知识库问答 | RAG |
| 项目资料自动整理 | Long context + Chunking |
| 财报对比分析 | Long context + 并行分析 |

---

## 📚 核心知识点

### 1. 上下文窗口策略

**三种基本策略**：

| 策略 | 适用 | 缺点 |
|---|---|---|
| **直接塞** | 文档 < 窗口的 50% | 成本高、"中间迷失" |
| **分块（Chunking）** | 文档过长 | 丢失跨块信息 |
| **RAG 检索** | 知识库很大 | 依赖检索质量 |

⚠️ **"Lost in the Middle" 现象**：长上下文里，模型对**开头和结尾**信息最敏感，中间部分容易被忽略。解决：把关键信息放头尾，或在 Prompt 中重复强调。

### 2. Prompt Caching（提示词缓存）

**原理**：把不变的 system prompt / 长文档缓存起来，重复调用只需计算新增部分。

**收益**（以 Anthropic 为例）：
- 缓存写入：1.25× 普通价格
- 缓存命中：**0.1× 普通价格**（省 90%）
- 缓存 TTL：5 分钟（滚动续期）

**使用场景**：
- 客服机器人（同一套 system prompt 反复用）
- 文档问答（同一份文档多个问题）
- Agent 工具定义（工具 schema 不变）

### 3. RAG 基础

**Retrieval-Augmented Generation** = 检索 + 生成

```
用户问题
  ↓ 向量化
  ↓ 向量库检索 top-k 相关片段
  ↓ 拼接到 Prompt
LLM → 基于检索结果回答
```

**关键点**：
- Chunk 大小：300–1000 token，重叠 50–100 token
- Embedding 模型：`text-embedding-3-small`（OpenAI）/ `bge-m3`（开源中文）
- 必须让模型**引用来源**，防止幻觉

### 4. 长对话的记忆压缩

多轮对话不要原样全存，用 3 种方式压缩：

- **Running Summary**：每 N 轮把历史换成 1 段摘要
- **Entity Memory**：只存关键实体（客户名、订单号、偏好）
- **分级记忆**：最近 3 轮原文 + 早期摘要 + 长期档案

---

## 🛠 学习步骤

### Step 1：Long Context 实测（2 小时）

把一份 10 万字标书塞给 Claude（200K 窗口），让它回答 10 个问题。
记录：响应时间、成本、"中间迷失"是否发生。

### Step 2：Prompt Caching 实操（2 小时）

用 Anthropic SDK，给同一 system prompt 连续调用 10 次，观察第 2 次起成本变化。

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    system=[
        {
            "type": "text",
            "text": "长的 system prompt...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[...]
)
```

```python
# 验证是否命中缓存（第二次调用后查看）
print(f"命中缓存 tokens: {response.usage.cache_read_input_tokens}")
print(f"写入缓存 tokens: {response.usage.cache_creation_input_tokens}")
# 命中后 cache_read_input_tokens > 0，说明缓存生效
```

### Step 3：最小 RAG 实现（4 小时）

用 Python + Chroma/FAISS + Embedding 模型，搭一个 100 行内的 RAG：

> **Embedding 模型推荐**：
> - **Voyage AI**（Anthropic 合作方）：`voyage-3` 或 `voyage-3-lite`，中英文都好，与 Claude 配合最佳
> - **OpenAI**：`text-embedding-3-small`，生态成熟
> - **开源**：`bge-m3`（中文最强之一，可本地部署）

1. 文档切块
2. 向量化入库
3. 查询 → 检索 → 拼 Prompt → 调用 LLM
4. 输出答案 + 引用来源

### Step 4：对话记忆压缩（2 小时）

写一个客服多轮对话的 Demo，实现 Running Summary：每 5 轮压缩一次历史。

### Step 5：实战项目（2 小时）

---

## 💻 示例：带引用的 RAG Prompt

```xml
<role>
你是一位严谨的知识库问答助手，只能依据提供的资料回答。
</role>

<rules>
- 仅使用 <documents> 中的内容
- 回答必须标注来源，格式 [doc_id:段落号]
- 资料中没有的，直接说"资料中未提及"
- 不臆造、不外推
</rules>

<documents>
<doc id="1">
段落 1: ...
段落 2: ...
</doc>
<doc id="2">
段落 1: ...
</doc>
</documents>

<question>
{{用户问题}}
</question>

<output_format>
<answer>...答案正文，引用处标[doc_id:段落号]...</answer>
<sources>
  - [1:2] 原文摘录...
</sources>
</output_format>
```

---

## 🏗 实战项目：标书文档问答助手

**要求**：
- 输入：一份 PDF 标书 + 用户自然语言问题
- 技术：PDF 解析 + Chunking + Embedding + 向量检索 + RAG Prompt
- 输出：带原文引用的答案

**验收**：
- [ ] 支持至少 3 份标书切换
- [ ] 答案必带引用，无引用不输出
- [ ] "资料中未提及"类问题能正确识别
- [ ] 命中缓存后第二次响应 < 首次 50% 时间

---

## ✅ 本模块自检清单

- [ ] 理解上下文窗口三种策略的取舍
- [ ] 会用 Prompt Caching 降本
- [ ] 能独立搭一个最小 RAG 系统
- [ ] 能设计多轮对话的记忆压缩方案

---

## 📎 推荐资源

- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Lost in the Middle Paper](https://arxiv.org/abs/2307.03172)
- [LangChain RAG 教程](https://python.langchain.com/docs/tutorials/rag/)
- [LlamaIndex 入门](https://docs.llamaindex.ai/)

---

## 📝 我的笔记
