SELECT method, COUNT(*)
FROM fights
WHERE perf_bonus = True
GROUP BY method

-- For Stance Dashboard
-- Visualization: Pie Chart
-- Show: Calculated
-- Piechart Type: Pie
-- Legend Visibility: On
-- Legend Position: Right
-- Legend Mode: Table
-- Color Palette: Classic