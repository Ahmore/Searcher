import scrapy


class WikiSpider(scrapy.Spider):
    name = 'wikispider'
    start_urls = ['https://en.wikipedia.org/wiki/Mathematics']

    def parse(self, response):
        yield {
            'title': response.css("title ::text").extract_first(),
            'content': response.css('div.mw-parser-output ::text').extract(),
            'url': response.url
        }

        for next_page in response.css('div.mw-parser-output a ::text'):
            yield response.follow(next_page, self.parse)