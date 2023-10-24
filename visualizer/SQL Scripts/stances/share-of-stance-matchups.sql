SELECT (CASE
	   WHEN fr1.stance = 'Orthodox' AND fr1.stance = fr2.stance THEN 'Orthodox vs Orthodox'
	   WHEN (fr1.stance = 'Orthodox' AND fr2.stance = 'Southpaw') OR (fr1.stance = 'Southpaw' AND fr2.stance = 'Orthodox') THEN 'Orthodox vs Southpaw'
	   WHEN fr1.stance = 'Southpaw' AND fr1.stance = fr2.stance THEN 'Southpaw vs Southpaw'
	   WHEN fr1.stance = 'Switch' AND fr1.stance = fr2.stance THEN 'Switch vs Switch'
		WHEN (fr1.stance = 'Orthodox' AND fr2.stance = 'Switch') OR (fr1.stance = 'Switch' AND fr2.stance = 'Orthodox') THEN 'Orthodox vs Switch'
		WHEN (fr1.stance = 'Southpaw' AND fr2.stance = 'Switch') OR (fr1.stance = 'Switch' AND fr2.stance = 'Southpaw') THEN 'Southpaw vs Switch'
		WHEN fr1.stance IS NULL OR fr2.stance IS NULL THEN 'Unknown'
		END) as stance_matchup, COUNT(*)
FROM fights f
INNER JOIN fighters fr1
ON f.red_id = fr1.id
INNER JOIN fighters fr2 
ON f.blue_id = fr2.id
GROUP BY stance_matchup