"""
模块 6 · Agent 与工具调用 — 投资分析 Agent(Mock 工具版)

演示:
    - Anthropic Tool Use 闭环
    - ReAct 模式(交替 Thought / Action / Observation)
    - Planning + 步数上限
    - 工具失败兜底

⚠️ 工具返回的是 mock 数据,仅用于演示闭环。
"""

import json
from datetime import datetime

import anthropic
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()
MODEL = "claude-sonnet-4-6"


# ================== Mock 工具实现 ==================

def get_stock_price(symbol: str) -> dict:
    prices = {"601012.SH": 18.30, "600519.SH": 1680.00, "000001.SZ": 11.50}
    if symbol not in prices:
        return {"error": f"未找到股票 {symbol}"}
    return {
        "symbol": symbol,
        "price": prices[symbol],
        "currency": "CNY",
        "as_of": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def get_financials(symbol: str) -> dict:
    data = {
        "601012.SH": {"revenue_yoy": -0.08, "net_profit_yoy": -0.45,
                       "gross_margin": 0.18, "pe_ttm": 15.0, "roe": 0.085},
        "600519.SH": {"revenue_yoy": 0.12, "net_profit_yoy": 0.14,
                       "gross_margin": 0.91, "pe_ttm": 22.0, "roe": 0.32},
    }
    if symbol not in data:
        return {"error": f"无财报数据: {symbol}"}
    return {"symbol": symbol, "latest_quarter": "2025Q4", **data[symbol]}


def search_news(query: str, days: int = 7) -> dict:
    return {
        "query": query,
        "results": [
            {"title": f"{query} 行业产能过剩持续", "date": "2026-04-20", "source": "财经网"},
            {"title": f"{query} 海外出口面临贸易摩擦", "date": "2026-04-18", "source": "新华社"},
        ],
    }


TOOLS_IMPL = {
    "get_stock_price": get_stock_price,
    "get_financials": get_financials,
    "search_news": search_news,
}


# ================== Tool Schemas ==================

TOOLS = [
    {
        "name": "get_stock_price",
        "description": "获取指定股票的实时价格",
        "input_schema": {
            "type": "object",
            "properties": {"symbol": {"type": "string", "description": "股票代码如 601012.SH"}},
            "required": ["symbol"],
        },
    },
    {
        "name": "get_financials",
        "description": "获取最近季度的主要财务指标",
        "input_schema": {
            "type": "object",
            "properties": {"symbol": {"type": "string"}},
            "required": ["symbol"],
        },
    },
    {
        "name": "search_news",
        "description": "搜索近期相关新闻",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "days": {"type": "integer", "default": 7},
            },
            "required": ["query"],
        },
    },
]


SYSTEM = """<role>
你是一个投资分析 Agent,能调用工具获取数据并综合分析。
</role>

<working_style>
1. 收到任务后,先输出 <plan>...</plan>,拆解为 3-5 个子步骤
2. 每一步先思考再调用工具
3. 不重复调用相同参数的工具
4. 步数上限 8 步
</working_style>

<safety>
- 只做分析,不输出"建议买入/卖出"
- 数据缺失时明确说明,不臆造
- 输出最终答案时结尾附免责声明
</safety>
"""


# ================== Agent Loop ==================

def run_agent(task: str, max_steps: int = 8) -> str:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": task}]

    for step in range(max_steps):
        console.print(f"\n[bold blue]--- Step {step + 1} ---[/bold blue]")
        resp = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            temperature=0.2,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        )

        for block in resp.content:
            if block.type == "text" and block.text.strip():
                console.print(f"[cyan]{block.text}[/cyan]")

        if resp.stop_reason == "end_turn":
            return "\n".join(b.text for b in resp.content if b.type == "text")

        if resp.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": resp.content})
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    console.print(f"[yellow]🔧 调用 {block.name}({block.input})[/yellow]")
                    try:
                        result = TOOLS_IMPL[block.name](**block.input)
                    except Exception as e:
                        result = {"error": str(e)}
                    console.print(f"[green]📥 {json.dumps(result, ensure_ascii=False)}[/green]")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    })
            messages.append({"role": "user", "content": tool_results})

    console.print("[red]⚠️ 已达步数上限[/red]")
    return "[达到步数上限,未完成]"


def demo():
    task = "请分析 601012.SH 这只股票,给出综合观察"
    console.print(f"[bold magenta]📋 任务: {task}[/bold magenta]")
    final = run_agent(task)
    console.print(f"\n[bold green]=== 最终结论 ===[/bold green]\n{final}")


if __name__ == "__main__":
    demo()
