#!/usr/bin/env python2

import psycopg2

DBNAME = "news"
def main(query):
	# connect to database
	connection = psycopg2.connect(database=DBNAME)
	c = connection.cursor()
	c.execute(query)
	results = c.fetchall()
	connection.close()
	return results

def pop_3_articles_print():
	print " popular 3 articles"
	print '--'
	query1 = """
		select popular_3_articles.title , popular_3_articles.views as views from 
		popular_3_articles order by popular_3_articles.views desc limit 3;
		"""
	popular_articles = main(query1)
	for (title, views) in popular_articles:
		print(" {} - {} views".format(title,views))
	print "\n"
def pop_authors_print():
	print "Most Popular Authors"
	query2 = """
		select pop_authors_named.name,pop_authors_named.requested_views as views from 
		pop_authors_named order by views desc;
		"""
	popular_authors = main(query2)
	for(name, views) in popular_authors:
		print(" {} - {} views".format(name, views))
	print "\n"
def error_day_print():
	print"The day that 404 requests were greater then 1%"
	query3 = """
		select day, percent from error_day;
		"""
	errorDay= main(query3)
	for(day,percent) in errorDay:
		print("{} -- {}%".format(day,percent))

if __name__ =="__main__":
	pop_3_articles_print() 
	pop_authors_print()
	error_day_print()
