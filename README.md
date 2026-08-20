# AI-Powered Business Report Generator

Turns raw operational data into a written executive summary using SQL for analysis and the Claude API for narrative generation.

Built to demonstrate an end-to-end workflow: **structured data → SQL analysis → AI-generated business writing** — the same kind of pipeline used to automate reporting for distributed teams.

## What it does

1. Reads sales data from a SQLite database (`data/business.db`)
2. Runs SQL queries to compute revenue totals, regional breakdowns, product performance, and monthly trends
3. Passes those metrics to Claude via the Anthropic API with a structured prompt
4. Claude generates a Markdown executive report (summary, highlights, regional/product analysis, recommendations)
5. Report is saved to `output/` with a timestamp

A sample output is included at [`output/sample_report.md`](output/sample_report.md) so you can see the result without needing an API key.

## Why this project

I built this to bring together three things from my day-to-day work: SQL-based data analysis, Python automation, and structured prompting with the Claude API. It reflects how I've used generative AI in practice — not to replace analysis, but to turn data that's already been queried and verified into clear, readable reporting for stakeholders.

## Tech stack

- Python 3
- SQLite (swap in Postgres/MySQL by changing the connection logic)
- [Anthropic Claude API](https://docs.claude.com)

## Setup

\`\`\`bash
git clone https://github.com/Marvellous52/ai-report-generator.git
cd ai-report-generator
pip install -r requirements.txt
\`\`\`

Set your API key:

\`\`\`bash
export ANTHROPIC_API_KEY="your-api-key-here"
\`\`\`

## Usage

Seed the sample database (already included, but you can re-seed or modify it):

\`\`\`bash
python seed_data.py
\`\`\`

Generate a report:

\`\`\`bash
python generate_report.py
\`\`\`

The report will be saved to `output/report_<timestamp>.md`.

## Using your own data

Replace the contents of `data/business.db` with your own `sales` table (or edit `fetch_metrics()` in `generate_report.py` to match your schema). The prompt-building logic in `build_prompt()` can be adapted to any tabular dataset — it's intentionally decoupled from the SQL layer so the two can evolve independently.

## Project structure

\`\`\`
ai-report-generator/
├── data/
│   └── business.db          # sample SQLite database
├── output/
│   └── sample_report.md     # example generated report
├── generate_report.py       # main script: query data → call Claude → save report
├── seed_data.py             # generates sample data
├── requirements.txt
└── README.md
\`\`\`

## Possible extensions

- Export reports to PDF or DOCX instead of Markdown
- Schedule the script to run weekly and email the report automatically
- Swap SQLite for a live Postgres connection
- Add a simple web dashboard to view historical reports

## Author

**Marvellous Gift Ighoyivwi**
AI Operations & Business Support Professional
[LinkedIn](https://linkedin.com/in/marvellousighoyivwi-3b45a8417) · [GitHub](https://github.com/Marvellous52)
