# Equity Report — Phase 5: Quality Assurance

> Read by the agent during Phase 5 when `output_type = EQUITY_REPORT`.

---

## 5.1 Pre-Check

Run `scripts/report_validator.py --html [report.html] --json`. Fix validator-reported problems first.

---

## 5.2 Layout Self-Check

Run in this order. Fix any failure before proceeding.

| #   | Priority | Check                                                             | Fix                                                                                              |
| --- | -------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 0   | Highest  | Cover page blank (>20% white area)                                | Verify `@page:first{margin:0}`, `.report-container{padding:0}`, brand-bar outside `.cover-split` |
| 0b  | Highest  | Cover visual defect (bar cropped, text squeezed, grid misaligned) | Check CSS: `.cover-split{display:table}`, `.cover-main/.cover-sidebar{display:table-cell}`       |
| 1   | Highest  | Supply chain diagram blank or raw Mermaid text visible            | Pre-render to SVG before embedding; never include `<script src="mermaid">`                       |
| 2   | Highest  | Section title orphaned at page bottom                             | Add `page-break-after: avoid` to title; or `page-break-before: always` to section                |
| 3   | High     | Chart/diagram cut off at page edge                                | Shrink chart width to 100%; add `page-break-inside: avoid`                                       |
| 4   | High     | Table spans page break                                            | Add `page-break-inside: avoid` to table; split wide tables                                       |
| 5   | High     | Font overflow or CJK rendering issue                              | Check `report_language` class applied; verify font-family in CSS                                 |
| 6   | Medium   | Chart/table too small to read                                     | Increase font ≥8pt; enlarge container; reduce data density                                       |
| 7   | Medium   | Over-pagination (large white space)                               | Remove unnecessary `page-break-before`; merge short sections                                     |
| 8   | Medium   | Last page <30% content                                            | Condense preceding section; or add content                                                       |

**Visual Inspection (mandatory)**: After PDF generation, open HTML in browser (`file://` URL), capture full-page screenshot, verify cover layout and scroll through all pages. No delivery without visual check.

---

## 5.3 Quality Gate Loop

```
LOOP START (max 3 iterations):
|
|- Step 1: STRUCTURAL INTEGRITY
|   Count </body> and </html> — if >1 of either: HTML duplicated → regenerate
|
|- Step 2: GENERATE PDF via Playwright native page.pdf()
|   See report-layout.md §4.9 for code
|
|- Step 3: PAGE COUNT
|   Must be ≥25 pages. If <25: expand sections. If >40: check duplication.
|
|- Step 4: A-TIER CHECKS → any fail = prohibit delivery
|   Run cover checks (A0a, A0b) FIRST. If fail: fix → return to LOOP START.
|   Then remaining A-tier. If fail: repair section → return to LOOP START.
|
|- Step 5: B-TIER CHECKS → >3 fails = prohibit delivery
|
|- Step 6: C-TIER CHECKS → record only
|
|- Step 7: ALL PASS → deliver
LOOP END
```

**Rule**: After ANY modification — no matter how small — re-run the full loop. No exceptions.

---

## A-Tier Checks (Any Failure = Prohibit Delivery)

