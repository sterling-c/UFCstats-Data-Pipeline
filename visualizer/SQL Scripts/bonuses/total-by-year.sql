SELECT SUM(total_bonuses) as total_bonuses, year 
FROM (SELECT e.name, DATE_PART('year', e.date) as year, (COUNT(CASE WHEN f.perf_bonus THEN 1 END) + COUNT(CASE WHEN f.fight_bonus THEN 1 END)) as total_bonuses
FROM events as e
JOIN fights as f
ON  e.id = f.event_id
GROUP BY e.name, e.date
ORDER BY total_bonuses desc
)
GROUP BY year
HAVING YEAR != date_part('year', CURRENT_DATE)
ORDER BY year ASC