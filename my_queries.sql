-- Kohli Centuries: all 18 queries solved
-- Table: centuries
-- Run one query at a time: select it with the mouse, then press Ctrl+Enter.


-- ============ LEVEL 1 ============

-- Q1. Total centuries
SELECT COUNT(*) AS total_centuries
FROM centuries;

-- Q2. Highest score, against whom and when
SELECT runs, against, match_date
FROM centuries
ORDER BY runs DESC
LIMIT 1;

-- Q3. All centuries against Australia, latest first
SELECT *
FROM centuries
WHERE against = 'Australia'
ORDER BY match_date DESC;

-- Q4. How many centuries were not out
SELECT COUNT(*) AS not_out_count
FROM centuries
WHERE not_out = 1;

-- Q5. How many scores were 150 or more
SELECT COUNT(*) AS scores_150_plus
FROM centuries
WHERE runs >= 150;


-- ============ LEVEL 2 ============

-- Q6. Centuries per opponent, highest first
SELECT against, COUNT(*) AS total
FROM centuries
GROUP BY against
ORDER BY total DESC, against;

-- Q7. Centuries per year
SELECT year, COUNT(*) AS total
FROM centuries
GROUP BY year
ORDER BY year;

-- Q8. Centuries at Home, Away and Neutral venues
SELECT ground, COUNT(*) AS total
FROM centuries
GROUP BY ground;

-- Q9. Average century score per opponent, only opponents with 3+ centuries
SELECT against, COUNT(*) AS total, ROUND(AVG(runs), 1) AS avg_runs
FROM centuries
GROUP BY against
HAVING COUNT(*) >= 3
ORDER BY avg_runs DESC;

-- Q10. Overall win percentage when he scored a century
SELECT ROUND(AVG(CASE WHEN result = 'Won' THEN 1.0 ELSE 0 END) * 100, 1) AS win_pct
FROM centuries;

-- Q11. Win percentage at Home vs Away vs Neutral
SELECT ground,
       COUNT(*) AS total,
       ROUND(AVG(CASE WHEN result = 'Won' THEN 1.0 ELSE 0 END) * 100, 1) AS win_pct
FROM centuries
GROUP BY ground;

-- Q12. Centuries by batting position
SELECT batting_position, COUNT(*) AS total
FROM centuries
GROUP BY batting_position
ORDER BY total DESC;


-- ============ LEVEL 3 ============

-- Q13. Innings 1 vs innings 2: count, average score, win %
SELECT innings,
       COUNT(*) AS total,
       ROUND(AVG(runs), 1) AS avg_runs,
       ROUND(AVG(CASE WHEN result = 'Won' THEN 1.0 ELSE 0 END) * 100, 1) AS win_pct
FROM centuries
WHERE innings IN (1, 2)
GROUP BY innings;

-- Q14. Top 5 cities by number of centuries, with total runs scored there
SELECT city, COUNT(*) AS total, SUM(runs) AS total_runs
FROM centuries
GROUP BY city
ORDER BY total DESC, total_runs DESC
LIMIT 5;

-- Q15. Opponent with the highest win % (min 5 centuries), top row is the answer
SELECT against,
       COUNT(*) AS total,
       ROUND(AVG(CASE WHEN result = 'Won' THEN 1.0 ELSE 0 END) * 100, 1) AS win_pct
FROM centuries
GROUP BY against
HAVING COUNT(*) >= 5
ORDER BY win_pct DESC;

-- Q16. Running total of centuries year by year
SELECT year,
       COUNT(*) AS yearly,
       SUM(COUNT(*)) OVER (ORDER BY year) AS running_total
FROM centuries
GROUP BY year
ORDER BY year;

-- Q17. Rank the years by total runs scored in centuries
SELECT year,
       SUM(runs) AS total_runs,
       RANK() OVER (ORDER BY SUM(runs) DESC) AS rnk
FROM centuries
GROUP BY year
ORDER BY rnk;

-- Q18. Longest gap (in days) between two consecutive centuries
WITH gaps AS (
    SELECT match_date,
           LAG(match_date) OVER (ORDER BY match_date) AS prev_date
    FROM centuries
)
SELECT prev_date,
       match_date,
       CAST(julianday(match_date) - julianday(prev_date) AS INTEGER) AS gap_days
FROM gaps
WHERE prev_date IS NOT NULL
ORDER BY gap_days DESC
LIMIT 1;


-- ============ LEVEL 4: FORMAT (needs the format column from the new load_data.py) ============

-- Q19. Centuries per format
SELECT format, COUNT(*) AS total
FROM centuries
GROUP BY format
ORDER BY total DESC;

-- Q20. Average score, 150+ scores and win % per format
SELECT format,
       COUNT(*) AS total,
       ROUND(AVG(runs), 1) AS avg_runs,
       SUM(CASE WHEN runs >= 150 THEN 1 ELSE 0 END) AS scores_150_plus,
       ROUND(AVG(CASE WHEN result = 'Won' THEN 1.0 ELSE 0 END) * 100, 1) AS win_pct
FROM centuries
GROUP BY format;

-- Q21. Each opponent split by format
SELECT against,
       SUM(CASE WHEN format = 'Test' THEN 1 ELSE 0 END) AS test,
       SUM(CASE WHEN format = 'ODI'  THEN 1 ELSE 0 END) AS odi,
       SUM(CASE WHEN format = 'T20I' THEN 1 ELSE 0 END) AS t20i,
       COUNT(*) AS total
FROM centuries
GROUP BY against
ORDER BY total DESC, against;

-- Q22. Innings 1 vs innings 2 for ODI only (chasing is only meaningful in ODIs)
SELECT innings,
       COUNT(*) AS total,
       ROUND(AVG(runs), 1) AS avg_runs,
       ROUND(AVG(CASE WHEN result = 'Won' THEN 1.0 ELSE 0 END) * 100, 1) AS win_pct
FROM centuries
WHERE format = 'ODI'
GROUP BY innings;
