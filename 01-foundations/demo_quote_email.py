"""
模块 1 · 基础认知与 Prompt 结构 — 报价邮件生成器

演示要点:
    - Role / Task / Context / Format 四件套结构
    - XML 标签分隔
    - 结构化输入 → 模板化输出

运行方法:
    pip install anthropic python-dotenv rich
    export ANTHROPIC_API_KEY=sk-ant-...
    python demo_quote_email.py
"""

from dataclasses import dataclass
from typing import List

import anthropic
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

MODEL = "claude-sonnet-4-6"


@dataclass
class Product:
    name: str
    quantity: int
    unit_price: float
    unit: str = "台"


@dataclass
class QuoteRequest:
    customer_company: str
    contact_name: str
    contact_title: str
    products: List[Product]
    delivery_days: int
    payment_terms: str
    warranty_years: int = 1
    sales_name: str = "Felix"


def build_prompt(req: QuoteRequest) -> str:
    product_lines = "\n".join(
        f"- {p.name} × {p.quantity} {p.unit},单价 {p.unit_price} 万元"
        for p in req.products
    )
    total = sum(p.quantity * p.unit_price for p in req.products)

    return f"""<role>
你是一位有 10 年经验的电气设备销售经理,熟悉配电设备的商务沟通。
</role>

<task>
根据以下信息,起草一封正式、专业的报价邮件给客户。
</task>

<customer>
客户公司:{req.customer_company}
联系人:{req.contact_name}({req.contact_title})
</customer>

<products>
{product_lines}
合计约:{total:.2f} 万元
</products>

<commercial_terms>
交付期:{req.delivery_days} 天
付款方式:{req.payment_terms}
质保:{req.warranty_years} 年
</commercial_terms>

<rules>
- 语气:专业、克制、体现经验,避免过度推销
- 结构:问候 → 简要致谢 → 报价明细(Markdown 表格)→ 商务条款 → 下一步建议 → 结束语
- 长度:300-500 字
- 不要"尊敬的""此致敬礼"等过度正式表达
- 落款使用:"{req.sales_name}"
</rules>

<output_format>
第一行为:主题: xxx
空一行后为邮件正文(中文)。
</output_format>
"""


def generate_quote_email(req: QuoteRequest) -> str:
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        temperature=0.3,
        messages=[{"role": "user", "content": build_prompt(req)}],
    )
    return resp.content[0].text


def demo():
    req = QuoteRequest(
        customer_company="华东某新能源有限公司",
        contact_name="张经理",
        contact_title="采购部经理",
        products=[
            Product("10kV 环网柜", 5, 8.5),
            Product("配电变压器 500kVA", 2, 12.0),
        ],
        delivery_days=60,
        payment_terms="30% 预付 + 60% 发货前 + 10% 质保金",
    )
    console.print("[bold cyan]📧 正在生成报价邮件...[/bold cyan]\n")
    email = generate_quote_email(req)
    console.print("[bold green]生成结果:[/bold green]\n")
    console.print(email)


if __name__ == "__main__":
    demo()
