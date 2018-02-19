# scrapy-test
a simple crawler by modifying scrapy tutorial

Most of the files were created by downloading scrapy from

A few files were created(C) or modified(M) as follows:
M  tutorial/spiders/bhrc.py - spider to crawl BHRRC site for labeled
                              artiles.

M  tutorial/pipelines.py - prepare the data scraped by bhrc.py for input
                           to FastText - remove HTML markup, non-ascii 
                           characters, insert default label, all text in
                           lowercase etc. 

C  tutorial/exporters.py - to export scrapped data to a text file 
                           that can be readily consumed by FastText.

M  tutorial/settings.py


Usage
-----
- run 'scrapy crawl bhrc' to 

How to use fasttext with data from BHRRC site:
- copy 
