# T20 World Cup Analytics Dashboard Project

A complete end-to-end cricket analytics project focused on **ICC T20 World Cup match data**, built with **Python + SQL + Power BI-ready outputs**.

---

## 1) Project Goals

This project helps you:
- Clean and standardize T20 World Cup match data.
- Perform exploratory data analysis (EDA).
- Generate key insights:
  - Top teams
  - Top players
  - Win percentage by team
  - Match and scoring trends
- Export cleaned data for Power BI.
- Use SQL queries for analytical reporting.
- Build a professional-level Power BI dashboard with key KPIs.

---

## 2) Tech Stack

- **Python 3.10+**
- **pandas** (data processing)
- **matplotlib** + **seaborn** (data visualization)
- **SQL** (analysis queries)
- **Power BI** (dashboarding)

---

## 3) Folder Structure

```text
.
├── data/
│   ├── raw/
│   │   └── t20_world_cup_matches.csv
│   └── processed/
│       └── t20_world_cup_cleaned.csv (generated)
├── outputs/
│   ├── kpis.json (generated)
│   ├── top_teams.csv (generated)
│   ├── top_players.csv (generated)
│   ├── win_percentage.csv (generated)
│   ├── match_trends.csv (generated)
│   └── plots/
│       ├── top_teams_wins.png
│       ├── top_players_awards.png
│       └── match_trends.png
├── sql/
│   └── analysis_queries.sql
├── src/
│   └── t20_analytics.py
├── requirements.txt
└── README.md
```

---

## 4) Dataset Schema

Input file: `data/raw/t20_world_cup_matches.csv`

Expected columns:
- `match_id`
- `date`
- `stage`
- `venue`
- `team1`
- `team2`
- `team1_runs`
- `team2_runs`
- `winner`
- `margin_runs`
- `margin_wickets`
- `player_of_match`
- `toss_winner`
- `toss_decision`

---

## 5) Step-by-Step Instructions

### Step 1: Clone and enter project
```bash
git clone <your-repo-url>
cd -t20-worldcup-analytics-dashboard
```

### Step 2: Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate          # Windows PowerShell
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run analytics pipeline
```bash
python src/t20_analytics.py
```

### Step 5: Validate generated outputs
After running the script, verify:
- `data/processed/t20_world_cup_cleaned.csv`
- `outputs/kpis.json`
- `outputs/*.csv`
- `outputs/plots/*.png`

### Step 6: Load into Power BI
In Power BI Desktop:
1. **Get Data → Text/CSV**.
2. Load `data/processed/t20_world_cup_cleaned.csv`.
3. Optionally load `outputs/top_teams.csv`, `outputs/top_players.csv`, and `outputs/win_percentage.csv`.
4. Build visuals according to the layout section below.

---

## 6) EDA and Insights Covered

The Python script performs:

1. **Data Cleaning**
   - Trims strings and handles missing values.
   - Parses date fields.
   - Converts numeric columns to proper numeric types.
   - Creates derived columns:
     - `total_runs`
     - `result_type`
     - `year`
     - `month`

2. **Core KPIs**
   - Total matches
   - Total runs
   - Top team (by wins)
   - Best player (by Player of the Match awards)

3. **EDA/Insights Tables**
   - Top teams by wins
   - Top players by awards
   - Team-wise win percentage
   - Monthly match and total run trends

4. **Visual Outputs**
   - Top teams bar chart
   - Top players bar chart
   - Monthly trends line chart

---

## 7) SQL Analysis Queries

See: `sql/analysis_queries.sql`

Included query sets:
1. Total matches + total runs
2. Top teams by wins
3. Top players by Player of the Match awards
4. Team win percentage
5. Monthly match trends
6. Toss impact on match result

---

## 8) Power BI Dashboard Layout (Professional)

### Page 1: Executive Summary
**Top KPI cards (header row):**
- Total Matches
- Total Runs
- Top Team
- Best Player

**Main visuals:**
- Clustered bar chart: Top 10 teams by wins
- Clustered bar chart: Top 10 players by awards
- Donut chart: Result type split (By Runs / By Wickets / No Result)

**Filters (right panel):**
- Year
- Stage
- Team
- Venue

---

### Page 2: Team Performance Deep Dive
- Table/matrix: Team, matches played, wins, win %
- Horizontal bar: Win percentage by team
- Stacked column: Team wins by tournament stage
- Slicer: Year, Team

---

### Page 3: Match Trends & Scoring
- Line chart: Matches per month
- Line chart: Total runs per month
- Scatter plot: Team1 runs vs Team2 runs
- Map visual: Matches by venue/country (if geodata available)

---

### Page 4: Toss & Match Outcome Analysis
- Pie/Donut: Toss winner won vs toss winner lost
- Bar chart: Toss decision (bat/field) vs win count
- Matrix: Toss winner, winner, match count

---

## 9) Recommended DAX Measures for Power BI

```DAX
Total Matches = COUNTROWS(t20_world_cup_cleaned)

Total Runs = SUM(t20_world_cup_cleaned[team1_runs]) + SUM(t20_world_cup_cleaned[team2_runs])

Top Team =
VAR TeamTable =
    SUMMARIZE(
        FILTER(t20_world_cup_cleaned, t20_world_cup_cleaned[winner] <> "No Result"),
        t20_world_cup_cleaned[winner],
        "Wins", COUNTROWS(t20_world_cup_cleaned)
    )
RETURN
    MAXX(TOPN(1, TeamTable, [Wins], DESC), t20_world_cup_cleaned[winner])

Best Player =
VAR PlayerTable =
    SUMMARIZE(
        FILTER(t20_world_cup_cleaned, NOT(ISBLANK(t20_world_cup_cleaned[player_of_match]))),
        t20_world_cup_cleaned[player_of_match],
        "Awards", COUNTROWS(t20_world_cup_cleaned)
    )
RETURN
    MAXX(TOPN(1, PlayerTable, [Awards], DESC), t20_world_cup_cleaned[player_of_match])
```

---

## 10) How to Replace with Your Full Dataset

1. Download a complete T20 World Cup dataset (CSV).
2. Replace file at: `data/raw/t20_world_cup_matches.csv`
3. Ensure required columns exist (or rename headers accordingly).
4. Re-run:
   ```bash
   python src/t20_analytics.py
   ```
5. Refresh Power BI dataset.

---

## 11) Example KPIs Produced

KPIs are exported in `outputs/kpis.json`:
- `total_matches`
- `total_runs`
- `top_team`
- `best_player`

---

## 12) Next Enhancements

- Add player-level batting and bowling datasets.
- Add advanced metrics (strike rate, economy, net run rate).
- Build prediction model for match outcome.
- Deploy dashboard + APIs using Streamlit/FastAPI.

---

## 13) License

This project is for educational and portfolio use. Add your preferred license (e.g., MIT) before public release.
