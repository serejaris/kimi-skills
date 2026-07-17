# Equity Report — Phase 4: Visual Design + Report Generation

> **This file is read by the agent during Task 3 (Report Generation) via `SKILL-task3-report.md`.**
> All paths are relative to the skill root directory.
>
> **Task 3 Note**: All analytical content comes from the Task 1 Research Document and Task 2 Valuation Analysis.
> Financial data is extracted from the Task 2 Excel model via openpyxl. The layout instructions in this file
> (HTML templates, CSS classes, page break rules) are what you need for report generation.

---

## 4.1 Layout Strategy

**Equity report does NOT self-layout in dual-box format.** Output complete analysis content (text + charts + tables) as structured HTML, then **generate PDF via Playwright native `page.pdf()`**.

**Why**: Playwright native `page.pdf()` uses Chromium's print engine — reliable, no skill dependency, full CSS @page support. 

### PDF Generation Rules
- ✅ Use **Playwright native `page.pdf()`** for HTML → PDF conversion
- ❌ **DO NOT call or invoke the environment PDF skill.** Paged.js has strict Mermaid limits (≤12 nodes, ≤3 subgraphs) that conflict with our supply chain diagrams (≥20 nodes, ≥4 layers).
- ❌ **DO NOT let any external tool generate a cover page.** Our report has its own cover page design (see §Cover Page below).
- ❌ **DO NOT add any headers, footers, or front matter** in the HTML body. Use Playwright `header_template`/`footer_template` parameters in `page.pdf()`.

**CSS sole source**: `output/report.css` — read the file and embed its full content in a `<style>` tag within the HTML `<head>`. Do NOT use `<link rel="stylesheet">`.

**Hard Constraints**:
- Page Margin: 18mm top/bottom, 20mm left/right
- Chinese: `.report-container`
- English: `.report-container report-container-en`
- Content: Full-width paragraphs as primary layout
- Two-column only when explicitly needed (e.g., scenario + risk side-by-side)

---

## 4.2 Content Structure

### Running Header / Footer (P1)

### Running Header / Footer (Playwright header_template/footer_template)

**Do NOT** add these as HTML elements in the body. Playwright's `page.pdf()` accepts `header_template` and `footer_template` parameters that inject headers/footers automatically. These appear on every page EXCEPT the cover (`@page :first` suppresses them).

```python
header_html = (
    '<div style="display:flex;justify-content:space-between;width:100%;'
    'font-size:8pt;color:#888;font-family:Helvetica Neue,Arial,sans-serif;'
    'border-bottom:0.5px solid #CCC;padding-bottom:3px;margin:0 20px;">'
    '<span style="white-space:nowrap;">Kimi Research — Equity Research</span>'
    '<span style="white-space:nowrap;">[Company Name] ([Ticker])</span></div>'
)
footer_html = (
    '<div style="display:flex;justify-content:space-between;width:100%;'
    'font-size:7.5pt;color:#AAA;font-family:Helvetica Neue,Arial,sans-serif;'
    'border-top:0.5px solid #DDD;padding-top:3px;margin:0 20px;">'
    '<span style="white-space:nowrap;">[Report Date]</span>'
    '<span style="white-space:nowrap;">Page <span class="pageNumber"></span>'
    ' / <span class="totalPages"></span></span></div>'
)

page.pdf(
    path="report.pdf", format="A4", print_background=True,
    margin={"top": "18mm", "right": "20mm", "bottom": "18mm", "left": "20mm"},
    display_header_footer=True,
    header_template=header_html,
    footer_template=footer_html
)
```

### Cover Page — Left-Right Split (P1) — Kimi Research Branded

**Cover additions:**
- Cover rating line → `.price-target-bar` (Current → Target → Upside)
- Right-column Key Data → `.key-data-grid` (denser 2-col grid)
- **Kimi Research header branding** — every cover page is authored by Kimi Research
- All numbers use tabular-nums for clean vertical alignment
- **No analyst bylines or hardcoded sample tickers**

### Cover Language Rules (report_language driven)

| `report_language` | Cover Title | Key Data Sidebar   | Exec Summary | Module Titles |
| ----------------- | ----------- | ------------------ | ------------ | ------------- |
| `zh` (Chinese)    | 中文          | 中文标签 + 英文metrics保留 | 中文           | 中文            |
| `en` (English)    | English     | English            | English      | English       |

**Chinese report — what to translate vs. keep in English:**
- ✅ **Translate**: 标题、正文、标签、段落、模块名称、产业链图标题
- ✅ **Keep English**: 财务metrics (P/E, EV/EBITDA, P/B, EPS, ROE, FCF Yield 等)、公司英文名称、产品英文名称、Ticker代码
- ✅ **Mixed**: "P/E 市盈率" (metric缩写保留，中文释义可添加)

**Example (zh)**: `Key Data` → `关键数据`, `Executive Summary` → `摘要`, `Investment Thesis` → `投资论点`, but `P/E (FY1)` stays as `P/E (FY1)`.

