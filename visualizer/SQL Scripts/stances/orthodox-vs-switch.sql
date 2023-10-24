SELECT (CASE
	   WHEN (fr1.stance = 'Orthodox' AND fr2.stance = 'Switch') OR (fr1.stance = 'Switch' AND fr2.stance = 'Orthodox') THEN 'Orthodox vs Switch' 
		END) as stance_matchup,
		SUM(CASE
		WHEN (fr1.id = f.winner_id) AND (fr1.stance = 'Orthodox') THEN 1
		WHEN (fr2.id = f.winner_id) AND (fr2.stance = 'Orthodox') THEN 1
		END) as orthodox_wins,
		SUM(CASE
		WHEN (fr1.id = f.winner_id) AND (fr1.stance = 'Switch') THEN 1
		WHEN (fr2.id = f.winner_id) AND (fr2.stance = 'Switch') THEN 1
		END) as switch_wins,
		SUM(CASE
		   WHEN f.winner_id IS NULL THEN 1
		   END) as inconclusive_results
FROM fights f
INNER JOIN fighters fr1
ON f.red_id = fr1.id
INNER JOIN fighters fr2 
ON f.blue_id = fr2.id
WHERE (CASE
	   WHEN (fr1.stance = 'Orthodox' AND fr2.stance = 'Switch') OR (fr1.stance = 'Switch' AND fr2.stance = 'Orthodox') THEN 'Orthodox vs Switch' 
		END) IS NOT NULL
GROUP BY stance_matchup