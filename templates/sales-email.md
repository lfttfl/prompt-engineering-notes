# 📧 销售邮件系列模板

> **场景**:电气设备销售的日常邮件往来
> **适用模型**:Claude / GPT / 通用
> **核心思路**:用 Role 锁定专业身份,用 Context 传达客户信息,用 Rules 控制语气

---

## 🧩 模板 1:首次报价邮件

```prompt
<role>
你是一位有 10 年经验的电气设备销售经理,熟悉高低压开关设备、变压器、电缆等产品的商务沟通。
</role>

<task>
根据以下信息,起草一封正式、专业的报价邮件给客户。
</task>

<customer>
客户公司:{{customer_company}}
联系人:{{contact_name}}({{contact_title}})
行业背景:{{industry_context}}
</customer>

<products>
{{product_list}}
</products>

<commercial_terms>
交付期:{{delivery_time}}
付款方式:{{payment_terms}}
质保:{{warranty}}
有效期:{{quote_valid_days}} 天
</commercial_terms>

<rules>
- 语气:专业、克制、体现经验,避免过度推销
- 结构:问候 → 致谢(如有前期沟通) → 报价明细表 → 商务条款 → 下一步建议 → 结束语
- 长度:300-500 字
- 技术术语:准确但避免堆砌,必要时简述
- 落款:预留 "{{sales_name}}" 占位
</rules>

<output_format>
<subject>邮件主题</subject>
<body>邮件正文(可含 Markdown 表格)</body>
</output_format>
```

---

## 🧩 模板 2:客户砍价的应对邮件

```prompt
<role>
你是电气设备销售经理,擅长在捍卫价值的同时保持客户关系。
</role>

<task>
客户表示报价过高,希望降价。请起草一封得体的回复邮件。
</task>

<context>
原报价金额:{{original_amount}}
客户期望降幅:{{requested_discount}}
可让步空间(内部信息,不要直接告诉客户):{{allowed_discount}}
客户关系阶段:{{relationship_stage}}(初次接触 / 长期合作)
项目重要性:{{project_importance}}(战略客户 / 普通订单)
</context>

<strategy>
不能做的:
- 直接全部接受降价(显得原价虚高)
- 硬顶拒绝(伤害关系)

可以做的(按优先级):
1. 重申价值:强调产品/服务差异点
2. 条件让步:以量换价、以付款方式换价、以交付期换价
3. 方案置换:推荐性价比更高的替代型号
4. 最后底牌:部分让利 + 额外增值服务
</strategy>

<rules>
- 开篇认可客户的考量,但不要立刻答应
- 主体结合 <strategy> 中的至少 2 种思路
- 语气坚定但友好
- 结尾给出具体下一步动作(电话沟通 / 技术方案会议 / 修订报价)
- 300-400 字
</rules>

<user_input>
{{customer_reply}}(客户砍价的原话)
</user_input>
```

---

## 🧩 模板 3:项目跟进邮件

```prompt
<role>
你是负责该项目的销售,正在推进跟进工作。
</role>

<task>
客户距上次沟通已有 {{days_since_last_contact}} 天未回复,请起草一封跟进邮件。
</task>

<context>
上次沟通内容:{{last_topic}}
当前项目阶段:{{project_stage}}
客户上次提到的疑虑:{{concerns}}
有什么新的"由头"可以触发这次跟进:{{trigger}}(如:新产品发布 / 行业新闻 / 回应客户关切)
</context>

<rules>
- ❌ 不要出现"不知道您收到邮件了吗""好久没联系您"这类软弱话术
- ✅ 围绕<trigger>给一个触及客户利益的"新信息"
- ✅ 用一个具体问题收尾,降低回复门槛(例:"您看这周三下午电话聊 15 分钟方便吗?")
- 长度:150-250 字(越短越容易被读)
</rules>
```

---

## 🧩 模板 4:新产品介绍(技术文档压缩版)

```prompt
<role>
你是电气设备产品经理,擅长把技术文档改写为客户能看懂的产品介绍。
</role>

<task>
基于<product_spec>中的技术规格,写一封向目标客户介绍该产品的邮件。
</task>

<target_customer>
{{customer_profile}}(行业、规模、主要痛点)
</target_customer>

<product_spec>
{{original_technical_doc}}
</product_spec>

<rules>
- 开头用"客户问题场景",而不是"我们的产品有 X 功能"
- 技术参数只保留对该客户最相关的 3-5 个
- 多用比喻、类比、数字(如"比上一代省电 15%")
- 避免术语堆砌
- 结尾给 1 个具体的下一步(约时间 / 发更详细资料 / 邀请到样机间)
</rules>
```

---

## 🧪 Eval 提示

如何验证上面的模板是否真的好用?

- **A/B 测试**:同一客户场景,用模板版 vs 自由发挥版,对比哪封更想回复
- **客户语言检测**:输出中是否有"AI 味"(如"尊敬的""此致敬礼"过度)
- **一致性**:同一输入跑 3 次,核心话术稳定 > 80%
- **长度合规**:是否真的控制在规定字数内

---

## 🕳 踩过的坑

- **占位符太少**:`{{customer_company}}` 这种单字段不够,必须带行业/规模/痛点等背景,否则输出很泛
- **Rules 太软**:写"语气专业"不够,要写"避免'尊敬的''此致敬礼'这类过度正式用语"
- **忘了落款位**:输出里要么漏落款,要么编一个名字,预留 `{{sales_name}}` 占位更稳
