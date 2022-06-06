import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
class BestBooksSpider(CrawlSpider):
    name = 'best_books'
    allowed_domains = ['books.toscrape.com']
    url = 'http://books.toscrape.com'
    user_agent ='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    def start_requests(self):
       yield scrapy.Request(url=self.url,headers={
            'User-Agent':self.user_agent
        })
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3"), callback='parse_item', follow=True,process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"),follow=True,process_request='set_user_agent'),
    )
    def set_user_agent(self,request,spider):
        request.headers['User-Agent'] = self.user_agent
        return request
    def parse_item(self, response):
        name = response.xpath("//h1/text()").get()
        price = response.xpath("//div[@class='col-sm-6 product_main']/p[@class='price_color']/text()").get()
        yield {
            'name':name,
            'price':price
        }