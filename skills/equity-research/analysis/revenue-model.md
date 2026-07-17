# Revenue Model Deep Dive — Equity Report Only

> **Scope**: This file is read ONLY when `output_type = EQUITY_REPORT`.
> It forces a structured, bottom-up revenue decomposition that goes far beyond
> the top-line growth rates used in the tear sheet.

---

## Purpose

The tear sheet uses top-line revenue with simple YoY growth estimates.
The equity report must build revenue from the ground up — segment by segment,
product by product — so every growth assumption is transparent and testable.
This file produces the raw data that feeds into:
- The Financial Analysis module (Section 9)
- The Projection Assumptions section
- The DCF model inputs
- The Scenario Analysis variants

---

## 1. Revenue Architecture

### Step 1: Identify Revenue Segments

Map the company's revenue into 3-6 major segments using the most recent annual filing.
For each segment, identify the **revenue driver formula**:

| Segment Type | Driver Formula | Example |
|-------------|---------------|---------|
| Product (units) | Units Sold × Average Selling Price (ASP) | iPhone: 230M units × $930 ASP |
| Subscription | Subscribers × ARPU × 12 months | Services: 1.1B subs × $8.50/mo |
| Transaction-based | GMV × Take Rate | App Store: $95B GMV × 30% take |
| Licensing/royalty | Licensed base × Royalty per unit | Patent licensing: 500M devices × $2/device |
| Project/contract | # Projects × Avg Contract Value | Enterprise deals: 50 contracts × $2M avg |
| Advertising | Impressions × CPM (or DAU × Ad load × CPM) | Search ads: XB impressions × $YY CPM |

### Step 2: Historical Decomposition Table

```
Exhibit X: Revenue Decomposition by Segment

                          FY22A    FY23A    FY24A    FY25A    CAGR
──────────────────────────────────────────────────────────────────
[Segment 1]
  Revenue ($B)            xxx      xxx      xxx      xxx      x.x%
  Volume (units/subs)     xxx      xxx      xxx      xxx      x.x%
  Price (ASP/ARPU)        $xxx     $xxx     $xxx     $xxx     x.x%
  % of Total              xx.x%    xx.x%    xx.x%    xx.x%

[Segment 2]
  Revenue ($B)            xxx      xxx      xxx      xxx      x.x%
  Volume                  xxx      xxx      xxx      xxx      x.x%
  Price                   $xxx     $xxx     $xxx     $xxx     x.x%
  % of Total              xx.x%    xx.x%    xx.x%    xx.x%

[Segment 3-6...]

──────────────────────────────────────────────────────────────────
Total Revenue ($B)        xxx      xxx      xxx      xxx      x.x%
```

---

## 2. Growth Driver Analysis

For EACH major segment (≥10% of revenue), analyze:

### Volume Drivers
- **Market growth**: What is the industry growth rate? (TAM/SAM per research-document-template.md §IV)
- **Market share trajectory**: Gaining, stable, or losing? (per research-document-template.md §IV Competitive Landscape)
- **Product cycle**: New product launches, replacement cycles, cannibalization
- **Geographic expansion**: New market entry, penetration increase
- **Channel expansion**: New distribution partners, DTC growth

### Price Drivers
- **ASP / ARPU trends**: Historical direction and sustainability
- **Mix shift**: Higher-end products growing faster (positive mix) or commoditization (negative mix)
- **Pricing power**: Ability to raise prices (per research-document-template.md §IV pricing power / Five Forces)
- **Currency impact**: FX translation effects on reported ASP
- **Promotional intensity**: Discounting trends, promotional calendar

### Writing Requirement

For EACH major segment, produce a **bold-keyword paragraph** documenting:
1. The primary growth driver (volume or price) with supporting data
2. The sustainability of the current growth trajectory
3. Risks specific to this segment
4. Our base case assumption vs. consensus

**Minimum**: 150-200 words per segment. 3-6 segments = 450-1,200 words total.

---

## 3. Revenue Projection Build

### Forward Estimates Table

