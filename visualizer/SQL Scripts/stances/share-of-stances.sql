SELECT stance, COUNT(*)
FROM fighters 
GROUP BY stance
HAVING stance IS NOT NULL

-- For Stance Dashboard
-- Visualization: Pie Chart
-- Show: All Values
-- Piechart Type: Pie
-- Legend Visibility: On
-- Legend Position: Right
-- Legend Mode: Table
-- Color Palette: Classic