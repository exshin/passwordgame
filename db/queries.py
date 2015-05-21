#!/usr/bin/python27
#-*- coding: utf-8 -*-


sql_profiles = """
WITH s AS (
SELECT DISTINCT
	p.id
	,p.first_name || ' ' || p.last_name candidate_name
	,op.presence_url
	,p.created_at
	,p.last_scrape_update_date
	,MAX(app.created_at) max_app_date
FROM
	people p
	INNER JOIN online_presences op
	ON p.id = op.reference_id AND op.reference_type = 'Person' AND op.online_presence_type_id = 1
	LEFT JOIN employments e
	ON e.person_id = p.id AND e.display_order = 1
	LEFT JOIN applications app
	ON app.person_id = p.id
WHERE
	p.last_scrape_update_date IS NULL
	AND
	p.function_type_id = 1
	AND
	(e.title ilike '%%dir%%' OR e.title ilike '%%vp%%')
	AND
	(p.state_abbreviation = 'CA' OR p.state_abbreviation IS NULL)
	AND
	app.created_at IS NOT NULL
	AND
	p.id NOT IN %s
GROUP BY
	p.id
	,p.first_name
	,p.last_name
	,op.presence_url
	,p.created_at
ORDER BY
	MAX(app.created_at) desc
LIMIT 25
)
SELECT DISTINCT
	s.*
	,row_number() OVER (ORDER BY s.id) AS rownum
FROM
	s
ORDER BY
	s.id
"""

sql_insert_served_candidates = """
INSERT INTO riviclick_candidates (person_id,user_email,served_date)
SELECT %s,%s,current_date
WHERE
	NOT EXISTS (
		SELECT id FROM riviclick_candidates WHERE person_id = %s
	)
"""

sql_get_served_candidates = """
SELECT DISTINCT
	person_id
FROM
	riviclick_candidates
"""

sql_get_viewed_candidates = """
WITH data AS (
SELECT DISTINCT
  DATE_TRUNC('week',served_date) wk, person_id
FROM riviclick_candidates
WHERE user_email = %s )
SELECT wk::date, COUNT(DISTINCT person_id) COUNTS
FROM data
GROUP BY wk
ORDER BY wk ASC
"""