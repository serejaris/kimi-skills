# Kimi Skills — полная коллекция скиллов Kimi

Снимок всех скиллов, доступных агенту Kimi в сандбоксе, выгруженный автоматически.

- **267 встроенных скиллов** — каталог ниже, папка [`skills/`](skills/)
- **7 скиллов плагинов** — папка [`plugin-skills/`](plugin-skills/)
- **В репо сейчас:** этот каталог всех 274 скиллов с описаниями + полные `SKILL.md` 16 скиллов, непосредственно доступных агенту (9 built-in: docx, pdf, xlsx, kimi-slides, webapp-building, backend-building, skill-creator, kimi-help-center, kimi-widget — и все 7 плагинов)
- **Полный дамп** (все 274 скилла со скриптами, шаблонами и референсами — 2 574 файла, 37 МБ) собран и ждёт заливки через GitHub Actions: у OAuth-токена интеграции нет scope `workflow`, поэтому workflow-файл через API не запушить. Переподключи плагин GitHub с расширенными правами — и всё долетит одним прогоном
- Исключены из дампа: `node_modules/`, `.git/`, `__pycache__/`, файлы > 2 МБ — подробности в [EXCLUDED.md](EXCLUDED.md)

## Скиллы плагинов

| Скилл | Плагин | Описание |
|---|---|---|
| [`audio_generation`](plugin-skills/audio_generation) | audio_generation | Generate audio in two ways: text-to-speech with pre-built Mandarin voices, or custom AI sound effects from an English description (0.5–22 s). Output saved locally as mp3. |
| [`image_generation`](plugin-skills/image_generation) | image_generation | Create an image from a text description using AI image generation. Ratios up to 16:9/9:16, resolutions 1K/2K/4K, optional transparent background, reference-image guidance. |
| [`imf`](plugin-skills/imf) | imf | IMF provides global macroeconomic data through the World Economic Outlook database, including historical statistics and forecasts for GDP growth, inflation, government debt, unemployment, trade balances, and other indicators across 190+ countries and regions, plus COFER reserve currency composition data. |
| [`scholar`](plugin-skills/scholar) | scholar | A freely accessible web search engine that indexes the full text or metadata of scholarly literature across an array of publishing formats and disciplines: paper search, citation counts, author profiles with h-index. |
| [`sec_edgar`](plugin-skills/sec_edgar) | sec_edgar | SEC EDGAR provides comprehensive US public company filings and financial data, including company info, filings, XBRL facts, financial statements, insider trades, institutional holdings, and material company events. |
| [`world_bank_open_data`](plugin-skills/world_bank_open_data) | world_bank_open_data | World Bank Open Data is a free global development data platform with access to countries worldwide and 29,000+ indicators covering economic, social, and environmental metrics from 1960 to present. |
| [`yahoo_finance`](plugin-skills/yahoo_finance) | yahoo_finance | Yahoo Finance provides stock information for a given ticker symbol, including stock price and trading information, company information, financial metrics, earnings and revenue, dividends, balance sheet data, ownership, analyst coverage, and risk metrics. |

## 9 built-in скиллов, доступных агенту (полные SKILL.md в репо)

| Скилл | Описание |
|---|---|
| [`docx`](skills/docx) | Create and edit Word documents (.docx) — C# + OpenXML SDK for creation, WIR engine for editing/comments/tracked changes. Use for any .docx task including document creation, editing, comments, revisions, footnotes, TOC, and Markdown-to-Word conversion. |
| [`pdf`](skills/pdf) | Professional PDF solution. Create PDFs using HTML+Paged.js (academic papers, reports, documents). Process existing PDFs using Python (read, extract, merge, split, fill forms). Supports KaTeX math formulas, Mermaid diagrams, three-line tables, citations. Also for explicit LaTeX (.tex) requests. |
| [`xlsx`](skills/xlsx) | Specialized utility for advanced manipulation, analysis, and creation of spreadsheet files (XLSX, XLSM, CSV). Formula deployment, complex formatting, data visualization, mandatory recalculation, and finance-focused modeling (three-statement models, DCF, public comps). |
| [`kimi-slides`](skills/kimi-slides) | Create and edit presentations in PPTX format via a .pptd intermediate DSL. Also reads uploaded PPTX and converts PPTX to images; can render infographics/posters as PPTX. |
| [`webapp-building`](skills/webapp-building) | Tools for building modern React webapps with TypeScript, Tailwind CSS and shadcn/ui. Best suited for applications with complex UI components and state management. Supports optional templates. |
| [`backend-building`](skills/backend-building) | Backend building that grafts tRPC + Drizzle ORM + Hono onto an existing webapp-building frontend. Incremental features (db, auth). Requires webapp-building first. |
| [`skill-creator`](skills/skill-creator) | Guide for creating effective skills — creating or updating skills that extend agent capabilities with specialized knowledge, workflows, or tool integrations. |
| [`kimi-help-center`](skills/kimi-help-center) | Kimi Product Help Center. Routes questions about Kimi features, membership, pricing, credits, billing, invoices, login/account issues to the matching help article on kimi.com. |
| [`kimi-widget`](skills/kimi-widget) | Kimi widget design system. Defines when to use an inline widget and the runtime contract: sandboxed iframe with the Kimi design system pre-loaded. |

## Каталог всех 267 встроенных скиллов

