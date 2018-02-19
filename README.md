# scrapy-test
a simple crawler by modifying scrapy tutorial

Downloads and links
-------------------
- scrapy crawler
    pip install scrapy

- scrapy tutorial: Follow the instructions at 
    https://docs.scrapy.org/en/latest/intro/tutorial.html

- fasttext - instructions to download and build
    https://fasttext.cc/docs/en/support.html

- fasttext tutorial (highly recommended to quickly learn fasttext)
    https://fasttext.cc/docs/en/supervised-tutorial.html

- 300 dimensional English word vector for fasttext
    https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki-news-300d-1M-subword.vec.zip

- Other English word vectors:
     https://fasttext.cc/docs/en/english-vectors.html

Changes to scrapy tutorial
--------------------------


Following files in scrapy tutorial directory and its subdirectories were 
created(C) or modified(M) as follows:
M  tutorial/spiders/bhrrc.py - spider to crawl BHRRC site for labeled
                              artiles.

M  tutorial/pipelines.py - prepare the data scraped by bhrrc.py for input
                           to FastText - remove HTML markup, non-ascii 
                           characters, insert default label, all text in
                           lowercase etc. 

C  tutorial/exporters.py - to export scrapped data to a text file 
                           that can be readily consumed by FastText.

M  tutorial/settings.py


Usage
-----
- cd to the root directory of the scrapy-test git project, i.e. 
  the directory containing README.md
- modify tutorial/spiders/bhrrc.py to configure the number of articles 
  to process. It is hardcoded to 10,000 lines. Scraping these can take
  30 minutes or so on a 2-4 core CPU machine.
- run 'scrapy crawl bhrrc' to generate bhrrc_fasttext.txt file in the 
  root directory.
- copy bhrrc_fasttext.txt to root directory of fasttext installation.
- cd to the root directory of fasttext.
- count the number of lines in bhrrc_fasttext.txt with the command
  'wc -l bhrrc_fasttext.txt'
- split bhrrc_fasttext.txt into training and validation data sets by 
  splitting it into 80/20 (e.g. if total lines in bhrrc_fasttext.txt are 
  1000, allocate 800 lines for training and allocate 200 lines for 
  validation) and storing these into bhrrc.train and bhrrc.valid as 
  follows:
     head -n 800 bhrrc_fasttext.txt > bhrrc.train 
     tail -n 200 bhrrc_fasttext.txt > bhrrc.valid 
- Train the model:
     ./fasttext supervised -input bhrrc.train -output model_bhrrc_multilabel -epoch 15 -wordNgrams 3 -dim 300 -lr 1.0 -pretrainedVectors data/wiki-news-300d-1M-subword.vec
- Test the model:
     ./fasttext test model_bhrrc_multilabel.bin bhrrc.valid

