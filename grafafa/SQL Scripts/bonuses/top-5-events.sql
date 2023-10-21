SELECT e.name,  TO_CHAR(e.date,'mm/dd/yyyy') date, (COUNT(CASE WHEN f.perf_bonus THEN 1 END) + COUNT(CASE WHEN f.fight_bonus THEN 1 END)) as total_bonuses
FROM events as e
JOIN fights as f
ON  e.id = f.event_id
GROUP BY e.name, e.date
ORDER BY total_bonuses desc
LIMIT 5