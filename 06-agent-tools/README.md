# 模块 6 · Agent 与工具调用

> **难度**：⭐⭐⭐⭐ 高级
> **建议周次**：第 9–10 周（约 14 小时）
> **前置**：模块 1–5
> **产出能力**：设计能自主"做事"的 Agent

---

## 🎯 本模块目标

从"让模型回答"跨越到"让模型**行动**"。

做完本模块，你能构建一个能调用 API、查数据、执行运算、产出结论的自动化助手。

---

## 💼 应用场景

| 场景 | Agent 能做什么 |
|---|---|
| 销售数据分析 | 查 CRM → 算指标 → 出报告 |
| 自动化报价 | 查库存 → 算价格 → 出邮件 |
| 服务器运维 | 查日志 → 诊断 → 给建议 |
| 投资分析 | 查行情 → 拉财报 → 多路径分析 |
| 客服工单 | 查订单 → 查知识库 → 回复客户 |

---

## 📚 核心知识点

### 1. Tool Use / Function Calling

让模型"决定"何时调用哪个工具，以及传什么参数。

**三方约定**：
1. **你定义工具**：名字、描述、参数 schema
2. **模型决定调用**：输出工具名 + 参数 JSON
3. **你执行工具**：拿结果回传给模型

```python
tools = [
    {
        "name": "get_stock_price",
        "description": "获取指定股票的实时价格",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码，如 AAPL"}
            },
            "required": ["symbol"]
        }
    }
]
```

### 2. ReAct 循环

Agent 的心脏节律：

```
Thought（思考）→ Action（调工具）→ Observation（看结果）→ Thought → ...
                                                         ↓
                                                    Final Answer
```

**关键**：每一步都有 reasoning，不是盲目调工具。

### 3. Planning（规划）

复杂任务让模型先给计划，再执行。

**Prompt 模式**：
```xml
<instruction>
在开始行动前，请先：
1. 拆解任务为 3–5 个子步骤
2. 为每步指出需要的工具
3. 输出计划后，再逐步执行
</instruction>
```

**好处**：避免模型"无脑调工具"，增加可控性。

### 4. 错误恢复

工具调用必然失败，Agent 要能扛。

**三级兜底**：
1. **重试**：transient error 直接 retry 2 次
2. **降级**：主工具挂了换备用（如主 API 挂了查缓存）
3. **澄清**：无法继续时向用户提问，而不是瞎猜

### 5. Agent 的终止条件

防止无限循环，必须设：
- **最大步数**（如 10 步）
- **预算上限**（如 $0.5 / 任务）
- **超时**（如 120 秒）

### 6. 并行工具调用

Claude 支持在一次响应中返回多个 `tool_use` blocks，实现并行调用。对需要同时获取多组数据的 Agent（如同时查股价、财报、新闻）可以大幅提升效率：

```python
# 模型可能一次返回多个工具调用
for block in resp.content:
    if block.type == "tool_use":
        # 收集所有工具调用
        tool_calls.append(block)

# 并行执行（可用 ThreadPoolExecutor）
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    futures = {
        executor.submit(TOOLS_IMPL[tc.name], **tc.input): tc
        for tc in tool_calls
    }
    # 把所有结果一并回传
    tool_results = [
        {"type": "tool_result", "tool_use_id": tc.id, "content": str(f.result())}
        for f, tc in [(f, futures[f]) for f in futures]
    ]
```

**注意**：并行工具调用时，所有 `tool_result` 必须在同一条 `user` 消息里一起回传，不能分开发。

### 7. Streaming（流式输出）

生产环境的 Agent 几乎都需要 Streaming——用户无需等待整个答案生成完才看到内容：

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "分析这只股票..."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**带工具调用的 Streaming**：使用 `stream.get_final_message()` 拿到完整消息（含 `tool_use` blocks）再处理工具逻辑，其余与普通 Streaming 一致。

---

## 🛠 学习步骤

### Step 1：Tool Use Hello World（2 小时）

用 Anthropic SDK 实现最简工具调用：天气查询。

```python
from anthropic import Anthropic

client = Anthropic()

tools = [{
    "name": "get_weather",
    "description": "获取城市天气",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"]
    }
}]

messages = [{"role": "user", "content": "北京今天天气怎么样？"}]

while True:
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    if resp.stop_reason == "end_turn":
        break
    for block in resp.content:
        if block.type == "tool_use":
            # 这里替换为你的真实 API，此处用 mock 演示
            city = block.input["city"]
            result = {"city": city, "weather": "晴", "temp": "25°C"}  # mock 数据
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                }]
            })
```

### Step 2：ReAct 模式实操（3 小时）

在 system prompt 中强制 Thought-Action-Observation 交替，观察与自由模式的区别。

### Step 3：多工具 Agent（4 小时）

做一个带 3 个工具的股票分析 Agent：
- `get_price(symbol)` 实时价格
- `get_financials(symbol)` 财报摘要
- `search_news(query)` 新闻搜索

### Step 4：Planning + 错误恢复（2 小时）

给上面的 Agent 加：
- 开局先出计划
- 工具失败重试 / 降级
- 步数上限 + 预算上限

### Step 5：实战项目（3 小时）

---

## 💻 示例：Agent 的 System Prompt 模板

```xml
<role>
你是一个投资分析 Agent，能调用多种工具获取数据并综合分析。
</role>

<available_tools>
1. get_price(symbol) - 实时股价
2. get_financials(symbol) - 最近 4 季度财报
3. search_news(query, days) - 新闻检索
4. calculate(expression) - 数学运算
</available_tools>

<working_style>
1. 收到任务后，先输出 <plan>...</plan>，拆解为 3–5 个子步骤
2. 每一步先 <thought> 思考，再调用工具
3. 工具返回后写 <observation>，然后进入下一步 <thought>
4. 完成后输出 <final_answer>
5. 步数上限：10；超过请输出已有结论
</working_style>

<safety>
- 只做分析，不给具体买卖建议
- 数据缺失时明确说明，不臆造
- 工具返回错误时尝试一次重试，仍失败则在最终答案中说明
</safety>

<user_task>
{{用户的实际问题}}
</user_task>
```

---

## 🏗 实战项目：投资分析 Agent

**要求**：
- 工具：实时行情 API + 财报 API + 新闻搜索 API + 计算器
- 功能：用户问"X 股票值得关注吗"，Agent 自动规划、调工具、综合分析
- 输出：结构化分析报告

**验收**：
- [ ] 能独立完成至少 3 种分析请求类型
- [ ] 工具调用失败时有重试 / 降级
- [ ] 步数上限生效，不死循环
- [ ] 最终答案包含：事实（工具获取） + 推理 + 结论 + 免责声明

---

## ✅ 本模块自检清单

- [ ] 能独立写出一个带工具调用的 Agent
- [ ] 理解 ReAct 为什么比直接调用更稳
- [ ] 懂得给 Agent 加 planning 和终止条件
- [ ] 完成投资分析 Agent 实战

---

## 📎 推荐资源

- [Anthropic Tool Use 完整指南](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- [调试遇到问题？](../cheatsheets/debugging.md) — 工具调用不稳定 / 死循环查这里

---

## 📝 我的笔记
