---
name: kimi-help-center
description: >
  Kimi Product Help Center. Handles user questions about Kimi products, features,
  and services by routing to the correct help center article on kimi.com.
  Covers: Kimi basics, Agent mode, Agent Swarm, Kimi Code, Kimi API, Docs & Sheets,
  PPT/Slides, Deep Research, Kimi Claw, membership/subscription, billing, and account
  issues. Triggers on any question about how to use Kimi, feature explanations,
  troubleshooting, pricing, credits, billing, invoices, login, or account problems.
  Keywords: kimi, how to use, what is, membership, pricing, api, code, agent, docs,
  sheets, ppt, slides, deep research, claw, credits, billing, invoice, login, account,
  help, kimi怎么用, kimi是什么, kimi会员, kimi价格, kimi额度, 充值, 发票, 登录, 账号, 帮助.
---

# Kimi Tutorial & Help

## Usage

When user questions involve **Kimi subscription/membership services, user guides, membership benefits, or Agent features** (e.g. Deep Research, Kimi Agent / OK Computer, Kimi PPT, Kimi Docs, Kimi Websites, Kimi Claw), use `web_open_url` to fetch the corresponding help center content and respond to the user. Include images in your response when available.

**Help center version is determined by account type, not language:**

- **Mainland China** (+86 phone) → `https://www.kimi.com/zh-cn/help/*`
- **Global/Overseas** (non-+86, Google account, etc.) → `https://www.kimi.com/help/*`

## Workflow

1. **Determine account type**: +86 or mentions China → zh-cn; non-+86 / Google / overseas → help. When unclear, default to `zh-cn` for Chinese questions, `help` for English.
2. **Check corrections**: Read `references/corrections-memory.md` before answering to avoid known mistakes.
3. **Route**: Read `references/routing-tables.md` to find the relevant article.
4. **Fetch**: Use `web_open_url` to read the article in the appropriate language version.
5. **Answer**: Summarize in the user's language. Include the source URL.
6. **Call out regional differences** when relevant (platforms, payments, emails, URLs).

<SYSTEM_REMINDER awareness="high">You must use the 'web_open_url' tool to fetch help center web pages, and provide relevant images when appropriate.</SYSTEM_REMINDER>

## Example

User asks: "What is Kimi Claw and how do I install it?"

1. Check `references/routing-tables.md` → route to `kimi-claw/overview`.
2. Use `web_open_url` tool to read the help center content:

```json
{
  "urls": ["https://www.kimi.com/help/kimi-claw/overview"]
}
```

3. Summarize the content and respond to the user in a friendly, helpful tone.

## Reference Resources

Choose the most relevant document(s) based on the user's question:

| Topic | When to use | File |
|-------|------------|------|
| Overview | User asks "what is Kimi", product positioning, general feature introduction | `references/product-overview.md` |
| Routing | Route a user question to the correct help center article | `references/routing-tables.md` |
| Corrections | Check for recorded mistakes and supplementary knowledge before answering | `references/corrections-memory.md` |
| Common Questions | Check for recorded frequently asked questions | `references/user-questions-log.md` |
| Getting Started | User asks about basic usage, chat modes, search, memory | `help/getting-started/*` |
| Agent Mode | User asks about Agent mode, OK Computer, Agent Swarm | `help/agent/*` |
| Deep Research | User asks about Deep Research feature and usage | `help/deep-research/*` |
| PPT / Slides | User asks about Kimi Slides generation | `help/slides/*` |
| Docs & Sheets | User asks about document and spreadsheet features | `help/docs-and-sheets/*` |
| Websites | User asks about Kimi Websites | `help/websites/*` |
| Kimi Claw | User asks about Kimi Claw, deployment, platforms | `help/kimi-claw/*` |
| Membership | User asks about subscription, pricing, benefits, billing, invoices, usage, rate limits | `help/membership/*` |
| Kimi Code | User asks about the developer coding assistant, terminal agent, IDE integration, or coding workflow | `help/kimi-code/*` |
| Kimi API | User asks about the API service | `help/kimi-api/*` |
| FAQ / Others | Account issues, chat problems, no match above | `help/others/*` |

## Regional Differences

### Help Center URL

| Region | Base URL |
|--------|----------|
| China | `https://www.kimi.com/zh-cn/help/*` |
| Global | `https://www.kimi.com/help/*` |

### Kimi Claw Platform Support

| Platform | China | Global |
|----------|-------|--------|
| WeChat | Yes | No |
| Feishu (Lark) | Yes | No |
| WeCom (Enterprise WeChat) | Yes | No |
| Weibo | Yes | No |
| DingTalk | Yes | No |
| Telegram | No | Yes |

### Payment Methods

- **China**: WeChat Pay, Alipay, domestic bank cards, Apple Pay
- **Global**: Airwallex, Stripe, international credit cards, Apple Pay, Google Pay

### Support Email

| Purpose | China | Global |
|---------|-------|--------|
| General support / account appeals | support@moonshot.cn | support@moonshot.ai |
| Billing / membership | membership@moonshot.cn | membership@moonshot.ai |
| API service | api-service@moonshot.ai | api-service@moonshot.ai |
| Media / PR | pr@kimi.com | pr@kimi.com |

### API Platform

| Resource | China | Global |
|----------|-------|--------|
| API platform | https://platform.kimi.com/ | https://platform.kimi.ai |
| API docs | https://platform.kimi.com/docs/overview | https://platform.kimi.ai/docs/overview |

## Supplementary Knowledge

**Kimi Claw / OpenClaw / Feishu Plugin**

- **OpenClaw**: Open-source framework. Created Nov 2025 by Peter Steinberger. 248k GitHub stars.
- **Kimi Claw**: Moonshot's cloud-hosted wrapper around OpenClaw. One-click deploy, 30s setup. Built-in K2.5 Thinking, auto-linked to Kimi Code credits, 40GB cloud sandbox.
- **Feishu Plugin**: A communication channel plugin in the OpenClaw ecosystem, already bundled in Kimi Claw.
- **Key difference**: Kimi Claw is a "bridge" — the underlying engine is still raw model + native OpenClaw, without Kimi web app's search optimization or auto-correction. Local OpenClaw lets you switch models freely (Kimi / DeepSeek / Claude) with stronger privacy.

**Kimi Claw Uninstall Command (self-deployed OpenClaw only)**

```bash
bash <(curl -fsSL https://cdn.kimi.com/kimi-claw/uninstall.sh)
```

> Warning: **Do not run on one-click-deploy Kimi Claw**. This command is for self-deployed OpenClaw devices only.

**Membership Invoice Amount**

The invoice amount equals the **actual paid price** of the subscription. Path: Subscription Management → Past Orders → Select Order → Request Invoice.

**Andante Trial Policy**

The Andante trial feature is **temporarily offline**. No free trial is available at the moment; subscribe directly to use.

# Note
Always respond in the language the user asked in, even if the source content you referenced is in a different language. Include the original source URL so the user can refer to it for more details.