| No. | Item                       | Standard                                                                                                                                       | Method                                      |
| --- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| A0a | Cover blank check          | Page 1 content coverage ≥80%. Brand bar + cover split + exec summary all render fully.                                                         | Visual inspection                           |
| A0b | Cover visual integrity     | Brand bar full-width; company name ≥18pt; key data grid aligned; price target bar shows Current/Target/Upside with correct badge color         | Visual inspection per report-layout.md §4.2 |
| A1  | Page layout                | No large white space; last page content ≥30%                                                                                                   | Visual inspection                           |
| A1b | Executive summary          | Present on page 1 with all 4 items (Thesis, Financials, Valuation, Risks), each 1-2 sentences with numbers. Cover does not overflow to page 2. | Visual + content check                      |
| A2  | Section sequence           | Matches report-layout.md §4.4 order                                                                                                            | Compare module list                         |
| A3  | Section completeness       | All 21 modules present (Cover through Disclaimer, including Data Summary and Glossary). Business segments ≥2 sub-sections.                     | Count modules                               |
| A3b | References                 | ≥10 cited sources with URLs where applicable. No orphan citations.                                                                             | Count + verify URLs                         |
| A3c | Business segment depth     | ≥2 sub-sections, each ≥200 words + ≥1 exhibit                                                                                                  | Content check                               |
| A3d | Exhibit count              | ≥15 total (charts + tables)                                                                                                                    | Count exhibit labels                        |
| A4  | Chart alignment            | Charts fit page width, no overflow                                                                                                             | Visual inspection                           |
| A5  | Page margins               | 18mm top/bottom, 20mm left/right, consistent                                                                                                   | Measure PDF                                 |
| A6  | No fabricated data         | All data from real sources                                                                                                                     | Spot-check vs. iFind/Yahoo Finance          |
| A7  | Data cross-validation      | Key numbers verified from dual sources                                                                                                         | Check variance <5%                          |
| A8  | Model data tags            | Calculated data labeled (especially DCF)                                                                                                       | Check labels                                |
| A9  | Narrative consistency      | All sections align with Phase 3 core narrative                                                                                                 | Read-through                                |
| A10 | Investment thesis table    | 4 rows with bull/bear arguments + key assumptions + pivot signals                                                                              | Check table                                 |
| A11 | Short-term fund flow       | Includes fund flow / market structure analysis                                                                                                 | Check text                                  |
| A12 | Page balance               | No orphaned titles; no charts/tables spanning pages                                                                                            | Validator + visual                          |
| A13 | Analysis brief             | File exists per references/output-schema.md                                                                                                    | Check file                                  |
| A14 | DCF assumptions documented | Every projection has assumption + basis + risk                                                                                                 | Check assumption table                      |
| A15 | Sensitivity base case      | Base case cell highlighted in every matrix                                                                                                     | Check formatting                            |
| A16 | Cross-method synthesis     | Valuation compares all methods, notes convergence/divergence                                                                                   | Check synthesis section                     |
| A17 | Phase 2.7 completion       | All 6 deep research modules executed before Phase 4                                                                                            | Verify analysis brief content               |
| A18 | Scenario probabilities     | Bull + Base + Bear sum to 100%; Base 45-60%                                                                                                    | Check scenario section                      |
| A19 | HTML integrity             | Exactly 1 `</body>` and 1 `</html>`. No duplicated content.                                                                                    | `grep -c '</body>' file.html` must return 1 |
| A20 | Page count range           | ≥25 and ≤40 pages                                                                                                                              | Check immediately after PDF generation      |
| A21 | Page 2 data summary        | Data Summary page present with 2-column layout, all tables populated from Task 2 Excel, no placeholders                                        | Inspect page 2                              |
| A22 | Charts embedded | ≥3 base64 SVG images | embed_charts.py count |
| A23 | Language consistency | HTML `lang` matches `report_language` | Check HTML lang attr            | ≥3 occurrences of `data:image/svg+xml;base64,` in HTML                                                                                         | Run embed_charts.py count                   |

---

## B-Tier Checks (>3 Failures = Prohibit Delivery)

| No. | Item | Standard |
|-----|------|----------|
| B2 | Data source tags | All data tagged with source |
| B3 | Catalyst calendar | ≥4 events, includes next earnings, ≥2 high-importance |
| B4 | Comparable companies | 3-5 competitors with real data |
| B5 | 52-week stock chart | Renders correctly, benchmark overlay, labels complete |
| B6 | Company overview | Full paragraphs (not bullet-only), management details |
| B7 | Supply chain map | Embedded SVG or HTML/CSS table. No raw Mermaid text or `<script src="mermaid">` |
| B8 | Earnings quality | Includes OCF/NI, DuPont, FCF analysis |
| B9 | Consensus expectation | Includes sell-side expectations |
| B10 | Competitive landscape | CR concentration, pricing power |
| B11 | Historical band | 5Y PE/PB band summary table with percentile |
| B12 | DCF projection table | 5-year FCF projection + equity bridge |
| B13 | Sensitivity matrix | At least WACC × Terminal Growth |
| B14 | Module depth | Each of 21 modules ≥2 paragraphs + ≥1 table/exhibit |
| B15 | Revenue decomposition | Segment-level revenue table with volume × price |
| B16 | Competitive depth | ≥5 named competitors with profile table + market share |
| B17 | TAM/SAM/SOM | Quantified market sizing with sources |
| B18 | Projection assumptions | Margin bridge table + CapEx/WC assumptions |
| B19 | Risk count | ≥8 distinct risks across ≥3 categories |
| B20 | Scenario quantification | Each scenario has specific metrics (revenue, margin, EPS, target price) |
| B21-B27 | Chart checks | Revenue segment, margin trends, market share, PE band, scenario, price performance, glossary — see Chart Checks section below |

---

## C-Tier Checks (Record Only)

| No. | Item | Standard |
|-----|------|----------|
| C1 | Table count | 12-18 |
| C2 | Paragraph quality | 3-5 sentences per analysis paragraph |
| C3 | Data timeliness | Latest financials and market data |
| C4 | Compliance statement | Present |
| C5 | Exhibit numbering | Sequential, no repeats/gaps |
| C6 | Change highlighting | YoY/QoQ use .change-positive / .change-negative |
| C7 | English font | US reports use .report-container-en |
| C8 | Table of contents | Present for reports ≥10 pages |
| C9 | WACC reasonability | Within typical range per valuation/dcf-and-sensitivity.md |
| C10 | Terminal value ratio | 50-70% of EV (flag if >80%) |
| C11-C13 | Chart-table consistency, exhibit labels, page placement | See Chart Checks |

