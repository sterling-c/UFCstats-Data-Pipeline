SELECT stance, COUNT(*)
FROM fighters 
GROUP BY stance
HAVING stance IS NOT NULL