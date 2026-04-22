# 📐 XML 标签速查表

> Claude 对 XML 标签解析最稳。常用标签见下表。
> 自定义标签名没有"官方列表",但以下命名是社区共识。

---

## 🏗 结构性标签(一个 Prompt 几乎必备)

| 标签 | 用途 | 示例 |
|---|---|---|
| `<role>` | 定义模型角色 | `<role>你是资深电气工程师</role>` |
| `<task>` | 说明要做什么 | `<task>从合同中提取关键条款</task>` |
| `<context>` | 背景信息 | `<context>客户是国企,预算 500 万</context>` |
| `<instruction>` | 核心指令 | `<instruction>按 JSON 格式输出</instruction>` |
| `<rules>` | 规则约束 | `<rules>不臆造、缺失值填 null</rules>` |

---

## 📥 输入数据标签(与指令隔离,防注入)

| 标签 | 用途 |
|---|---|
| `<user_input>` | 用户输入(**必须 XML 包裹!**) |
| `<document>` | 待处理文档 |
| `<data>` | 结构化数据(JSON/CSV) |
| `<email>` | 邮件内容 |
| `<code>` | 代码片段 |
| `<conversation>` | 对话历史 |
| `<image_description>` | 图片描述(文字版) |

---

## 🎭 示例与格式标签

| 标签 | 用途 |
|---|---|
| `<examples>` `<example>` | Few-shot 示例容器 |
| `<input>` `<output>` | 示例内部的输入/输出 |
| `<reasoning>` | 示例或输出的推理过程 |
| `<output_format>` | 规定输出格式 |
| `<schema>` | JSON Schema / 数据结构定义 |

---

## 🧠 推理引导标签

| 标签 | 用途 |
|---|---|
| `<thinking>` | 让模型在这里展开思考(CoT) |
| `<step_back>` | Step-back 推理:先想通用原理 |
| `<analysis>` | 分析过程 |
| `<answer>` `<final_answer>` | 最终答案 |
| `<reasoning_instruction>` | 告诉模型"怎么思考" |

---

## 🛡 安全与高优标签

| 标签 | 用途 |
|---|---|
| `<system_rules priority="highest">` | 最高优先级规则(防注入) |
| `<safety>` | 安全相关指令 |
| `<forbidden>` | 明确禁止事项 |
| `<disclaimer>` | 免责声明(投资、医疗) |

---

## 🤖 Agent / 工具调用标签

| 标签 | 用途 |
|---|---|
| `<plan>` | Agent 执行前的计划 |
| `<thought>` | ReAct 中的思考步骤 |
| `<action>` | 调用的工具 |
| `<observation>` | 工具返回结果 |
| `<available_tools>` | 列出可用工具 |

---

## 🎯 惯用组合模板

### 最小可行 Prompt
```xml
<role>...</role>
<task>...</task>
<user_input>...</user_input>
```

### 标准信息提取
```xml
<role>...</role>
<task>...</task>
<schema>...</schema>
<examples>
  <example><input>...</input><output>...</output></example>
</examples>
<document>...</document>
<output_format>...</output_format>
```

### 带防注入的客服
```xml
<system_rules priority="highest">...</system_rules>
<role>...</role>
<knowledge_base>...</knowledge_base>
<user_input>...</user_input>
```

### Agent 运行循环
```xml
<role>...</role>
<available_tools>...</available_tools>
<plan>...</plan>
<thought>...</thought>
<action>...</action>
<observation>...</observation>
<final_answer>...</final_answer>
```

---

## ⚠️ 三条红线

1. **用户输入必须 XML 包裹** — 直接字符串拼接 = 裸奔
2. **标签要闭合** — `<role>...</role>` 不要漏斜杠
3. **嵌套不要超过 3 层** — 深嵌套模型反而容易乱
