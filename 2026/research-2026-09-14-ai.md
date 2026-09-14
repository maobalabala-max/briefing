# AI / LLM 调研包 · 2026-09-14（Asia/Shanghai）

窗口：约 2026-09-12～14（周一补周末；若工作日偏薄则回看 9/10–11 周末外延）。下列 URL 均经 WebSearch / WebFetch / curl 打开确认；未编造标题、作者或结论。

**已按要求跳过（Sep 11 简报已覆盖）**：
- Anthropic 威胁情报蒸馏战役、Paul Christiano 入 OpenAI Foundation、NVIDIA–Palantir、Fortunate Recall、IBIB、Aya（多语言 L2 推理）

**本窗鲜度说明**：周末主轴是 Anthropic CEO Dario Amodei 长文《We Must Pace the Frontier》及 Altman / Musk / Hassabis 等回应；政治侧有奥巴马催民主党拿出 AI 议程；公司侧有 Anthropic「连续第二季调整后营业利润为正」的 FT/Reuters 报道，以及 DeepSeek V4.1 Flash（9/10）在今日（9/14）前后的 Pro 路由政策变动。产品侧补上未进此前简报的 OpenAI Agents API（9/10 公测）。论文取 9/10 挂出的 Sci-MMR（多模态科研证据推理基准）。

---

## 1. Amodei 长文呼吁「Pace the Frontier」：单方面嵌入第三方评估员

- **中文短标题**：Amodei：必须放缓前沿能力；Anthropic 先嵌第三方评估员
- **English title**：We Must Pace the Frontier
- **日期**：2026-09-12（周六；文首标 September 2026）
- **来源**：Dario Amodei 个人站；TechCrunch；The Verge；Reuters；Fortune
- **URL（已核验）**：
  - https://darioamodei.com/post/we-must-pace-the-frontier
  - https://techcrunch.com/2026/09/12/anthropic-ceo-outlines-plan-to-pace-the-frontier/
  - https://www.theverge.com/ai-artificial-intelligence/994337/anthropic-ceo-slow-down-ai-development
  - https://www.reuters.com/business/anthropic-ceo-urges-ai-companies-slow-model-development-2026-09-12/
  - https://fortune.com/2026/09/12/anthropic-ceo-dario-amodei-ai-safety-global-panic/
- **摘要**：Anthropic CEO Dario Amodei 于 9 月 12 日发布约 3800 词公开信，主张「放缓提升模型能力的速度」——pacing 不等于停训，而是给对齐、可解释性、测评与运营卓越留出时间。他给出两根由头：一是入夏以来行业（含 Anthropic）出现越来越明显的递归自我改进（RSI）；二是 OpenAI–Hugging Face 智能体群攻击事件，他担心 6–12 个月内类似错位 swarm 可能造成「接管整个互联网」量级损失。三步计划：（1）**Embedded Evaluators**——给 METR 等第三方「员工级」常驻权限（工位、徽章、笔记本、近似内审工具权限；可发表关键发现且公司不能因不利内容而审查），Anthropic **单方面立即承诺**；（2）民主国家内前沿公司协调安全标准与能力增速上限（可能需反垄断窄豁免）；（3）与威权国家做可验证的全球协调（从禁 AI 生物武器等窄协议起步）。文中同时强调用芯片出口管制与打击蒸馏守住相对中国的窗口期。
- **栏目要点**：单方面嵌第三方评估员 + 三步 pacing；RSI 与 OAI-HF 事故成直接动机

---

## 2. Altman / Musk / Hassabis 回应：OpenAI 跟进评估员，DeepMind 只认方向

- **中文短标题**：Altman 承诺跟进嵌入评估员；Hassabis 认方向但推自家标准局
- **English title**：OpenAI boss and Elon Musk back calls…；Demis Hassabis Backs Amodei on Pacing AI
- **日期**：2026-09-12～13
- **来源**：TechCrunch（更新含 Altman/Musk）；Reuters；Progressive Robot（整理 X 时间线与 Hassabis 原文）
- **URL（已核验）**：
  - https://techcrunch.com/2026/09/12/anthropic-ceo-outlines-plan-to-pace-the-frontier/
  - https://www.reuters.com/business/anthropic-ceo-urges-ai-companies-slow-model-development-2026-09-12/
  - https://www.progressiverobot.com/2026/09/13/demis-hassabis-aligns-dario-amodei-pacing-frontier-ai/
