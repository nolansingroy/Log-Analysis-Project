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
#Solution3.1:
create view error_requests as select date_trunc('day', time), count(*) as Failed_Requests from log where status != '200 OK' group by date_trunc('day', time) order by Failed_Requests desc;
```
#Solution3.2:
```psql
create view total_requests as select date_trunc('day', time), count(*) as tot_requests from log group by date_trunc('day',time) order by tot_requests desc;
```
#Question3.3:
```psql
create view percent_error_test1 as select total_requests.date_trunc, Round(((error_requests.failed_requests*1.0)/total_requests.tot_requests),3) as percentage from total_requests,error_requests where total_requests.date_trunc = error_requests.date_trunc order by total_requests.date_trunc;
```
#Question3.4:
```psql
create view error_day_results as select percent_error_test1.date_trunc as day, percent_error_test1.percentage as percent from percent_error_test1 where percent_error_test1.percentage > 0.01;
```
##Results

#1: What are the top 3 articles in the database?

 Candidate is jerk, alleges rival - 342102 views
 Bears love berries, alleges bear - 256365 views
 Bad things gone, say good people - 171762 views

#2: Who are the most popular authors?

 Ursula La Multa - 507594 views
 Rudolf von Treppenwitz - 423457 views
 Anonymous Contributor - 170098 views
 Markoff Chaney - 84557 views

#3:The day that 404 requests were greater then 1%?

July 17, 2016---2.3% errors
