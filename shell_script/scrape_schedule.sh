#!/bin/bash

cd /app/ufcstats-Data-Pipeline/ufcstats-Data-Pipeline/stat_scrape
PATH=$PATH:/app/ufcstats-Data-Pipeline/ufcstats-Data-Pipeline/stat_scrape
export PATH
scrapy crawl ufcstatspider