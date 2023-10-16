# ufcstats.com-Data-Pipeline

This program is a fully dockerized application consisting of a Scrapy project and a Postgres database that scrapes and extracts data from the Ultimate Fighting Championship's dedicated website for statistics, ufcstats.com.

## PRE-REQUISITES
* At least Python 3.10 is necessary
* Docker must be installed and accessible from the command line. Desktop application is recommended. \
  
## INSTALLATION

Create the following environment variables (creating an environment file like ".env" is highly recommended):

1. POSTGRES_DB = The name you would like to give the database
2. POSTGRES_USER = The name of the user that will be created
3. POSTGRES_PASSWORD = The password of the created user
4. POSTGRES_HOST = This should always be set to 'db' as the virtual network docker creates all services recognizable to each other by their service name. DO NOT use 'localhost'.
5. POSTGRES_PORT = The port that the Postgres database will be listening from and the Scrapy project will connect to for the database connection.
6. PGADMIN_DEFAULT_EMAIL = The email used to log in to PGadmin
7. PGADMIN_DEFAULT_PASSWORD = The password used to login to PGadmin

From the root of the project directory, enter from the command line:
```
docker-compose up
```

## USAGE

This pipeline is configured through crontab to execute the pipeline every week on Sunday past midnight. You can amend the schedule to your liking by changing the cron schedule, or if you would like to execute the pipeline manually:
```
cd $PATH/TO/stat_scrape
scrapy crawl ufcstatspider
```
