#!/usr/bin/env python3

import psycopg2

# Question 1: What are the most popular three articles of all time?
question1 = """
SELECT articles.title, count(*) as logs
from articles
inner join log
ON log.path like concat('/article/', articles.slug)
GROUP BY articles.title
ORDER BY logs DESC
LIMIT 3;
"""

# Question 2: Who are the most popular article authors of all time?
question2 = """
SELECT authors.name, count(*) as logs
from articles
inner join authors on articles.author = authors.id
inner join log on concat('/article/', articles.slug) = log.path
where log.status like '%200%'
GROUP BY authors.name
ORDER BY logs DESC
LIMIT 3;
"""

# Question 3: On which days did more than 1% of requests lead to errors

question3 = """
SELECT day, dailyrate
FROM errorpercentages
WHERE dailyrate > 1;
"""


# Get Started connecting to the DB and
# processing the SQL queries defined above.
def executeQuery(query):
    try:
        db = psycopg2.connect('dbname=news')
        c = db.cursor()
        c.execute(query)
        rows = c.fetchall()
        db.close()
        return rows
    except:
        print('Could Not Connect')

# process each of the questions and store as a result
result1 = executeQuery(question1)
result2 = executeQuery(question2)
result3 = executeQuery(question3)


def prepcontent(sqlresults):
    for i in range(len(sqlresults)):
        label = sqlresults[i][0]
        value = sqlresults[i][1]
        print("%s--%d" % (label, value))

print (
       "1. What are the most popular three "
       "articles of all time? (article name--logs)")
prepcontent(result1)
print (
       "2. Who are the most popular article "
       "authors of all time? (author name--logs)")
prepcontent(result2)
print (
       "3. On which days did more than 1% of requests "
       "lead to errors? (date--percentage errors)")
prepcontent(result3)