```html
<!-- Kimi Research branding bar — full-width, above the split layout -->
<div class="kimi-brand-bar">
  <span class="kimi-logo">Kimi Research</span>
  <span class="kimi-tagline">AI-Powered Equity Research</span>
</div>

<div class="cover-split">
  <!-- Left 60%: headline + viewpoint -->
  <div class="cover-main">
    <div class="header-top">
      <div class="header-company">
        <span class="header-name">[Company Name]</span>
        <span class="header-code">[Ticker]</span>
      </div>
      <div class="header-tags">
        <span class="tag">[Sector]</span>
        <span class="tag highlight">[Market]</span>
      </div>
    </div>
    <h1 class="header-main-title">[Core Judgment — 8-15 words]</h1>

    <div class="cover-rating-line">
      <span class="cover-rating-badge">[Rating e.g. BUY / HOLD / SELL]</span>
    </div>

    <!-- Price Target Bar -->
    <div class="price-target-bar">
      <div class="ptb-cell">
        <div class="ptb-label">Current</div>
        <div class="ptb-value">[$XXX.XX]</div>
      </div>
      <div class="ptb-cell">
        <div class="ptb-label">12m Target</div>
        <div class="ptb-value">[$XXX.XX]</div>
      </div>
      <div class="ptb-cell">
        <div class="ptb-label">Upside</div>
        <div class="ptb-value ptb-upside-positive">[+XX.X%]</div>
        <!-- Use ptb-upside-negative for downside, ptb-upside-neutral for ≤2% -->
      </div>
    </div>

    <div class="cover-viewpoint">[4-6 sentence core viewpoint paragraph]</div>
  </div>

  <!-- Right 40%: Key Data sidebar (expanded grid) -->
  <div class="cover-sidebar">
    <div class="sidebar-title">Key Data</div>

    <!-- Key Data Grid — labels adapt to report_language -->
    <!-- zh labels: 关键数据 / 市场 / 股价 / 市值 / 52周高 / 52周低 / 3月日均成交额 / 自由流通比例 / 收益 / 估值 -->
    <!-- en labels: Key Data / Market / Price / Mkt Cap / 52w High / 52w Low / ADTV (3m) / Free Float / Return / Valuation -->
    <!-- Financial metrics (P/E, EV/EBITDA, P/B, Div Yield) ALWAYS stay in English regardless of language -->
    <div class="key-data-grid">
      <div class="kd-group-header">[Market / 市场]</div>
      <div class="kd-row"><span class="kd-label">[Price / 股价]</span><span class="kd-value">[$XXX.XX]</span></div>
      <div class="kd-row"><span class="kd-label">[Mkt Cap / 市值]</span><span class="kd-value">[$X.XXT]</span></div>
      <div class="kd-row"><span class="kd-label">[52w High / 52周高]</span><span class="kd-value">[$XX.XX]</span></div>
      <div class="kd-row"><span class="kd-label">[52w Low / 52周低]</span><span class="kd-value">[$XX.XX]</span></div>
      <div class="kd-row"><span class="kd-label">[ADTV (3m) / 3月日均成交]</span><span class="kd-value">[$XXM]</span></div>
      <div class="kd-row"><span class="kd-label">[Free Float / 自由流通比]</span><span class="kd-value">[XX.X%]</span></div>

      <div class="kd-group-header">[Return / 收益]</div>
      <div class="kd-row"><span class="kd-label">3m</span><span class="kd-value">[±XX.X%]</span></div>
      <div class="kd-row"><span class="kd-label">6m</span><span class="kd-value">[±XX.X%]</span></div>
      <div class="kd-row"><span class="kd-label">12m</span><span class="kd-value">[±XX.X%]</span></div>
      <div class="kd-row"><span class="kd-label">YTD</span><span class="kd-value">[±XX.X%]</span></div>

      <div class="kd-group-header">[Valuation / 估值]</div>
      <div class="kd-row"><span class="kd-label">P/E (FY1)</span><span class="kd-value">[XX.Xx]</span></div>
      <div class="kd-row"><span class="kd-label">EV/EBITDA</span><span class="kd-value">[XX.Xx]</span></div>
      <div class="kd-row"><span class="kd-label">P/B</span><span class="kd-value">[X.Xx]</span></div>
      <div class="kd-row"><span class="kd-label">Div Yield</span><span class="kd-value">[X.X%]</span></div>
    </div>

    <div class="sidebar-forecast">
      <div class="forecast-title">[Earnings Forecast / 盈利预测]</div>
      <table>
        <tr><th></th><th>[FYn-1]</th><th>[FYn E]</th><th>[FYn+1 E]</th></tr>
        <tr><td>Revenue</td><td>[$XXB]</td><td>[$XXB]</td><td>[$XXB]</td></tr>
        <tr><td>EPS</td><td>[$X.XX]</td><td>[$X.XX]</td><td>[$X.XX]</td></tr>
      </table>
    </div>
  </div>
</div>
```

**Key rules**:
- `.kimi-brand-bar` is a **standalone full-width element** above `.cover-split` — NOT inside `.cover-split`
- `.cover-split` uses `display: table` with `.cover-main` (60%) and `.cover-sidebar` (40%) as `display: table-cell`
- Left side (`.cover-main`): rating badge, Price Target Bar, core viewpoint
- Right side (`.cover-sidebar`): Key Data Grid (2×N) + 3-year earnings forecast mini-table
- All bracketed `[...]` values MUST be populated from real data (Task 1 research + Task 2 Excel); never leave placeholders, never fabricate, never copy sample tickers (AAPL/BYD/TSLA/MSFT)
- The `.header-top` bar spans only the left column (inside `.cover-main`)
- The `key-data-table` class still works (backward-compat) but new reports must use `key-data-grid`

### Executive Summary — Below Cover Split (Still Page 1)

Place this section **inside** `.report-container`, immediately **after** the closing `</div>` of `.cover-split` and **before** any `<h2>` content body sections. The CSS `page-break-after: always` on `.exec-summary` ensures page 1 ends here.

**Language**: Title and labels follow `report_language`:
- `zh`: `摘要` (not "Executive Summary"), labels: `投资论点`, `财务亮点`, `估值与目标价`, `关键风险`
- `en`: `Executive Summary`, labels as shown below

