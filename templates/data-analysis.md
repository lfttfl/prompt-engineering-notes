# 📊 数据分析预处理模板

> **场景**:把 LLM 用作 pandas/Excel 的"前处理助手",把非结构化数据变成能跑数据分析的干净数据
> **核心技法**:结构化输出 + 数据类型规范 + 与 Python 无缝衔接

---

## 🧩 模板 1:把"自然语言描述"转成查询条件

**场景**:你在做销售数据分析,老板扔给你一句"帮我看下 Q1 华东区 A 类客户的订单金额",你想让 LLM 把它转成 DataFrame 筛选条件。

```prompt
<role>
你是数据分析助手,把业务人员的自然语言需求翻译为 pandas 查询代码。
</role>

<task>
根据用户问题,生成能在 DataFrame 上执行的代码。
</task>

<schema>
可用的 DataFrame 叫 `df`,字段如下:
{{dataframe_schema}}
例如:
- customer_name (str)
- region (str, 值域: 华东/华北/华南/西部)
- customer_level (str, 值域: A/B/C/D)
- order_date (datetime)
- order_amount (float)
- product (str)
</schema>

<rules>
1. 只输出可执行的 pandas 代码,不加解释
2. 日期字段用 `pd.Timestamp` 处理
3. 对字符串字段用 `.str.contains` 时考虑大小写
4. 最终结果赋值给变量 `result`
5. 如果用户问题有歧义,在代码下方用 `# 假设: ...` 注明
</rules>

<user_question>
{{question}}
</user_question>

<output_format>
```python
# 代码
result = df[...]
# 假设: ...(如有)
```
</output_format>
```

---

## 🧩 模板 2:异构数据统一格式

**场景**:不同来源的 Excel 里"金额"字段有 `"300万"`、`"3,000,000 元"`、`"¥3000000"`,需要统一成数字。

```prompt
<role>
你是数据清洗助手,专注把形态各异的原始字段标准化。
</role>

<task>
将以下字段值标准化为目标格式。
</task>

<normalization_rules>
字段:{{field_name}}
目标格式:{{target_format}}(例:数值类型,单位:元)

标准化规则:
- "X 万" → X * 10000
- "X 万元"、"¥X" → 去掉单位
- 千位分隔符 "," 去除
- 科学计数法展开
- 空、"-"、"N/A" → null
- 范围值(如 "100-200 万") → {"min": X, "max": Y}
</normalization_rules>

<examples>
<example><raw>300 万</raw><std>3000000</std></example>
<example><raw>¥3,000,000</raw><std>3000000</std></example>
<example><raw>-</raw><std>null</std></example>
<example><raw>100-200 万</raw><std>{"min": 1000000, "max": 2000000}</std></example>
</examples>

<raw_values>
{{value_list}}(JSON 数组)
</raw_values>

<output_format>
输出同长度的 JSON 数组,每项是标准化后的值。
</output_format>
```

---

## 🧩 模板 3:异常检测与数据质量报告

```prompt
<role>
你是数据质量分析师,擅长从一份 DataFrame 样本中发现异常。
</role>

<task>
检查数据,输出质量报告。
</task>

<sample>
{{df_sample_head}}(DataFrame 的 describe() 和前 20 行)
</sample>

<checks_to_perform>
1. **类型一致性**:同列数据类型是否统一
2. **极端值**:IQR 法则下的离群点
3. **缺失值**:每列缺失比例
4. **重复行**
5. **业务异常**:
   - 日期未来时间(超过当前日期)
   - 负数出现在不应为负的字段(如金额)
   - 枚举字段有未知值
   - 跨字段一致性(如单价 × 数量 ≠ 总金额)
</checks_to_perform>

<output_format>
## 数据概览
- 行数 / 列数 / 数据类型简报

## 🚨 高优先级问题(必须处理)
- ...

## ⚠️ 中等问题(建议处理)
- ...

## 💡 观察到的数据特征
- ...

## 推荐处理代码(pandas)
```python
# 针对上述问题的清洗代码骨架
...
```
</output_format>
```

---

## 🧩 模板 4:数据分析结论生成(从图表到文字)

```prompt
<role>
你是数据分析师,擅长把数字和图表翻译成业务能听懂的洞察。
</role>

<task>
基于以下数据,写一段 3-5 句的分析结论。
</task>

<style>
- ❌ 避免:"从数据可以看出...""总体来说呈上升趋势..."(废话)
- ✅ 用:具体数字 + 对比 + 可行动建议
- 例:"华东区 Q1 订单均价较去年同期下降 12%,主要是中标单价偏低的公建项目占比从 30% 升到 45%;建议销售团队 Q2 适度提高工业客户比重。"
</style>

<data>
{{analysis_results}}(表格、指标、趋势数据)
</data>

<context>
- 业务场景:{{business_context}}
- 分析目的:{{analysis_purpose}}
- 受众:{{audience}}(老板汇报 / 团队例会 / 客户提案)
</context>

<rules>
- 每个结论必须回溯到具体数据
- 给至少 1 条"下一步行动"建议
- 根据 <audience> 调整专业术语密度
</rules>
```

---

## 🧪 Eval 提示

- **代码可执行率**:生成的 pandas 代码能直接运行比例 > 95%
- **数据清洗正确率**:对 100 条测试值,标准化结果与人工一致 > 98%
- **结论回溯性**:随机抽 5 条分析结论,都能在原始数据里找到支撑

## 🕳 踩过的坑

- **Schema 必须真实**:把你的 DataFrame 的 `df.dtypes` 和 `df.head()` 真贴进去,模型才会用对字段
- **日期字段最坑**:字符串日期 vs datetime 类型的差异,务必在 rules 里明说
- **输出 pandas 代码别让它加 `print`**:你自己决定怎么输出,让它只赋值给 `result`
