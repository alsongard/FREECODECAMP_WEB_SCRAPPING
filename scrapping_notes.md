# TOPICS

1. 
2. Setting up scrapy
3. 
4. First scrapy spider
5. 
6. clearnin data
7. saving data to files and databases
8. faking scrapy headers and user-agents
9. rotating proxies and proxy APIS
10. deploying and scheduling spiders using scrapyd
11. deploying and scheduling spiders with scrapeops
12.



## setting up a project
``scrapy startproject bookscraper``


## 7 saving data 
- via command line  
``scrapy crawl bookspider -O bookData.csv``

appending data to a file
``scrapy crawl bookspider -o bookData.csv``

- via Feed setting
go to setting and add the following line:

```
FEEDS = {
    'booksdata.json' : {'format': 'json'}
}
```
After this run your spider and the file will be created, booksdata.json == filename, format == specifies the format === csv, json


To overide settings in setting file:
add :
```
customer_settings = {
    'FEEDS' : {
        'books_new_data' : {'format': 'csv'}
    }
}
```
in spiderfile.
- data into database