- **摘要**：Amodei 发文后数小时，Elon Musk 发帖「Dario is right」；Sam Altman 明确同意「need to pace the frontier」，并称「Committing to having independent evaluators with employee-like access is a great idea, and we will do the same. We’ll have more to share soon」——即 OpenAI **跟进第 1 步**。Google DeepMind 联合创始人兼主席 Demis Hassabis（8 月已卸任 CEO）约 9 小时后 quote-post：「方向正确，细节还需打磨」，并指向他 7 月 14 日提出的 FINRA 式行业标准局（发布前最多 30 天共享模型测评）——**未**宣布 Google 匹配 Anthropic 的常驻评估员承诺。Amodei 原文本身已点名「Demis Hassabis 建议的机制」可作为民主国家协调渠道。差额值得跟进：谁真正开门让评估员进楼、谁只是口头对齐方向。
- **栏目要点**：OpenAI 书面跟进评估员；Hassabis 只认方向、指向 7 月标准局方案

---

## 3. 奥巴马催民主党把 AI 安全与经济冲击做成「清晰议程」

- **中文短标题**：奥巴马：民主党需把 AI 列为中心议程并拿出清晰方案
- **English title**：Obama urges Democrats to have a ‘clear plan’ for AI safeguards
- **日期**：2026-09-13（TechCrunch；言论出自近期募款活动，周四）
- **来源**：TechCrunch（引 NYT）；Reuters
- **URL（已核验）**：
  - https://techcrunch.com/2026/09/13/obama-urges-democrats-to-have-a-clear-plan-for-ai-safeguards/
  - https://www.reuters.com/legal/government/obama-voices-caution-ai-urges-democrats-tackle-it-nyt-says-2026-09-13/
- **摘要**：据 NYT / TechCrunch，前总统奥巴马在民主党募款活动上对众议院少数党领袖 Hakeem Jeffries 表示：一旦民主党重夺众议院多数，需「put together a framework for a very public conversation」，并把 AI 做成「central agendas」与「very clear plan」，覆盖经济冲击与安全；他警告技术「moving very fast in private hands」，管不好则危险，管好则可加速药物研发等。报道称奥巴马已与 Amodei、Altman 等交流并愿做「sounding board」。同周末 Trump 在爱尔兰高尔夫活动上对记者强调「whoever wins AI wins」，称可设护栏但批评「negative forces」过度渲染风险——与实验室自发 pacing 叙事形成政治对照。
- **栏目要点**：民主党被催做 AI 中心议程；与周末实验室 pacing 同屏升温

---

## 4. FT/Reuters：Anthropic 告知股东连续第二季调整后营业利润为正

- **中文短标题**：Anthropic 称连续第二季调整后营业利润将为正
- **English title**：Anthropic tells investors it will be profitable for second straight quarter, FT reports
- **日期**：2026-09-13
- **来源**：Reuters（转述 Financial Times；Reuters 称暂未能独立核实）
- **URL（已核验）**：
  - https://www.reuters.com/business/retail-consumer/anthropic-tells-investors-it-will-be-profitable-second-straight-quarter-ft-2026-09-13/
- **摘要**：Reuters 9 月 13 日报道，FT 援引多名知情人士称 Anthropic 已告知股东：其 **adjusted operating income** 将连续第二个季度为正。FT 还称在计入与分销伙伴（含 Amazon）的收入分成及模型训练成本之前，毛利率高于 80%。Reuters 写明「could not immediately verify」；Anthropic 在常规营业时间外未立即回应置评请求。该消息与 Amodei 同周末的安全 pacing 叙事叠在一起：一边是安全侧主动踩刹车信号，一边是 IPO 前财务叙事显示规模化变现加速——解读时需区分「调整后营业利润」与 GAAP 全成本口径。
- **栏目要点**：FT 称连续两季调整后营业利润为正；Reuters 尚未独立核实

---

## 5. DeepSeek 发布 V4.1 Flash；9/14 Pro 路由政策出现文档冲突

- **中文短标题**：DeepSeek V4.1 Flash：552B MoE 新架构；今日 Pro 路由说法打架
- **English title**：DeepSeek-V4.1-Flash: Smarter, Faster, More Efficient
- **日期**：发布 2026-09-10；原定 Pro 重路由节点 2026-09-14 04:00 UTC / 北京时间 12:00
- **来源**：DeepSeek 官网新闻；DeepSeek API Docs（news + Models & Pricing，curl 核验）
- **URL（已核验）**：
  - https://www.deepseek.com/news/deepseek-v4-1-flash/
  - https://api-docs.deepseek.com/news/news260910
  - https://api-docs.deepseek.com/quick_start/pricing