```html
<div class="exec-summary">
  <div class="exec-summary-title">[Executive Summary / 摘要]</div>
  <div class="exec-summary-grid">
    <div class="exec-summary-item">
      <span class="es-label">[Investment Thesis / 投资论点]</span>
      <span class="es-content">[1-2 sentences: core structural advantage, paradigm positioning, why this company deserves attention now]</span>
    </div>
    <div class="exec-summary-item">
      <span class="es-label">[Financial Highlights / 财务亮点]</span>
      <span class="es-content">[1-2 sentences: latest revenue/growth, margin trend, earnings quality signal — pull key numbers from Task 2 model]</span>
    </div>
    <div class="exec-summary-item">
      <span class="es-label">[Valuation & Target / 估值与目标价]</span>
      <span class="es-content">[1-2 sentences: valuation method summary, target price derivation, upside/downside vs. current price]</span>
    </div>
    <div class="exec-summary-item">
      <span class="es-label">[Key Risks / 关键风险]</span>
      <span class="es-content">[1-2 sentences: top 2-3 risks from risk framework, with probability/impact indicator]</span>
    </div>
  </div>
</div>
```

**Content Rules**:
- Each item is **1-2 sentences max** — concise, data-driven, no filler
- Use specific numbers (e.g., "Revenue +15.7% YoY to RMB 174B", "DCF implies 28% upside")
- Language matches `report_language` (Chinese report → Chinese content, English report → English content)
- Content is distilled from: Research Document §I (thesis), Task 2 model (financials), Valuation Analysis (target), Risk Framework (risks)
- The entire cover page (`.cover-split` + `.exec-summary`) must fit on a single A4 page — if it overflows, shorten the `cover-viewpoint` paragraph first, then trim exec summary items

---

### Page 2 — Data Summary Page (MANDATORY, force-include)

> **This module is REQUIRED on every equity report. No exceptions.**
> The entire page must fit on ONE A4 page. If the content overflows, tighten padding, reduce font-size from 7.5pt to 7pt on `.ds-table-dense`, or trim line items.
> All numbers come from the Task 2 Excel model. Never use placeholder data.
> Chart on this page is chart **C6 (Price Performance rebased)** — see `modules/equity-report-charts.md`.

```html
<div class="module-row data-summary-page">
  <div class="ds-title">[Financial Summary / 财务数据摘要]</div>
  <div class="ds-subtitle">All figures from company filings and model calculation. FY denotes fiscal year. E = estimate.</div>

  <div class="ds-grid">
    <!-- LEFT COLUMN (45%) -->
    <div class="ds-left">

      <div class="ds-block">
        <div class="ds-block-title">[Ratios & Valuation / 比率与估值]</div>
        <table class="ds-table-dense">
          <thead>
            <tr>
              <th>[Metric]</th>
              <th>[FYn-2]</th>
              <th>[FYn-1]</th>
              <th>[FYn]</th>
              <th class="ds-forecast-header">[FYn+1 E]</th>
              <th class="ds-forecast-header">[FYn+2 E]</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>P/E (x)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>EV/EBITDA (x)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>P/B (x)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>P/S (x)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Dividend Yield (%)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>FCF Yield (%)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>ROE (%)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>ROIC (%)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Net Debt / EBITDA (x)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
          </tbody>
        </table>
      </div>

      <div class="ds-block">
        <div class="ds-block-title">[Growth & Margins / 成长与利润率]</div>
        <table class="ds-table-dense">
          <thead>
            <tr>
              <th>[Metric]</th>
              <th>[FYn-2]</th>
              <th>[FYn-1]</th>
              <th>[FYn]</th>
              <th class="ds-forecast-header">[FYn+1 E]</th>
              <th class="ds-forecast-header">[FYn+2 E]</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Revenue growth (%)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>EBITDA growth (%)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>EPS growth (%)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Gross margin (%)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Operating margin (%)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Net margin (%)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
          </tbody>
        </table>
      </div>

      <div class="ds-block">
        <div class="ds-block-title">[Price Performance / 股价表现]</div>
        <!-- Chart C6: 12-month rebased performance vs. benchmark + sector
             Generated by chart_generator.py (chart_type: price_performance)
             Embed as base64 SVG via embed_charts.py -->
        <div class="chart-container" style="text-align:center;margin:4px 0;">
          <!-- Placeholder: {{C6_IMG_TAG}} — replaced during build -->
        </div>
        <table class="perf-table">
          <thead>
            <tr><th>Return</th><th>3m</th><th>6m</th><th>12m</th><th>YTD</th></tr>
          </thead>
          <tbody>
            <tr><td>[Ticker]</td><td>[..%]</td><td>[..%]</td><td>[..%]</td><td>[..%]</td></tr>
            <tr><td>[Benchmark]</td><td>[..%]</td><td>[..%]</td><td>[..%]</td><td>[..%]</td></tr>
            <tr><td>[Sector]</td><td>[..%]</td><td>[..%]</td><td>[..%]</td><td>[..%]</td></tr>
          </tbody>
        </table>
        <div class="data-source">Model calculation; exchange data as of [date]</div>
      </div>

    </div>

    <!-- RIGHT COLUMN (55%) -->
    <div class="ds-right">

      <div class="ds-block">
        <div class="ds-block-title">[Income Statement / 利润表] ([currency] [unit])</div>
        <table class="ds-table-dense">
          <thead>
            <tr>
              <th>[Line item]</th>
              <th>[FYn-2]</th>
              <th>[FYn-1]</th>
              <th>[FYn]</th>
              <th class="ds-forecast-header">[FYn+1 E]</th>
              <th class="ds-forecast-header">[FYn+2 E]</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Revenue</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>  COGS</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td></tr>
            <tr class="ds-row-total"><td>Gross Profit</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>  SG&A</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td></tr>
            <tr><td>  R&D</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td></tr>
            <tr class="ds-row-total"><td>Operating Income</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>  Interest / Other</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>  Tax</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td></tr>
            <tr class="ds-row-total"><td>Net Income</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Diluted EPS</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>DPS</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
          </tbody>
        </table>
      </div>

      <div class="ds-block">
        <div class="ds-block-title">[Balance Sheet / 资产负债表] ([currency] [unit])</div>
        <table class="ds-table-dense">
          <thead>
            <tr>
              <th>[Line item]</th>
              <th>[FYn-2]</th>
              <th>[FYn-1]</th>
              <th>[FYn]</th>
              <th class="ds-forecast-header">[FYn+1 E]</th>
              <th class="ds-forecast-header">[FYn+2 E]</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Cash & Equivalents</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Current Assets</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>PP&E (net)</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Intangibles / Goodwill</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr class="ds-row-total"><td>Total Assets</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Current Liabilities</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Long-term Debt</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr class="ds-row-total"><td>Total Equity</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>Net Debt</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
          </tbody>
        </table>
      </div>

      <div class="ds-block">
        <div class="ds-block-title">[Cash Flow / 现金流量表] ([currency] [unit])</div>
        <table class="ds-table-dense">
          <thead>
            <tr>
              <th>[Line item]</th>
              <th>[FYn-2]</th>
              <th>[FYn-1]</th>
              <th>[FYn]</th>
              <th class="ds-forecast-header">[FYn+1 E]</th>
              <th class="ds-forecast-header">[FYn+2 E]</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Net Income</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>  D&A</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>  Working capital Δ</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr class="ds-row-total"><td>CFO</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>  CapEx</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td></tr>
            <tr class="ds-row-total"><td>Free Cash Flow</td><td>[..]</td><td>[..]</td><td>[..]</td><td class="ds-col-forecast">[..]</td><td class="ds-col-forecast">[..]</td></tr>
            <tr><td>  Dividends</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td></tr>
            <tr><td>  Buybacks</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td><td class="ds-col-forecast neg-paren">([..])</td></tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
  <div class="data-source" style="margin-top:6px;">Company filings (annual + interim); model calculation. Forecast periods shown with light highlight.</div>
</div>
```

