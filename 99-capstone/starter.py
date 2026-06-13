"""
Capstone · 销售 Agent 骨架代码

这份文件是起点,不是终点。
标有 TODO 的地方是你在 4 周开发计划里需要填充的部分。

所有 TODO 完成后,`python starter.py` 应该能跑一次完整闭环。
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import anthropic
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

# ================== 配置 ==================

CLASSIFIER_MODEL = "claude-haiku-4-5-20251001"
AGENT_MODEL = "claude-sonnet-4-6"
MAX_AGENT_STEPS = 8


# ================== 数据结构 ==================

class IntentLevel(str, Enum):
    A = "A"  # 热
    B = "B"  # 温
    C = "C"  # 冷
    D = "D"  # 无效


@dataclass
class CustomerProfile:
    customer_id: str
    name: str
    company: str
    level: IntentLevel
    history: list = field(default_factory=list)
    preferences: dict = field(default_factory=dict)


@dataclass
class AgentRequest:
    raw_input: str           # 客户邮件或问题
    customer_id: Optional[str] = None
    conversation_history: list = field(default_factory=list)


@dataclass
class AgentResponse:
    draft: str               # 邮件草稿
    intent_level: IntentLevel
    reasoning: str           # 决策依据
    confidence: float        # 0-1
    warnings: list = field(default_factory=list)  # 如 "涉及未授权折扣,请人工审阅"


# ================== 模块 1:意向分类器(M2) ==================

CLASSIFIER_SYSTEM = """你是销售运营专家,从客户沟通中判断意向等级(A/B/C/D)。
# TODO: 参考 templates/classification.md 完整 Prompt
"""


def classify_intent(text: str) -> tuple[IntentLevel, float]:
    """返回 (等级, 置信度)"""
    # TODO: Week 1 实现
    # 1. 构造 Few-shot + CoT Prompt
    # 2. 调用 CLASSIFIER_MODEL
    # 3. 解析 JSON,返回等级和置信度
    return IntentLevel.B, 0.5  # placeholder


# ================== 模块 2:客户档案 RAG(M5) ==================

class CustomerRAG:
    def __init__(self):
        # TODO: Week 2
        # - 初始化 ChromaDB
        # - 加载 data/customers.json 与 sales_history.json
        # - 构建向量索引
        pass

    def query(self, customer_id: str, question: str, top_k: int = 3) -> list[str]:
        """返回相关历史片段"""
        # TODO: Week 2
        return []


# ================== 模块 3:Agent 工具(M6) ==================

def get_customer_profile(customer_id: str) -> dict:
    # TODO: Week 2 - 从 data/customers.json 读
    return {"error": "not_implemented"}


def get_inventory(sku: str) -> dict:
    # TODO: Week 2
    return {"error": "not_implemented"}


def get_historical_price(sku: str, customer_level: str) -> dict:
    # TODO: Week 2
    return {"error": "not_implemented"}


def calculate_quote(products: list, discount_strategy: str) -> dict:
    # TODO: Week 2
    return {"error": "not_implemented"}


TOOLS_IMPL = {
    "get_customer_profile": get_customer_profile,
    "get_inventory": get_inventory,
    "get_historical_price": get_historical_price,
    "calculate_quote": calculate_quote,
}

TOOL_SCHEMAS = [
    # TODO: Week 2 - 参考 06-agent-tools/demo_agent.py
]


# ================== 模块 4:Agent 主循环(M6) ==================

AGENT_SYSTEM = """# TODO: Week 3
<role>...销售助理 Agent...</role>
<working_style>...Plan → ReAct loop...</working_style>
<safety>...</safety>
"""


def run_agent(req: AgentRequest) -> str:
    """返回最终结论的文本"""
    # TODO: Week 3
    # 参考 06-agent-tools/demo_agent.py 实现 ReAct 循环
    return "[TODO: agent not implemented]"


# ================== 模块 5:邮件起草(M2+M3) ==================

DRAFTER_SYSTEM = """# TODO: Week 3
你是资深销售经理,基于 Agent 收集的信息起草回复邮件。
...
"""


def draft_email(req: AgentRequest, agent_output: str, intent: IntentLevel) -> str:
    # TODO: Week 3
    # 参考 templates/sales-email.md
    return "[TODO: drafter not implemented]"


# ================== 模块 6:安全(M8) ==================

SYSTEM_RULES = """<system_rules priority="highest">
# TODO: Week 4 - 从 prompts/system_rules.md 加载
</system_rules>
"""


def wrap_user_input(text: str) -> str:
    """关键:永远用 XML 包裹用户输入"""
    return f"<user_input>\n{text}\n</user_input>"


def scrub_sensitive(text: str) -> str:
    # TODO: Week 4 - 参考 08-security/demo_red_team.py
    return text


def check_safety(draft: str) -> list[str]:
    """输出审查:返回警告列表"""
    warnings = []
    # TODO: Week 4
    # - 检测未授权折扣("5 折""半价"等)
    # - 检测敏感信息未脱敏
    return warnings


# ================== 主入口 ==================

def process(req: AgentRequest) -> AgentResponse:
    try:
        # 1. 意向分类
        intent, confidence = classify_intent(req.raw_input)
        console.print(f"📊 客户意向: [bold]{intent.value}[/bold] (置信 {confidence:.0%})")

        # 2. Agent 主循环(收集信息)
        agent_output = run_agent(req)

        # 3. 邮件起草
        draft = draft_email(req, agent_output, intent)

        # 4. 输出审查
        warnings = check_safety(draft)
        draft = scrub_sensitive(draft)

        # 5. 组装响应
        return AgentResponse(
            draft=draft,
            intent_level=intent,
            reasoning=agent_output,
            confidence=confidence,
            warnings=warnings,
        )
    except Exception as e:
        console.print(f"[red]❌ 处理出错: {e}[/red]")
        return AgentResponse(
            draft="处理失败，请人工介入或重试。",
            intent_level=IntentLevel.D,
            reasoning=f"异常: {e}",
            confidence=0.0,
            warnings=["系统错误，需人工处理"],
        )


def demo():
    sample = AgentRequest(
        raw_input="您好 Felix,你们上次报的环网柜价格能再降 10% 吗?我们这次要 10 台。— 李经理",
        customer_id="CUST_001",
    )
    console.print(f"[cyan]📨 客户消息:[/cyan] {sample.raw_input}\n")
    resp = process(sample)
    console.print(f"\n[green]📝 邮件草稿:[/green]\n{resp.draft}")
    console.print(f"\n[yellow]⚠️  警告:[/yellow] {resp.warnings or '无'}")


if __name__ == "__main__":
    demo()
