import scrapy
import sys
from w3lib.html import remove_tags

class QuotesSpider(scrapy.Spider):
    name = "bhrc"
    start_urls = [
        'https://www.business-humanrights.org/en/news/'
    ]
    count = 0

    def parse(self, response):
        for a in response.css('div.story_outer.component_outer h2 a'):
            yield response.follow(a, callback=self.parse_article)
            self.count+=1
            if (self.count >= 10000):
                sys.exit()

        for href in response.css('li.pager-next a::attr(href)'):
            yield response.follow(href, callback=self.parse)


    def parse_article(self, response):
        yield {
                'title': response.css('div.primary h1').extract(),
                'author': response.css('div.primary h2').extract(),
                'content': response.css('div.primary p').extract(),
                'labels': response.css('a.related_module_content_element.related_tags::text').extract(),
#                'firstLabel': response.css('a.related_module_content_element.related_tags.first::text').extract(),
                'combined': '',
                'b_orig_content': response.css('div.primary p').extract(),
        }
