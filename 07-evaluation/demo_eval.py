"""
模块 7 · 评估与迭代优化 — Eval 脚本骨架

演示:
    - Eval 集(简易 JSONL 风格)
    - Rule-based 精确匹配评估
    - LLM-as-Judge(含位置互换消偏)
    - 版本对比报告(rich Table)
"""

import json
import re
from statistics import mean
from typing import Callable

import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()
console = Console()
JUDGE_MODEL = "claude-sonnet-4-6"


# ================== Eval 集示例 ==================

EVAL_SET = [
    {"id": "E001", "input": "预算 300 万,截止 2026-05-15 14:00",
     "expected": {"预算": "300 万", "截止": "2026-05-15 14:00"}, "tags": ["easy"]},
    {"id": "E002", "input": "某项目要求 ISO9001,工期 90 天",
     "expected": {"资质": ["ISO9001"], "工期": "90 天"}, "tags": ["medium"]},
    {"id": "E003", "input": "本次招标无明确预算",
     "expected": {"预算": None}, "tags": ["hard", "null_handling"]},
]


# ================== Rule-based 评估 ==================

def rule_based_score(actual: dict, expected: dict) -> float:
    if not expected:
        return 1.0
    total = len(expected)
    correct = sum(1 for k, v in expected.items() if k in actual and actual[k] == v)
    return correct / total


def evaluate(prompt_fn: Callable[[str], dict], eval_set: list) -> dict:
    scores = []
    by_tag = {}
    for item in eval_set:
        try:
            actual = prompt_fn(item["input"])
            score = rule_based_score(actual, item["expected"])
        except Exception as e:
            console.print(f"[red]{item['id']} 失败: {e}[/red]")
            score = 0.0
        scores.append(score)
        for tag in item.get("tags", []):
            by_tag.setdefault(tag, []).append(score)

    return {
        "overall": mean(scores),
        "by_tag": {tag: mean(s) for tag, s in by_tag.items()},
    }


# ================== LLM-as-Judge(含位置互换消偏) ==================

JUDGE_RUBRIC = """你是严格的评审员。对两个答案从以下维度打分(1-5):
- accuracy: 信息是否正确
- completeness: 是否覆盖所有要求
- conciseness: 无冗余
- format: 符合指定格式
综合分 = 四项平均。

<question>{question}</question>
<answer_a>{a}</answer_a>
<answer_b>{b}</answer_b>

只输出 JSON,格式:
{{"scores_a": {{"accuracy":X,"completeness":X,"conciseness":X,"format":X,"总分":X.X}},
  "scores_b": {{...}},
  "winner": "A" | "B" | "tie",
  "reason": "..."}}
"""


def llm_judge(question: str, a: str, b: str) -> dict:
    """位置互换 2 次取多数,消除位置偏见"""
    client = anthropic.Anthropic()
    verdicts = []
    for first, second, swap in [(a, b, False), (b, a, True)]:
        resp = client.messages.create(
            model=JUDGE_MODEL,
            max_tokens=800,
            temperature=0.0,
            messages=[{"role": "user",
                       "content": JUDGE_RUBRIC.format(question=question, a=first, b=second)}],
        )
        raw = resp.content[0].text
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        verdict = json.loads(m.group(0))
        if swap:
            verdict["winner"] = {"A": "B", "B": "A", "tie": "tie"}[verdict["winner"]]
            verdict["scores_a"], verdict["scores_b"] = verdict["scores_b"], verdict["scores_a"]
        verdicts.append(verdict)

    winners = [v["winner"] for v in verdicts]
    final = winners[0] if winners[0] == winners[1] else "tie"
    return {"final_winner": final, "verdicts": verdicts}


# ================== 版本对比 ==================

def render_report(v1: dict, v2: dict):
    def delta(a, b):
        diff = b - a
        arrow = "↑" if diff > 0 else ("↓" if diff < 0 else "=")
        return f"{diff:+.2%} {arrow}"

    table = Table(title="Prompt 版本对比")
    table.add_column("维度")
    table.add_column("v1")
    table.add_column("v2")
    table.add_column("变化")
    table.add_row("整体", f"{v1['overall']:.2%}", f"{v2['overall']:.2%}",
                  delta(v1['overall'], v2['overall']))
    for tag in sorted(set(v1['by_tag']) | set(v2['by_tag'])):
        a = v1['by_tag'].get(tag, 0)
        b = v2['by_tag'].get(tag, 0)
        table.add_row(f"  [{tag}]", f"{a:.2%}", f"{b:.2%}", delta(a, b))
    console.print(table)


# ================== Mock Prompt 实现(两个版本) ==================

def prompt_v1(text: str) -> dict:
    """v1: 简易规则,不处理 null"""
    result = {}
    if m := re.search(r"预算\s*(\S+\s*万)", text):
        result["预算"] = m.group(1).strip()
    if m := re.search(r"(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2})", text):
        result["截止"] = m.group(1).strip()
    if m := re.search(r"(ISO\d+)", text):
        result["资质"] = [m.group(1)]
    if m := re.search(r"工期\s*(\d+\s*天)", text):
        result["工期"] = m.group(1).strip()
    return result


def prompt_v2(text: str) -> dict:
    """v2: 改进版,处理 null"""
    result = prompt_v1(text)
    if "无明确预算" in text:
        result["预算"] = None
    return result


def demo():
    console.print("[bold cyan]📊 评估 v1 ...[/bold cyan]")
    v1 = evaluate(prompt_v1, EVAL_SET)
    console.print(f"整体: {v1['overall']:.2%}")

    console.print("\n[bold cyan]📊 评估 v2 ...[/bold cyan]")
    v2 = evaluate(prompt_v2, EVAL_SET)
    console.print(f"整体: {v2['overall']:.2%}\n")

    render_report(v1, v2)

    console.print("\n[dim]// LLM-as-Judge 示例见 llm_judge() 函数,使用请取消注释[/dim]")
    # verdict = llm_judge("总结以下", "答案 A", "答案 B")
    # console.print(verdict)


if __name__ == "__main__":
    demo()
