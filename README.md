# KAPAdvisor Safety Dashboard

This dashboard presents safety evaluation results across five KAPAdvisor bots using an executive-friendly Streamlit interface. It highlights risk distribution, recurring issue patterns, and row-level evidence to support product and quality decisions.

## Setup

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Follow the Data Setup section below.

## Deploy To Streamlit Cloud

1. Push this project to a Git repository.
2. In Streamlit Cloud, create a new app pointing to `app.py`.
3. Ensure the five required CSV files are available in `data/`, then deploy.

## Data Setup

This dashboard requires 5 scored safety CSV files, one per bot, placed in a
`data/` folder in the project root:

data/
├── Brainstorm_Bot_safety_scores.csv
├── Essay_Bot_safety_scores.csv
├── Free_Chat_Bot_safety_scores.csv
├── SAT_Bot_safety_scores.csv
└── Transcript_Bot_safety_scores.csv

TODO: CONFIRM AGAINST REAL CSV SCHEMA
These exact filenames are placeholders while scoring exports are in progress.

These files contain proprietary production data and are not included
in this repository (excluded via .gitignore).

Use your final safety scoring export source once ready and place all
five files directly in the `data/` folder before running the app.

## Running the app

1. Clone this repository
2. Create a virtual environment and install dependencies:
   pip install -r requirements.txt
3. Add the 5 safety CSVs listed above into data/
4. Run: streamlit run app.py

If any file is missing, the app will show a clear error telling you
exactly which file is missing and where it expects it.

## Data Privacy Note

CSV datasets are not stored in this repository. Download them from the shared company Google Drive folder and place them in the local `data/` directory before running the app.

## Placeholder Assumptions

This sister project was scaffolded before real safety CSVs were available.
Core schema assumptions are clearly marked in code with:

`# TODO: CONFIRM AGAINST REAL CSV SCHEMA`

Do one follow-up correction pass after the real files are ready.
