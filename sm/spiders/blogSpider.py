import scrapy
from sm.items import BlogItem
from sm.base.spiders import MybaseSpider
from scrapy.http import Request
from sm.utils import get_nums
from sm.utils import hash_item_fields



class BlogSpider(MybaseSpider):
    IMAGES_URLS_FIELD = 'image_urls'
    name = 'blog'
    allowed_domains = ["www.mikedoesweb.com"]
    host_url = 'http://www.mikedoesweb.com/'
    start_urls = [
        "http://www.mikedoesweb.com/",
    ]
    page_format = 'http://www.mikedoesweb.com/'

    def get_page_urls(self, response):
        return self.start_urls

    def parse(self, response):
        for page_url in self.get_page_urls(response):
            yield Request(page_url, callback=self.parse_page)

    def parse_page(self, response):
        for sel in response.xpath('/html/body/section[1]/article'):
            title = sel.xpath('h2/a/text()').extract()[0]
            link = sel.xpath('h2/a/@href').extract()[0]
            content = sel.xpath('div/p/text()').extract()[0]
            item = BlogItem()
            item['title'] = title
            item['content'] = content
            item['link'] = self._join_link(link)
            yield item

