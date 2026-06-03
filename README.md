# Vela AI Scoring Engine — README

A two-stage screening pipeline that scores Southeast-Asian software companies
against Vela's investment criteria. It runs an audit, a cheap rule-based filter,
data enrichment, and an AI scoring layer, then exports results as a colour-coded
Excel report and a CSV.

**The engine runs fully WITHOUT an API key** (rule-based mode). The API key is
only needed for the optional live-AI demo.

---

## 1. Files

| File | Description |
|------|-------------|
| `vela_scoring_engine.py` | Main engine: audit → filter → enrich → score → export |
| `generate_dummy_data.py` | Generates the 80-company sample input CSV |
| `vela_companies_input.csv` | Sample input (80 dummy companies) — already included |
| `vela_scoring_results.csv` | Output (generated on run) — BD-ready CSV |
| `vela_scoring_results.xlsx` | Output (generated on run) — colour-coded by Tier |

---

## 2. Requirements

- **Python 3.9+** (check with `python --version`)
- Two libraries:
  - `openpyxl` — required, for the Excel export
  - `pydantic` — optional, only for the live-AI demo (the engine still runs without it)

Install:

```bash
# Windows
pip install openpyxl pydantic

# macOS / Linux
pip3 install openpyxl pydantic
```

---

## 3. Quick start (NO API key needed)

This is the main mode. It scores all 80 sample companies and writes the output files.

```bash
# Step 1 — generate the input CSV (only needed once; file is also pre-included)
python generate_dummy_data.py

# Step 2 — run the engine
python vela_scoring_engine.py
```

*(On macOS/Linux use `python3` instead of `python`.)*

**What you'll see / get:**
- A Data Audit summary and the Tier distribution printed in the terminal
- `vela_scoring_results.csv` and `vela_scoring_results.xlsx` created in the same folder
- A short security demo showing prompt-injection filtering

> If you get "file not found" for the CSV, run `generate_dummy_data.py` first
> (Step 1). If `python` isn't recognised on Windows, see Troubleshooting below.

---

## 4. Optional — live AI demo (needs an API key)

This mode makes ONE real call to the Claude API to show the AI reasoning layer
returning structured JSON. It is **optional** — everything else works without it.

### Get a key
1. Go to `console.anthropic.com` → add a small amount of credit
2. Create an API key (looks like `sk-ant-...`)
3. The API is billed separately from any Claude Pro subscription. One demo call
   costs well under one cent.

### Run it

```powershell
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-..."
python vela_scoring_engine.py --demo-ai
```

```bash
# macOS / Linux
export ANTHROPIC_API_KEY="sk-ant-..."
python3 vela_scoring_engine.py --demo-ai
```

**If no key is set**, the command does NOT crash — it prints a friendly message
explaining how to add one, and exits cleanly.

### Security note
- The key is read from an **environment variable** — it is never written in the code.
- Never paste your key into any file you submit or share.
- The model name is set in `CLAUDE_MODEL` near the bottom of the file; model names
  change over time, so verify the current name at `docs.claude.com` if you get a
  model error.

---

## 5. Customising the input

To score your own companies, edit `vela_companies_input.csv` (or change
`generate_dummy_data.py`). Columns:

```
name, country, is_software, is_b2b, founded_year, product_desc, vertical,
num_competitors, customer_count, revenue_concentration, founder_background,
employee_count, registry_revenue, pricing_model, g2_long_tenure,
recent_funding, founder_age_signal
```

- Leave a cell **empty** to mark a field as unknown (the engine handles this —
  empty ≠ low score).
- Booleans: `True` / `False`. Numbers: plain digits.

---

## 6. Troubleshooting

| Problem | Fix |
|---------|-----|
| `python` not recognised (Windows) | Use the version that works: try `python`, `py`, or reinstall Python from python.org with **"Add to PATH"** ticked |
| `ModuleNotFoundError: openpyxl` | Run `pip install openpyxl` |
| `FileNotFoundError: vela_companies_input.csv` | Run `python generate_dummy_data.py` first |
| AI demo: `model not found` | Update `CLAUDE_MODEL` to a current name from docs.claude.com |
| AI demo: authentication error | Check the key is correct and your account has credit |

---

## 7. How it works (one-paragraph summary)

The engine reads the company list, audits data quality (Layer 0), applies a cheap
rule-based filter (Layer 1), enriches the survivors — prioritising Vietnamese
registries for VN companies — then scores them with a 9-criteria rubric (Layer 2).
Missing data is marked "unknown" rather than penalised, every score carries a
confidence level, and Tier B is split into "ready" and "needs enrichment". Results
are exported for the BD team as Excel and CSV.
