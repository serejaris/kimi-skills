---
name: deep-research
description:
    Utilizes a suite of tools to facilitate exhaustive, evidence-based deep research and long-form report engineering. Supports multi-dimensional research with iterative search, recursive reflection, quantitative visualization, and structured outputs in multiple formats (Markdown, docx, pdf, xlsx, pptx, webapp).
---

# Deep Research

Conduct thorough, multi-dimensional research on complex questions using file creation and editing, search engines and browsers, code execution, image and multimedia generation, slide creation, website deployment, and visual processing of tool outputs. Think critically, use the current date as the temporal reference, verify uncertain information proactively, and deliver comprehensive, well-structured, rigorously grounded findings.

## Research & Discovery Phase (The 10+ Step Loop)

1.  **Read Attached Files**: Start by checking any attachments to understand the background information.
2.  **Clarify Intent**: Ask targeted clarification questions **via the `ask_user` tool** to ensure you fully understand their goals before proceeding.
3.  **Iterative Search**: Perform **at least 10 search steps** to ensure comprehensive coverage across multiple dimensions. Avoid keyword redundancy; ensure each round brings substantial new information.
4.  **Credibility & Verification**: Prioritize authoritative sources (government sites, academic databases, peer-reviewed journals). **Never fabricate data.** Every statistic and claim must be accurate and traceable.
5.  **Recursive Reflection**: After EACH search round, output a **Thinking Process** and a **Summary**.
    - **Thinking**: Reflect on content found, identify unmet needs, and plan the next specific step.
    - **Summary**: Concise recap of key findings.
    - *Constraint*: Both sections must be **short and concise**.
6. **Quantitative Analysis**: Use **Python** for calculations, data cleaning, statistical analysis, and verification when precision is required. 
7. **Visualization Planning**: Based on the report content, create necessary, content-relevant visualizations and follow the **Visualization Workflow** for chart/diagram authoring, rendering, embedding, and visual consistency.

## Report Engineering Standards

### 1. Structural Logic & Opening

- **Conditional TL;DR**: Provide a **short direct answer** at the beginning **only if** the user's question can be answered in a few sentences. 
- **Style Adaptation**:
    - If a specific style is implied (e.g., story, interview, case narrative), adhere to it.
    - **Default**: Strict academic report format.
    - Omit generic Introduction/Background sections unless explicitly required.

### 2. Depth and Analysis (Mode-Based)

- **Academic/Survey Mode**:
    - Prioritize comprehensive fact-based detail. Include full definitions, formulas, statistical indicators (CI, metrics), and baseline comparisons.
    - Avoid speculative interpretation; ensure all statements are supported by references.
- **Lifestyle/Practical Mode**:
    - Incorporate observations, human insights, Pros/Cons, and actionable trade-offs.
    - Reflect on implications and explain why certain patterns matter.

### 3. Length and Paragraph Constraints

- **Total Volume**: As a default target, the report should generally reach long-form report scale.
- **Paragraph Rules**:
    - Each paragraph must be **at least 100 words** (max 1,000 words). Each paragraph should be substantial and well developed, without becoming mechanically overextended.
    - **Subsection Rule**: Every subsection (e.g., `## 3.1`) MUST contain **more than one paragraph**.
- **Natural Transitions**: In English writing, avoid rigid patterns like "First, second, third" or "Firstly, secondly, lastly."
- **Expansion Rule**: If the draft is still underdeveloped, expand the logically relevant existing sections rather than adding disconnected filler.

### 4. Mandatory Table Architecture

- **Usage**: Use tables as the primary structural tool to replace or shorten long prose for comparisons, workflows, or results.
- **Centralized Comparison**: Aggregate recurring entities, models, or metrics from across different sections into single, coherent comparison tables.
- **Source Integration**: **Do not include a separate "Source" column**. Place numeric citations (e.g., `[^1^]`) directly within the data cells.

### 5. Revision and Completion

- **Completion Standard**: The report must ultimately be complete, well-structured, and fully compliant with all content, formatting, and length requirements.
- **Final Verification**: Before finalizing, verify that the report fully satisfies all structure, depth, table, citation, and length requirements, especially that it has developed into a sufficiently substantial long-form report rather than a brief or compressed write-up.
- **Targeted Revision**: If the report remains insufficient in scope or depth, strengthen it by elaborating underdeveloped sections, adding missing evidence or comparisons, or introducing additional analytical dimensions where appropriate.
- **Integrated Improvement**: Any necessary revision must be incorporated into the logically relevant existing section, rather than appended as a disconnected add-on or catch-all section.
- **Substance over Filler**: Prioritize substantive depth, specificity, and analytical value over repetition, redundancy, or filler.

### 6. Formatting & Citation Rules