**Page 2 Rules (MANDATORY)**:
1. This entire block must fit on ONE A4 page. If it doesn't: reduce `.ds-table-dense` line-items (drop 1-2 secondary rows), then tighten padding, then last resort shrink font to 7pt.
2. Column headers use pattern `FYn-2 / FYn-1 / FYn / FYn+1 E / FYn+2 E`. Map `n` to the latest completed fiscal year.
3. Forecast columns have `.ds-col-forecast` class (light cream background) + `.ds-forecast-header` on `<th>` (italic color).
4. Negative values use `(123.4)` via `.neg-paren` class (never `-123.4`).
5. Labels use `report_language` — Chinese reports show Chinese labels; English reports show English labels. Pick ONE, never mix.
6. **Every single number in the 4 tables must come from the Task 2 Excel model.** If a cell is truly not available, leave it as "n.m." (not meaningful) — never invent.
7. Chart C6 (Price Performance) is required in the Price Performance block. If C6 generation fails, fall back to a 3-row table only and mark QA flag.

---

### Glossary Section (MANDATORY, force-include)

> **Placed right before the Compliance Disclaimer (after References & Data Sources).**
> Terms are sector-filtered — pick ≥6 and ≤12 terms that actually appear in this specific report. Never leave boilerplate placeholders. Never hardcode terms unrelated to the company's sector.

**Sector term banks (examples — expand/filter to fit the report)**:

- Oil / Petrochemical: PX (paraxylene), PTA, MEG, 裂解价差 (crack spread), 芳烃联合装置, 炼化一体化, 轻质化, catalytic cracker utilization
- Semiconductors / Tech: HBM, ASP, wafer yield, NAND/DRAM bit growth, capex intensity, foundry node migration, design wins
- Consumer: DTC, ASP, same-store sales (SSS), sell-through, channel mix, brand elasticity
- Industrials: book-to-bill, backlog coverage, capex cycle, order intake, utilization
- Financials: NIM, CET1, cost-of-risk, LDR, provision coverage, RWA
- EV / Auto: BOM cost, battery GWh, take-rate, ASP mix, localisation rate, OEM capture

```html
<div class="module-row glossary-section">
  <div class="glossary-title">[Glossary / 术语表]</div>
  <div class="glossary-grid">
    <div class="glossary-item">
      <span class="glossary-term">[Term 1]</span>
      <span class="glossary-def">[One-line definition as used in this report.]</span>
    </div>
    <div class="glossary-item">
      <span class="glossary-term">[Term 2]</span>
      <span class="glossary-def">[One-line definition.]</span>
    </div>
    <!-- ... 6-12 terms total, 2 columns auto-fill ... -->
  </div>
  <div class="data-source" style="margin-top:6px;">Definitions compiled from industry standards and company disclosures.</div>
</div>
```

**Glossary Rules**:
1. Minimum 6 terms, maximum 12 terms. Terms must be sector-appropriate.
2. Definitions in same language as report (`report_language`).
3. Every term used in the glossary must appear somewhere else in the report (no orphan terms).
4. Every term must be sector-relevant and used elsewhere in the report.

---

