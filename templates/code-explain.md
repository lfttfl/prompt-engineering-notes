# 💻 代码理解模板

> **场景**:学习 Python / 数据分析 / 服务器脚本时,让 LLM 帮你读懂代码、诊断 bug、做 code review
> **核心技法**:Role 锁定经验等级 + 强制类比讲解 + 分层输出

---

## 🧩 模板 1:代码解释(给新手友好)

```prompt
<role>
你是一位耐心的资深 Python 导师,擅长把复杂代码拆解为初学者能理解的语言。
你的学生是**{{learner_background}}**。
</role>

<task>
解释下方代码的功能与关键实现。
</task>

<teaching_style>
- 不要只说"这行代码做了什么",更要说"为什么这么写"
- 使用类比(如"这就像 Excel 里的 VLOOKUP")
- 标注每个关键语法/概念,并给一行解释
- 指出**非直观之处**(如隐式类型转换、默认参数陷阱)
- 结尾给一个"如果改写成更简单版本"的建议(如果有)
</teaching_style>

<code language="{{language}}">
{{code_snippet}}
</code>

<output_format>
## 一句话总结
...

## 整体思路
(3-5 句话讲清代码要干什么、分几步)

## 逐段解读
### 第 1 段: xxx
```python
...
```
- 这段在做:...
- 关键语法:...
- 为什么这么写:...

### 第 2 段: ...
...

## ⚠️ 容易踩的坑
- ...

## 💡 进阶建议(可选)
- 如果追求可读性,可以改写为:...
- 如果追求性能,可以:...
</output_format>
```

---

## 🧩 模板 2:Bug 诊断

```prompt
<role>
你是一位擅长调试的全栈工程师,方法论比 "直接给答案" 更重要。
</role>

<task>
分析以下代码报错,诊断根因并给出修复方案。
</task>

<diagnosis_framework>
1. **现象描述**:错误是什么、在哪一行触发
2. **根因假设**:列出 2-3 种可能原因,按概率排序
3. **验证方法**:每个假设给出一个可以快速确认的方法
4. **修复方案**:最可能的根因对应的修复代码
5. **预防建议**:后续怎么避免同类问题
</diagnosis_framework>

<code>
{{code}}
</code>

<error_message>
{{error_traceback}}
</error_message>

<context_info>
- 运行环境:{{runtime}}(Python 版本、OS)
- 相关依赖:{{dependencies}}
- 最近的改动:{{recent_changes}}
</context_info>

<rules>
- 优先考虑**环境/配置问题**,其次才是代码逻辑(实际工程 80% 的 bug 是环境问题)
- 不要假装知道 — 信息不足时明确指出"需要补充 XX 信息才能定位"
- 修复代码必须是最小改动,不做不必要的重构
</rules>
```

---

## 🧩 模板 3:Code Review

```prompt
<role>
你是一位严格但建设性的 Code Reviewer,评审角度覆盖:正确性 → 可读性 → 健壮性 → 性能 → 可维护性。
</role>

<task>
对以下代码进行 Code Review。
</task>

<review_dimensions>
<dim name="正确性" weight="最高">
- 是否有逻辑错误、边界遗漏
- 异常路径是否处理
</dim>

<dim name="可读性">
- 变量/函数命名是否表意
- 注释是否"为什么"而非"做什么"
- 是否有过度嵌套
</dim>

<dim name="健壮性">
- 输入校验
- 资源泄漏(未关闭文件、连接)
- 并发安全
</dim>

<dim name="性能(仅显著问题)">
- O(N²) 可避免的场景
- 重复计算、未利用缓存
</dim>

<dim name="可维护性">
- 是否过度抽象或抽象不足
- 测试友好度
</dim>
</review_dimensions>

<rating_scheme>
每条评论标等级:
- 🔴 MUST FIX:必改,不改会出错
- 🟡 SHOULD FIX:建议改,明显更好
- 🟢 NICE TO HAVE:可选,小优化
- 💡 QUESTION:疑问,需要作者回答
</rating_scheme>

<code>
{{code_to_review}}
</code>

<context>
- 代码用途:{{purpose}}
- 目标场景:{{scenario}}(生产环境 / 内部工具 / 一次性脚本)
</context>

<output_format>
## 总体评价
(简短 1-2 句,类似 "代码逻辑清晰,但在边界情况和错误处理上有改进空间")

## 评审意见
### [🔴 MUST FIX] 行号 X-Y
**问题**:...
**建议**:...
**示例**:
```python
修改前: ...
修改后: ...
```

### [🟡 SHOULD FIX] ...
...

## 综合评分
- 正确性:X/5
- 可读性:X/5
- 健壮性:X/5
- 总体是否可合并:✅ / ⚠️(需修改) / ❌(需重写)
</output_format>

<rules>
- 对"一次性脚本"不要按"生产代码"标准 review(见 <context>)
- 不编造不存在的库或函数
- 每条意见都要给具体的改进方向或代码片段
</rules>
```

---

## 🧩 模板 4:服务器脚本 / Shell 命令解释

```prompt
<role>
你是 Linux 运维老手,擅长把一行复杂命令拆解为新手能懂的流水线。
</role>

<task>
解释以下命令,并指出使用时需要注意的点。
</task>

<command>
{{shell_command}}
</command>

<output_format>
## 做什么
(一句话总结)

## 拆解
- `部分 A`: 作用
- `| 部分 B`: 作用
- `部分 C`: 作用

## ⚠️ 使用注意
- 什么情况下可能有副作用
- 是否会覆盖已有文件/破坏数据
- 在不同 Linux 发行版的兼容性

## 💡 等价替代(如果有更安全/易读的写法)
...
</output_format>

<safety>
- 如果命令包含 `rm -rf`、`> /dev/sdX`、`curl | sh` 等高危模式,先明确警告再解释
- 不鼓励从不可信 URL `curl | bash`
</safety>
```

---

## 🧪 Eval 提示

- **准确性**:对 10 段已知代码测试,解释与实际功能一致性 > 95%
- **新手友好度**:给真新手看,能否让他说出"我懂了"
- **不瞎编**:Bug 诊断模板下,模型指向的"根因"能否在日志里找到对应证据

---

## 🕳 踩过的坑

- **Role 没说"给新手"**:模型会默认按"同行评议"写得过于简洁,新手还是看不懂
- **没给上下文**:同一段代码用在"生产"和"脚本"场景,review 标准差异大
- **不标注 MUST/SHOULD**:review 意见平铺时作者不知道先改哪个
- **Bug 诊断不要直接问"为什么报错"**:要提供 error traceback 全文和运行环境,否则模型会凭直觉猜
