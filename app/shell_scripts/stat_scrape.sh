#!/bin/bash

cd /stat_scrape
PATH=$PATH:/stat_scrape
export PATH
scrapy crawl ufcstatspider