### Exhibit Index (Recommended, force-include)

> **Placed right after the Table of Contents (if TOC present).**
> Uses `.figure-index` class (already in `report.css`). Replaces ad-hoc exhibit lists.

See §4.6 below for the HTML pattern (already in the file) — change: **always include** the Exhibit Index for equity reports (previously optional). Count the entries; must match the actual exhibit count in the body.

---

### Content Body

1. **Title hierarchy**: `<h2>` for section titles, `<h3>` for sub-sections
2. **Paragraphs**: Fully developed, not bullets. Each paragraph 3-5 sentences with data support.
3. **Charts/Tables**: Embedded inline with Exhibit numbering
4. **No dual-box layout by default**: Use `.two-column` only for specific paired content (e.g., scenario + risk)
5. **Callout boxes**: Use `.callout` class for key insights or important conclusions

### Writing Conventions (Institutional Standards)

**Bold-Keyword Paragraphs (P6):** Begin analytical paragraphs with a bolded key phrase + colon, then continue in normal weight. This aids scanability.

```html
<p class="kw-paragraph"><span class="kw-lead">Revenue acceleration driven by Services:</span> The Services segment grew 14% YoY to $26.3B, driven by...</p>
```

**Square Bullets (P8):** All bullet lists use `■` via the `.bullet-item` class. Do NOT use `<ul>` — use `<div class="bullet-item">` for each item.

**Parenthetical Negatives (P3):** Negative financial values are displayed as `(1,234.5)` instead of `-1,234.5`. Apply class `.neg-paren` to the `<td>` or `<span>`. Example: `<td class="col-number neg-paren">(2.3%)</td>`

**Exhibit Labels (P4):** Every chart and table has an exhibit label. The number portion uses brand blue; the description is gray italic.

```html
<div class="exhibit-label">
  <span class="exhibit-number">Exhibit 3:</span>
  <span class="exhibit-desc">Revenue Breakdown by Segment (FY2023–FY2026E)</span>
</div>
```

### Section Title HTML

```html
<h2 class="section-heading">Section Title</h2>
```

### Callout Box HTML

```html
<div class="callout">
  <strong>Key Insight:</strong> [Important conclusion or finding]
</div>
```

---

## 4.3 Module Title Mapping

| #   | Module                                | Chinese Title | English Title                            |
| --- | ------------------------------------- | ------------- | ---------------------------------------- |
| 1   | Stock Price & Market Performance      | 股价表现与市场概况     | Stock Price & Market Performance         |
| 2   | Investment Thesis & Key Debates       | 投资逻辑与核心争议     | Investment Thesis & Key Debates          |
| 3   | Investment Thesis Comprehensive Table | 投资论点综合分析      | Investment Thesis Comprehensive Analysis |
| 4   | Company Overview & Business Model     | 公司概览与商业模式     | Company Overview & Business Model        |
| 5   | Business Segment Deep Dives           | 业务板块深度分析      | Business Segment Deep Dives              |
| 6   | Industry & Competitive Landscape      | 行业与竞争格局       | Industry & Competitive Landscape         |
| 7   | TAM / Market Sizing                   | 市场规模分析        | TAM / Market Sizing                      |
| 8   | Supply Chain & Industry Chain         | 产业链分析         | Supply Chain & Industry Chain Analysis   |
| 9   | Upstream/Downstream Analysis          | 上下游分析         | Upstream/Downstream Analysis             |
| 10  | Financial Analysis & Projections      | 财务分析与预测       | Financial Analysis & Projections         |
| 11  | Valuation Analysis                    | 估值分析          | Valuation Analysis                       |
| 12  | Management & Governance               | 管理层与公司治理      | Management & Governance                  |
| 13  | ESG & Sustainability                  | ESG与可持续发展     | ESG & Sustainability                     |
| 14  | Scenario Analysis                     | 情景分析          | Scenario Analysis                        |
| 15  | Risk Assessment                       | 风险评估          | Risk Assessment                          |
| 16  | Shareholder & Capital Structure       | 股东结构与资本结构     | Shareholder & Capital Structure          |
| 17  | References & Data Sources             | 参考文献与数据来源     | References & Data Sources                |
| 18  | Compliance Disclaimer                 | 免责声明          | Disclaimer                               |

Use the language column matching `report_language` set in Phase 0.1.

---

## 4.4 Module Generation Order

### ⚠️ CRITICAL: This is NOT a Tear Sheet

The equity report is a **≥25 page institutional deep-dive**. Every module must be written with depth and substance — **full paragraphs, not bullet summaries**. If a module can be mistaken for a tear-sheet section, it is too thin.

**DO NOT TAKE SHORTCUTS:**
- ✅ Each major module should span **at least 1.5-2 full pages** of content
- ✅ Include data tables, charts, and exhibits generously — aim for **≥15 exhibits total**
- ✅ Write analytical paragraphs (3-5 sentences each) with specific data points, not generic observations
- ✅ **Actively research** during report writing — the Task 1/2 deliverables are a starting framework, not the ceiling
- ✅ Add **company-specific sub-sections** where the business warrants it (e.g., a tech company might need a "Product Roadmap" sub-section; a consumer company might need "Brand Portfolio Analysis")
- ❌ Do NOT copy-paste from Task 1/2 deliverables verbatim — synthesize, expand, and add new research
- ❌ Do NOT produce a report that reads like an expanded tear sheet

### Module Table — All Modules Are MANDATORY

**Module titles follow `report_language`**: Use Chinese titles for `zh` reports, English for `en` reports. Financial metrics within module content (P/E, EV/EBITDA, ROE, etc.) always stay in English.

