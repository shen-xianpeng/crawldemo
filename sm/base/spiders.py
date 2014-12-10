import scrapy
from sm.items import BbedenItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

from scrapy.http import Request

from sm.utils import replace_true_src


class MybaseSpider(CrawlSpider):
    IMAGES_URLS_FIELD = 'image_urls'
    name = ''
    allowed_domains = []
    host_url = ''
    start_urls = [
    ]
    page_format = ''

    def _get_page_count(self, response):
        pass

    def _get_page_url(self, index):
        ''' '''
        return self.page_format % index

    def get_page_urls(self, response):
        count = self._get_page_count(response)
        for index in count:
            page_url = self._get_page_url(index)
            yield page_url

    def save_body(self, soup, img_src='src'):
        desc_body_content = soup
        body = unicode(desc_body_content)
        desc_body_images = [image[img_src] for image in soup.findAll("img")]
        orig_img_list_dict = {link:self._join_link(link) for link in  desc_body_images}
 
        if img_src=='src':
            for i in orig_img_list_dict:
                body = body.replace(i, orig_img_list_dict[i])
        else:
            body = replace_true_src(body, img_src)
        orig_img_list = orig_img_list_dict.values()
        return {'body':body, 'orig_previews':orig_img_list}

    def parse(self, response):
        for page_url in self.get_page_urls(response):
            yield Request(page_url, callback=self.parse_page)
    
    def _join_link(self, link):
        if link.startswith('http://') \
            or link.startswith('https://'):
            return link
        elif link.startswith('/'):
            link = link.split('/', 1)[-1]
            return self.host_url+link
        elif link:
            return self.host_url + link
        return ''

    def parse_page(self, response):
        pass

    def save_content(self, soup):
        paras = soup.findAll('p')
        content = ''
        for p in paras:
            txt = p.text.strip()
            if txt: content += txt+'\n'
        content = p_quote.sub('',content)
        return {'content':content}

import re
p_quote=re.compile(ur'(&quot;|&nbsp;)')