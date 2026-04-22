# 📦 Prompt 模板库

**即拿即用** 的 Prompt 模板合集,按场景分类。每个模板都经过实战验证,替换 `{{占位符}}` 即可。

---

## 🗂 目录

### 销售与商务
- [销售邮件系列](./sales-email.md) — 首次报价 / 砍价回复 / 跟进 / 产品介绍
- [客服与咨询](./customer-service.md) — FAQ / 投诉处理 / 技术咨询
- [会议纪要](./meeting-summary.md) — 客户会议 / 内部评审
- [标书分析](./bid-analysis.md) — 招标文件关键信息提取

### 数据与分析
- [信息提取](./info-extraction.md) — 合同/邮件/PDF 结构化抽取
- [数据分析预处理](./data-analysis.md) — 为 pandas/Excel 准备数据
- [分类与标注](./classification.md) — 客户分级 / 文本分类

### 投资与财经
- [投资分析](./investment-analysis.md) — 股票/基金/财报解读

### 技术
- [代码理解](./code-explain.md) — 代码解释 / Bug 诊断 / Code Review

---

## 🎯 使用方法

### 方法 1:直接复制粘贴
1. 找到对应场景的模板
2. 替换 `{{占位符}}`
3. 扔进 Claude / ChatGPT / Gemini

### 方法 2:Python 模板变量
```python
from string import Template
from pathlib import Path

def load_template(name: str) -> Template:
    text = Path(f"templates/{name}.md").read_text(encoding="utf-8")
    # 提取 ```prompt ... ``` 代码块内容
    start = text.find("```prompt") + len("```prompt")
    end = text.find("```", start)
    return Template(text[start:end].strip())

# 使用
tpl = load_template("sales-email")
prompt = tpl.safe_substitute(customer="张经理", product="10kV 环网柜")
```

### 方法 3:Claude Projects / 自定义 GPT
把常用模板做成 Claude Project 的 custom instruction 或 GPT 的 system prompt。

---

## 📐 模板设计原则

本库所有模板遵循以下规范,可以作为你自己写模板的参考:

1. **XML 结构化**:Role / Task / Context / Rules / Examples / Input 分块清晰
2. **防注入包裹**:用户输入一律放在 `<user_input>` 标签内
3. **显式约束**:输出格式、长度、语气必须明说
4. **失败处理**:字段缺失、数据冲突怎么办都要写清楚
5. **可测试**:模板下附 Eval 提示,帮你验证输出质量

---

## 🧭 贡献你的模板

学习过程中遇到一条特别好用的 Prompt,按以下模板格式保存到这个目录:

```markdown
# 模板名称

> **场景**:...
> **适用模型**:Claude / GPT / 通用
> **测试记录**:调用了 N 次,成功率 X%

## Prompt

\`\`\`prompt
<role>...</role>
<task>...</task>
...
\`\`\`

## 使用示例
...

## 踩过的坑
...
```