| # | English Title | Chinese Title (`zh`) | Layout | Min. Words (EN) | Min. Words (中文 ≈EN×1.6) | Key Content |
|---|---------------|----------------------|--------|-----------------|---------------------------|-------------|
| 1 | **Stock Price & Market Performance** | **股价与市场表现** | Full-Width | 800-1,200 | 1,280-1,920 | Custom stock chart (see §4.4.1 below), price performance narrative, key price drivers, relative performance vs. benchmark + sector peers. **NOT the tear sheet chart script.** |
| 2 | **Investment Thesis & Key Debates** | **投资论点与核心争议** | Full-Width | 800-1,200 | 1,280-1,920 | Core thesis (structural advantage, paradigm positioning), 3-5 key catalysts with timeline, key investor debate points framed as questions with the report's answers. Inspired by institutional "addressing key debates" format. |
| 3 | **Investment Thesis Comprehensive Table** | **投资论点综合分析表** | Full-Width | — | — | 4×6 debate table (bull/bear/assumption/inflection/judgment) + commentary |
| 4 | **Company Overview & Business Model** | **公司概览与商业模式** | Full-Width | 1,200-1,600 | 1,920-2,560 | Company history, business model deep dive, revenue model explanation, management team overview, organizational structure. Full paragraphs. |
| 5 | **Business Segment Deep Dives** | **业务分部深度分析** | Full-Width | 800-1,500+ | 1,280-2,400+ | **⚠️ MANDATORY — Agent must create 2-4 sub-sections**, one per major business segment or product line, tailored to the company. Each sub-section: segment overview, competitive dynamics, growth drivers, margin profile, outlook. This module alone should be 3-5 pages. If the company has only 1 segment, go deeper: sub-divide by geography, customer type, or use case. |
| 6 | **Industry & Competitive Landscape** | **行业与竞争格局** | Full-Width | 800-1,200 | 1,280-1,920 | Market landscape map, 5-8 named competitors with comparison table, market share analysis, competitive positioning, pricing power, barriers to entry. Source content from Research Doc §IV (Industry Overview + TAM/SAM/SOM + Competitive Landscape + Entry Barriers). |
| 7 | **TAM / Market Sizing** | **市场规模测算 (TAM/SAM/SOM)** | Full-Width | 1,000-1,600 | 1,600-2,560 | TAM/SAM/SOM framework with specific dollar figures, market growth projections, penetration analysis, addressable market evolution over 3-5 years. At least 1 exhibit (market sizing chart or waterfall). |
| 8 | **Supply Chain & Industry Chain** | **产业链全景** | Full-Width | 800-1,200 | 1,280-1,920 | Pre-rendered SVG supply chain diagram + narrative. See `modules/industry-chain.md` §Rendering Pipeline. |
| 9 | **Upstream/Downstream Analysis** | **上下游分析** | Full-Width | 600-1,000 | 960-1,600 | Supplier concentration, customer concentration, bargaining power, key supply chain risks. |
| 10 | **Financial Analysis & Projections** | **财务分析与预测** | Full-Width | 1,000-1,500 | 1,600-2,400 | **DEEP VERSION**: Revenue decomposition by segment, margin bridge (historical → projected), DuPont decomposition, FCF analysis, earnings quality, balance sheet quality, working capital trends. Multiple tables from Excel model. This module should be 3-4 pages minimum. |
| 11 | **Valuation Analysis** | **估值分析** | Full-Width | 800-1,200 | 1,280-1,920 | Full spec in §4.5: Comps + Historical Band + DCF + Sensitivity + Cross-Method Synthesis |
| 12 | **Management & Governance** | **管理层与公司治理** | Full-Width | 800-1,200 | 1,280-1,920 | CEO/CFO/key exec profiles (250-400 words each), management track record, compensation alignment, insider ownership, board independence, succession considerations. |
| 13 | **ESG & Sustainability** | **ESG与可持续发展** | Full-Width | 600-1,000 | 960-1,600 | Environmental metrics/targets, social (workforce, supply chain), governance quality. Specific KPIs, not just narrative. |
| 14 | **Scenario Analysis** | **情景分析** | Full-Width | 1,200-1,600 | 1,920-2,560 | Quantified Bull/Base/Bear with probability weights, scenario comparison table, probability-weighted target price, key assumptions per scenario. |
| 15 | **Risk Assessment** | **风险评估** | Full-Width | 1,000-1,400 | 1,600-2,240 | 8-12 categorized risks with Probability × Impact scoring, risk mitigation factors, key monitoring signals. Structured risk table + narrative. |
| 16 | **Shareholder & Capital Structure** | **股东与资本结构** | Full-Width | 600-1,000 | 960-1,600 | Top institutional holders, insider activity, buyback programs, float analysis, recent 13F/shareholding changes. |
| 17 | **References & Data Sources** | **参考文献与数据来源** | Full-Width | — | — | See §4.8 below. Every data source cited in the report must be listed here. |
| 18 | **Compliance Disclaimer** | **合规声明与免责声明** | Full-Width | — | — | Market-specific disclaimer (see below). Must include "Kimi Research" as issuing entity. |

### §4.4.1 Stock Price & Market Performance (Custom Chart)

**⚠️ DO NOT use the tear sheet stock chart script (`scripts/stock_chart_generator.py`) for the equity report.** The equity report chart should be larger, more detailed, and custom-built using Python + matplotlib.

**Required Chart Elements**:
- **Full-page width** chart, ~300px height
- Stock price line (primary axis) + trading volume bars (secondary axis)
- **Benchmark index overlay** (恒生指数, 沪深300, S&P 500 — based on market) as a rebased comparison line
- 52-week high/low markers
- Key event annotations (earnings dates, major news) — at least 3 annotations
- Professional styling: clean grid, Kimi Research watermark, date axis, dual y-axes

