WITH bonus_per_year AS
(SELECT e.name, DATE_PART('year', e.date) as year, (COUNT(CASE WHEN f.perf_bonus THEN 1 END) + COUNT(CASE WHEN f.fight_bonus THEN 1 END)) as total_bonuses
FROM events as e
JOIN fights as f
ON  e.id = f.event_id
GROUP BY e.name, e.date
ORDER BY total_bonuses desc
)

SELECT AVG(total_bonuses) as total_bonuses, year 
FROM bonus_per_year
GROUP BY year
HAVING YEAR != date_part('year', CURRENT_DATE)
ORDER BY year ASC

-- For Bonus Dashboard
-- Visualization: Bar Chart
-- X-Axis: Year