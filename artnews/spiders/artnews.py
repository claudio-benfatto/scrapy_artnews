import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector

class ArtnewsSpider(CrawlSpider):
    name = "artnews"
    allowed_domains = ["artnews.com"]
    start_urls = [ "http://www.artnews.com/category/artists-2/"]

    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow='2015/[0-9]{2}/[0-9]{2}/[\w-]+/$'),
            callback='parse_page',
            follow=True
        ),

        # Sites which should be followed, but not saved
    #    Rule(SgmlLinkExtractor(allow='(aktuell|thema|themenarchiv)/[\/\w.-]+(/|s[\d]+.html)$')),
    )

    def parse_page(self, response):
        #filename = response.url.split("/")[-2] + '.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        hxs = Selector(response)
        content = ''
        title = ''
        content += ''.join(response.xpath('//div[@class="main-content"]/descendant::text()[not(ancestor::div[contains(@class, "wp-caption")])]').extract())
        content.encode('utf8')
        title += ''.join(response.xpath('//h1[@class="entry-title"]/text()').extract())
        title.encode("utf8")
        filename = title

        with open("artists/"+filename, 'wb') as f:
            f.write(content.encode("utf8"))