**Implementation**: Use `matplotlib` or `plotly` to generate a high-resolution SVG or PNG. Build the chart from the stock price CSV data and benchmark CSV data.

```python
# Example structure — agent should adapt based on data available
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# ... load stock_csv, benchmark_csv
# ... rebase both to 100 at start date
# ... plot with dual axes, volume bars, annotations
# ... save as SVG for embedding
```

### §4.4.2 Business Segment Deep Dives — Flexible Structure

This module is where the report differentiates itself from a tear sheet. The agent MUST:

1. **Identify 2-4 major business segments** (or product lines, geographies, customer types) from the research document
2. **Create a sub-section (`<h3>`) for each segment** with its own narrative, data, and exhibits
3. **Tailor the analysis** to what matters most for each segment — don't use a cookie-cutter template
4. **Add company-specific analysis** that wouldn't appear in a generic template (e.g., for a tech company: model benchmark scores, API pricing comparison; for a consumer company: brand value, channel mix)

The agent is **encouraged** to research additional data points during this module — web searches for recent product launches, competitive moves, regulatory changes, etc.

### Module 18: Disclaimer Content (Kimi Research Issued)

**Every equity report cover page AND compliance disclaimer MUST include "Kimi Research" as the issuing entity.**

**Cover page**: Kimi Research logo bar at the top of every cover (see §4.2 Cover Page HTML template).
**Disclaimer**: "Kimi Research" must appear at least once as the report issuer.

Use market-appropriate language:

- **A-shares (zh)**: "本报告由 **Kimi Research** 基于AI辅助分析生成，仅供参考，不构成投资建议。数据来源包括公开财务报告、行业数据及第三方API（iFind、Yahoo Finance等）。投资者应独立判断并自行承担投资风险。"
- **HK stocks (zh)**: "本报告由 **Kimi Research** 基于AI辅助分析生成，仅供参考，不构成投资建议。数据来源包括公开财务报告、行业数据及第三方API。投资者应独立判断并自行承担投资风险。如适用，请遵守香港证监会相关风险披露规定。"
- **US stocks (en)**: "This report was generated by **Kimi Research** using AI-assisted analysis. It is provided for informational purposes only and does not constitute investment advice. Data sources include public financial filings, industry data, and third-party APIs (iFind, Yahoo Finance). Investors should exercise independent judgment and assume their own investment risks."

---

## ⚠️ 4.4.3 Deep Research During Report Generation

> **The Task 1/2 deliverables are a STARTING POINT, not the ceiling.**

When writing each module, the agent MUST actively seek to enrich the content beyond what the research document and Excel model provide:

- ✅ **Web Search**: For each major module, do **at least 1 web search** to find the latest data, news, or competitive intelligence. No cap on total searches — use as many as needed.
- ✅ **Additional Charts**: Beyond the 5 required charts (C1-C5), generate **additional charts** wherever they add value. Aim for **≥15 total exhibits** (charts + tables). Good candidates: revenue waterfall, margin bridge, market share trend, competitive positioning scatter, historical PE band chart, scenario comparison.
- ✅ **Company-Specific Sub-Sections**: If the company has unique characteristics (e.g., a unique business model, regulatory dynamics, technology moat), create custom sub-sections under the relevant module.
- ✅ **Cross-Reference**: When writing about financials, reference the competitive landscape. When writing about competition, reference the financial implications. The report should feel integrated, not siloed.
- ❌ **DO NOT say "as noted in the research document"** or "per the analysis brief" — synthesize the content and add to it.
- ❌ **DO NOT skip modules because the research document section was thin** — this is exactly when you should research more.

**Research Budget**: Unlimited web searches. Up to 10 additional API calls for financial data. The goal is institutional-grade depth — do not optimize for speed at the expense of quality.

---

## 4.5 Valuation Section Specification (L1 vs L2)

The valuation section adapts based on `valuation_depth`:

| Sub-section | L1 (Streamlined) | L2 (Full) |
|-------------|-------------------|-----------|
| 4.5.1 Comparable Company Table | ✅ Table + premium/discount narrative | ✅ Same |
| 4.5.2 Historical Valuation Band | ❌ Skip | ✅ 5Y PE/PB band with percentiles |
| 4.5.3 DCF Model | ❌ Skip | ✅ WACC/FCF/Terminal Value/Equity Bridge |
| 4.5.4 Sensitivity Matrix | ❌ Skip | ✅ WACC × Growth matrix |
| 4.5.5 Cross-Method Synthesis | ✅ Comps + Consensus only | ✅ DCF + Comps + Historical combined |

---

### 4.5.1 Comparable Company Table (L1 + L2)
Comparable company valuation table + premium/discount narrative. Data from iFind/Yahoo Finance (NOT Web Search). See `valuation/comparable.md` §Data Sources.

---

### 4.5.2 Historical Valuation Band (L2 Only)
- 5Y PE/PB band summary table (High / Low / Mean / Median / ±1σ / Current / Percentile)
- Percentile interpretation narrative per `valuation/dcf-and-sensitivity.md` §Part 2 (Historical Valuation Band)
- Note any structural breaks in the analysis period
- **L1**: Replace with a brief paragraph on historical PE range from the research document

---

### 4.5.3 DCF Model (L2 Only)
- Assumption summary table (WACC, growth rates, margins, CapEx intensity)
- 5-year FCF projection table
- Equity bridge table (EV → Equity Value → Per Share)
- Per-share value conclusion with comparison to current price
- **L1**: Skip entirely. Do not include DCF assumptions or FCF projections.

