--
-- PostgreSQL View
--

CREATE VIEW count_table AS
SELECT date(time), count(status) FILTER (WHERE status!='200 OK') AS nfcount, count(time) AS total_request
FROM log
GROUP BY date(time)