```
Exhibit X: Revenue Projection Build ($B)

                     FY25A   FY26E   FY27E   FY28E   Notes
────────────────────────────────────────────────────────────
[Segment 1]          xxx     xxx     xxx     xxx     [key assumption]
  Volume growth      +x.x%   +x.x%  +x.x%  +x.x%
  ASP/ARPU change    +x.x%   +x.x%  +x.x%  +x.x%
  Revenue growth     +x.x%   +x.x%  +x.x%  +x.x%

[Segment 2]          xxx     xxx     xxx     xxx     [key assumption]
  Volume growth      +x.x%   +x.x%  +x.x%  +x.x%
  ASP/ARPU change    +x.x%   +x.x%  +x.x%  +x.x%
  Revenue growth     +x.x%   +x.x%  +x.x%  +x.x%

[Segment 3-6...]

────────────────────────────────────────────────────────────
Total Revenue        xxx     xxx     xxx     xxx
Total Revenue Gr.    +x.x%   +x.x%  +x.x%  +x.x%
Consensus            —       xxx     xxx     xxx
Our vs Consensus     —       +/-x%  +/-x%   +/-x%
```

### Consensus Comparison

- Document the consensus revenue estimate for FY+1 and FY+2
- State our estimate vs. consensus: above, in-line, or below
- Explain the key drivers of any divergence (which segments differ and why)
- This informs the H2 dimension (market pricing) and H3 (market error) from six-dimension analysis

---

## 4. Revenue Quality Assessment

| Metric | Current | Trend | Benchmark | Assessment |
|--------|---------|-------|-----------|------------|
| Recurring vs. one-time % | xx% recurring | Improving / Stable / Declining | Industry: xx% | Good / Fair / Poor |
| Customer concentration (top 10) | xx% of revenue | — | — | Risk level |
| Contract duration (avg) | X years | — | — | Visibility |
| Backlog / Pipeline | $XXB | +xx% YoY | — | Growth support |
| Revenue recognition timing | At delivery / Over time / Upfront | — | — | Conservatism |

**Writing requirement**: 100-150 words summarizing revenue quality — is the revenue base durable, growing from high-quality sources, or vulnerable?

---

## 5. Mix Shift Impact Analysis

Analyze how the revenue mix is changing and what it means for overall margins:

| Segment | FY-2 Share | Current Share | FY+2E Share | Segment GM | Impact on Blended GM |
|---------|-----------|---------------|-------------|-----------|---------------------|
| [Seg 1] | xx% | xx% | xx% | xx% | Positive / Negative / Neutral |
| [Seg 2] | xx% | xx% | xx% | xx% | Positive / Negative / Neutral |
| [Seg 3] | xx% | xx% | xx% | xx% | Positive / Negative / Neutral |

**Writing requirement**: 100-150 words on mix shift implications. This feeds directly into the margin bridge in projection-assumptions.md.

---

## Integration with Other Analysis Files

- **TAM / Market opportunity** (`research-document-template.md §IV` — TAM/SAM/SOM + Market Opportunity Narrative): Market size provides the ceiling for segment revenue projections
- **Competitive landscape** (`research-document-template.md §IV` — Competitive Landscape + Entry Barriers): Market share trajectory informs volume assumptions
- **Projection assumptions** (`projection-assumptions.md`): Revenue buildup feeds directly into projection documentation
- **Scenario deep dive** (`scenario-deep-dive.md`): Bull/Base/Bear revenue numbers must come from this decomposition

---

## Output Quality Gate

- [ ] ≥3 segments with volume × price decomposition
- [ ] Historical decomposition table (3-5 years)
- [ ] Forward projection table (3 years)
- [ ] Consensus comparison with divergence explanation
- [ ] Revenue quality assessment table
- [ ] Mix shift impact analysis
- [ ] Per-segment narrative (≥150 words each)
- [ ] Total section word count ≥800 words (target 1,000-1,500)

---

> **The following sections are merged from projection-assumptions.md.**

## 2. Revenue Buildup — Geographic Level

For companies with meaningful geographic diversification (>15% from any single non-home region):

### Required Per Geography

| Element | Requirement |
|---------|-------------|
| Historical revenue or % share | 3 years minimum |
| Growth driver for that region | Market expansion, penetration, pricing, regulation |
| Currency exposure | Functional currency, hedging, translation impact |
| Competitive dynamics | Different competitors by region |
| FY+1 through FY+3 estimate | With basis |

### Geographic Mix Table Template