---

## Chart Quality Checks (Equity Report Only)

### B-Tier Chart Checks

| No. | Item | Standard |
|-----|------|----------|
| B21 | Revenue segment chart | Present; segments match revenue table; forecast bars hatched |
| B22 | Margin trends chart | 3 lines (gross/operating/net); forecast dashed |
| B23 | Market share chart | Target company highlighted; shares sum ~100% |
| B24 | PE band chart | Current value marked; mean/SD bands visible |
| B25 | Scenario chart | 3 scenarios with correct colors (green/blue/red) |
| B26 | Price performance + table | C6 rebased line on page 2 left; perf-table 6 rows (1M/3M/6M/YTD/1Y/3Y); real API data only |
| B27 | Glossary section | 6-12 sector-relevant terms in 2-column grid; no placeholders |

### C-Tier Chart Checks

| No. | Item | Standard |
|-----|------|----------|
| C11 | Chart-table consistency | Chart data matches adjacent table |
| C12 | Exhibit labels | All charts have sequential labels and source lines |
| C13 | Chart page placement | No chart split across pages; label not orphaned |
| C14 | Language enforcement | `report_language` set deterministically per SKILL.md algorithm; no mid-report language switches |

---

## Structure Inspection

### Required Sections (in order)

```
Header: Company name + ticker + key data
Title + subtitle + core viewpoint (4-6 sentences)
[Table of Contents if ≥10 pages]
Stock Price + Trading Data: chart + narrative
Investment Logic: full paragraphs
Investment Thesis Table: 4×6
Company Overview: full paragraphs, management, business model
Valuation Analysis:
  Comparable company table + premium/discount narrative
  Historical valuation band table + percentile narrative
  DCF: assumptions + projection + equity bridge
  Sensitivity: WACC × Growth matrix (mandatory)
  Cross-method synthesis narrative
Catalyst Calendar: ≥4 events, impact analysis
Industry & Competitive Landscape:
  TAM/SAM/SOM sizing table with sources
  5-8 competitor profile table
  Market share table (3-year trend)
  Competitive positioning narrative (pricing power, moat)
Supply Chain: Pre-rendered SVG diagram (no raw Mermaid, no mermaid.min.js)
Upstream/Downstream: Paired analysis
Financial Analysis + Projections:
  Segment revenue decomposition (volume × price)
  Margin bridge (gross + operating)
  CapEx/WC assumptions
  DuPont decomposition
  FCF analysis + earnings quality
[Expansion Modules if selected — each ≥2 paragraphs + ≥1 exhibit]
Scenario Analysis + Risk:
  Bull/Base/Bear with specific metrics + probability weights
  Probability-weighted target calculation
  Scenario comparison table
  8-12 risks across 4 categories with P×I scoring
  Risk-reward synthesis
Compliance Disclaimer
```

---

## Data Cross-Validation

| Data Type | Primary Source | Verify With | Acceptable Variance |
|-----------|---------------|-------------|-------------------|
| Revenue / Net Income | iFind | Yahoo Finance | <5% |
| PE / PB | iFind | Yahoo Finance | <10% |
| Business Breakdown | iFind | Web Search | <10% |
| Industry Data | Web Search | Web Search | <15% |
| Next Earnings Date | Web Search | Exchange Calendar | No variance |
| Beta | iFind | Yahoo Finance | <20% |
| Risk-Free Rate | Web Search | Central bank data | No variance |

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Page 1 mostly blank | Brand-bar inside `.cover-split`; or `.report-container` padding non-zero; or `@page:first{margin:0}` missing | Move brand-bar outside `.cover-split`; set `.report-container{padding:0}`; add `@page:first{margin:0}` |
| Brand bar squeezed | `.cover-split` still `display:flex` | Change to `display:table`; children to `display:table-cell` |
| Supply chain blank | Raw Mermaid not pre-rendered | Pre-render to SVG via Playwright; see modules/industry-chain.md |
| Raw `<pre class="mermaid">` in HTML | Mermaid code not pre-rendered | Must pre-render to SVG before embedding |
| Chart not rendering | base64 SVG not embedded correctly | Verify `<img src="data:image/svg+xml;base64,...">` is complete |
| Section titles orphaned | Large section at page bottom | Add `page-break-before: always` |
| Report too short (<25 pages) | Phase 2.7 not fully executed | Return to Phase 2.7, complete all 6 sub-steps |
| Report too long (>40 pages) | Over-expanded or duplicated | Tighten prose; check for duplicated content |
| Sensitivity matrix all same color | Too-narrow variable ranges | Widen ranges per valuation/dcf-and-sensitivity.md |
| DCF value far from market | Unreasonable assumptions | Check WACC range, terminal growth, margin projection |