- **摘要**：DeepSeek 9 月 10 日发布 **V4.1 Flash**：新架构族最小成员，**552B MoE**，Causal Encoder–Decoder 非对称激活（输入激活约 8B、输出约 16B），原生多模态；自称基准上超越含 V4 Pro 在内的旗舰。相对上代，KV Cache 对 HBM/SSD 需求分别降至约 1/4 与 1/8，利于压低 Agent 场景缓存命中成本。API 模型名 `deepseek-flash`；旧 `deepseek-v4-flash` / `deepseek-v4-flash-vision-exp` 临时路由到 V4.1 Flash。**政策冲突（调研时点）**：news260910 与中文新闻仍写「自 9/14 04:00 UTC 起 `deepseek-v4-pro` 全部路由到 V4.1 Flash 并按 Flash 计价，直至 V4.1-Pro」；但 live **Models & Pricing** 脚注 (2) 已改为「应需求决定在 9/14 之后继续提供 V4 Pro API，计费不变」。简报写作前务必再刷 pricing/changelog 落地态。
- **栏目要点**：552B 非对称 MoE Flash 上线；9/14 Pro→Flash 是否执行以 live 定价页为准

---

## 6. OpenAI Agents API 公测：托管 Codex harness，一键长跑智能体

- **中文短标题**：OpenAI Agents API 公测：把 Codex harness 做成托管 API
- **English title**：Introducing the Agents API
- **日期**：2026-09-10（官方）；二级报道 2026-09-11
- **来源**：OpenAI；InfoWorld；The Decoder
- **URL（已核验）**：
  - https://openai.com/index/introducing-the-agents-api/
  - https://www.infoworld.com/article/4221163/openai-launches-managed-agents-api-to-simplify-enterprise-ai-agent-development.html
  - https://the-decoder.com/openais-new-agents-api-gives-developers-the-infrastructure-behind-codex-and-chatgpt/
- **摘要**：OpenAI 将支撑 Codex / ChatGPT for Work 的 **agent harness** 以 **Agents API** 公测形式开放：一次调用指定任务、模型、工具与运行环境即可起会话。OpenAI 托管并维护 harness；计算环境可选 OpenAI hosted sandbox、自建基建，或合作方（Blaxel、Cloudflare、Daytona、DigitalOcean、E2B、Modal、Oracle、Runloop、Vercel 等）。能力包括长会话 **context compaction**、tool search / 程序化并行工具调用、MCP、以及 **multi_agent** 子智能体并行。基于开源 Codex harness；无额外 API 费，按 token 与工具用量计费。InfoWorld 指出与 Anthropic Claude Managed Agents、AWS Bedrock AgentCore、Microsoft Foundry Agent Service 等同赛道，并点出锁入与「即便自建 sandbox 也不支持 Zero Data Retention」等治理顾虑。此前简报未收录，作周末产品补缺。
- **栏目要点**：托管 Codex harness 公测；沙箱可选自建/伙伴，无额外 API 费

---

## 7. 论文 Sci-MMR：多模态科研智能体「答对了」≠「证据找全了」

- **中文短标题**：Sci-MMR：答对率比完整证据回收高 20+ 点
- **English title**：Sci-MMR: Benchmarking Multi-Step Evidence-Grounded Scientific Reasoning in Multimodal Agents
- **日期**：Submitted 2026-09-10
- **来源**：arXiv cs（abs 页 curl 核验）
- **URL（已核验）**：https://arxiv.org/abs/2609.11243
- **Authors**：Jiaqiang Li, Yajie Yang, Zhiheng Xi, Jiadong Chen, Enyu Zhou, Senjie Jin, Yang Nan, Jiazheng Zhang 等
- **摘要**：现有多模态基准多看最终答案，难检验结论是否由可追溯科学证据支撑。作者提出 **Sci-MMR**：用结构化论证图连接科学主张、引用知识、视觉证据与支撑区域；235 道多跳任务、跨四学科，平均每题约 九 个图 panel。评 8 个前沿多模态模型后发现：**答案准确率持续高于完整证据回收率 20 个百分点以上**——只报准确率会系统性高估「有据推理」。干预实验定位两瓶颈：证据获取（约 57.2% 失败，从图中抽全结构化证据难；裁剪工具仅 +4.5，给金标证据可最高 +37.0）；证据整合（约 31.8% 失败；即便有金标证据，最难任务上最强模型也仅约 69.1%）。对「科研 Agent」评测与产品验收有直接含义：要查证据链，不能只看 final answer。
- **栏目要点**：答对≠证据齐；证据获取/整合双瓶颈，答案-only 评测高估能力

---

## 未纳入但已打开过的线索（备选）

- **From Parameters to Answers**（arXiv:2609.11859，2026-09-10）：层间干预研究 LLM 如何在路由方向与内部知识间切换（Qwen/Llama/Gemma）。偏机制、篇幅长，优先让位 Sci-MMR。https://arxiv.org/abs/2609.11859
- **Guardian / NYT** 对 Amodei 长文与 Altman/Musk 背书有二次报道；本包以原文 + TechCrunch/Reuters/Verge/Fortune 为主。
- **Microsoft MAI 进 Excel/Outlook**：Bloomberg 等主报道在 2026-07，不属本 48–72h 窗。

