"""Chart utilities for the Streamlit dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import SAFETY_COLORS, SAFETY_LABELS


def score_distribution_bar(df: pd.DataFrame, bot_name: str | None = None) -> go.Figure:
    counts = (
        df["safety_score"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0).reset_index()
    )
    counts.columns = ["score", "count"]
    counts["label"] = counts["score"].map(SAFETY_LABELS)
    total = counts["count"].sum()
    counts["percent"] = (counts["count"] / total * 100).round(1)

    y_labels = counts["score"].apply(lambda x: f"Score {x}")
    fig = go.Figure(
        data=[
            go.Bar(
                x=counts["count"],
                y=y_labels,
                orientation="h",
                text=counts["count"],
                textposition="outside",
                marker_color=[SAFETY_COLORS[s] for s in counts["score"]],
                width=0.72,
                customdata=counts[["label", "percent"]].values,
            )
        ]
    )
    fig.update_traces(
        hovertemplate="%{y}<br>Count: %{x}<br>Label: %{customdata[0]}<br>Percentage: %{customdata[1]}%<extra></extra>"
    )
    title_text = (
        f"Safety Score Distribution — {bot_name}<br><sup>Distribution of safety judge scores for selected bot responses</sup>"
        if bot_name
        else "Safety Score Distribution Across All Bots<br><sup>Distribution of safety judge scores across all evaluated responses</sup>"
    )

    fig.update_layout(
        title={
            "text": title_text,
            "font": {"size": 20},
        },
        xaxis_title="Count of Rows",
        yaxis_title="Score",
        showlegend=False,
        template="plotly_white",
        height=430,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="white",
        margin={"l": 30, "r": 20, "t": 80, "b": 30},
    )
    fig.update_xaxes(title_font={"size": 14}, tickfont={"size": 13})
    fig.update_yaxes(title_font={"size": 14}, tickfont={"size": 13})
    fig.update_yaxes(categoryorder="array", categoryarray=["Score 1", "Score 2", "Score 3", "Score 4", "Score 5"])
    return fig


def grouped_scores_by_bot(df: pd.DataFrame) -> go.Figure:
    grouped = (
        df.groupby(["bot", "safety_score"]).size().reset_index(name="count")
    )

    fig = go.Figure()
    for score in [1, 2, 3, 4, 5]:
        part = grouped[grouped["safety_score"] == score]
        fig.add_trace(
            go.Bar(
                x=part["bot"],
                y=part["count"],
                name=f"Score {score}",
                marker_color=SAFETY_COLORS[score],
                hovertemplate="Bot: %{x}<br>Count: %{y}<extra></extra>",
                width=0.16,
            )
        )

    fig.update_layout(
        barmode="group",
        template="plotly_white",
        title={
            "text": "Safety Score Count by Bot<br><sup>Each bar group shows how responses are distributed by safety score for each bot</sup>",
            "font": {"size": 20},
        },
        xaxis_title="Bot",
        yaxis_title="Rows",
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="white",
        margin={"l": 30, "r": 20, "t": 85, "b": 30},
    )
    fig.update_xaxes(title_font={"size": 14}, tickfont={"size": 13})
    fig.update_yaxes(title_font={"size": 14}, tickfont={"size": 13})
    return fig


def radar_score_profile(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    bot_palette = ["#2b6cb0", "#d97706", "#0f766e", "#7c3aed", "#be123c", "#334155"]

    for idx, (bot, bot_df) in enumerate(df.groupby("bot")):
        proportions = (
            bot_df["safety_score"].value_counts(normalize=True).reindex([1, 2, 3, 4, 5], fill_value=0)
        )
        categories = [f"Score {s}" for s in [1, 2, 3, 4, 5]]
        color = bot_palette[idx % len(bot_palette)]
        fill_color = f"rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:7], 16)},0.1)"

        fig.add_trace(
            go.Scatterpolar(
                r=proportions.values,
                theta=categories,
                fill="toself",
                name=bot,
                line={"width": 3, "color": color},
                fillcolor=fill_color,
                hovertemplate="%{theta}<br>Share: %{r:.1%}<extra></extra>",
            )
        )

    fig.update_layout(
        template="plotly_white",
        title="Bot Safety Score Profile (Radar)",
        polar={
            "radialaxis": {"visible": True, "ticksuffix": "%", "tickformat": ".0%", "tickfont": {"size": 12}},
            "angularaxis": {"tickfont": {"size": 13}},
        },
        height=500,
        width=500,
        margin={"l": 40, "r": 40, "t": 70, "b": 30},
    )
    return fig


def score_pie_for_bot(bot_df: pd.DataFrame, bot_name: str) -> go.Figure:
    counts = bot_df["safety_score"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
    mean_score = bot_df["safety_score"].mean()

    fig = go.Figure(
        data=[
            go.Pie(
                labels=[f"Score {s}" for s in counts.index],
                values=counts.values,
                marker_colors=[SAFETY_COLORS[s] for s in counts.index],
                hole=0.45,
                textinfo="percent+label",
            )
        ]
    )
    fig.update_layout(
        title=f"{bot_name} Safety Score Distribution",
        template="plotly_white",
        height=500,
        annotations=[
            {
                "text": f"Mean<br><b>{mean_score:.2f}</b>",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
                "font": {"size": 16, "color": "#1a2744"},
            }
        ],
    )
    return fig


def flag_rate_bar(query_summary: pd.DataFrame, title: str) -> go.Figure:
    fig = px.bar(
        query_summary,
        x="Flag Rate %",
        y="Category",
        orientation="h",
        color="Flag Rate %",
        color_continuous_scale="YlOrRd",
        text="Flag Rate %",
    )
    fig.update_layout(template="plotly_white", title=title, height=420, coloraxis_showscale=False)
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    return fig


def score_over_time_line(df: pd.DataFrame, timestamp_col: str, bot_name: str) -> go.Figure:
    tmp = df.copy()
    tmp[timestamp_col] = pd.to_datetime(tmp[timestamp_col], errors="coerce")
    tmp = tmp.dropna(subset=[timestamp_col])

    daily = (
        tmp.set_index(timestamp_col)
        .resample("D")["safety_score"]
        .mean()
        .reset_index(name="mean_score")
    )

    fig = px.line(
        daily,
        x=timestamp_col,
        y="mean_score",
        markers=True,
        title=f"{bot_name} Mean Safety Score Over Time",
        template="plotly_white",
    )
    fig.update_layout(height=360, yaxis_range=[0.7, 5.3], xaxis_title="Date", yaxis_title="Mean Score")
    return fig
