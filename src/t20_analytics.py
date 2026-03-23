from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


@dataclass
class Paths:
    raw_data: Path = Path("data/raw/t20_world_cup_matches.csv")
    processed_data: Path = Path("data/processed/t20_world_cup_cleaned.csv")
    outputs_dir: Path = Path("outputs")
    plots_dir: Path = Path("outputs/plots")


EXPECTED_COLUMNS = [
    "match_id",
    "date",
    "stage",
    "venue",
    "team1",
    "team2",
    "team1_runs",
    "team2_runs",
    "winner",
    "margin_runs",
    "margin_wickets",
    "player_of_match",
    "toss_winner",
    "toss_decision",
]


def ensure_directories(paths: Paths) -> None:
    paths.processed_data.parent.mkdir(parents=True, exist_ok=True)
    paths.outputs_dir.mkdir(parents=True, exist_ok=True)
    paths.plots_dir.mkdir(parents=True, exist_ok=True)


def load_data(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    missing_columns = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    text_columns = [
        "stage",
        "venue",
        "team1",
        "team2",
        "winner",
        "player_of_match",
        "toss_winner",
        "toss_decision",
    ]
    for column in text_columns:
        cleaned[column] = cleaned[column].fillna("Unknown").astype(str).str.strip()

    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")

    numeric_columns = ["team1_runs", "team2_runs", "margin_runs", "margin_wickets"]
    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce").fillna(0)

    cleaned["total_runs"] = cleaned["team1_runs"] + cleaned["team2_runs"]
    cleaned["result_type"] = cleaned.apply(
        lambda row: "No Result"
        if row["winner"] == "No Result"
        else ("By Runs" if row["margin_runs"] > 0 else "By Wickets"),
        axis=1,
    )
    cleaned["year"] = cleaned["date"].dt.year
    cleaned["month"] = cleaned["date"].dt.to_period("M").astype(str)

    return cleaned.sort_values("date").reset_index(drop=True)


def team_matches_played(df: pd.DataFrame) -> pd.Series:
    team1_counts = df["team1"].value_counts()
    team2_counts = df["team2"].value_counts()
    return team1_counts.add(team2_counts, fill_value=0)


def build_kpis(df: pd.DataFrame) -> dict:
    valid_matches = df[df["winner"] != "No Result"]
    top_team = valid_matches["winner"].value_counts().idxmax()
    best_player = (
        valid_matches[valid_matches["player_of_match"] != "Unknown"]["player_of_match"]
        .value_counts()
        .idxmax()
    )

    return {
        "total_matches": int(df.shape[0]),
        "total_runs": int(df["total_runs"].sum()),
        "top_team": top_team,
        "best_player": best_player,
    }


def build_insights(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    valid_matches = df[df["winner"] != "No Result"]

    top_teams = (
        valid_matches["winner"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "team", "winner": "wins"})
        .head(10)
    )

    top_players = (
        valid_matches[valid_matches["player_of_match"] != "Unknown"]["player_of_match"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "player", "player_of_match": "awards"})
        .head(10)
    )

    matches_played = team_matches_played(df)
    wins = valid_matches["winner"].value_counts()
    win_percentage = (
        pd.DataFrame({"matches": matches_played, "wins": wins})
        .fillna(0)
        .assign(win_pct=lambda d: (d["wins"] / d["matches"] * 100).round(2))
        .sort_values("win_pct", ascending=False)
        .reset_index(names="team")
    )

    match_trends = (
        df.groupby("month", as_index=False)
        .agg(matches=("match_id", "count"), total_runs=("total_runs", "sum"))
        .sort_values("month")
    )

    return {
        "top_teams": top_teams,
        "top_players": top_players,
        "win_percentage": win_percentage,
        "match_trends": match_trends,
    }


def save_tables(tables: dict[str, pd.DataFrame], outputs_dir: Path) -> None:
    for name, frame in tables.items():
        frame.to_csv(outputs_dir / f"{name}.csv", index=False)


def create_visualizations(tables: dict[str, pd.DataFrame], plots_dir: Path) -> None:
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 5))
    sns.barplot(data=tables["top_teams"], x="team", y="wins", palette="Blues_d")
    plt.title("Top Teams by Wins")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(plots_dir / "top_teams_wins.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.barplot(data=tables["top_players"], x="player", y="awards", palette="Greens_d")
    plt.title("Top Players by Player of the Match Awards")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(plots_dir / "top_players_awards.png", dpi=300)
    plt.close()

    plt.figure(figsize=(12, 5))
    sns.lineplot(data=tables["match_trends"], x="month", y="matches", marker="o", label="Matches")
    sns.lineplot(data=tables["match_trends"], x="month", y="total_runs", marker="o", label="Total Runs")
    plt.title("Monthly Match and Run Trends")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(plots_dir / "match_trends.png", dpi=300)
    plt.close()


def save_kpis(kpis: dict, outputs_dir: Path) -> None:
    with (outputs_dir / "kpis.json").open("w", encoding="utf-8") as file:
        json.dump(kpis, file, indent=2)


def run_pipeline(paths: Paths) -> None:
    ensure_directories(paths)

    raw_df = load_data(paths.raw_data)
    cleaned_df = clean_data(raw_df)
    cleaned_df.to_csv(paths.processed_data, index=False)

    kpis = build_kpis(cleaned_df)
    insights = build_insights(cleaned_df)

    save_kpis(kpis, paths.outputs_dir)
    save_tables(insights, paths.outputs_dir)
    create_visualizations(insights, paths.plots_dir)

    print("Pipeline completed successfully.")
    print(f"Cleaned data exported: {paths.processed_data}")
    print(f"KPI summary: {kpis}")


if __name__ == "__main__":
    run_pipeline(Paths())
