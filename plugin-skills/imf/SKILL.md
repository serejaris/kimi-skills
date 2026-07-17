---
name: imf
description: "IMF provides global macroeconomic data through the World Economic Outlook database, including historical statistics and forecasts for GDP growth, inflation, government debt, unemployment, trade balances, and other indicators across 190+ countries and regions, plus COFER reserve currency composition data."
---

# IMF

Use this skill to answer questions that require IMF macroeconomic data,
World Economic Outlook data, or COFER reserve currency composition data.

## Setup

Check whether the agent-gw Python SDK is available in the current Python environment, and install it only if the check fails:

```bash
python3 -c "import agent_gw" || python3 -m pip install "$(curl -s https://cdn.kimi.com/agentgw/pysdk/manifest.json | python3 -c "import json,sys; print(json.load(sys.stdin)['latest']['url'])")"
```

The SDK needs an API key from `api_key=...`, `KIMI_API_KEY`, or
`~/.kimi/agent-gw.json`.

## Workflow

1. Run `python3 scripts/imf_tool.py describe` from the plugin directory to call
   `get_data_source_desc({"name": "imf"})`.
2. Read the returned Markdown carefully. It contains the overall data source
   rules, country and region formats, indicator names, dataset constraints, and
   each API's description, required parameters, optional parameters, defaults, and
   allowed values.
3. Select the API that best matches the user's question.
4. Build `params` exactly from the Markdown requirements. Pay attention to
   country or region, indicator, year or date range, forecast versus historical
   periods, dataset or source table, unit, and frequency requirements.
5. Use `python3 scripts/imf_tool.py call` to call `call_data_source_tool`.
6. If the call fails, explain the failure reason from the response.
7. If the call succeeds, save any returned files first, then answer using
   `resp.result.assistant`; ignore `resp.result.user` unless display content is
   specifically needed.

## Common Use Cases

- Cross-country comparison of GDP growth, inflation, unemployment, government
  debt, current account, trade balance, or other macroeconomic indicators.
- Historical macroeconomic trend analysis and World Economic Outlook forecasts.
- Policy research that requires IMF country, region, or global macro data.
- COFER analysis of official foreign exchange reserve currency shares such as
  USD, EUR, CNY, JPY, GBP, CHF, AUD, and CAD.

## Script

Use the bundled script from the plugin directory:

```bash
python3 scripts/imf_tool.py describe
```

After reading the Markdown and selecting an API:

```bash
python3 scripts/imf_tool.py call \
  --api-name "<api name from markdown>" \
  --params-json '{"required_param":"value"}'
```

For larger params, write a JSON object and pass
`--params-file path/to/params.json`.

The script:

- sends `{"name": "imf"}` to `get_data_source_desc`
- sends `{"data_source_name": "imf", "api_name": ..., "params": ...}` to
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
