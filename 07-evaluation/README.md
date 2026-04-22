# 模块 7 · 评估与迭代优化

> **难度**：⭐⭐⭐⭐ 高级
> **建议周次**：第 11 周（约 10 小时）
> **前置**：模块 1–6
> **产出能力**：量化 Prompt 质量，系统性调优

---

## 🎯 本模块目标

告别"改改试试感觉不错"。建立可量化、可回归的评估体系。

一句话：**没有评估的 Prompt，不是工程。**

---

## 💼 应用场景

| 场景 | 为什么需要评估 |
|---|---|
| Prompt 改版 | 新版真的比旧版好吗？ |
| 模型选型 | GPT / Claude / Gemini 谁更适合本任务？ |
| 生产回归 | 改了一个字段会不会影响其他输出？ |
| 成本优化 | 能不能换小模型不掉准确率？ |

---

## 📚 核心知识点

### 1. 构建 Eval 集（黄金样本）

**原则**：
- **量**：初期 20–50 条够用，产品化后扩到 200+
- **质**：覆盖常见场景 + 边界场景 + 已知失败案例
- **分层**：按难度 / 类型打标签，便于分析

**结构示例**：

```jsonl
{"id": "E001", "input": "...", "expected": "...", "tags": ["easy", "extraction"]}
{"id": "E002", "input": "...", "expected": "...", "tags": ["hard", "reasoning"]}
```

### 2. 三种评估方式

| 类型 | 适用 | 成本 | 可靠性 |
|---|---|---|---|
| **Rule-based** | 格式、字段、正则、数值 | 几乎为零 | 高（但只能评"形") |
| **Pairwise** | 两版本 A/B 比选 | 中（人力或 LLM 裁判) | 中-高 |
| **LLM-as-Judge** | 主观质量、长文本 | 中 | 中（有偏见) |

### 3. LLM-as-Judge 的陷阱与对策

**已知偏见**：
- **位置偏见**：倾向于先出现的答案 → 随机两次交换位置取平均
- **长度偏见**：倾向于更长的答案 → 评分时明确"简洁性"纳入
- **同源偏见**：裁判模型偏爱自家模型输出 → 用不同厂商的模型当裁判

**Rubric 评分模板**：

```xml
<rubric>
对答案从以下维度打 1-5 分：
- 准确性：信息是否符合输入
- 完整性：是否覆盖所有要求字段
- 简洁性：是否冗余
- 专业性：术语使用是否恰当
</rubric>
```

### 4. 建立 Baseline + 回归测试

每改一版 Prompt：
1. 在完整 Eval 集上跑 baseline 分数（旧版）
2. 跑新版分数
3. 对比：**整体提升 + 分类别细看**（有没有某类任务反而变差）
4. 只有**综合得分提升 + 关键类别不退步**才上线

### 5. 常见指标

- **准确率 / F1**：分类、抽取任务
- **Exact Match**：短答案
- **BLEU / ROUGE**：翻译、摘要（但对 LLM 参考价值有限）
- **Pass@k**：允许多次尝试的场景（如代码生成）
- **人工打分 / LLM 打分均值**：主观任务

---

## 🛠 学习步骤

### Step 1：构建 Eval 集（2 小时）

回到模块 2 的"招投标信息提取"，手工标注 30 条样本：
- 10 条简单（常见字段齐全）
- 10 条中等（部分字段缺失）
- 10 条困难（格式非标、有干扰信息）

### Step 2：Rule-based 评估脚本（2 小时）

写 Python 脚本：
```python
def evaluate(prompt_version, eval_set):
    results = []
    for item in eval_set:
        output = call_llm(prompt_version, item["input"])
        score = rule_check(output, item["expected"])
        results.append(score)
    return {
        "accuracy": sum(results) / len(results),
        "by_tag": group_by_tag(results)
    }
```

### Step 3：LLM-as-Judge 实现（3 小时）

对同一组输出，用另一个强模型按 Rubric 打分。实现"交换位置 + 平均"对抗位置偏见。

### Step 4：回归测试工作流（2 小时）

建立 `prompts/v1.md`, `prompts/v2.md`...，每改一版都跑完整 Eval，结果存 CSV 对比。

### Step 5：实战项目（1 小时）

---

## 💻 示例：LLM-as-Judge Prompt

```xml
<role>
你是一个严格的评审员，根据 rubric 对答案打分。
</role>

<task>
针对同一问题的两个答案，分别打分并选出更好的一个。
</task>

<rubric>
对每个答案从以下维度 1-5 分打分：
1. 准确性：信息是否正确
2. 完整性：是否覆盖所有要求
3. 简洁性：无冗余
4. 格式合规：是否符合指定格式

最终综合分 = 四项平均。
</rubric>

<question>{{question}}</question>

<answer_a>{{answer_a}}</answer_a>

<answer_b>{{answer_b}}</answer_b>

<output_format>
<scores_a>
  accuracy: X
  completeness: X
  conciseness: X
  format: X
  总分: X.X
</scores_a>
<scores_b>...</scores_b>
<winner>A / B / tie</winner>
<reason>简述理由</reason>
</output_format>
```

---

## 🏗 实战项目：给现有 Prompt 建 Eval 体系

**要求**：选之前任一模块的实战项目（推荐模块 2 招投标提取），建立：

1. Eval 集（30 条带标注）
2. Rule-based 评估脚本
3. LLM-as-Judge 脚本
4. 回归报告模板（Markdown / CSV）

**然后**：迭代 3 版 Prompt，记录每版分数变化。

**验收**：
- [ ] Eval 集覆盖简单/中/难三档
- [ ] 新版 Prompt 在综合分上 > 旧版 ≥ 10%
- [ ] 回归报告能一眼看出哪类任务变好/变差

---

## ✅ 本模块自检清单

- [ ] 能独立构建 Eval 集
- [ ] 会写 Rule-based 评估代码
- [ ] 理解 LLM-as-Judge 的偏见及对策
- [ ] 建立了自己的回归测试工作流

---

## 📎 推荐资源

- [Anthropic: Create strong empirical evaluations](https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests)
- [Promptfoo（开源 Prompt 评估工具）](https://www.promptfoo.dev/)
- [LangSmith Evaluations](https://docs.smith.langchain.com/evaluation)
- [Eugene Yan: Evaluating LLM Applications](https://eugeneyan.com/writing/evals/)

---

## 📝 我的笔记
