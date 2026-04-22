# 🏷 分类与标注模板

> **场景**:客户意向分级、文本情感、意图识别、标签打标
> **核心技法**:Few-shot + CoT + 明确标签定义

---

## 🧩 模板 1:客户意向分级(A/B/C/D)

```prompt
<role>
你是一位销售运营专家,擅长从客户沟通记录中判断意向等级。
</role>

<task>
根据客户沟通记录,将其意向分为 A/B/C/D 四级。
</task>

<label_definition>
- **A 级(热)**:明确预算、明确时间(3 个月内)、有决策权、主动推进
- **B 级(温)**:有明确需求,但时间/预算未定,在多家比较中
- **C 级(冷)**:在搜集信息,无明确时间表,需持续培育
- **D 级(无效)**:非目标客户、随口询问、已明确放弃
</label_definition>

<examples>
<example>
<input>
张经理:你们 10kV 环网柜的交期能做到多快?我们 6 月底前必须完成供货。预算 200 万已经批了,就等选型。
</input>
<reasoning>
- 明确时间:6 月底前 ✓
- 明确预算:200 万已批 ✓
- 决策权:说"已经批了"暗示有推进权
- 主动性:主动问交期
</reasoning>
<output>{"level": "A", "confidence": "高", "key_signals": ["明确时间","预算已批","主动问交期"]}</output>
</example>

<example>
<input>
李工:我看看你们的产品资料,我们公司可能明年有这个需求。
</input>
<reasoning>
- 时间:"可能明年" → 不明确
- 预算:未提及
- 决策权:未明确
- 主动性:被动
</reasoning>
<output>{"level": "C", "confidence": "中", "key_signals": ["时间模糊","仅搜集信息"]}</output>
</example>
</examples>

<reasoning_instruction>
先分析 4 个维度:时间紧迫度 / 预算明确度 / 决策权 / 主动性,再综合给出等级。
</reasoning_instruction>

<conversation>
{{customer_conversation}}
</conversation>

<output_format>
<reasoning>(先按 4 维度分析)</reasoning>
<output>{"level": "A|B|C|D", "confidence": "高|中|低", "key_signals": [...]}</output>
</output_format>
```

---

## 🧩 模板 2:多标签打标(例:客户关注点)

```prompt
<role>
你是市场分析师,从客户沟通中识别其关注点。
</role>

<task>
为以下客户对话打多个标签(可多选)。
</task>

<label_catalog>
- 价格敏感
- 技术规格严格
- 交付周期紧
- 品牌知名度在意
- 售后服务重视
- 环保/能耗关注
- 定制化需求
- 合作方式灵活(愿意分期/联合开发)
- 决策周期长
- 对竞品有明确偏好
</label_catalog>

<rules>
- 至少识别 1 个,最多 5 个(按重要性排序)
- 每个标签必须有原文依据
- 原文没提到的标签不要打
</rules>

<conversation>
{{text}}
</conversation>

<output_format>
{
  "labels": [
    {"tag": "价格敏感", "evidence": "原文中'能不能再便宜点'"},
    {"tag": "交付周期紧", "evidence": "原文中'下月就要'"}
  ]
}
</output_format>
```

---

## 🧩 模板 3:情感与意图识别

```prompt
<role>
你是 NLP 专家,擅长识别文本情感和用户意图。
</role>

<task>
分析以下文本的情感倾向和主要意图。
</task>

<sentiment_scale>
-2 极度不满 | -1 轻度不满 | 0 中性 | +1 积极 | +2 非常满意
</sentiment_scale>

<intent_types>
- QUERY(咨询)
- COMPLAIN(投诉)
- PRAISE(表扬)
- REQUEST_ACTION(要求行动)
- CHIT_CHAT(闲聊)
- OTHER
</intent_types>

<text>
{{text}}
</text>

<output_format>
{
  "sentiment": -2 | -1 | 0 | 1 | 2,
  "sentiment_reason": "...",
  "intent": "QUERY|COMPLAIN|...",
  "urgency": "低|中|高"
}
</output_format>
```

---

## 🧪 Eval 提示

- **分类准确率**:对 30 条黄金样本,目标 > 85%
- **置信度校准**:模型说"高"的样本,准确率应 > 模型说"低"的样本
- **边界样本**:主动在 Eval 集里放 5 条模棱两可的,看模型是否倾向某个类别

## 🕳 踩过的坑

- **类别定义模糊 = 准确率上不去**:花时间把 A/B/C/D 的边界写清,不要"差不多"
- **Few-shot 要覆盖边界**:不要只给典型 A 和典型 D,要给"像 A 又像 B"的
- **不给 reasoning 直接要 label**:模型会偏向"安全选择",反而不准
