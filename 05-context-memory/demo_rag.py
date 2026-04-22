"""
模块 5 · 上下文与记忆管理 — 最小 RAG 问答系统

演示:
    - 文档切块(带 overlap)
    - 向量化入库(chromadb 默认 all-MiniLM-L6-v2)
    - 检索 + 拼 Prompt + 调用 LLM
    - 强制答案带引用来源

运行前:
    pip install anthropic chromadb python-dotenv rich
"""

from typing import List

import anthropic
import chromadb
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
console = Console()
MODEL = "claude-sonnet-4-6"


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += chunk_size - overlap
    return chunks


def build_index(docs: dict) -> chromadb.Collection:
    client = chromadb.Client()
    try:
        client.delete_collection("kb")
    except Exception:
        pass
    col = client.create_collection("kb")

    for doc_id, text in docs.items():
        chunks = chunk_text(text)
        col.add(
            ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))],
            documents=chunks,
            metadatas=[{"doc_id": doc_id, "chunk": i} for i in range(len(chunks))],
        )
    return col


RAG_PROMPT = """<role>
你是严谨的知识库问答助手,只能依据提供的资料回答。
</role>

<rules>
- 仅使用 <documents> 中的内容
- 回答必须标注来源,格式 [doc_id:chunk]
- 资料中没有的,直接说"资料中未提及"
- 不臆造、不外推
</rules>

<documents>
{docs}
</documents>

<question>
{question}
</question>

<output_format>
<answer>...答案正文,引用处标注 [doc_id:chunk]...</answer>
<sources>
  - [doc_id:chunk] 原文摘录
</sources>
</output_format>
"""


def rag_ask(col: chromadb.Collection, question: str, top_k: int = 3) -> str:
    results = col.query(query_texts=[question], n_results=top_k)
    docs_block = "\n\n".join(
        f'<doc id="{m["doc_id"]}" chunk="{m["chunk"]}">\n{d}\n</doc>'
        for d, m in zip(results["documents"][0], results["metadatas"][0])
    )

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        temperature=0.0,
        messages=[{
            "role": "user",
            "content": RAG_PROMPT.format(docs=docs_block, question=question),
        }],
    )
    return resp.content[0].text


SAMPLE_DOCS = {
    "tender_2026_04": """
    某市政新能源汽车充电站建设项目招标公告
    招标方:某市城市建设投资有限公司
    项目编号:CS-2026-0418
    总预算:1200 万元(含税)。
    工期:合同签订后 120 日历天内完成全部供货及安装。
    资质要求:
    1. 独立法人资格,注册资本不低于 3000 万元;
    2. 电力施工总承包三级及以上资质;
    3. 通过 ISO9001、ISO14001、ISO45001 三体系认证;
    4. 近 3 年 2 个以上类似项目业绩(合同额不低于 500 万)。
    投标截止:2026 年 5 月 30 日 10:00。
    """,
    "tender_2026_03": """
    某工业园区配电升级改造项目招标
    预算:800 万元
    工期:90 天
    资质:注册资本 2000 万元以上,需有电力二级资质
    截止:2026 年 4 月 18 日 16:00
    技术要求:采用 SF6 环保气体绝缘开关柜。
    """,
}


def demo():
    console.print("[bold cyan]📚 正在建立向量索引(首次需要下载 embedding 模型)...[/bold cyan]")
    col = build_index(SAMPLE_DOCS)

    questions = [
        "新能源充电站项目的预算是多少?",
        "两个项目中哪个对注册资本的要求更高?",
        "项目的环保材料要求是什么?",
    ]
    for q in questions:
        console.print(f"\n[bold yellow]❓ {q}[/bold yellow]")
        console.print(Markdown(rag_ask(col, q)))


if __name__ == "__main__":
    demo()
