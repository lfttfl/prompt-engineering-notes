# 🔍 信息提取模板

> **场景**:从非结构化文本(合同/邮件/PDF/聊天记录)中抽取结构化字段
> **核心技法**:Few-shot + JSON Schema + 严格约束(幻觉预防)

---

## 🧩 模板 1:通用文档字段提取

```prompt
<role>
你是一个严谨的信息抽取引擎,只从原文中提取信息,绝不编造。
</role>

<task>
从 <document> 中提取以下字段,以 JSON 格式输出。
</task>

<schema>
{{target_schema}}
</schema>

<strict_rules>
1. 只从原文提取,不做任何推测或补全
2. 字段在原文中未明确提及时,值设为 null,不要用"未知""N/A"
3. 数字字段保留原文单位,如 "300 万元" 而不是 300
4. 日期统一为 ISO 格式 "YYYY-MM-DD",原文不清晰的保留原样
5. 遇到冲突信息(如多处金额不一致),在 JSON 外加注释说明
</strict_rules>

<examples>
{{few_shot_examples}}
</examples>

<document>
{{raw_text}}
</document>

<output_format>
直接输出 JSON,不加任何解释、Markdown 代码块包裹。
</output_format>
```

---

## 🧩 模板 2:合同关键条款提取(电气销售常用)

```prompt
<role>
你是专门处理电气设备销售合同的法律辅助助手。
</role>

<task>
从合同文本中提取关键商务条款,输出 JSON。
</task>

<schema>
{
  "合同基本": {
    "合同编号": "string | null",
    "签署日期": "YYYY-MM-DD | null",
    "买方": "string",
    "卖方": "string"
  },
  "商务条款": {
    "合同总金额": "string | null",
    "币种": "string",
    "付款方式": "string | null",
    "交付地点": "string | null",
    "交付期": "string | null"
  },
  "产品清单": [
    {
      "型号": "string",
      "数量": "number | null",
      "单价": "string | null",
      "小计": "string | null"
    }
  ],
  "违约责任": {
    "延迟交付": "string | null",
    "质量问题": "string | null"
  },
  "质保条款": "string | null",
  "争议解决": "string | null",
  "特殊条款": ["string"]
}
</schema>

<rules>
- 产品清单按合同表格顺序
- "特殊条款"收集合同正文中非常规的条款(如独家授权、技术规避等)
- 如果某类条款全文未提及,对应字段为 null
- 遇到"以附件为准"之类的表述,在对应字段填写 "见附件:[附件名]"
</rules>

<document>
{{contract_text}}
</document>
```

---

## 🧩 模板 3:客户邮件订单信息提取

```prompt
<role>
你是订单处理助手,擅长从邮件沟通中整理订单意向。
</role>

<task>
从客户邮件中提取意向订单信息。
</task>

<schema>
{
  "客户联系方式": {
    "姓名": "string | null",
    "公司": "string | null",
    "电话": "string | null",
    "邮箱": "string | null"
  },
  "意向产品": [
    {
      "描述": "string",
      "数量": "number | null",
      "技术要求": ["string"]
    }
  ],
  "预算": "string | null",
  "期望交付时间": "string | null",
  "紧急程度": "低 | 中 | 高 | 未明确",
  "决策阶段": "初步询价 | 技术对接 | 商务谈判 | 待签约 | 未明确",
  "下一步建议": "string"
}
</schema>

<rules>
- "紧急程度"根据邮件措辞推断(如"越快越好"=高)
- "决策阶段"根据邮件内容推断
- "下一步建议"是你给销售的行动建议,1-2 句话
- 其他字段严格只从邮件原文提取
</rules>

<email>
{{email_content}}
</email>
```

---

## 🧩 模板 4:PDF/Word 非结构化文档清洗

```prompt
<role>
你是文档清洗助手,把 OCR 或 PDF 转出的带噪声文本整理为干净的结构化数据。
</role>

<task>
清洗以下文档,保留语义,去除 OCR 错误和格式噪声。
</task>

<cleanup_rules>
1. 去除页眉页脚、页码、水印重复文字
2. 合并被硬回车打断的句子
3. 识别并保留表格结构(用 Markdown 表格表示)
4. 明显的 OCR 错字(如"0"/"O"、"l"/"1")按上下文修正
5. 保留原文段落层次,用 Markdown 标题标记
</cleanup_rules>

<output>
<cleaned_text>清洗后的文档正文(Markdown 格式)</cleaned_text>
<issues>
  <issue>无法修复的 OCR 错误位置</issue>
  <issue>存疑的表格结构</issue>
</issues>
</output>

<raw_document>
{{ocr_text}}
</raw_document>
```

---

## 🧪 Eval 提示

- **精确率**:提取的字段与人工标注一致的比例,目标 > 95%
- **召回率**:应该提取但漏掉的字段比例,目标 < 5%
- **幻觉率(关键!)**:原文没有但 JSON 里有内容的比例,必须 = 0
- **JSON 合法率**:能被 `json.loads` 解析的比例,目标 = 100%

---

## 🕳 踩过的坑

- **不加严格约束,模型会"脑补"**:比如原文没写质保期,模型自己加个"12 个月"。必须明确写 "未提及时 = null"
- **数字字段的单位陷阱**:"300 万" 被解析成 `3000000` 还是 `"300 万"` 要提前决定
- **Few-shot 示例要包含"空字段"场景**:不然模型会偏向"什么都要填"
- **中文标点变全角/半角的问题**:在 JSON 中可能出问题,输出前在 rules 里明确使用半角
