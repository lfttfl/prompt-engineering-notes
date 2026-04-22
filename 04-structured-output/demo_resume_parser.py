"""
模块 4 · 结构化输出 — 简历信息抽取器

演示要点:
    - Anthropic Tool Use 强制 JSON Schema
    - tool_choice 强制调用
    - 失败 retry 兜底
"""

import json

import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.syntax import Syntax

load_dotenv()
console = Console()
MODEL = "claude-sonnet-4-6"


RESUME_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": ["string", "null"]},
        "contact": {
            "type": "object",
            "properties": {
                "email": {"type": ["string", "null"]},
                "phone": {"type": ["string", "null"]},
                "location": {"type": ["string", "null"]},
            },
        },
        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "school": {"type": "string"},
                    "degree": {"type": "string"},
                    "major": {"type": ["string", "null"]},
                    "year": {"type": ["string", "null"]},
                },
                "required": ["school", "degree"],
            },
        },
        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "company": {"type": "string"},
                    "title": {"type": "string"},
                    "start": {"type": ["string", "null"]},
                    "end": {"type": ["string", "null"]},
                    "highlights": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["company", "title"],
            },
        },
        "skills": {
            "type": "object",
            "properties": {
                "hard": {"type": "array", "items": {"type": "string"}},
                "soft": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
    "required": ["name", "education", "experience", "skills"],
}

RESUME_TOOL = {
    "name": "extract_resume",
    "description": "从简历文本中提取结构化信息",
    "input_schema": RESUME_SCHEMA,
}

SYSTEM = """你是一位专业的简历信息抽取专家。

规则:
- 严格按 schema 输出,字段缺失时用 null 或空数组
- 工作经验按时间倒序排列
- 硬技能(如 Python、SQL)和软技能(如沟通、领导力)分开
- 不要臆造原文没有的信息
- 日期使用 YYYY-MM 格式,在职使用 "present"
"""


def parse_resume(resume_text: str, max_retries: int = 2) -> dict:
    client = anthropic.Anthropic()
    messages = [{
        "role": "user",
        "content": f"请从以下简历中提取结构化信息:\n\n{resume_text}",
    }]

    last_err = None
    for attempt in range(max_retries + 1):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=2000,
                temperature=0.0,
                system=SYSTEM,
                tools=[RESUME_TOOL],
                tool_choice={"type": "tool", "name": "extract_resume"},
                messages=messages,
            )
            for block in resp.content:
                if block.type == "tool_use":
                    return block.input
            raise ValueError("模型未调用 tool")
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                console.print(f"[yellow]解析失败,retry {attempt + 1}[/yellow]: {e}")
    raise last_err


SAMPLE = """
张三 / zhangsan@example.com / 138-0000-1234 / 北京

教育背景
2018-2022 清华大学 电气工程及其自动化 本科
2022-2024 北京航空航天大学 电力系统与自动化 硕士

工作经历
2024.07 - 至今  国家电网北京公司  配电技术工程师
- 主导 10kV 配电线路自动化改造项目 3 个,节约运维成本约 15%
- 参与编写《北京地区配电网规划技术导则》2025 版

2022.06 - 2024.06 某能源科技公司(实习)技术工程师
- 参与微网能源管理系统开发(Python + MQTT)
- 完成 5 个光伏项目的并网设计

技能
- 编程: Python, MATLAB, SQL
- 工具: ETAP, CAD, PSCAD
- 英语六级
- 具备良好的跨部门沟通和项目推进能力
"""


def demo():
    console.print("[bold cyan]📄 正在解析简历...[/bold cyan]\n")
    result = parse_resume(SAMPLE)
    console.print("[bold green]提取结果:[/bold green]\n")
    console.print(Syntax(json.dumps(result, ensure_ascii=False, indent=2), "json"))


if __name__ == "__main__":
    demo()
