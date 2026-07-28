import pandas as pd
from pathlib import Path
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# TODO: CONFIRM AGAINST REAL CSV SCHEMA
# Filename assumption for pre-scored safety files. Update once final exports are available.
BOT_FILES = {
    "Brainstorm_Bot": "Brainstorm_Bot_safety_scores.csv",
    "Essay_Bot": "Essay_Bot_safety_scores.csv",
    "Free_Chat_Bot": "Free_Chat_Bot_safety_scores.csv",
    "SAT_Bot": "SAT_Bot_safety_scores.csv",
    "Transcript_Bot": "Transcript_Bot_safety_scores.csv",
}

OPTIONAL_TEXT_COLUMNS = [
    "safety_worst_claim",
    "safety_claim_classification",
]


def _resolve_bot_filepath(filename: str) -> Path:
    primary = DATA_DIR / filename
    if primary.exists():
        return primary

    # Accept legacy/current export naming if *_safety_scores.csv is absent.
    alternate = DATA_DIR / filename.replace("_safety_scores.csv", "_scores.csv")
    if alternate.exists():
        return alternate

    return primary

@st.cache_data
def load_data():
    dfs = []
    bot_dfs = {}
    for bot_name, filename in BOT_FILES.items():
        filepath = _resolve_bot_filepath(filename)
        if not filepath.exists():
            raise FileNotFoundError(
                f"Missing file: {filepath}. "
                f"Please place all 5 scored safety CSV files in the data/ folder."
            )
        df = pd.read_csv(filepath)
        df["bot"] = bot_name
        for col in OPTIONAL_TEXT_COLUMNS:
            if col not in df.columns:
                df[col] = ""
        bot_dfs[bot_name] = df
        dfs.append(df)
    combined = pd.concat(dfs, ignore_index=True)
    for col in OPTIONAL_TEXT_COLUMNS:
        if col not in combined.columns:
            combined[col] = ""
    return combined, bot_dfs

load_scored_data = load_data
