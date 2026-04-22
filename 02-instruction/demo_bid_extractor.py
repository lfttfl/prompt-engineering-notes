"""
模块 2 · 核心技法 — 招投标关键信息提取器

演示要点:
    - Few-shot + CoT + XML delimiter
    - <thinking> 强制模型先推理
    - 解析失败时自动 retry
"""

import json
import re

import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.syntax import Syntax

load_dotenv()
console = Console()
MODEL = "claude-sonnet-4-6"


SYSTEM_PROMPT = """<role>
你是一位资深招投标分析师,擅长从标书中快速定位关键信息。
</role>

<task>
从 <document> 中提取关键字段,以 JSON 格式输出。
</task>

<schema>
{
  "项目名称": "string | null",
  "招标方": "string | null",
  "预算金额": "string | null",
  "截止日期": "YYYY-MM-DD HH:MM | null",
  "交付期": "string | null",
  "资质要求": ["string"],
  "技术要求": ["string"],
  "特别关注事项": ["string"]
}
</schema>

<examples>
<example>
<input>某 10kV 配电项目招标,预算 300 万元,要求通过 ISO9001 认证。
投标截止:2026 年 5 月 15 日 14:00。</input>
<output>
<thinking>
- 预算:300 万元
- 截止:2026-05-15 14:00
- 资质:ISO9001
- 其他字段未提及,填 null/空数组
</thinking>
<json>
{
  "项目名称": null,
  "招标方": null,
  "预算金额": "300 万元",
  "截止日期": "2026-05-15 14:00",
  "交付期": null,
  "资质要求": ["ISO9001"],
  "技术要求": [],
  "特别关注事项": []
}
</json>
</output>
</example>
</examples>

<rules>
- 严格只从原文提取,未提及的字段填 null 或空数组
- 不要编造任何原文没有的信息
- 日期标准化为 YYYY-MM-DD HH:MM 格式
- "特别关注事项"收集原文中非常规条款
</rules>

<output_format>
必须以这个结构输出:
<thinking>推理过程</thinking>
<json>合法 JSON</json>
</output_format>
"""


def _extract_json(text: str) -> dict:
    match = re.search(r"<json>\s*(.*?)\s*</json>", text, re.DOTALL)
    if not match:
        match = re.search(r"(\{.*\})", text, re.DOTALL)
    if not match:
        raise ValueError(f"无法提取 JSON: {text[:200]}")
    return json.loads(match.group(1))


def extract_bid_info(document: str, max_retries: int = 2) -> dict:
    client = anthropic.Anthropic()
    user_msg = f"<document>\n{document}\n</document>"

    last_err = None
    for attempt in range(max_retries + 1):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=2000,
                temperature=0.0,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_msg}],
            )
            return _extract_json(resp.content[0].text)
        except (json.JSONDecodeError, ValueError) as e:
            last_err = e
            if attempt < max_retries:
                console.print(f"[yellow]解析失败,retry {attempt + 1}[/yellow]")
                user_msg += f"\n\n<!-- 上次输出解析失败({e}),请严格按 <json> 标签输出合法 JSON -->"
    raise last_err


SAMPLE = """
某市政新能源汽车充电站建设项目招标公告

招标方:某市城市建设投资有限公司
项目编号:CS-2026-0418

一、项目概况
本项目拟建设 20 个新能源汽车充电站,配套 10kV 进线配电设备。
总预算:人民币 1,200 万元(含税)。

二、工期要求
合同签订后 120 日历天内完成全部供货及安装。

三、投标人资格要求
1. 具有独立法人资格,注册资本不低于 3000 万元;
2. 具有电力施工总承包三级及以上资质;
3. 通过 ISO9001、ISO14001、ISO45001 三体系认证;
4. 近 3 年有 2 个及以上类似项目业绩(单个合同额不低于 500 万)。

四、技术要求
1. 充电设备必须符合 GB/T 18487.1-2015 标准;
2. 配电柜采用环保气体绝缘(SF6 替代);
3. 具备远程监控功能。

五、投标截止时间
2026 年 5 月 30 日 10:00,逾期不予受理。

六、特别说明
中标方需提供终身维护服务,首次故障响应不超过 4 小时。
"""


def demo():
    console.print("[bold cyan]🔍 正在提取招投标信息...[/bold cyan]\n")
    result = extract_bid_info(SAMPLE)
    console.print("[bold green]提取结果:[/bold green]\n")
    console.print(Syntax(json.dumps(result, ensure_ascii=False, indent=2), "json"))


if __name__ == "__main__":
    demo()
