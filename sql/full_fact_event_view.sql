CREATE VIEW full_fact_event AS
WITH city_add AS (
  SELECT city.city_name, fact.*
FROM fact_event as fact
LEFT JOIN dim_city as city
ON fact.city_id = city.city_id
),
date_add AS (
  SELECT date.full_datetime, ca.*
FROM city_add as ca
LEFT JOIN dim_date as date
ON ca.date_id = date.date_id
)
SELECT da.event_id, da.city_name, da.full_datetime, w.weather_name, da.temperature, da.pressure, da.humidity, da.wind_speed
FROM date_add as da
LEFT JOIN dim_weather as w
ON da.weather_id = w.weather_id;

CREATE VIEW columbia_events AS
  SELECT * FROM full_fact_event WHERE city_name = 'Columbia';

CREATE VIEW kansas_city_events AS
  SELECT * FROM full_fact_event WHERE city_name = 'Kansas City';

CREATE VIEW jefferson_city_events AS
  SELECT * FROM full_fact_event WHERE city_name = 'Jefferson City';

CREATE VIEW springfield_events AS
  SELECT * FROM full_fact_event WHERE city_name = 'Springfield';

CREATE VIEW st_louis_events AS
  SELECT * FROM full_fact_event WHERE city_name = 'St Louis';