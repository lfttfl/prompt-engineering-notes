# 📎 参考资源汇总

本页汇总 3 个月学习路线里涉及的所有重要资源。按"官方文档 → 系统课程 → 论文 → 工具 → 社区"分类。

---

## 🏛 官方文档（优先级最高）

- [Anthropic Prompt Engineering 官方指南](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) — 最系统、工程化最强
- [OpenAI Prompt Engineering Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google Gemini Prompting Guide](https://ai.google.dev/gemini-api/docs/prompting-intro)

---

## 🎓 系统课程（免费）

- 吴恩达《[ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)》— 入门必看
- 吴恩达《[Building Systems with the ChatGPT API](https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/)》
- 吴恩达《[LangChain for LLM Application Development](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/)》
- [Learn Prompting 中文站](https://learnprompting.org/zh-Hans/docs/intro)
- [Prompt Engineering Guide 中文版](https://www.promptingguide.ai/zh)

---

## 📄 必读论文（按模块分）

### 推理类
- [Chain-of-Thought Prompting (2022)](https://arxiv.org/abs/2201.11903)
- [Self-Consistency (2022)](https://arxiv.org/abs/2203.11171)
- [Tree of Thoughts (2023)](https://arxiv.org/abs/2305.10601)
- [Step-Back Prompting (2023)](https://arxiv.org/abs/2310.06117)
- [ReAct (2022)](https://arxiv.org/abs/2210.03629)

### 上下文
- [Lost in the Middle (2023)](https://arxiv.org/abs/2307.03172)

### Agent
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents)

---

## 🛠 工具清单

### Prompt 开发与调试
- [Anthropic Console](https://console.anthropic.com/) — 官方 Playground，推荐
- [OpenAI Playground](https://platform.openai.com/playground)
- [Promptfoo](https://www.promptfoo.dev/) — 开源评估工具

### 向量数据库（模块 5 RAG 用）
- [Chroma](https://www.trychroma.com/) — 最易上手
- [FAISS](https://github.com/facebookresearch/faiss) — 本地高性能
- [Qdrant](https://qdrant.tech/) — 生产级

### Agent 框架
- [LangChain](https://python.langchain.com/)
- [LlamaIndex](https://docs.llamaindex.ai/)
- [Anthropic SDK 直接用](https://docs.anthropic.com/en/api/client-sdks) — 很多场景不需要框架

### Token / 成本计算
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer)
- [tiktoken (Python)](https://github.com/openai/tiktoken)
- [Anthropic Token Counter API](https://docs.anthropic.com/en/api/messages-count-tokens)

### 安全与红队
- [Gandalf](https://gandalf.lakera.ai/) — 越狱练手游戏
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---

## 📚 博客与长文

- [Simon Willison's Weblog](https://simonwillison.net/) — 最前沿的 LLM 实践观察
- [Eugene Yan: Evaluating LLM Applications](https://eugeneyan.com/writing/evals/)
- [Lilian Weng: Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
- [Anthropic Research Blog](https://www.anthropic.com/research)

---

## 🇨🇳 中文社区

- [DataWhale LLM 教程](https://github.com/datawhalechina/llm-cookbook)
- [LangChain 中文文档](https://python.langchain.com.cn/)
- 知乎话题：#大语言模型应用

---

## 📰 持续关注（订阅）

- **Twitter/X**：@simonw、@karpathy、@AnthropicAI、@OpenAI
- **Newsletter**：The Batch（吴恩达）、Ben's Bites
- **Podcast**：Latent Space、No Priors

---

## 🎯 学习时长预算

| 阶段 | 理论 | 实战 | 总计 |
|---|---|---|---|
| 模块 1 | 2h | 4h | 6h |
| 模块 2 | 4h | 8h | 12h |
| 模块 3 | 4h | 8h | 12h |
| 模块 4 | 3h | 5h | 8h |
| 模块 5 | 4h | 8h | 12h |
| 模块 6 | 5h | 9h | 14h |
| 模块 7 | 4h | 6h | 10h |
| 模块 8 | 3h | 5h | 8h |
| **合计** | 29h | 53h | **82h** |

**每周投入 7 小时，12 周完成。** 想加速可压到 10 周。