```
Exhibit X: Revenue by Geography

Region          | FY24A  | %   | FY25A  | %   | FY26E  | %   | Driver
──────────────────────────────────────────────────────────────────────
[Home market]   | xxx    | xx% | xxx    | xx% | xxx    | xx% | [driver]
[Region 2]      | xxx    | xx% | xxx    | xx% | xxx    | xx% | [driver]
[Region 3]      | xxx    | xx% | xxx    | xx% | xxx    | xx% | [driver]
Other           | xxx    | xx% | xxx    | xx% | xxx    | xx% |
──────────────────────────────────────────────────────────────────────
Total           | xxx    | 100%| xxx    | 100%| xxx    | 100%|
```

**Minimum**: 100-150 words per material region. Total geographic section: 300-600 words.

---

## 3. Margin Bridge

Document how margins evolve from current to projected:

### Gross Margin Bridge

| Driver | Impact (bps) | Basis |
|--------|-------------|-------|
| Revenue mix shift (e.g., Services growing faster) | +XX bps | Services at 70% GM vs. Hardware at 35% |
| Input cost changes (COGS, raw materials, memory) | ±XX bps | Memory pricing cycle, commodity outlook |
| Pricing power / ASP trends | ±XX bps | Premium positioning, competition |
| FX impact | ±XX bps | Currency exposure, hedging |
| **Net GM change** | **+XX bps** | FY25 → FY26E: XX.X% → XX.X% |

### Operating Margin Bridge

| Driver | Impact (bps) | Basis |
|--------|-------------|-------|
| Operating leverage (revenue growth > OpEx growth) | +XX bps | Fixed cost base on SG&A |
| R&D investment trajectory | ±XX bps | % of revenue trend, capitalization |
| SG&A efficiency | ±XX bps | Channel optimization, marketing ROI |
| One-time items | ±XX bps | Restructuring, litigation, impairment |
| **Net EBIT margin change** | **+XX bps** | FY25 → FY26E: XX.X% → XX.X% |

**Writing requirement**: 200-300 words narrating the margin bridge, explaining which driver matters most and why.

---

## 4. Capital Expenditure & Working Capital

### CapEx Assumptions

| Element | Requirement |
|---------|-------------|
| Historical CapEx / Revenue % | 3-5 years |
| Management guidance (if any) | Quote or paraphrase |
| CapEx type split | Maintenance vs. Growth (if estimable) |
| FY+1 through FY+3 CapEx estimate | $ amount and % of revenue |
| Key driver | Capacity expansion, technology upgrade, regulatory |

### Working Capital Assumptions

| Element | Requirement |
|---------|-------------|
| Days Sales Outstanding (DSO) trend | 3 years + projection |
| Days Inventory Outstanding (DIO) trend | 3 years + projection |
| Days Payable Outstanding (DPO) trend | 3 years + projection |
| Cash Conversion Cycle trend | Improving/stable/deteriorating |
| Working capital as % of revenue | Historical + projected |

**Writing requirement**: 150-200 words. Highlight any structural changes (e.g., shift to subscription model improving working capital).

---

## 5. Tax Rate & Other Assumptions

| Element | Assumption | Basis |
|---------|-----------|-------|
| Effective tax rate | XX% | Statutory rate ± permanent differences |
| Share count | XX.XB (diluted) | Buyback trajectory, option dilution |
| D&A as % of revenue | X.X% | Asset base, useful life policies |
| Interest expense | $XXM | Debt outstanding, avg coupon |
| Minority interest / JVs | $XXM | Consolidated vs. equity method |

---

## 6. Assumption Sensitivity Tags

For each major assumption, tag its sensitivity impact on the final valuation:

| Assumption | Base Case | Bull Variant | Bear Variant | Valuation Swing |
|-----------|-----------|-------------|-------------|----------------|
| iPhone revenue growth | +5% | +10% | 0% | ±$25/share |
| Services margin | 72% | 75% | 68% | ±$15/share |
| Terminal growth rate | 3.0% | 3.5% | 2.0% | ±$40/share |
| WACC | 7.4% | 6.9% | 8.4% | ±$30/share |

This table directly links to the scenario-deep-dive.md and sensitivity analysis.

---

## Output Quality Gate

- [ ] ≥3 segments with volume/price decomposition
- [ ] Geographic breakdown if company has >15% non-home revenue
- [ ] Gross margin bridge with ≥3 drivers quantified in bps
- [ ] Operating margin bridge with ≥3 drivers quantified in bps
- [ ] CapEx and working capital assumptions documented
- [ ] Total section word count ≥1,500 words (target 2,000-2,500)
- [ ] Every forward number traces to a documented assumption
- [ ] Assumption sensitivity tags connect to scenario analysis
