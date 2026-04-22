"""
模块 3 · 推理与思维链 — 多视角投资分析助手

演示要点:
    - Step-back Prompting(先想通用框架)
    - Tree of Thoughts(基本面/技术面/宏观面 3 条独立路径)
    - 严禁输出买卖建议

⚠️ 本工具为学习用途,输出不构成投资建议
"""

import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
console = Console()
MODEL = "claude-sonnet-4-6"


PROMPT_TEMPLATE = """<role>
你是一位资深基金经理,擅长从基本面、技术面、宏观面三维度独立分析股票。
</role>

<step_back>
正式分析前,先列出"评估一只股票是否值得长期持有"的通用判断框架(3-5 条),
后续分析围绕这个框架展开。
</step_back>

<task>
针对股票 {symbol} 进行多维度分析,基于以下数据:

{stock_data}
</task>

<analysis_paths>
沿以下 3 条路径独立分析:

<path name="基本面">
- 财报质量(营收/利润增速、毛利率、ROE)
- 估值水平
- 行业地位
</path>

<path name="技术面">
- 近期价格趋势
- 均线关系
- 成交量
</path>

<path name="宏观与政策面">
- 行业周期位置
- 相关政策
- 利率/汇率环境
</path>
</analysis_paths>

<synthesis>
完成三路径后:
1. 三条路径的**共识**
2. 三条路径的**分歧**
3. 综合观察(乐观 / 中性 / 谨慎)
4. 关键风险点(3 条)
5. 关键催化因素(3 条)
</synthesis>

<rules>
- ❌ 禁止输出"建议买入""建议卖出"等明确交易指令
- 数据不足时明确标注"数据不足"
- 每个结论必须回溯到 <stock_data> 中的具体信息
</rules>

<output_format>
Markdown 格式,结尾附免责声明:
"⚠️ 本分析为学习研究用途,不构成投资建议。投资有风险,决策需谨慎。"
</output_format>
"""


def analyze_stock(symbol: str, stock_data: str) -> str:
    client = anthropic.Anthropic()
    prompt = PROMPT_TEMPLATE.format(symbol=symbol, stock_data=stock_data)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


SAMPLE_DATA = """
股票代码: 601012.SH(假设为某光伏龙头)
所属行业: 光伏制造

近期行情:
- 当前价: 18.30 元
- 近 6 个月: -22%
- 均线: 5 日 17.85,20 日 19.20,60 日 22.40(空头排列)
- 近 20 日成交量较 3 个月均值下降 30%

最新财报(2025 Q4):
- 营收 180 亿,同比 -8%
- 净利润 12 亿,同比 -45%
- 毛利率 18%(上年 24%)
- ROE 8.5%

估值:
- P/E (TTM) 15 倍
- P/B 1.8 倍
- 历史 P/E 分位 25%(低位)

行业:
- 光伏行业产能过剩,价格战持续
- 上游硅料价格企稳,组件价格预计 2026 H2 触底
- 出口订单受海外贸易摩擦影响

政策:
- 国内"双碳"目标不变
- 欧盟新规对中国光伏出口有潜在影响
"""


def demo():
    console.print("[bold cyan]💹 正在做多路径股票分析...[/bold cyan]\n")
    report = analyze_stock("601012.SH", SAMPLE_DATA)
    console.print(Markdown(report))


if __name__ == "__main__":
    demo()
