-- 1) Total matches and total runs
SELECT
    COUNT(*) AS total_matches,
    SUM(team1_runs + team2_runs) AS total_runs
FROM t20_world_cup_cleaned;

-- 2) Top 5 teams by wins
SELECT
    winner AS team,
    COUNT(*) AS wins
FROM t20_world_cup_cleaned
WHERE winner <> 'No Result'
GROUP BY winner
ORDER BY wins DESC
LIMIT 5;

-- 3) Top 10 players by Player of the Match awards
SELECT
    player_of_match,
    COUNT(*) AS awards
FROM t20_world_cup_cleaned
WHERE player_of_match IS NOT NULL
  AND player_of_match <> 'Unknown'
GROUP BY player_of_match
ORDER BY awards DESC
LIMIT 10;

-- 4) Team-wise win percentage
WITH matches_played AS (
    SELECT team1 AS team, COUNT(*) AS played FROM t20_world_cup_cleaned GROUP BY team1
    UNION ALL
    SELECT team2 AS team, COUNT(*) AS played FROM t20_world_cup_cleaned GROUP BY team2
),
played_agg AS (
    SELECT team, SUM(played) AS matches_played
    FROM matches_played
    GROUP BY team
),
wins AS (
    SELECT winner AS team, COUNT(*) AS wins
    FROM t20_world_cup_cleaned
    WHERE winner <> 'No Result'
    GROUP BY winner
)
SELECT
    p.team,
    p.matches_played,
    COALESCE(w.wins, 0) AS wins,
    ROUND((COALESCE(w.wins, 0) * 100.0) / p.matches_played, 2) AS win_percentage
FROM played_agg p
LEFT JOIN wins w ON p.team = w.team
ORDER BY win_percentage DESC;

-- 5) Monthly match trends
SELECT
    DATE_TRUNC('month', date) AS month,
    COUNT(*) AS matches,
    SUM(team1_runs + team2_runs) AS total_runs
FROM t20_world_cup_cleaned
GROUP BY DATE_TRUNC('month', date)
ORDER BY month;

-- 6) Toss impact analysis
SELECT
    CASE WHEN toss_winner = winner THEN 'Toss winner won' ELSE 'Toss winner lost' END AS toss_impact,
    COUNT(*) AS matches
FROM t20_world_cup_cleaned
WHERE winner <> 'No Result'
GROUP BY 1
ORDER BY matches DESC;
