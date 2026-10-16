-- Kohli Centuries: SQL practice
-- Table: centuries
-- Columns: century_no, runs, not_out (1 = not out), against, batting_position,
--          innings (1 or 2 mostly, 3/4 are Tests), stadium, city,
--          ground (Home / Away / Neutral), match_date (YYYY-MM-DD), year,
--          result (Won / Lost / Drawn / Tied)
--
-- How to use: write your query under each question, run it, and note the answer.
-- Open the database with:  sqlite3 kohli.db   (or use DB Browser for SQLite)


-- ============ LEVEL 1: SELECT, WHERE, ORDER BY, COUNT ============

-- Q1. How many centuries are in the table?
-- (worked example)
SELECT COUNT(*) AS total_centuries FROM centuries;

-- Q2. What is his highest score, and against whom and when?
-- Hint: ORDER BY ... DESC LIMIT 1


-- Q3. List all centuries against Australia, latest first.


-- Q4. How many centuries were not out?


-- Q5. How many scores were 150 or more?



-- ============ LEVEL 2: GROUP BY, HAVING, AVG, SUM ============

-- Q6. Centuries per opponent, highest first.


-- Q7. Centuries per year.


-- Q8. How many centuries at Home, Away and Neutral venues?


-- Q9. Average century score per opponent, only for opponents with 3+ centuries.
-- Hint: HAVING


-- Q10. In what percentage of matches did India win when he scored a century?
-- Hint: AVG(CASE WHEN result = 'Won' THEN 1.0 ELSE 0 END) * 100


-- Q11. Win percentage at Home vs Away vs Neutral.


-- Q12. Centuries by batting position.



-- ============ LEVEL 3: CASE, subqueries, window functions ============

-- Q13. Compare innings 1 and innings 2: number of centuries, average score, win %.


-- Q14. Top 5 cities by number of centuries, with total runs scored there.


-- Q15. Which opponent has the highest win % in his centuries (min 5 centuries)?


-- Q16. Running total of centuries year by year.
-- Hint: SUM(...) OVER (ORDER BY year)


-- Q17. Rank the years by total runs scored in centuries.
-- Hint: RANK() OVER (ORDER BY ... DESC)


-- Q18. Longest gap (in days) between two consecutive centuries.
-- Hint: LAG(match_date) OVER (ORDER BY match_date), then julianday() to subtract dates
