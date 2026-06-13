# 模块 4 · 结构化输出与约束控制

> **难度**：⭐⭐⭐ 中级
> **建议周次**：第 6 周（约 8 小时）
> **前置**：模块 1、2
> **产出能力**：输出可被程序稳定消费的结构化数据

---

## 🎯 本模块目标

打通 **Prompt → 程序** 的通路。让 LLM 输出的东西能直接喂给 Python、SQL、API，不用人工改格式。

这是从"玩 Prompt"到"做产品"的关键一跃。

---

## 💼 应用场景

| 场景 | 价值 |
|---|---|
| 爬虫 + LLM 抽取结构化数据 | 替代正则，应对非结构化源 |
| 表单自动填充 | 客户资料、报价表、合同信息 |
| API 间数据桥接 | 自然语言 → 调用参数 |
| Python 数据分析预处理 | 非结构化文本 → DataFrame |
| 批量简历 / 标书入库 | 文档 → 数据库 |

---

## 📚 核心知识点

### 1. JSON Schema 约束

在 Prompt 里明确目标 schema，让模型按 schema 填字段。

```xml
<output_schema>
{
  "customer_name": "string",
  "order_items": [
    {
      "product": "string",
      "quantity": "integer",
      "unit_price": "number"
    }
  ],
  "total_amount": "number",
  "delivery_date": "YYYY-MM-DD or null"
}
</output_schema>
```

**进阶**：主流 API 都支持 `response_format` / `Structured Outputs`，在 API 层强制 JSON 合法。

### 2. XML 标签输出

Claude 模型对 XML 解析特别稳。适合需要"既要结构化、又要长文"的场景。

```xml
<analysis>...一大段分析...</analysis>
<risks>
  <risk level="high">...</risk>
  <risk level="low">...</risk>
</risks>
<recommendation>...</recommendation>
```

### 3. 硬约束 vs 软约束

| 类型 | 位置 | 用途 |
|---|---|---|
| 硬约束 | API 层（response_format / Tool Use） | 强制 JSON 合法、字段齐全 |
| 软约束 | Prompt 描述 | 内容质量、字段含义、边界情况 |

**组合拳**：API 保证格式，Prompt 保证内容。

### 4. 失败兜底

模型偶尔还是会输出坏 JSON。生产环境必做：
1. `try/except` 捕获 JSON 解析错误
2. 带上错误信息回灌给模型重试（"上次输出无法解析，错误：...，请修正"）
3. 最多重试 2–3 次，仍失败走人工兜底

---

## 🛠 学习步骤

### Step 1：JSON Schema Prompt（2 小时）

选一个场景（报价单 / 客户档案），设计完整 schema，写成 Prompt，测试 20 条样本。

### Step 2：API 强制 JSON（2 小时）

用 OpenAI 或 Anthropic SDK 调用：
- OpenAI：`response_format={"type": "json_object"}`
- Anthropic：用 Tool Use 定义目标 schema

```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=[{
        "name": "extract_order",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer": {"type": "string"},
                "amount": {"type": "number"}
            },
            "required": ["customer", "amount"]
        }
    }],
    tool_choice={"type": "tool", "name": "extract_order"},
    messages=[{"role": "user", "content": "..."}]
)
```

### Step 3：XML 标签实操（1 小时）

同一个任务用 XML 输出 vs JSON 输出，比较解析稳定性。

### Step 4：失败兜底机制（1 小时）

写一个 `safe_parse_json(text, max_retry=2)` 工具函数，能自动 retry。

### Step 4.5：用 Pydantic 替代手写解析（30 分钟）

生产级代码推荐用 Pydantic 代替手写 `json.loads` + 校验：

```python
from pydantic import BaseModel, field_validator
from typing import Optional
import json

class OrderItem(BaseModel):
    product: str
    quantity: int
    unit_price: float

class Order(BaseModel):
    customer_name: str
    order_items: list[OrderItem]
    total_amount: float
    delivery_date: Optional[str] = None

    @field_validator("total_amount")
    @classmethod
    def amount_must_be_positive(cls, v):
        assert v > 0, "金额必须大于 0"
        return v

# 解析 LLM 输出
raw = response.content[0].text
order = Order.model_validate_json(raw)  # 自动校验，字段不对直接报错
```

好处：字段类型自动转换，校验错误信息清晰，直接生成 JSON Schema 用于 Tool Use。

### Step 5：实战项目（2 小时）

---

## 💻 示例：PDF 简历 → JSON 抽取

```xml
<role>
你是一个简历信息抽取专家。
</role>

<task>
从下方简历文本中，提取结构化信息。
</task>

<rules>
- 严格按 schema 输出，字段缺失填 null
- 工作经验按时间倒序
- 技能分为 "硬技能" 和 "软技能"
- 不臆造信息；原文无则为 null
</rules>

<schema>
{
  "name": "string | null",
  "contact": {
    "email": "string | null",
    "phone": "string | null"
  },
  "education": [
    {"school": "string", "degree": "string", "year": "YYYY"}
  ],
  "experience": [
    {
      "company": "string",
      "title": "string",
      "start": "YYYY-MM",
      "end": "YYYY-MM or present",
      "highlights": ["string"]
    }
  ],
  "skills": {
    "hard": ["string"],
    "soft": ["string"]
  }
}
</schema>

<resume>
{{简历原文}}
</resume>
```

---

## 🏗 实战项目：批量简历结构化入库

**要求**：
- 输入：10 份不同格式的简历 PDF
- 处理：PDF 解析 → Prompt 抽取 → JSON 校验 → 入库（SQLite 或 CSV）
- 输出：可查询的简历库

**验收**：
- [ ] JSON 解析成功率 = 100%（含 retry）
- [ ] 核心字段（姓名、手机、最近公司）准确率 > 95%
- [ ] 代码 < 150 行（Python）

---

## ✅ 本模块自检清单

- [ ] 能设计清晰的 JSON Schema
- [ ] 会用 Tool Use / response_format 强制格式
- [ ] 能写健壮的失败重试逻辑
- [ ] 完成简历入库实战

---

## 📎 推荐资源

- [Anthropic Tool Use 文档](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [JSON Schema 官方文档](https://json-schema.org/)

---

## 📝 我的笔记