| Скилл | Описание |
|---|---|
| `about-me-avatar` | Generate a 1-bit monochrome pixel-art portrait from a user's About Me. Central face anchored to a fixed base; surrounding elements derived from About Me. Always black-and-white, no text, gender-neutral by default. |
| `academic-paper-reviewer` | Simulates academic peer review, evaluating papers across Originality, Methodology, Results, and Writing to provide Major/Minor Revision recommendations with actionable feedback. |
| `ad-copywriter` | 广告创意写作与优化技能，覆盖标题、描述、正文及完整广告方案的生成与迭代，适用于Google Ads、Meta、LinkedIn、TikTok、Twitter/X等主流付费广告平台。 |
| `ad-creative` | Generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad variations — for any paid advertising platform. |
| `adhd-assistant` | ADHD-friendly life management assistant for daily planning, task breakdown, time management, and maintaining routines. |
| `adhd-daily-planner` | ADHD 生活管理助手，通过每日规划、任务拆解、时间感知辅助、优先级排序、虚拟陪伴工作和情绪支持来帮助管理日常。 |
| `anki-card-maker` | Extract key knowledge from study materials and generate front-question + back-answer flashcards, producing an Anki-compatible CSV file ready for import. |
| `api-doc-gen` | 从 Flask、FastAPI、Express 或 Gin 等 Web 框架的源代码中自动扫描路由定义，生成符合 OpenAPI 3.0 / Swagger 规范的标准化 API 文档文件。 |
| `api-shape-explorer` | Generate multiple radically different interface designs for a module using parallel sub-agents. Use when designing an API, exploring interface options, or comparing module shapes. |
| `astro-observation-report` | Skill for writing gravitational-wave observational results papers for compact binary coalescence events (BNS, BBH, NSBH) detected by LIGO, Virgo, or KAGRA. |
| `astro-observation-report-cn` | 用于撰写 LIGO、Virgo、KAGRA 探测到的致密双星合并事件引力波观测结果论文的 Skill，复刻《Physical Review X》双栏期刊风格。 |
| `audience-adapter` | 向上汇报与跨部门沟通助手，根据受众角色（CEO、VP、技术负责人或运营）自动调整信息粒度、语言风格和侧重点。 |
| `audience-adaptive-comms` | Adapt stakeholder communication to the target audience (CEO, VP, Tech Lead, or Operations), adjusting detail level, language, and focus. |
| `auto-hypothesis-test` | Automatically selects and runs the right statistical test for your data — t-test, ANOVA, chi-square, Mann-Whitney — and provides plain-language interpretations. |
| `auto-stat-test` | 自动执行统计检验，根据数据特征智能选择 t 检验、卡方检验、ANOVA、Mann-Whitney U 等合适方法，并输出完整报告。 |
| `backend-building` | Backend building that grafts tRPC + Drizzle ORM + Hono onto an existing webapp-building frontend. Supports incremental features (db, auth). |
| `backend-building-swarm` | Swarm-aware backend building that grafts tRPC + Drizzle ORM + Hono onto an existing webapp-building-swarm frontend on a worktree of the shared repo. |
| `baoyu-infographic` | 生成专业级信息图。提供 21 种版式与 21 种视觉风格，可自动解析内容并推荐最优「版式 × 风格」组合。 |
| `batch-download` | Batch download helper (skill file present in snapshot). |
| `bloom-quiz-maker` | 按布鲁姆认知分类学自动生成包含选择题、简答题、案例分析题在内的模拟试题，每题附完整解析。 |
| `brand-name-forge` | A systematic brand naming workshop that generates 8 distinct name candidates using classic methods like portmanteau and metaphor. |
| `brand-naming-lab` | 为产品、服务或项目提供系统性品牌命名方案，运用8种经典命名方法生成候选名称并附含义解读与域名建议。 |
| `browse` | Automate browser interactions via CLI commands to navigate web pages, extract data, take screenshots, fill forms; supports CAPTCHA solving and anti-bot stealth. |
| `business-plan-ppt` | 创建专业精美的投资路演PPT和商业计划书，默认输出18页、白色背景搭配藏青色点缀的PPTX格式，支持中英文。 |
| `campaign-plan` | Generate a full campaign brief with objectives, audience, messaging, channel strategy, content calendar, and success metrics. |
| `campaign-planner` | 生成完整的营销活动策划方案，涵盖目标设定、受众分析、核心信息、渠道策略、内容日历及效果指标。 |
| `cashflow-valuation` | DCF现金流折现估值模型，支持完整的自由现金流预测、终值计算和企业价值推导，并生成敏感性分析矩阵。 |
| `chart-gen` | 从JSON数据生成高质量PNG/SVG图表图片，支持折线图、柱状图、面积图、散点图、K线图、饼图、热力图等多种类型。 |
| `chart-image` | Generate publication-quality PNG chart images from data: line, bar, area, candlestick, pie, and heatmap charts via headless Node.js. |
| `chrono-flow` | 根据JSON数据生成精美的交互式时间线HTML页面，支持垂直、水平、双侧三种布局，适配移动端。 |
| `churn-prevention` | Reduce voluntary and involuntary churn through cancel flow design, save offers, exit surveys, and dunning sequences. |
| `cite-style-converter` | Convert academic citations between APA, MLA, IEEE, and Harvard styles with batch processing and format validation. |
| `cn-finance-data` | 通过 Tushare Pro 获取中国金融市场数据，覆盖 A 股、港股、美股、基金、期货、债券等 220+ 个数据接口。 |
| `code-arch-optimizer` | 探索代码库，识别架构摩擦点，并通过“加深浅模块”来提升可测试性，输出详细重构建议与GitHub Issue RFC。 |
| `code-mentor` | Comprehensive AI programming tutor offering interactive lessons, code reviews, debugging help, algorithm practice, and project guidance for Python and JavaScript. |
| `code-safety-audit` | 扫描代码安全漏洞，检测依赖漏洞、密钥泄露和OWASP安全模式。 |
| `code-to-chart` | 解析代码仓库的 import/依赖关系，自动生成架构图、流程图和组织架构图，输出 Mermaid 文本或 SVG 图片。 |
| `code-to-diagram` | Analyze codebases and automatically generate architecture diagrams, flowcharts, and org charts using AST parsing; outputs Mermaid or SVG. |
| `code-vuln-audit` | Scan code for security issues: dependency vulnerabilities, secret leaks, and OWASP anti-patterns like SQL injection, XSS, command injection. |
| `commodities-outlook` | Produce institutional-grade commodity outlook reports with supply-demand analysis, price forecasts, and trade recommendations (PDF/DOCX/PPTX). |
| `commodity-research-outlook` | 撰写遵循卖方券商惯例的大宗商品专业研究报告与投资建议，涵盖能源、金属及农产品。 |
| `competitive-seo-intel` | 深入分析竞争对手的SEO与GEO策略，涵盖关键词排名、内容打法、外链画像、技术SEO评估及AI引用模式。 |
| `competitor-analysis` | Analyzes competitor SEO and GEO strategies — ranking keywords, content, backlinks, and AI citations — to reveal opportunities to outperform them. |
| `compliance-review-planner` | 为特定业务场景构建合规检查清单，覆盖 GDPR、个保法、广告法、数据安全法等主要法规。 |
| `content-research-writer` | Assists in writing high-quality content by conducting research, adding citations, improving hooks, iterating on outlines, and providing real-time feedback. |
| `conventional-commit-gen` | Analyzes git diff to generate commit messages following the Conventional Commits spec, with automatic scope detection. |
| `copy-editing` | Edit, review, or improve existing marketing copy — feedback, proofreading, polish, copy sweeps. |
| `copy-editor` | 优化营销文案，通过七轮专业编辑（清晰度、语气、关我什么事、证据、具体化、情感、风险消除）来润色和强化表达。 |
| `copywriting` | Write, rewrite, or improve marketing copy for any page — homepage, landing, pricing, feature, about, or product pages. |
| `corr-insight` | 计算变量间的Pearson或Spearman相关矩阵、偏相关分析，并自动识别因混淆变量导致的伪相关。 |
| `correlation-auditor` | Analyzes correlation matrices (Pearson/Spearman), computes partial correlations, and flags potential spurious correlations. |
| `creative-writing` | Creative writing skill (file present in snapshot). |
| `cross-examine` | Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. |
| `cross-platform-adapter` | Adapts and repurposes content for LinkedIn, Twitter/X, WeChat, Zhihu, and Slack — adjusting tone, length, formatting, and language. |
| `customer-reply-craft` | 客服话术生成器，为售前咨询、售后服务、投诉处理、退换货四大场景生成专业回复。 |
| `cv-tailor` | Optimize resumes by matching keywords to the job description, rewriting experience with the quantified STAR method, and checking ATS compatibility. |
| `data-viz-gen` | 从 JSON 数据生成自包含的 HTML/SVG 信息图：KPI 统计卡片、分组柱状图、流程图和混合仪表盘，8 套配色。 |
| `data-viz-renderer` | Generate self-contained HTML/SVG infographics from JSON data: stat cards, bar charts, flow diagrams, and mixed dashboards. |
| `database-inspector` | 探索 SQLite 或 PostgreSQL 数据库，执行安全只读查询，提供表结构、数据预览，并生成 Mermaid ER 图。 |
| `database-scout` | Explore SQLite and PostgreSQL databases: list tables, inspect schemas, preview data, generate Mermaid ER diagrams, run safe read-only queries. |
| `dataset-health-audit` | 执行数据质量检查，对CSV/Excel/TSV/JSON等表格数据进行12个维度的全面审计，输出质量评分和修复建议。 |
| `dataset-quality-audit` | Run comprehensive quality checks on tabular data: missing values, duplicates, outliers, format issues, type inconsistencies. |
| `ddd-glossary-gen` | 从当前对话中提取和规范领域术语，生成DDD风格统一语言术语表，保存为UBIQUITOUS_LANGUAGE.md文件。 |
| `deep-module-refactor` | Explore a codebase to find architectural improvement opportunities, focusing on testability by deepening shallow modules. |
| `deep-probe` | 对用户的方案或设计进行连环追问，逐一排查决策树的每个分支，直到双方达成共识。 |
| `deep-research` | Conduct thorough, multi-dimensional research on complex questions using file creation, search engines, browsers, code execution, and multimedia generation. |
| `deep-research-swarm` | Orchestrate multi-agent epistemic triangulation: diverge across research dimensions, detect contradictions, verify deeply, converge into validated synthesis. |
| `design-system-builder` | Extract design systems from reference UI images and generate implementation-ready UI design prompts. |
| `dev-guide-generator` | Generates complete technical tutorials from prerequisites and environment setup to core steps, troubleshooting, and a final cheatsheet. |
| `dev-guide-writer` | 技术教程生成器：将任何技术主题转化为完整教程，包含前置知识、环境搭建、核心步骤、常见报错和速查表。 |
| `discounted-cashflow-model` | Builds a DCF valuation model with enterprise value, equity value, per-share price, and growth × discount sensitivity matrix. |
| `docx` | Create and edit Word documents (.docx) — C# + OpenXML SDK for creation, WIR engine for editing/comments/tracked changes. |
| `domain-glossary` | Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. |
| `earnings-review-note` | Generate professional sell-side earnings review reports for quarterly or annual results (PDF/DOCX/PPTX) with EPS analysis and variance tables. |
| `ecom-copy-assistant` | 一站式生成电商平台商品详情页文案，包括标题、核心卖点、规格参数和FAQ问答，适配淘宝、京东、亚马逊风格。 |
| `ecom-listing-copywriter` | Writes complete e-commerce product listing copy including titles, selling points, specifications, and FAQs for Taobao, JD.com, or Amazon. |
| `edge-tts` | Convert text to high-quality spoken audio using Microsoft Edge's neural TTS, with multiple voices, languages, speed/pitch, and subtitle generation. |
| `email-manager` | 收发和管理邮件，支持查看未读邮件、搜索邮件、下载附件、发送带附件的邮件，兼容Gmail、Outlook、QQ邮箱等。 |
| `email-newsletter-builder` | Generate professional HTML email newsletters compatible with Gmail and Outlook using table-based layouts with inline CSS. |
| `email-to-calendar` | Extract calendar events and deadlines from emails and create calendar entries; inbox-monitor or forward-to-address modes. |
| `equity-earnings-review` | 生成专业的卖方股票财报点评文档，覆盖上市公司季度或年度业绩回顾，含EPS分析、业绩指引点评、估值更新。 |
| `equity-research` | Analyze companies and generate investment research for Chinese A-shares, HK stocks, and US stocks: Tear Sheet (3-5p) or full Equity Report (≥25p PDF). |
| `equity-research-report` | Create institutional-grade investment research reports with sell-side styling, dense information layout, and comprehensive section structure. |
| `equity-research-report-cn` | 创建机构级别的投资研报，采用卖方研究视觉风格，对标高盛、摩根士丹利、摩根大通等投行研报风格。 |
| `equity-researcher` | 机构级投研报告生成技能，覆盖中国A股、港股、美股：投资速览（3-5页）或深度研报（≥25页，含三表模型、DCF）。 |
| `event-etf-study` | 基于关键事件进行ETF研究：识别相关股票，构建市值加权ETF指数，分析事件窗口市值变化，生成交互式HTML仪表盘。 |
| `fashion-sketch` | Create professional apparel technical specification packages (tech packs) with collection overviews, specs, measurement charts, BOM. |
| `fashion-sketch-cn` | 创建专业服装技术规格包（Tech Pack），包含系列概览、款式规格、工艺细节、尺寸表、面料库、物料清单。 |
| `fast-browser-use` | Fast browser automation with anti-bot bypass and DOM extraction via Chrome DevTools Protocol; runs 10x faster than Puppeteer. |
| `financial-ratio-toolkit` | Analyzes company fundamentals by computing 20+ financial ratios and DuPont Analysis from user-provided financial statements. |
| `financial-report-reader` | 财报三表深度解读，自动进行同比/环比变动分析并执行多维度财务异常检测。 |
| `financial-statement-analyzer` | Analyzes income statement, balance sheet, and cash flow data to generate YoY/QoQ trend analysis and flag anomalies. |
| `flashcard-studio` | 从学习材料中提取核心知识点，生成符合间隔重复记忆原理的闪卡，输出可直接导入Anki的CSV文件。 |
| `fund-risk-analyzer` | ETF多维对比工具：计算并对比多只ETF的年化收益率、最大回撤、夏普比率，并生成相关性矩阵图表。 |
| `fund-risk-compare` | Compare multiple ETFs using NAV CSV data: annualized return, max drawdown, Sharpe ratio, and correlation matrix. |
| `fundraising-bp-planner` | 生成融资BP大纲，完整覆盖从问题定义到融资需求的六大核心模块，并提供数据呈现建议。 |
| `gantt-chart-builder` | 根据任务列表和依赖关系生成交互式HTML甘特图，支持关键路径分析（CPM）。 |
| `gantt-planner` | Generate interactive HTML Gantt charts with Critical Path Method analysis from task lists and dependencies. |
| `general-writing` | General writing skill (file present in snapshot). |
| `geo-magazine-slides` | Create stunning geographic magazine-style presentation decks (PPTX) with editorial-quality layouts and large hero imagery. |
| `geo-magazine-slides-cn` | 创建震撼的地理杂志风格演示文稿（PPTX），具备编辑级版式、大幅主图、数据驱动图表与奢华美学。 |
| `git-repo-audit` | 深度分析 Git 仓库历史，识别高频变更的热点文件、分析代码贡献归属、扫描历史提交中的密钥泄露。 |
| `gitlab-cli-guide` | 提供 GitLab 命令行工具（glab）的完整参考与自动化脚本，涵盖超过30个子命令。 |
| `gitlab-cli-skills` | Guide users through GitLab CLI (glab) operations with command references and workflow examples for MRs, issues, CI/CD. |
| `guizang-ppt-skill` | 生成横向翻页网页 PPT（单 HTML 文件），含 WebGL 背景、章节幕封、数据大字报、图片网格等模板。 |
| `html-email-builder` | 生成兼容 Gmail/Outlook 的 HTML Newsletter，使用 table 布局和 inline CSS 确保渲染一致。 |
| `html-mail-builder` | 生成兼容 Gmail/Outlook/Apple Mail 的 HTML 邮件模板，采用 table 布局和 inline CSS，支持响应式设计。 |
| `html-mailer-builder` | Generate professional HTML email templates compatible with Gmail, Outlook, and Apple Mail. |
| `http-load-profiler` | Run stepped HTTP load tests with ab/wrk, collecting p50/p90/p99 latency and detecting performance inflection points. |
| `http-load-tester` | HTTP 阶梯式并发压测工具，采集 p50/p90/p99 延迟百分位数，输出结构化报告与最优并发建议。 |
| `humanizer` | Remove signs of AI-generated writing from text, based on Wikipedia's 'Signs of AI writing' guide. |
| `humanizer-zh` | 去除文本中的AI生成痕迹，使其读起来更自然、更像真人书写。 |
| `humanizer-zh-by-guizang` | 去除文本中的 AI 生成痕迹（归臧版）。 |
| `idea-to-prd` | 一句话需求生成完整产品需求文档（PRD），包含用户故事、功能清单、MoSCoW优先级排序和验收标准。 |
| `imap-smtp-email` | Manage email through IMAP and SMTP: read and search inboxes, fetch content, send emails with attachments. |
| `incident-retrospective` | 线上事故复盘与结构化 Blameless Postmortem 撰写工具，遵循 SRE 最佳实践。 |
| `incident-review-guide` | Blameless postmortem and incident review writing tool based on SRE best practices. |
| `interactive-research-report-en` | Turn any deep report/research document into a McKinsey/GS-grade interactive research website with drillable numbers. |
| `interface-design-lab` | 为模块生成多种截然不同的接口设计方案，通过并行探索产出多个接口签名、使用示例和封装说明。 |
| `interview-simulator` | 模拟真实面试官进行追问训练，覆盖行为面试、技术面试和案例面试三大场景。 |
| `investment-memo` | 创建结构清晰的投资分析备忘录（DOCX/PDF），支持风投式交易备忘录和主题/宏观备忘录两种格式。 |
| `investor-letter-writer` | Draft classic investment memos as DOCX or PDF, in the style of top VC deal memos or investor letters. |
| `investor-pitch-planner` | Generate a structured fundraising pitch deck outline covering Problem, Solution, Market, Business Model, Team, and The Ask. |
| `iso-27001-evidence-collection` | Collect, organize, and validate evidence for ISO 27001 and SOC 2 audits using API-first commands and cloud CLI tools. |
| `iteration-planner` | 敏捷 Sprint 规划助手，基于团队产能和历史 Velocity 完成 Sprint 范围选定、任务拆分估点、依赖分析。 |
| `journalistic-portrait` | Create magazine-style HTML pages replicating the visual design of Southern People Weekly. |
| `journalistic-portrait-cn` | 创建复刻《南方人物周刊》视觉设计的中文杂志风格 HTML 网页。 |
| `k8s-cluster-ops` | 通过 kubectl 命令行工具管理 Kubernetes 集群：查询资源、部署应用、查看日志、调试容器、监控集群健康。 |
| `keynote-composer` | Generates professional speech drafts for product launches, galas, TED-style talks using the Rhetorical Triangle framework. |
| `kimi-find-skills` | Search and discover skills for the agent — triggers on 'find skill', 'search skill', or when the user describes a problem. |
| `kimi-help-center` | Kimi Product Help Center — routes to the correct help center article on kimi.com for product/membership/billing questions. |
| `kimi-skills-finder` | 帮助用户搜索和发现Skills。 |
| `kimi-slides` | Create and edit presentations in PPTX format via the .pptd intermediate DSL; also reads/converts PPTX and renders infographics. |
| `kimi-widget` | Kimi widget design system — when to use an inline widget and the runtime contract (sandboxed iframe, design-system CSS). |
| `kubectl` | Execute kubectl commands to manage Kubernetes clusters — query pods, deploy apps, debug containers, monitor health. |
| `landing-page-scaffold` | Generate a self-contained landing page HTML prototype with Hero → Social Proof → Features → Pricing → CTA sections. |
| `legal-contract-gen` | 通过交互式问答生成常用法律文书初稿：NDA、服务协议、隐私政策、合作框架协议等。 |
| `legal-risk-analyzer` | 法律风险评估助手，基于“严重性 × 发生概率”框架评估法律风险并提供行动建议。 |
| `legal-risk-assessment` | Assess and classify legal risks using a severity-by-likelihood framework with escalation criteria. |
| `locale-guard` | 在前端代码库中搭建、审计和规范国际化/本地化流程，包括i18n框架配置、硬编码字符串替换、翻译键校验。 |
| `localization-toolkit` | Set up, audit, or enforce i18n/localization in UI codebases (React/TS, i18next, JSON locales). |
| `log-diagnostic` | 分析日志文件的错误模式，自动检测并输出错误聚类、频率统计和时间分布报告。 |
| `log-error-digest` | Analyze log files to troubleshoot errors: error clustering, frequency statistics, and time distribution reports. |
| `longread` | Longread skill (file present in snapshot). |
| `lp-proto-gen` | 一键生成结构完整的落地页HTML原型，包含Hero、Social Proof、Features、Pricing、CTA五大板块。 |
| `market-insight-report` | 生成具有顶级咨询公司视觉风格的数据驱动市场洞察报告（PDF/DOCX/PPTX）。 |
| `market-research-brief` | Generate professional consulting-style market insight reports with data-driven analysis and strategic recommendations. |
| `marketing-writer` | 撰写或优化各类页面的营销文案，专注于提升转化效果：标题、CTA、价值主张、首屏内容。 |
| `meeting-recap` | 将会议录音文字稿、笔记或聊天记录整理为结构化会议纪要，自动提取议题、结论和行动项。 |
| `mock-interview-drill` | Conduct realistic mock interviews with follow-up drills across Behavioral, Technical, and Case scenarios. |
| `nuwa-by-huashu` | 女娲造人：输入人名/主题，自动深度调研→思维框架提炼→生成可运行的人物Skill。 |
| `obsidian-markdown` | Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties. |
| `okr-planner` | OKR 制定/拆解/复盘教练。 |
| `okr-strategist` | OKR drafting, breakdown, and retrospective coach — objectives, key results, periodic reviews. |
| `outlier-scan` | CSV数据异常检测工具，使用Z-score、IQR、移动平均偏离三种方法扫描并分类异常点。 |
| `paper-review-coach` | 模拟学术同行评审，从原创性、方法论、结果、写作四个维度系统分析论文。 |
| `paper-writing` | Paper writing skill (file present in snapshot). |
| `pdf` | Professional PDF solution: HTML+Paged.js creation, Python processing, KaTeX/Mermaid/citations, LaTeX route. |
| `photo-magazine` | Create premium landscape documents with magazine-quality editorial design and data visualization cards. |
| `photo-magazine-cn` | 创建具备杂志级编辑设计品质的高端横版文档，主打粗体大字排版、满版出血摄影、数据可视化卡片。 |
| `pipeline-blueprint` | Provide CI/CD best practices and pipeline templates for GitHub Actions and GitLab CI. |
| `pitch-deck-creator` | Creates professional pitch decks and business plans in the style of a Chinese startup funding proposal. |
| `playwright-scraper-skill` | Scrape dynamic and anti-bot protected websites using Playwright; returns content, titles, screenshots. |
| `podcast-blueprint` | 为播客节目生成结构化的完整脚本，包含开场白、分段话题、过渡语、预设问题和收尾CTA。 |
| `podcast-episode-writer` | Creates complete, structured podcast scripts with timestamps for intros, topics, transitions, and CTAs. |
| `pricing-advisor` | 设计与优化SaaS产品的定价体系，包括套餐结构、价值指标、定价页面及涨价策略。 |
| `pricing-strategy` | Design, optimize, and communicate SaaS pricing — tier structure, value metrics, pricing pages, price increases. |
| `primary-market-research` | 生成专业的一级市场/风险投资（PE/VC）行业研究报告（PDF/DOCX/PPTX）。 |
| `pro-email-composer` | 商务邮件写作助手，覆盖催办、跟进、拒绝、感谢、道歉等常见场景，自动校准语气，中英双语。 |
| `process-doc` | Document a business process — flowcharts, RACI, and SOPs. |
| `product-spec-writer` | Transform one-line product ideas into complete PRD documents with user stories and MoSCoW prioritization. |
| `professional-email-composer` | Write professional business emails with tone adjusted for the recipient's role; bilingual Chinese-English. |
| `programming-tutor` | 全能 AI 编程导师，通过互动课程、代码审查、苏格拉底式调试引导、算法练习系统化教授编程。 |
| `project-sizing-guide` | Software project effort estimation: three-point estimates, T-shirt sizes, Function Point Analysis. |
| `py-perf-analyzer` | 定位 Python 脚本的性能瓶颈，集成 cProfile、tracemalloc 和 line_profiler。 |
| `quick-event-etf-study` | Event-driven concept ETF research with market-cap-weighted index construction and interactive HTML dashboard. |
| `quick-strategy-backtest` | Convert trading strategy descriptions into runnable backtest code with visual dashboards and writeups. |
| `r2-upload` | Upload files to Cloudflare R2, AWS S3, or S3-compatible storage and generate secure presigned download links. |
| `ref-style-converter` | 参考文献格式转换工具，可在APA、MLA、IEEE、Harvard四种格式间相互转换。 |
| `regression-insight` | 对 CSV/Excel 数据执行线性回归或逻辑回归，输出完整统计结果和中文通俗解读。 |
| `regression-modeler` | Run regression analysis (OLS or logistic) on uploaded CSV/Excel data with plain-language interpretation. |
| `regulatory-audit-generator` | Builds compliance checklists for business scenarios involving GDPR, PIPL, or advertising/data laws. |
| `repo-audit` | Deep analysis of Git history: hotspot files, code ownership, leaked secret scanning. |
| `report-writing` | Report writing skill (file present in snapshot). |
| `research-advisor` | 协助科研人员进行选题构思、项目规划、问题排查与科研决策。 |
| `research-paper-refiner` | 学术论文英文润色助手，按学术写作标准逐段审查语法、用词、语态与逻辑衔接。 |
| `research-writer` | 提供高质量的研究写作支持：资料调研、补充引用、优化开头、完善大纲、逐节反馈。 |
| `resume-craft` | 优化简历，基于目标岗位JD进行关键词匹配分析，用STAR法则量化改写经历描述。 |
| `retention-manager` | 用户挽留与流失防控助手：取消流程设计、挽留方案、催款邮件体系。 |
| `retro-tech-illustration` | Create retro tech art style visual content: Synthwave, Vaporwave, Cyberpunk, retro comics aesthetics. |
| `retro-tech-illustration-cn` | 创建复古科技艺术风格的视觉内容，覆盖 Synthwave、Vaporwave、Cyberpunk、复古漫画与复古未来主义美学。 |
| `rhetoric-speech-craft` | 生成发布会、年会、TED演讲等场景的专业演讲稿，基于修辞三角框架。 |
| `risk-heatmap` | 项目风险管理工具：录入风险条目，自动计算风险评分并生成交互式HTML风险热力图。 |
| `route-to-openapi` | Generates RESTful API documentation (OpenAPI 3.0 / Swagger) by scanning route definitions in code. |
| `rust-browser-pilot` | 基于 Rust 的高性能浏览器自动化工具，通过 Chrome DevTools 协议直接驱动浏览器。 |
| `saas-analyzer` | SaaS业务财务分析助手：计算ARR、流失率、LTV、CAC、NRR等关键指标并对标行业基准。 |
| `saas-metrics-coach` | SaaS financial health advisor — ARR, MRR, churn, LTV, CAC, NRR analysis from shared numbers. |
| `scholarly-writing-refiner` | Polishes academic English paragraph by paragraph: grammar, word choice, voice, coherence. |
| `sci-paper` | Structured guidance for composing scientific papers for top-tier venues (CVPR, NeurIPS, ACL, etc.). |
| `sci-paper-cn` | 按 CVPR、NeurIPS、ACL 等顶级会议惯例撰写、排版与呈现科研论文的结构化指南。 |
| `scientific-problem-selection` | Research problem selection, project ideation, troubleshooting stuck projects, strategic scientific decisions. |
| `secure-code-review` | Systematically reviews code for SQL injection, XSS, SSRF, broken access control, cryptographic failures, OWASP Top 10. |
| `seo-analyzer` | 网站SEO诊断与优化，提供全面的技术审计、页面内容分析和可执行建议。 |
| `seo-audit` | Audit, review, or diagnose SEO issues: technical SEO, rankings, on-page, meta tags, traffic drops. |
| `seo-content-writer` | Creates keyword-optimized SEO content using a 12-step workflow with CORE-EEAT checklist. |
| `seo-copywriting-guide` | 通过 12 步结构化工作流生成搜索引擎优化内容，含完整草稿、备选标题、Meta描述、FAQ。 |
| `short-video-script` | 生成抖音、TikTok、Reels短视频脚本，按「3秒Hook → 冲突 → 反转 → CTA」黄金结构。 |
| `skill-creator` | Guide for creating effective skills that extend agent capabilities. |
| `skill-creator-swarm` | Guide for creating effective skills, with swarm-style evaluation using sub-agents. |
| `smart-commit-gen` | Conventional Commits 规范化工具：分析 git diff 自动生成符合规范的提交信息。 |
| `smart-web-scraper` | 基于 Playwright 智能爬取网页内容，内置绕过 Cloudflare 等反爬机制的能力。 |
| `software-testing-guide` | 建立全面的软件QA测试流程，按照Google AAA标准编写测试用例，P0-P4分级追踪缺陷。 |
| `sop-writer` | 将业务流程梳理成完整的标准操作流程文档（SOP），包括流程图、RACI分工矩阵、详细操作步骤。 |
| `speech-synthesis` | 将文本转换为高质量语音，支持多语言、多种音色，可调节语速、音调和音量，并生成字幕。 |
| `split-test-evaluator` | A/B测试分析工具：转化率差异、显著性检验、置信区间、统计功效、最小样本量估算。 |
| `sprint-plan-builder` | Agile Sprint planning assistant: scope selection, story breakdown, dependency analysis, workload balancing. |
| `sql-insight` | Translate natural language to SQL, optimize query performance, and interpret EXPLAIN plans. |
| `sql-tutor` | 帮助编写和优化 SQL 查询：自然语言转SQL、查询优化建议、EXPLAIN 执行计划解读。 |
| `stock-finance-profiler` | 股票基本面分析工具：计算超过 20 项核心财务指标并进行详细的杜邦分析。 |
| `stock-research-report` | Generate securities research reports in Guotai Haitong / Haitong International style. |
| `stock-research-report-cn` | 生成国泰海通/海通国际风格的证券研究报告，支持国内与国际双模板。 |
| `stock-signal-analyzer` | Analyzes OHLCV data to compute 15+ technical indicators and generates bullish/bearish signal summary. |
| `stock-tech-analysis` | OHLCV 技术指标分析工具，计算15+种常见技术指标并生成多空信号汇总。 |
| `storage-analyzer-khazix` | macOS/Windows 只读存储分析助手：扫描磁盘占用，分级清理建议，生成交互式 HTML 报告。 |
| `story-map-builder` | Generates an interactive HTML user story map in Epic → Feature → Story structure with MoSCoW tagging. |
| `structured-minutes` | Transforms raw meeting materials into structured minutes with agenda topics, decisions, and action items. |
| `sun-path` | Analyzes sunlight and shadows for architectural design: sun path diagrams, solar position, shadow plots. |
| `sunlight-analysis` | 生成太阳轨迹图，计算实时太阳位置，分析建筑阴影投射范围与全年日照时数。 |
| `support-response-writer` | Generate professional customer support replies with emotional de-escalation strategies. |
| `swarm-workspace` | Swarm workspace skill (file present in snapshot). |
| `tdd-coach` | 指导测试驱动开发，遵循红-绿-重构循环。 |
| `terraform-deploy-pitfalls` | Operational traps for Terraform provisioners, multi-environment isolation, zero-to-deployment reliability. |
| `terraform-deploy-traps` | Terraform 部署实战踩坑指南，提供根因分析及可直接复制的修复方案。 |
| `test-driven-dev` | Test-driven development with red-green-refactor loop. |
| `test-suite-architect` | Establish comprehensive QA testing processes: strategies, Google-standard test cases, P0-P4 bug tracking. |
| `theme-factory` | Toolkit for styling artifacts with a theme: 10 pre-set themes with colors/fonts, or generate new ones on-the-fly. |
| `theme-kit` | 主题样式工具箱，内置10种预设风格（含配色与字体），也支持按需生成自定义主题。 |
| `timeline-builder` | Generate beautiful interactive timeline HTML pages from JSON data with vertical/horizontal/dual-side layouts. |
| `tos-clause-scanner` | Audit Terms of Service and privacy policies for consumer risks, flagging unfair clauses and data traps. |
| `tos-risk-checker` | 以消费者视角审计服务条款，识别霸王条款、隐蔽数据授权、自动续费陷阱等风险。 |
| `trading-strategy-backtest` | 将投资交易策略描述转成可运行的回测代码，输出回测结果、可视化图表和分析报告。 |
| `translation-craft` | Professional Chinese-English translation across academic, business, technical, and legal domains. |
| `ui-blueprint` | 从参考 UI 截图中提取完整的设计系统，生成设计文档并产出可直接用于实现的 MVP 界面提示词。 |
| `user-story-canvas` | 将产品需求可视化为交互式HTML用户故事地图，支持MoSCoW优先级色标和版本发布划线分组。 |
| `value-invest-scorer` | 巴菲特/格雷厄姆风格的价值投资评估技能，从护城河、管理层、财务、估值四大维度评分。 |
| `value-investing-scorecard` | Buffett/Graham value investing scorecard — 20 criteria in four dimensions, 0-100 score. |
| `vc-industry-research` | Generate professional primary market / VC industry research reports with sector deep-dives. |
| `vibecoding-general-swarm` | Vibecoding swarm skill (file present in snapshot). |
| `vibecoding-webapp-swarm` | Vibecoding webapp swarm skill (file present in snapshot). |
| `video-compare-tool` | 对比两个视频的压缩质量，计算画质指标（PSNR、SSIM），生成逐帧视觉对比的交互式 HTML 报告。 |
| `video-outline-planner` | 为B站UP主生成完整的视频策划方案：选题分析、结构设计、互动设计。 |
| `video-quality-diff` | Compare two videos for compression quality: PSNR, SSIM, frame-by-frame interactive HTML reports. |
| `web-security-audit` | 基于 OWASP Top 10 (2021) 标准提供代码安全审查，给出漏洞代码示例与修复方案。 |
| `webapp-building` | Tools for building modern React webapps with TypeScript, Tailwind CSS and shadcn/ui. |
| `webapp-building-swarm` | Swarm variant of webapp-building for parallel multi-agent webapp construction. |
| `wechat-post-craft` | 微信公众号文章写作助手，帮你写出高打开率、高转发率的爆款文章。 |
| `weighted-scorer` | Builds weighted scoring decision matrices for technology selection and vendor evaluation. |
| `weighted-scoring` | 加权评分决策矩阵框架，用于技术选型、供应商选择、方案对比等多准则决策场景。 |
| `whatsapp-integration` | WhatsApp integration for sending messages, managing contacts, and interacting with chats and groups. |
| `work-recap-writer` | Turn scattered work notes and git logs into structured weekly or monthly reports. |
| `work-report-writer` | 从零散的工作记录和 git log 生成结构化的周报或月报。 |
| `workload-calculator` | 软件项目工时估算助手：三点估算(PERT)、T-shirt sizing、功能点分析。 |
| `x-thread-crafter` | Craft engaging Twitter/X threads from long-form content with ≤280-character tweets. |
| `xhs-note-creator` | 小红书笔记全流程创作工具，自动撰写笔记内容并渲染生成精美的3:4比例图片卡片。 |
| `xindaya-translator` | 提供专业的中英双向翻译，遵循信达雅原则，并包含回译验证和质量检查清单。 |
| `xlsx` | Advanced spreadsheet manipulation: formulas, formatting, recalculation, finance modeling (3-statement, DCF, comps). |
| `zhihu-viral-answer` | 知乎高赞回答生成助手，匹配故事+干货+金句的最佳回答结构。 |

---
*Сгенерировано автоматически из `/app/.agents/skills` и `/app/.agents/plugins`.*