---

### 4.5.4 Sensitivity Matrix (L2 Only)
- WACC × Terminal Growth (mandatory) — use `.sensitivity-matrix` class, `.base-case` for center cell
- Revenue × Margin (optional)
- Interpretation narrative per `valuation/dcf-and-sensitivity.md` §Part 3 (Sensitivity Analysis)
- **L1**: Replace with a simple scenario table (Bull/Base/Bear with assumptions and implied prices, no matrix).

---

### 4.5.5 Cross-Method Synthesis (L1 + L2)

**L2 Version** (3 methods):
```html
<div class="valuation-synthesis">
  <div class="valuation-range">
    <strong>Valuation Range Summary:</strong>
    <ul>
      <li>Comparable Companies: ¥XX – ¥XX per share</li>
      <li>DCF (base case): ¥XX per share</li>
      <li>Historical Band (median): ¥XX implied</li>
    </ul>
    <p>Cross-method convergence analysis: [narrative]</p>
    <p>Final valuation judgment: [narrative]</p>
  </div>
</div>
```

**L1 Version** (comps + consensus only):
```html
<div class="valuation-synthesis">
  <div class="valuation-range">
    <strong>Valuation Summary (Comparable-Company Based):</strong>
    <ul>
      <li>Comparable Companies: ¥XX – ¥XX per share</li>
      <li>Consensus Target Price: ¥XX per share</li>
    </ul>
    <p>Premium/discount drivers: [narrative]</p>
    <p>Final valuation judgment: [narrative]</p>
  </div>
</div>
```

---

## 4.6 Table of Contents + Figure Index

Generate TOC programmatically from the module list. Use dot leaders between title and page number.
Use `class="toc-new-section"` for sections with page breaks.

Include a Figure/Exhibit Index after the TOC listing all exhibits with page references.

---

## 4.7 Page Break Control

### Equity Report Pagination Rule

**Page 1 (Cover) and Page 2 (Data Summary) have fixed layouts.**
**ALL other modules — including Table of Contents — start on a NEW page.**

This is enforced by CSS:
- `.module-row` has `page-break-before: always`
- `.toc` and `.figure-index` have `page-break-before: always`
- `.cover-split`, `.exec-summary`, and `.data-summary-page` are NOT `.module-row`, so they are NOT affected

**Result**: The report always follows this page structure:
```
P1: Cover (cover-split + exec-summary)     ← fixed, NO page break before
P2: Data Summary (data-summary-page)       ← fixed, NO page break before
P3: Table of Contents                      ← .toc, forced new page
P4: Figure Index                           ← .figure-index, forced new page
P5: Module 1 (Stock Price & Performance)   ← .module-row, forced new page
P6: Module 2 (Investment Thesis)           ← .module-row, forced new page
P7: Module 3 (Thesis Table)                ← .module-row, forced new page
... every subsequent module: new page
Last: Module 18 (Compliance Disclaimer)    ← .module-row, forced new page
```

**You do NOT need to add `module-newpage` to each module.** The CSS handles it automatically. Just use `<div class="module-row">` for every content module.

**Exception**: If two modules are very short (<200 words combined) and belong to the same analytical theme, you may place them inside a single `.module-row` to avoid excessive blank space. This is rare — default to one module per page.

**Core Rules**:
- Section titles prohibit being orphaned at page bottom
- Tables and charts prohibit spanning pages (`page-break-inside: avoid`)
- Every module (including TOC) starts on a new page — NO exceptions except P1 and P2

---

## 4.8 References & Data Sources Section

Include a full-width section listing ALL data sources with URLs. Track sources during writing
in a Python set/list, then output as a numbered list.

**Minimum**: 10 sources. **Format**: Numbered list with source name + URL + access date.

```html
<div class="module-row module-newpage">
  <h2>References & Data Sources</h2>
  <ol class="ref-list">
    <li>[Source name] — [URL] — Accessed [date]</li>
  </ol>
</div>
```

---

## 4.9 Generate PDF

Call PDF generation skill with:
- `page.emulate_media(media='print')`
- Inject `.report-container { padding: 0 !important; }`
- Page margin: `@page { margin: 18mm 20mm; }`
- After generation: check page count matches Phase 0.3 target (≥25 pages)

**Supply Chain Diagram (CRITICAL)**:
- Supply chain diagram must be **pre-rendered to SVG** before embedding in HTML.
- See `modules/industry-chain.md` §Rendering Pipeline for the Playwright scheme (Playwright → HTML/CSS flex fallback).
- Do NOT include `<script src="mermaid.min.js">` — PDF renderers do not execute JavaScript.
- Do NOT embed raw `<pre class="mermaid">` code — it will appear as plain text in the PDF.
- Embed the pre-rendered SVG inline (`<svg>...</svg>`) or as `<img src="chain.svg">`.

---

## 4.9 Chart Embedding (Quick Reference)

Charts are pre-rendered SVGs embedded as base64 `<img>` tags. Full specs → `modules/equity-report-charts.md`.

```html
<div class="exhibit-label">
  <span class="exhibit-number">Exhibit N:</span>
  <span class="exhibit-desc">[Description]</span>
</div>
<div class="chart-container">
  <img src="data:image/svg+xml;base64,BASE64STRING" style="max-width:100%;height:auto;" />
</div>
<p class="chart-source">Source: [Source] | Chart: Model Calculation</p>
```

**Rules**: Each chart AFTER its data table. One chart per module max. Number sequentially with tables.
