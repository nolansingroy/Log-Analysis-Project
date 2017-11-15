# Log-Analysis-Project

#Question 1:  What are the top 3 articles within the newsdata.sql data?
Solution # 1:

```psql
create view popular_3_articles as select title,count(*) as views from articles join log on log.path like concat('%',articles.slug, '%') group by articles.title order by views desc limit 3;
```

#Question2: Given newsdata.sql, what are the most popular authors?
```psql
create view pop_authors_named as select authors.name,count(*) as requested_views from articles join authors on articles.author = authors.id inner join log on log.path::text like '%'||articles.slug::text where status = '200 OK'group by authors.name order by requested_views desc;
```

#Question3:On which days did more than 1% lead to errors?
```psql
create view error_requests as select date_trunc('day', time), count(*) as Failed_Requests from log where status != '200 OK' group by date_trunc('day', time) order by Failed_Requests desc;
```
#Question3.1:
```psql
create view total_requests as select date_trunc('day', time), count(*) as tot_requests from log group by date_trunc('day',time) order by tot_requests desc;
```
#Question3.2:
```psql
create view percent_error as select total_requests.date_trunc, (100*error_requests.failed_requests/total_requests.tot_requests) as percentage from total_requests,error_requests where total_requests.date_trunc = error_requests.date_trunc order by total_requests.date_trunc;
```
#Question3.3:
```psql
create view error_day as select percent_error.date_trunc as day, percent_error.percentage as percent from percent_error where percent_error.percentage > 1;
```
##Results

Solution#1:
 popular 3 articles

 Candidate is jerk, alleges rival - 342102 views
 Bears love berries, alleges bear - 256365 views
 Bad things gone, say good people - 171762 views

Solution2:
Most Popular Authors

 Ursula La Multa - 507594 views
 Rudolf von Treppenwitz - 423457 views
 Anonymous Contributor - 170098 views
 Markoff Chaney - 84557 views

Solution3:
The day that 404 requests were greater then 1%

2016-07-17 00:00:00+00:00 -- 2%
