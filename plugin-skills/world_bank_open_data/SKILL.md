---
name: world_bank_open_data
description: "World Bank Open Data is a free global development data platform with access to countries worldwide and 29,000+ indicators covering economic, social, and environmental metrics including GDP, GNP, population, poverty, unemployment, trade, inflation, education, health, and environmental time series from 1960 to present."
---

# World Bank Open Data

Use this skill to answer questions that require World Bank Open Data country
indicators, development metrics, or national-level time series.

## Setup

Check whether the agent-gw Python SDK is available in the current Python environment, and install it only if the check fails:

```bash
python3 -c "import agent_gw" || python3 -m pip install "$(curl -s https://cdn.kimi.com/agentgw/pysdk/manifest.json | python3 -c "import json,sys; print(json.load(sys.stdin)['latest']['url'])")"
```

The SDK needs an API key from `api_key=...`, `KIMI_API_KEY`, or
`~/.kimi/agent-gw.json`.

## Workflow

1. Run `python3 scripts/world_bank_open_data_tool.py describe` from the plugin
   directory to call `get_data_source_desc({"name": "world_bank_open_data"})`.
2. Read the returned Markdown carefully. It contains the overall data source
   rules, country formats, indicator formats, date range constraints, and each
   API's description, required parameters, optional parameters, defaults, and
   allowed values.
3. Select the API that best matches the user's question.
4. Build `params` exactly from the Markdown requirements. Pay attention to
   country or region, indicator code or name, year range, unit, source,
   frequency, and national-level data constraints.
5. Use `python3 scripts/world_bank_open_data_tool.py call` to call
   `call_data_source_tool`.
6. If the call fails, explain the failure reason from the response.
7. If the call succeeds, save any returned files first, then answer using
   `resp.result.assistant`; ignore `resp.result.user` unless display content is
   specifically needed.

## Common Use Cases

- Country-level time series for GDP, GNP, population, poverty rates,
  unemployment, trade, inflation, education, health, and environmental data.
- Cross-country comparison of development indicators.
- Long-run trend analysis using annual data from 1960 to present where available.
- Economic, social, and environmental research that needs World Bank indicator
  definitions and national-level observations.

## Script

Use the bundled script from the plugin directory:

```bash
python3 scripts/world_bank_open_data_tool.py describe
```

After reading the Markdown and selecting an API:

```bash
python3 scripts/world_bank_open_data_tool.py call \
  --api-name "<api name from markdown>" \
  --params-json '{"required_param":"value"}'
```

For larger params, write a JSON object and pass
`--params-file path/to/params.json`.

The script:

- sends `{"name": "world_bank_open_data"}` to `get_data_source_desc`
- sends `{"data_source_name": "world_bank_open_data", "api_name": ..., "params": ...}` to
  `call_data_source_tool`
- prints failure messages from `error.user` or `error.assistant`
- saves returned files to each `files[].name` path returned by the data source
- prints the joined `result.assistant` texts on success

Expected `call_data_source_tool` response shape:

```python
{
    "is_success": bool,
    "result": {"user": list[str], "assistant": list[str]} | None,
    "error": {"user": list[str], "assistant": list[str]} | None,
    "files": [{"name": str, "content": str}],
}
```

When files are returned, `name` is the file path or name to write. The path is
usually dictated by the selected API's params in the Markdown docs. If an API
does not need files, the response normally has no files to save.
