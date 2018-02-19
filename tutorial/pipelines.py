# -*- coding: utf-8 -*-
from w3lib.html import remove_tags
import re
import string
from tutorial.exporters import FasttextItemExporter

# from scrapy.utils.markup import remove_tags

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class TutorialPipeline(object):
#     def process_item(self, item, spider):
#         return item

def clense(text, space_replacer = ' ', to_lower = True, remove_punc = True):
    # remove HTML comments first as suggested in https://stackoverflow.com/questions/28208186/how-to-remove-html-comments-using-regex-in-python
    text = re.sub("(<!--.*?-->)", "", text, flags=re.DOTALL)
    text = remove_tags(text)
    text = re.sub(r'[^\x00-\x7F]+',' ', text)   #remove non-ascii characters
    text = text.replace("&amp;", "and")
    text = text.replace("&", "and")
    text.strip()
    text.rstrip()
    text = text.replace("\r\n", "")
    if to_lower:
        text = text.lower()

    if remove_punc:
        # from https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        text = re.sub(r'[^\w\s]', '', text)   #remove punctuation marks and non-word
        text = text.replace(",", "")

    text = re.sub(' +', space_replacer, text)
    #if  all(ord(char) < 128 for char in text) == False:
    #    text = ''
    ''.join(i for i in text if ord(i)<128)
    return text
    
class BHRCPipeline(object):
    def __init__(self, file_name):
        # Storing output filename
        self.file_name = file_name
        # Creating a file handle and setting it to None
        self.file_handle = None

    @classmethod
    def from_crawler(cls, crawler):
        # getting the value of FILE_NAME field from settings.py
        output_file_name = crawler.settings.get('FILE_NAME')

        # cls() calls pipeline's constructor
        # Returning a pipeline object
        return cls(output_file_name)

    def open_spider(self, spider):
        print('Custom export opened')

        # Opening file in binary-write mode
        file = open(self.file_name, 'wb')
        self.file_handle = file

        # Creating a FanItemExporter object and initiating export
        self.exporter = FasttextItemExporter(file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        print('Custom Exporter closed')

        # Ending the export to file from FanItemExport object
        self.exporter.finish_exporting()

        # Closing the opened output file
        self.file_handle.close()

    def process_item(self, item, spider):
        new_labels = '__label__Human_Rights__ '  #default label
        for label in item['labels']:
            new_labels = new_labels + '__label__' + clense(label, "_", to_lower = False, remove_punc = False) + ' '
        item['labels'] = new_labels

        new_content = ''
        i = 0
        for content in item['content']:
            # skip content that has 
            # "Read the full post here" and "Related companies" in them
            # skip the 1st element as it contains a summary sentence
            content = clense(content)
            if content.lower().startswith("read the full post here"):
                continue
            if content.lower().startswith(" related companies"):
                continue
            # skip the first element. It contains article summary and publish date
            if (i > 0):
                new_content = new_content + " " + content
            i+=1
        item['content'] = new_content

        new_title = ''
        for title in item['title']:
            new_title = new_title + clense(title)
        item['title'] = new_title

        new_author = ''
        for author in item['author']:
            new_author = new_author + clense(author)
        item['author'] = new_author
        self.exporter.export_item(item)
        return item
