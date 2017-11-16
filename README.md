# Log-Analysis-Project

#Description
 The objective is to generate a report from the data newsdata.sql to answer 3 questions as follows.
 1. What are the most popular three articles of all time?
 2. Who are the most popular article authors of all time?
 3. On which days did more than 1% of requests lead to errors?
#Requirements
* [Virtualbox](https://www.virtualbox.org/)
* [Vigrant](https://www.vagrantup.com/)
* [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)
* [newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
* [Log-analysis](https://github.com/nolansingroy/Log-Analysis-Project) - import to run the project files and run loganalysis.py to generate the report.
# Steps
 * copy and paste the create views below to recreate the tables
#Navigating around the Data
## commands
* vagrant up
* vagrant ssh
* psql -d news -f newsdata.sql - to import the database
* psql -d news - to connect to the database
* cd into the vagrant directory and use psql -d news -f newsdata.sql
* \dt - to display tables
* \d table (replacing table with the corresponding table name) - shows the database schema for that table
* select * from table - to view the specific view from within pqsl

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
# Notes
  datetunc() function [resource](https://w3resource.com/PostgreSQL/date_trunc-function.php)
  strftime() function [resource](https://docs.python.org/2/library/time.html)
  [Udacity Log Analysis FAQ](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/b2ff9cba-210e-463e-9321-2605f65491a9)
