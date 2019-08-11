#Introduction

This is the readme file for Udacity Logs Analysis Project

## Set up vagrant
1. Go [virtualbox.org](https://www.virtualbox.org)
2. Download and install virtualbox for your operating systems
3. Go [vagrantup.com](https://www.vagrantup.com/downloads.html)
4. Download and install for your operating systems
5. Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)
6. Change directory to vagrant folder
7. Run this code to start vagrant

   `` $ vagrant up ``   
   `` $ vagrant ssh ``  

##Getting Started

1. Open logAnalysis folder

2. Run `` psql -d news -f newsdata.sql `` in terminal to connect to the news database and run newsdata.sql

3. Run `` python newsdb.py `` to setup news database query
   - Result of the query should appear in the terminal after this

4. Run `` python logAnalysis `` to Run the site

5. Browse the site at [http://0.0.0.0:8000/](http://0.0.0.0:8000/)

##Question 1 (Top Article)
[Top Article Link](http://0.0.0.0:8000/topArticle)

```
select articles.title as title, count(articles.title) as views        
from articles inner join log on (log.path='/article/'||articles.slug)            
group by title        
order by views           
desc     
limit 3;     
```

##Question 2 (Top Author)
[Top Author Link](http://0.0.0.0:8000/topAuthor)

```
select authors.name as name, count(authors.name) as views  
from authors right outer join (articles inner join log on (log.path='/article/'||articles.slug)) as ntable  
on (authors.id=ntable.author)  
group by name  
order by views  
desc;
```

##Question 3 (On which days did more than 1% of requests lead to errors? )
[Most Errors Link](http://0.0.0.0:8000/mostError)

1. Create a view to organize the data
```
create view count_table  
 as select date(time), count(status)  
 filter (where status='404 NOT FOUND') as nfcount,  
 count(time) as total_request  
 from log  
 group by date(time);
```

2. Get the result by entering this code
```
select date,  
 round( cast(float8 (nfcount*100::decimal)/total_request as numeric),2) as error_percentage  
 from count_table  
 where round( cast(float8 (nfcount*100::decimal)/total_request as numeric),2) > 1

```