- **Citation Format**: Use `[^index^]` for factual/formal pieces. Max **two citations per sentence**.
    - *Note*: Do not use citations for creative/non-formal writing.
    - *Note*: If citing multiple sources together, write them as separate markers: `[^1^][^2^]`, never `[^1,2^]`.
    - *Note*: Citation indices are **immutable source IDs from tool/search results**. Do **not** renumber them based on order of appearance, writing order, or any reference-list order; if a source already has an ID such as `[^85^]` from tool/search results, that same ID must be preserved everywhere in the document.
- **No End References Section**:
    - Do **not** include any end-of-report **"References"**, **"Reference"**, **"Sources"**, or similar bibliography/list of sources.
    - Citation IDs are used for frontend rendering and source mapping, not for a model-generated bibliography.
- **Bolding Strategy**: 
    - Bold **important keywords, critical numbers, major conclusions, and key insights**.
    - **Avoid redundant bolding**: Do not repeatedly bold the same entity within a short span.
- **High-Stakes Disclaimer**: For medical, legal, financial, or other high-stakes topics, end the response with a clear statement that the content is for general informational purposes only and does not constitute professional advice.
- **Visuals**: Incorporate diagrams, charts, or photographs generated or found during research to support arguments.

### 7. Visualization Workflow

- **Generation**: Cover both **data-driven charts** (built from verified, cited data — **never fabricate values**) and **conceptual diagrams** (framework, flow, architecture, or relationship schematics that make the report's structure and logic easier to follow). Build with **ECharts by default**, using **Python** (e.g., via IPython) when ECharts cannot faithfully express the intended visual.
- **Rendering & Embedding**: For an HTML presentation, charts may stay as native ECharts/HTML. For a `.md` or any other static-format report, ECharts and Python charts alike MUST be exported to static images and embedded with `![caption](path)`; never paste raw option objects, `<script>` blocks, or interactive HTML into the report body. **Note**: Static output format is **not** a reason to switch from ECharts to Python/matplotlib. When ECharts can faithfully express the intended visual, even for static reports, author the chart in ECharts first because it generally produces more polished, presentation-ready visuals; then render it to a static `.png`, `.jpg`, or supported `.svg` image and embed it in the report.
- **Quality Bar** (dimensions carry equal weight): **Correctness** — the visual matches its source: data charts reflect the underlying numbers, and diagrams stay faithful to the described structure, prose, and tables. **Chart-type fit** — reach for the type that fits the relationship, using ECharts' full repertoire rather than only bar/line/pie. **Clarity** — descriptive title, axis names with units, a legend for ≥2 series, key data labels, and no overlap or truncation. **Aesthetics** — maintain a cohesive visual style across the entire report, using a restrained, harmonious palette consistently across all charts and diagrams (same entity → same color), with sensible sizing, margins, and legible fonts. Avoid unrelated palettes across figures; all visuals in the same report should follow one consistent color system. **Diversity & coverage** — give each key quantitative thread its own fitting chart and vary the chart types instead of repeating one.

---

# File-Based Output Workflow

## Output Format Determination

Determine the output format based on user requirements using the following rules:

1. **User Explicitly Requests Specific Format**: If the user explicitly requests output in **docx**, **pdf**, **xlsx**, **pptx**, or **webapp** format, generate the file directly in the requested format and save to `/mnt/agents/output/` directory.

2. **User Does Not Specify Format**: If the user does not specify an output format, **default to Markdown format** and save to `/mnt/agents/output/` directory (e.g., `/mnt/agents/output/report.md`)

## Format-Specific Requirements

**Markdown Format (Default)**:
- Save path: `.md` file in `/mnt/agents/output/` directory.
- Must include complete article structure: Executive Summary, Comprehensive Analysis, tables, and citations.
- Use standard Markdown syntax: headers (#, ##, ###), tables, bold text, and lists.

**Non-Markdown Outputs (docx, pdf, xlsx, pptx, webapp)**:
- **Mandatory Skill Reading**: Before generating any non-Markdown output, you **must** first read the corresponding skill file.
- Follow the skill instructions strictly; they override general defaults for that format.
- **DOCX/PDF Generation Rule**: If the requested output format is `.docx` or `.pdf`, first generate a complete Markdown file under `/mnt/agents/output/`, then convert that Markdown through the workflow specified by the corresponding DOCX or PDF skill. Do not generate the DOCX or PDF directly from scratch unless that format skill explicitly requires otherwise.
- Save all outputs under `/mnt/agents/output/`.

**Additional Rule for Webapp Tasks**:
- Any frontend-related task, including website development, web application development, or visual/webpage reproduction, must first read the `webapp-building` skill documentation before starting implementation.
- Do not bypass the prescribed webapp setup workflow by directly using ad hoc initialization commands (such as `npx` commands). Follow the skill-defined initialization process first.
- After initialization, read any generated setup documentation (such as `info.md`) and use it to understand template-specific requirements, including configuration structure, required assets, and build instructions.
- When the skill defines a designated configuration entry point for customization, make content changes there instead of modifying core component files.
