---
- name: deep-research
  description: >
    Multi-agent deep research orchestration with adaptive routing. Use this skill
    whenever comprehensive, multi-dimensional, evidence-backed investigation is
    required — competitive intelligence, market analysis, controversy investigation,
    policy evaluation, academic landscape review, risk assessment, file-based
    analysis, or any task demanding cross-verified, multi-source findings.

    **Route Classification** (Phase 0 auto-determines):

    - **Route A — Wide Search**: Broad/exploratory topics where search breadth is
      critical (e.g., industry landscape, trend survey, competitive mapping, "help me
      research industry XX"). First deploy multi-agent wide exploration to maximize
      coverage, then multi-agent deep dive per dimension. Two-stage parallel swarm.

    - **Route B — Focused Search**: Specific questions with clear dimensions or a
      narrow topic. Standard pipeline: landscape scan → decompose → parallel deep dive.

    - **Route C — File-Only Research**: User uploads files and explicitly requests
      analysis based solely on file content (signals: "based on these files only",
      "analyze only the uploaded documents", "no external search", "just based on
      these files"). NO external search — multi-file deep analysis, cross-file
      insight extraction, then handoff to writing skill.

    - **Route D — File-Augmented Research**: User uploads files as reference or
      starting point, but does not restrict to file content only (signals: "refer to
      these files", "combine with files", "help me complete this", "based on this,
      write...", or simply no explicit restriction). Primarily analyze files,
      supplement with professional external sources for additional context and
      verification, then synthesize and write.

    Trigger Rule: When the user uses terms such as:
      - research, investigation, in-depth analysis, comprehensive analysis
      - trend analysis, comparative analysis, comparison, evaluation, assessment
      - future prediction, forecasting, industry outlook, market outlook
    Or when the user uploads files requesting research/analysis/report generation.
    You MUST load the `deep-research` capability skill before proceeding.
    Do NOT use for: simple factual lookup, single-source Q&A.
---

# Deep Research

Orchestrate multi-agent epistemic triangulation: diverge across research dimensions, detect overlaps and contradictions, verify deeply, then converge into a validated synthesis. Swarm parallelism serves epistemic robustness — not merely speed.

**Adaptive routing** ensures the pipeline fits the task: wide-search topics get a two-stage parallel swarm (breadth then depth); file-based tasks skip or augment external search; focused queries go straight to dimension decomposition.

## Output Directory — MANDATORY

**All deep research output files MUST be saved under:**

```
/mnt/agents/output/research/
```

This is non-negotiable. Every file produced in any phase MUST use this directory as the base path. Do NOT save any research artifact to `/mnt/agents/output/` directly — always use the `/mnt/agents/output/research/` subdirectory.

Before writing any file, ensure the directory exists (create it if not).

## Workflow Overview

```
User Query
  │
  ▼
Phase 0: Intent & Input Router
  │
  ├─ Route A: Wide Search (broad/exploratory, no clear dimensions)
  │   → Phase 1 (Quick Landscape)
  │     → Phase 1W (Multi-Agent Wide Exploration) ★ NEW
  │       → Phase 2 (Decompose, informed by rich landscape)
  │         → Phase 3 (Parallel Deep Dive)
  │           → Phase 4 (Cross-Verify) → Phase 5 (if conflicts)
  │             → Phase 6 (Insight Extraction) → Phase 7 (Report via writing skill)
  │
  ├─ Route B: Focused Search (specific question, clear dimensions)
  │   → Phase 1 (Landscape) → Phase 2 (Decompose)
  │     → Phase 3 (Parallel Deep Dive) → Phase 4 (Cross-Verify)
  │       → Phase 5 (if conflicts) → Phase 6 (Insight Extraction) → Phase 7 (Report)
  │
  ├─ Route C: File-Only Research (user explicitly restricts to file content)
  │   → Phase F (File Intake & Deep Analysis) ★ NEW
  │     → Phase 2 (Decompose from file themes)
  │       → Phase 3-F (Multi-Agent File Deep Dive, NO external search)
  │         → Phase 4 (Cross-Verify across file analyses)
  │           → Phase 6 (Insight Extraction) → Phase 7 (Report via writing skill)
  │
  └─ Route D: File-Augmented Research (files as primary reference + external supplement)
      → Phase F (File Intake & Deep Analysis) ★ NEW
        → Phase 1 (Targeted Landscape, informed by file gaps)
          → Phase 2 (Decompose, merging file themes + external landscape)
            → Phase 3 (Parallel Deep Dive, each agent has file context + search)
              → Phase 4 (Cross-Verify) → Phase 5 (if conflicts)
                → Phase 6 (Insight Extraction) → Phase 7 (Report via writing skill)
```

## Phase 0: Intent & Input Router

**Goal**: Classify the user's request into the correct route before any research begins.

**Process**:

1. Check for uploaded files:
   - Files present + explicit "only based on files" language → **Route C**
   - Files present + no restriction / "refer to" / "combine with" / "help me complete" → **Route D**
   - No files → continue to step 2

2. Assess topic breadth:
   - Broad, open-ended, landscape-level query (e.g., "current state of XX industry", "research XX field for me", "XX vs YY vs ZZ comprehensive comparison") → **Route A**
   - Specific, bounded question with identifiable dimensions → **Route B**

3. When ambiguous, default to:
   - **Route A** if the topic is clearly multi-faceted and no clear angle is given
   - **Route D** over Route C if file intent is unclear (prefer richer output)

**Output**: State the selected route and rationale in one sentence, then proceed to the first phase of that route.

**Classification signals summary**:

| Signal | Route |
|--------|-------|
| Files + "based on files only" / "only from uploaded" / "no search" | C |
| Files + "refer to" / "combine with" / "help me complete" / no restriction | D |
| No files + broad/exploratory topic | A |
| No files + specific/bounded question | B |

## Epistemic Reset Rule

Before any analysis or narrative generation, the system MUST:
- Assume internal knowledge may be outdated or incomplete. Always retrieve the current date and time using bash tool before any analysis or external search.
- Using bash to check the time now.
- **Time-awareness**: When the user's query has time-sensitivity requirements (e.g., "2026 Q1", "recent 6 months", "latest", "current"), treat the specified or implied time range as a hard constraint — search queries must target that window, and findings outside it should be flagged.
- Perform external wide search to establish the evidence landscape (except Route C)
- Avoid generating any factual claims before search/file-analysis outputs
- **Search language rule**: All search queries MUST be in the same language as the user's message. If the user writes in Chinese, search in Chinese; if in English, search in English. This ensures results are relevant to the user's locale and context.
- All outputs MUST use inline citations `[^number^]` referencing original sources.

---

## Phase F: File Intake & Deep Analysis (Route C & D Only)

**Goal**: Extract structured knowledge from all uploaded files, build an evidence map, and identify themes, claims, contradictions, and gaps across the file corpus.

**Trigger**: Route C or Route D (any request with user-uploaded files).

**Process**:

1. **File Inventory**: List all uploaded files with type, size, and a one-line content summary.

2. **Per-File Extraction** — for each file, extract:
   - Core themes and topics
   - Key claims, arguments, and conclusions
   - Data points, statistics, and figures (with page/section references)
   - Methodology (if applicable)
   - Limitations, caveats, or biases noted by the author

3. **Cross-File Mapping**:
   - Identify overlapping themes across files
   - Detect contradictions or conflicting data between files
   - Map complementary information (File A provides context that File B lacks)
   - Identify **gaps** — important aspects of the topic that no file covers

4. **Theme Consolidation**: Produce a consolidated theme list that will feed into Phase 2 dimension decomposition.

**Route-specific behavior**:
- **Route C**: The gap analysis is informational only (noted in output, but no external search will fill gaps). The consolidated themes become the sole basis for Phase 2.
- **Route D**: The gap analysis directly informs Phase 1's search strategy — Phase 1 targets these gaps with external search.

**Output**: Save to **`/mnt/agents/output/research/{topic}_file_analysis.md`** containing:
- File inventory table
- Per-file extraction summaries
- Cross-file mapping (overlaps, contradictions, complementarities)
- Gap analysis
- Consolidated theme list

---

## Phase 1: Landscape Scan (Route A, B, D)

**Goal**: Establish an evidence-grounded global narrative landscape through coarse-to-fine exploration before committing to dimension decomposition.

This phase operates under External-Evidence-First Mode. No analytical narrative may be generated before search outputs are reviewed. Every key finding must include `[^number^]` citation inline.

**Route-specific behavior**:
- **Route A (Wide Search)**: Lighter scan — 3–5 searches for macro framing only. The heavy lifting is delegated to Phase 1W.
- **Route B (Focused)**: Full 5-search coarse-to-fine scan as below.
- **Route D (File-Augmented)**: Targeted scan — use file gap analysis from Phase F to guide search queries. Focus on areas the files don't cover. 3–5 searches.

**Process** (full version for Route B; Route A/D adapt per above):

1. Perform 5 broad exploratory searches by yourself. Search MUST follow a coarse-to-fine progression. Don't search details at beginning.
   * Level 1 – Macro Overview (Search 1-2): Broad overview queries, Industry reports, High-level statistics, Wikipedia-level but verified via authoritative sources, General summaries
   * Level 2 – Structural Mapping (Search 2-4): Market structure, Major actors, Regulatory bodies
   * Level 3 – Emerging Issues & Tensions (Search 5): Recent developments, Conflicting narratives, Trend signals
2. After EACH search, output:
   - Key findings (concise)
   - Dominant narratives identified
   - Controversies or conflicting claims detected
   - Key actors and authoritative sources discovered
   - Gaps requiring deeper investigation
3. Revise dimension decomposition if landscape reveals unexpected structure

---

## Phase 1W: Multi-Agent Wide Exploration (Route A Only)

**Goal**: Maximize search breadth through parallel sub-agent exploration before committing to dimensions. This is the key differentiator for wide-search scenarios — the orchestrator cannot achieve sufficient breadth alone.

**Trigger**: Route A only. Executes after Phase 1 (Quick Landscape).

**Process**:

1. Based on Phase 1's macro framing, identify **5–8 broad exploration facets**. Facets should be:
   - Mutually complementary (together they cover the full problem space)
   - Partially overlapping (≥20% overlap for cross-verification)
   - Examples of facet types: technology landscape, market/commercial landscape, regulatory/policy landscape, competitive dynamics, user/consumer perspective, supply chain, geographic variations, historical evolution, emerging disruptions

2. **Deploy ≥5 sub-agents in parallel**, one per facet. Each sub-agent's prompt MUST include:
   - **(1) Facet scope**: what broad area to explore, with explicit boundaries
   - **(2) Phase 1 context**: key findings from the quick landscape scan
   - **(3) Search requirements**: ≥10 independent searches per agent, coarse-to-fine within the facet
   - **(4) Output format**: structured findings (see below)
   - **(5) Output file path**: `/mnt/agents/output/research/{topic}_wide{NN}.md`

3. Each wide-exploration sub-agent MUST:
   - Perform **≥10 independent searches** with varied queries (no keyword recycling)
   - Cast a wide net: different source types, different angles within the facet
   - Identify key players, data points, trends, and controversies within their facet
   - Flag areas that warrant deep investigation in Phase 3
   - **Save output to `/mnt/agents/output/research/{topic}_wide{NN}.md`**

**Sub-Agent Output Format** (all citations use `[^number^]`):

```
## Facet: [facet name]

### Key Findings
- [finding with inline citation]

### Major Players & Sources
- [entity]: [role/relevance]

### Trends & Signals
- [trend with citation]

### Controversies & Conflicting Claims
- [conflict description with citations to both sides]

### Recommended Deep-Dive Areas
- [area]: [why it warrants depth]
```

4. **Orchestrator Synthesis**: After all wide-exploration agents complete:
   - Read all `{topic}_wide{NN}.md` files
   - Merge findings into a unified landscape map
   - Identify the most promising and contentious areas
   - Feed this rich landscape into Phase 2 for dimension decomposition

**Output**: Each sub-agent saves to `/mnt/agents/output/research/{topic}_wide{NN}.md`. Orchestrator uses these to inform Phase 2.

**Key principle**: Phase 1W is about **breadth** — finding what exists, who matters, what's happening. Phase 3 is about **depth** — investigating each dimension thoroughly. The two-stage swarm ensures nothing important is missed.

---

## Phase 2: Dimension Decomposition

**Goal**: Finalize research dimensions and prepare sub-agent assignments.

**Input varies by route**:
- **Route A**: Phase 1 + Phase 1W wide exploration outputs (richest input)
- **Route B**: Phase 1 landscape scan
- **Route C**: Phase F file analysis — consolidated theme list only (no external input)
- **Route D**: Phase F file analysis + Phase 1 targeted landscape scan

**Rules**:
- **≥10 dimensions (mandatory minimum)**. More is better — 10–20 dimensions depending on topic complexity
- Each dimension approaches the topic from a **distinct angle or scenario**, ensuring the research covers the problem space from fundamentally different perspectives
- Dimensions may be organized by:
  - **Analytical angle** (technical, economic, regulatory, ethical, competitive, user-facing, supply-chain, etc.)
  - **Scenario** (optimistic, pessimistic, status quo, disruption, black swan, etc.)
  - **Stakeholder viewpoint** (consumer, enterprise, regulator, investor, competitor, workforce, etc.)
  - **Geography or market segment** (China, US, EU, emerging markets, etc.)
  - **Time horizon** (historical origins, current state, 1-year outlook, 5-year outlook, etc.)
  - **File-derived theme** (Route C/D: dimensions can map to major themes identified in Phase F)
  - Or any combination — the goal is maximum coverage with deliberate partial overlap
- ≥30% conceptual overlap between related dimensions — overlap creates cross-verification pressure
- Each dimension MUST cover:
  1. **Current state** — what is happening now from this angle, always with inline `[^number^]` citations
  2. **Key evidence** — data, sources, and concrete examples using `[^number^]`
  3. **Tensions and counter-arguments** — what opposing views exist from this angle, all claims referenced via `[^number^]`

**Route C special rule**: For file-only research, dimensions are derived entirely from file themes. Each dimension should map to one or more files, and the scope should reference specific file sections.

Output: a numbered dimension list (≥10 items) with clear scope, assigned angle/scenario, and expected source types for each.

## Phase 3: Parallel Deep Dive (Sub-Agent Deployment)

**Goal**: Execute depth-first research across all dimensions in parallel. **≥10 sub-agents launched simultaneously**, one per dimension.

**Route-specific variants**:

### Standard Mode (Route A, B, D)

1. Create one sub-agent per dimension via `task` — **launch all sub-agents in parallel** (do not serialize)
2. Each sub-agent investigates from its assigned angle/scenario, producing findings that are distinct from but partially overlapping with other agents
3. Each sub-agent's `prompt` MUST include:
   - **(1) Mission**: the dimension's scope, four required angles (current state, history, stakeholders, counter-narrative), and depth expectations
   - **(2) Context**: key findings from earlier phases relevant to this dimension
   - **(3) File context (Route D only)**: relevant excerpts from Phase F file analysis — the sub-agent should treat file content as primary evidence and search for supplementary/corroborating external sources
   - **(4) Output format**: the evidence template below
   - **(5) Output file path**: the sub-agent MUST save to `/mnt/agents/output/research/{topic}_dim{NN}.md`

**Sub-Agent Requirements** (Standard Mode):
- Perform **≥20 independent searches** (no repeated keyword cycles)
- Investigate primary sources where possible (government sites, academic journals, official filings, major media)
- Trace claims back to original publication
- Identify and document counter-arguments
- Avoid content farms, anonymous blogs, SEO aggregators
- **Route D**: Explicitly reference and build upon file-derived evidence. Search externally to fill gaps, verify file claims, and add depth. Clearly distinguish file-sourced vs. search-sourced evidence.
- **Save output to `/mnt/agents/output/research/{topic}_dim{NN}.md`**

### File-Only Mode (Route C)

1. Create one sub-agent per dimension via `task` — **launch all sub-agents in parallel**
2. Each sub-agent analyzes its assigned dimension **using only the uploaded file content** — NO external search
3. Each sub-agent's `prompt` MUST include:
   - **(1) Mission**: the dimension's scope and the specific files/sections relevant to it
   - **(2) Full file content or relevant excerpts**: provide the actual file content the agent needs (do not assume the sub-agent can access files independently)
   - **(3) Analysis requirements**: cross-reference between files, identify patterns, evaluate strength of evidence, note limitations
   - **(4) Output format**: the evidence template below (adapted — Source field references file name + section instead of URL)
   - **(5) Output file path**: `/mnt/agents/output/research/{topic}_dim{NN}.md`

**Sub-Agent Requirements** (File-Only Mode):
- Thoroughly analyze all provided file content relevant to the dimension
- Cross-reference claims and data across multiple files
- Evaluate evidence quality and identify potential biases
- Note where file evidence is thin or contradictory
- Identify implicit assumptions in the source material
- **Do NOT perform any external search**
- **Save output to `/mnt/agents/output/research/{topic}_dim{NN}.md`**

### Sub-Agent Output Format (all modes)

All citations use `[^number^]`:

```
Claim: [identified claim with inline citation]
Source: [source name / file name]
URL: [source URL / "File: {filename}, Section: {section}"]
Date: [publication date / "N/A" for files]
Excerpt: [verbatim raw excerpt — no paraphrasing]
Context: [surrounding context]
Confidence: [high / medium / low]
```

**Output**: Each sub-agent saves its output to **`/mnt/agents/output/research/{topic}_dim{NN}.md`**.

## Phase 4: Cross-Verification Engine (Orchestrator)

**Goal**: Compare all dimension outputs, classify confidence, surface contradictions, and **save the verification results to a file** for downstream use by report-writing.

**Process**:
1. Read all `/mnt/agents/output/research/{topic}_dim{NN}.md` files
2. Categorize every finding into one of four tiers:

| Tier | Criteria |
|------|----------|
| **High Confidence** | Confirmed by ≥2 agents from independent sources with consistent evidence |
| **Medium Confidence** | Confirmed by 1 agent from an authoritative source |
| **Low Confidence** | Weak sourcing, blog-level evidence, or single unverified claim |
| **Conflict Zone** | Statistical disagreement, interpretive divergence, temporal inconsistency between agents, or numerical discrepancy for the same metric (e.g., two agents report different figures for the same statistic) |

3. List all Conflict Zone items explicitly — contradictions are highlighted and analyzed, never suppressed. **Temporal conflicts are Conflict Zone**: if agents report data from different time periods for the same metric, flag this as a temporal inconsistency and record which time period each data point belongs to.
4. Determine if Phase 5 is needed (any Conflict Zone or critical Low Confidence items)
   - **Route C exception**: Phase 5 is skipped (no external search allowed). Conflicts are documented as-is and carried into Phase 6.
5. Inline citations `[^number^]` must be preserved
6. Conflict Zone analysis must include `[^number^]` references to all sources involved

**Output**: Save the complete cross-verification results (all tiers + conflict zone analysis) to **`/mnt/agents/output/research/{topic}_cross_verification.md`**. This file is critical — it carries confidence classifications that guide report-writing.

## Phase 5: Targeted Validation (Conditional)

**Goal**: Resolve conflicts and strengthen weak findings.

**Trigger**: Execute only if Phase 4 identified Conflict Zone or critical Low Confidence items. **NOT available for Route C** (file-only research cannot invoke external search).

All validation outputs must preserve inline `[^number^]` citations.

**Process**:
1. For each unresolved item, deploy a focused sub-agent with:
   - The specific conflicting claims and their sources
   - Instructions to find independent evidence that resolves the disagreement
   - Minimum 3 additional searches per conflict

2. Repeat until each item is either:
   - **Resolved** — reclassified to High/Medium Confidence with new evidence
   - **Explicitly marked unresolved** — documented as a genuine disagreement in the field

3. **Update** `/mnt/agents/output/research/{topic}_cross_verification.md` with the resolution results.

## Phase 6: Insight Extraction

**Goal**: Identify non-obvious insights that do not explicitly appear in previous findings, but emerge from cross-dimension analysis.

**Definition of Insight**:
An insight is a higher-level inference derived from multiple validated findings. It must not repeat previously stated claims or evidence.

**Process**:

1. Review all validated findings from Phase 3–5 (and Phase F file analysis, if applicable).
2. Identify patterns that only become visible when comparing multiple dimensions.
3. Extract insights that reveal: structural relationships, hidden tensions, emerging trends, systemic risks, strategic opportunities.
4. Ensure each insight is supported indirectly by evidence from at least two dimensions.

**Route-specific emphasis**:
- **Route C/D (file-based)**: Prioritize insights that emerge from cross-file synthesis — patterns that no single file reveals on its own. For Route D, also highlight where external evidence strengthens, contradicts, or extends file-derived conclusions.
- **Route A (wide search)**: Prioritize insights that bridge different exploration facets — connections between areas that were explored independently.

**Genre-aware insight extraction**: Adjust emphasis based on the intended downstream writing format:
- **Report** (industry report, market analysis, consulting deliverable): prioritize actionable strategic insights, market opportunities, competitive dynamics, and forward-looking implications
- **Academic paper** (survey, empirical study, literature review): prioritize research gaps, methodological contradictions, theoretical tensions, and novel contribution angles that position against prior work
- When the target genre is unclear, produce insights in a neutral format covering both strategic and academic angles — the writing skill will adapt

**Output Requirements**:

For each insight, record:

- Insight: concise statement of the inferred pattern
- Derived From:
  - Dimension references (e.g., Dim 02, Dim 07)
  - Supporting evidence clusters (include file references for Route C/D)
- Rationale: explanation of how the insight emerges from the evidence
- Implications: potential impact or significance
- Confidence: high / medium / exploratory

**Output**: Save all insights to **`/mnt/agents/output/research/{topic}_insight.md`**. This file is the core synthesis of the entire deep research process and will be the primary input for the downstream writing skill.

**Rules**:

- Insights must not duplicate existing findings.
- Insights must be derived from cross-dimension comparison.
- Avoid speculative claims unsupported by evidence.
- Minimum output: 5 insights.
- Insights must include references to supporting evidence using inline citations `[^number^]`

## Phase 7: Handoff to Writing Skill

**Goal**: Hand off all research artifacts to the appropriate writing skill for final document generation.

After cross-verification (and optional targeted validation) and insight extraction are complete:

1. Verify all required files exist under `/mnt/agents/output/research/`:
   - `{topic}_dim{NN}.md` — all dimension files (≥10)
   - `{topic}_cross_verification.md` — confidence tiers and conflict analysis
   - `{topic}_insight.md` — cross-dimension insights
   - `{topic}_file_analysis.md` — (Route C/D only) file intake analysis
   - `{topic}_wide{NN}.md` — (Route A only) wide exploration outputs
2. Determine the target writing skill based on user intent:
   - **`report-writing`** — industry reports, market analysis, consulting deliverables, policy briefs
   - **`paper-writing`** — academic papers, survey papers, literature reviews, conference submissions
3. Invoke the selected writing skill, providing **explicit file paths** in the handoff:
   - **Insight file**: `/mnt/agents/output/research/{topic}_insight.md`
   - **Cross-verification file**: `/mnt/agents/output/research/{topic}_cross_verification.md`
   - **Dimension files**: `/mnt/agents/output/research/{topic}_dim01.md` through `{topic}_dim{NN}.md`
   - **File analysis** (Route C/D): `/mnt/agents/output/research/{topic}_file_analysis.md`
   - **Wide exploration files** (Route A): `/mnt/agents/output/research/{topic}_wide{NN}.md`
   - **Research directory**: `/mnt/agents/output/research/`
4. The orchestrator MUST explicitly tell the writing skill that deep research is complete and no additional research sub-agents are needed.
5. The final document MUST incorporate insights from Phase 6.
6. If the user specified a time range, the orchestrator MUST verify that key data points and dates in the final artifacts fall within that range before handoff.

## Output Rules

- Insights from Phase 6 must be incorporated into the final document — as a dedicated Insights section (for reports) or woven into Discussion/Contribution sections (for papers).
- Insights must not be omitted even if the user requested a shorter output format.
- All outputs must include `[^number^]` style citations.
- The final document must clearly distinguish verified findings, conflict zones, and derived insights.
- **Route C**: Citations reference file names and sections (not URLs). The report must clearly state it is based solely on the provided files.
- **Route D**: Citations must distinguish file-sourced evidence from externally-sourced evidence.
- If the user doesn't specify file type, default to Word format.

## Core Principles

1. **Depth over breadth** (Route B) / **Breadth then depth** (Route A). Shallow aggregation is forbidden. Each dimension must be investigated thoroughly before moving on.
2. **Raw evidence required.** Sub-agents must return verbatim excerpts with source URLs/file references and dates. No paraphrased-only outputs.
3. **Contradictions are signal.** Conflicts are highlighted and analyzed, never suppressed or averaged away.
4. **Everything is a file.** Never output long-form research content in chat. Chat is for status updates only.
5. **Source quality matters.** Prioritize: government sites, academic journals, official filings, major media. Avoid: content farms, anonymous blogs, SEO aggregators. For file-based routes, treat user-provided files as primary authoritative sources.
6. **Search budget by route:**
   - Route A: ≥5 wide agents × ≥10 searches + ≥10 deep agents × ≥20 searches = **≥250 total searches**
   - Route B: ≥10 agents × ≥20 searches = **≥200 total searches**
   - Route C: **0 external searches** (file-only)
   - Route D: ≥10 agents × ≥15 searches = **≥150 total searches** (reduced because files provide base evidence)
7. **All outputs must include `[^number^]` style citations.**
8. **All files under `/mnt/agents/output/research/`.** No exceptions.
9. **Route C respects user intent.** If the user says "only based on files", do NOT sneak in external searches. Fidelity to user intent is paramount.
10. **Route D balances sources.** File content is primary; external search fills gaps and adds depth. Do not let external sources overshadow the user's provided materials.

## File Naming

All files are saved under `/mnt/agents/output/research/`.

| File | Phase | Route | Content |
|------|-------|-------|---------|
| `{topic}_file_analysis.md` | Phase F | C, D | File intake: per-file extraction, cross-file mapping, gap analysis |
| `{topic}_wide{NN}.md` | Phase 1W | A | Per-facet wide exploration output |
| `{topic}_dim{NN}.md` | Phase 3 | All | Per-dimension sub-agent research output |
| `{topic}_cross_verification.md` | Phase 4-5 | All | Confidence tier classification + conflict zone analysis |
| `{topic}_insight.md` | Phase 6 | All | Cross-dimension insights (core synthesis for downstream writing skill) |
