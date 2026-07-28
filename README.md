# KAPAdvisor Safety Dashboard

This dashboard presents safety evaluation results across five KAPAdvisor bots using an executive-friendly Streamlit interface. It highlights risk distribution, recurring issue patterns, and row-level evidence to support product and quality decisions.

The safety judge evaluates whether a bot response discloses student academic or personal data (for example GPA, SAT scores, college list, or essay content) to a recipient who is authorized to receive it (the student themselves, an authorized parent, or an authorized counselor). It also checks for other harm types: discrimination, account-access guidance, academic harm, age-inappropriate content, and scope violations (medical, legal, or financial guidance outside the AI's domain).

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
├── Brainstorm_Bot_scores.csv
├── Essay_Bot_scores.csv
├── Free_Chat_Bot_scores.csv
├── SAT_Bot_scores.csv
└── Transcript_Bot_scores.csv

These files contain proprietary production data and are not included
in this repository (excluded via .gitignore).

**To get the CSVs:** download them from the shared company Google
Drive folder:
https://drive.google.com/drive/u/0/folders/16lL_UWMowz8bW30E_Cb7KUoVt0y9nSgd

Download all 5 files and place them directly in the `data/` folder
before running the app.

Expected shared columns across files:

`trace_id, user_id, source_op, timestamp, user_input, ai_response, user_role, retrieval_context, conversation_history, safety_score, safety_reasoning, safety_evidence, safety_authorization_note, safety_authorization_check`

Each file may also include token/cost/latency metadata columns.


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

