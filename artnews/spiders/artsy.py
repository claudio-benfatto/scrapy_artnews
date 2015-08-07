import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector

class ArtnewsSpider(CrawlSpider):
    name = "artsy"
    allowed_domains = ["artsy.net"]
    start_urls = [ "https://www.artsy.net/articles"]

    def start_requests(self):
        page_size = 25
        headers = {'User-Agent' 'Scrapy spider',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Host': 'www.artsy.net',
                   'Origin': 'http://www.artsy.net',
                   'Accept': '*/*',
                   'Referer': 'http://www.artsy.net/',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        for offset in (0, 200, page_size):
            yield Request('http://www.ijreview.com/wp-admin/admin-ajax.php',
                          method='POST',
                          headers=headers,
                          body=urllib.urlencode(
                              {'action': 'load_more',
                               'numPosts': page_size,
                               'offset': offset,
                               'category': '',
                               'orderby': 'date',
                               'time': ''}))

    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow='article/[\w-]+$'),
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
        content += ''.join(response.xpath('//div[@class="article-section-text"]/descendant::text()').extract())
        content.encode('utf8')
        date = ''
        date += ''.join(response.xpath('//div[@class="article-date"]/descendant::text()').extract())
        title = response.url.encode("utf8")
        filename = title.rsplit('/')[-1]

        with open("artsy/"+filename, 'wb') as f:
            f.write(content.encode("utf8"))
