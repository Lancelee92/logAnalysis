#!/usr/bin/env python
#
# Database code for the News log database.

import psycopg2
import bleach
import datetime

DBNAME = "news"


def get_topArticle():
    """Return all posts from the 'database', most recent first."""
    articleQuery = """
                    select articles.title
                    as title, count(articles.title)
                    as views
                    from articles inner join log
                    on (log.path='/article/' || articles.slug )
                    group by title order by views
                    desc
                    limit 3
                   """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(articleQuery)
    posts = c.fetchall()
    db.close()
    return posts


def get_topAuthor():
    """Return all posts from the 'database', most recent first."""
    authorQuery = """
                  select authors.name as name, count(authors.name) as views
                  from authors right outer
                  join (articles inner join log
                  on (log.path='/article/'||articles.slug)) as ntable
                  on (authors.id=ntable.author)
                  group by name
                  order by views
                  desc
                  """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(authorQuery)
    posts = c.fetchall()
    db.close()
    return posts


def get_mostError():
    """Return all posts from the 'database', most recent first."""
    
    mostError = """
                select date,
                round( cast(float8 (nfcount*100::decimal)/total_request
                as numeric),2)
                as error_percentage
                from count_table
                where
                round( cast(float8 (nfcount*100::decimal)/total_request
                as numeric),2) > 1
                """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    c.execute(mostError)
    posts = c.fetchall()
    db.close()
    return posts

strViews = """%s -- %s views\n""" 

print('1. What are the most popular three articles of all time?')
print "--------------------------------------------------------"
print "".join(strViews % (title, views) for title, views in get_topArticle())

print('2. Who are the most popular article authors of all time?')
print "--------------------------------------------------------"
print "".join(strViews % (name, views) for name, views in get_topAuthor())

percentage = """%s -- %s%% errors"""

print('3. On which days did more than 1% of requests lead to errors?')
print "--------------------------------------------------------"
print "".join(percentage % ( date.strftime('%b %d,%Y'), error_percentage) for date, error_percentage in get_mostError())
print
