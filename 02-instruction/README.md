# 模块 2 · 核心技法：指令工程

> **难度**：⭐⭐ 初级
> **建议周次**：第 2–3 周（约 12 小时）
> **前置**：模块 1
> **产出能力**：掌握 Few-shot / CoT / Role / Delimiters 四大技法

---

## 🎯 本模块目标

掌握覆盖 **80% 日常场景** 的四大技法，写 Prompt 从"能用"到"好用"。

---

## 💼 应用场景

| 场景 | 对应技法 |
|---|---|
| 合同 / 标书字段提取 | Few-shot + Delimiters |
| 客户意向分级标注 | Few-shot + CoT |
| 财报数据解读 | Role + CoT |
| 文案风格改写 | Few-shot |
| 技术问题诊断 | CoT + Role |

---

## 📚 核心知识点

### 1. Zero-shot vs Few-shot

- **Zero-shot**：不给任何例子，直接说任务
- **Few-shot**：给 2–5 个输入-输出示例，让模型"照猫画虎"

**经验法则**：
- 任务简单、标准 → Zero-shot 够用
- 任务有特定风格 / 格式要求 → Few-shot 准确率可提升 20%–50%
- 示例数量：通常 3–5 个最优，更多会占 token，边际递减
- **示例顺序**：最难、最有代表性的例子放最后，模型会更多参考"最近"的示例

### 2. Chain-of-Thought (CoT)

加一句神奇咒语：**"请一步步思考，先分析再给结论"**（英文："Let's think step by step"）

**原理**：强制模型把推理过程"说出来"，相当于让它在输出空间里走"更长的路径"，减少跳步导致的错误。

**适用场景**：
- 数学 / 逻辑推理
- 多因素判断（例如客户意向评估）
- 复杂分类（需权衡多条件）

### 3. Role Prompting

给模型一个身份，输出的专业性和风格会被锚定。

- Role 要具体："资深电气工程师" > "工程师" > "专家"
- Role 可叠加："你是一个资深电气工程师，同时熟悉招投标流程"
- 不适合所有场景：纯数据提取用 Role 意义不大

### 4. Delimiters（分隔符）

用明显的标记把不同部分隔开。Claude 尤其偏爱 XML：

```xml
<instruction>你的任务是...</instruction>
<user_input>{{用户输入}}</user_input>
<examples>...</examples>
```

**好处**：
- 模型更清楚哪段是指令、哪段是数据
- 防止 Prompt Injection（见模块 8）
- 便于程序化模板拼接

---

## 🛠 学习步骤

### Step 1：Zero-shot / Few-shot 对比实验（3 小时）

选一个分类任务（例：客户意向分级 A/B/C/D），做三组测试：
- Zero-shot：只描述规则
- Few-shot 3 例
- Few-shot 5 例

用 20 条真实样本跑一遍，记录准确率。

### Step 2：CoT 对比实验（2 小时）

同一个推理题，分别用：
- 直接问 → 记录答案
- 加"一步步思考" → 记录答案

观察哪种更准、更稳定。

### Step 3：Role 消融实验（2 小时）

写 3 版 Prompt：无 Role / 笼统 Role / 具体 Role，对比输出。

### Step 4：XML Delimiters 改造（2 小时）

把模块 1 写的那几条 Prompt 全部改造成 XML 结构。

### Step 5：实战项目（3 小时）

见下方。

---

## 💻 综合示例：Few-shot + CoT + Role + XML

```xml
<role>
你是一位资深招投标分析师，擅长从标书中快速定位关键信息。
</role>

<task>
从下方招标文件中提取关键信息，以 JSON 格式输出。
</task>

<examples>
<example>
<input>某配电项目，预算 300 万元，要求通过 ISO9001 认证，交付期 90 天...</input>
<output>
{
  "预算": "300 万元",
  "资质要求": ["ISO9001"],
  "项目类型": "配电",
  "交付期": "90 天"
}
</output>
</example>
</examples>

<thinking_instruction>
先列出你在文档中找到的所有候选信息，再筛选归类到对应字段。
如果某字段未找到，填 null，不要臆造。
</thinking_instruction>

<document>
{{真实招标文件}}
</document>
```

---

## 🏗 实战项目：招投标关键信息自动提取器

**要求**：给定任意一份电气类招标文件（PDF 或文本），输出结构化信息：
- 项目名称、招标方、预算范围
- 技术要求清单
- 资质要求清单
- 关键时间节点（截止日期、交付日期）
- 特殊条款

**验收标准**：
- [ ] 至少用 5 份真实标书测试
- [ ] 提取准确率 > 85%
- [ ] 遇到字段不存在时返回 `null` 而非幻觉

---

## ✅ 本模块自检清单

- [ ] 能分辨何时用 Zero-shot，何时用 Few-shot
- [ ] 会在推理类任务上本能地加 CoT
- [ ] 习惯用 XML 组织 Prompt
- [ ] 完成招投标信息提取实战

---

## 📎 推荐资源

- [Anthropic: Use XML tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)
- [Chain-of-Thought Prompting Paper](https://arxiv.org/abs/2201.11903)
- [Prompt Engineering Guide（中文）](https://www.promptingguide.ai/zh)
- [调试遇到问题？](../cheatsheets/debugging.md) — 按症状查修复方案

---

## 📝 我的笔记

<!-- 最有效的 Few-shot 例子数量、最管用的 Role 描述... -->
