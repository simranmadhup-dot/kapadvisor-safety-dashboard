"""Issue and query-type detection helpers."""

from __future__ import annotations

import json
from typing import Dict, List

import pandas as pd

from config import AUTHORIZATION_CATEGORY_MAP, COMMON_ISSUES


QUERY_TYPE_RULES = {
    "College fit / school list": r"school|college|university|list|fit|apply|where",
    "Admission chances": r"chances|odds|probability|acceptance|likely",
    "Test prep advice": r"sat|act|score|prep|practice|improve",
    "Essay feedback": r"essay|write|prompt|topic|draft",
    "Transcript / GPA": r"transcript|gpa|grade|course|rigor",
}


def categorize_authorization(raw_text: str) -> str:
    return AUTHORIZATION_CATEGORY_MAP(raw_text)


def parse_conversation_history(raw_text):
    """Parse the conversation_history JSON string into a list of role/content dicts."""
    if not isinstance(raw_text, str) or not raw_text.strip():
        return []
    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, list):
            return [
                {"role": item.get("role", ""), "content": item.get("content", "")}
                for item in parsed
                if isinstance(item, dict)
            ]
    except (json.JSONDecodeError, TypeError):
        pass
    return []


def assign_query_category(df: pd.DataFrame) -> pd.Series:
    """Assign query category based on use_case or user_input keywords."""
    use_case = df.get("use_case", pd.Series(index=df.index, dtype=str)).fillna("")
    user_input = df.get("user_input", pd.Series(index=df.index, dtype=str)).fillna("")

    base = use_case.where(use_case.str.strip() != "", user_input)
    base = base.fillna("").str.lower()

    category = pd.Series("General information", index=df.index)
    for name, pattern in QUERY_TYPE_RULES.items():
        mask = base.str.contains(pattern, regex=True)
        category = category.mask(mask, name)

    return category


def build_query_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create query type analysis table with flag rates and score distribution."""
    working = df.copy()
    working["query_category"] = assign_query_category(working)

    grouped = working.groupby("query_category", as_index=False).agg(
        total_rows=("safety_score", "count"),
        flagged=("safety_score", lambda x: (x <= 2).sum()),
    )

    grouped["flag_rate_pct"] = (grouped["flagged"] / grouped["total_rows"] * 100).round(1)

    score_mode = (
        working.groupby("query_category")["safety_score"]
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        .reset_index(name="most_common_score")
    )
    merged = grouped.merge(score_mode, on="query_category", how="left")
    merged = merged.sort_values("flag_rate_pct", ascending=False).reset_index(drop=True)

    merged = merged.rename(
        columns={
            "query_category": "Category",
            "total_rows": "Total Rows",
            "flagged": "Flagged (1-2)",
            "flag_rate_pct": "Flag Rate %",
            "most_common_score": "Most Common Safety Score",
        }
    )
    return merged


def detect_common_issues(df: pd.DataFrame) -> List[Dict]:
    """Run issue detection functions and return issue-level result metadata."""
    results: List[Dict] = []

    for issue in COMMON_ISSUES:
        matches = issue["detection_fn"](df).copy()
        matches = matches.sort_values("safety_score", ascending=True)
        results.append(
            {
                "id": issue["id"],
                "title": issue["title"],
                "severity": issue["severity"],
                "color": issue["color"],
                "icon": issue["icon"],
                "bots_affected": issue["bots_affected"],
                "what_is_happening": issue["what_is_happening"],
                "why_it_matters": issue["why_it_matters"],
                "root_cause": issue["root_cause"],
                "recommended_fix": issue["recommended_fix"],
                "matched_df": matches,
                "count": len(matches),
            }
        )

    return results
