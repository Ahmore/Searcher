import scrapy
from scrapy.exceptions import CloseSpider


class WikiSpider(scrapy.Spider):
    name = 'wikispider'
    start_urls = ['https://en.wikipedia.org/wiki/Mathematics']
    close_down = False

    def __init__(self, n=0, k=0, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)

        self.n = int(n)
        self.k = self.n if k == 0 else int(k)

    def parse(self, response):
        if self.close_down:
            raise CloseSpider(reason='Have enought')

        yield {
            'title': response.css("title ::text").extract_first(),
            'content': response.css('div.mw-parser-output ::text').extract(),
            'url': response.url
        }

        for next_page in response.css('div.mw-parser-output a ::text'):
            yield response.follow(next_page, self.parse)