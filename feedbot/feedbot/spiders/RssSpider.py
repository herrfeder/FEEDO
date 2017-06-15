from scrapy.spiders import Spider
import pdb
import scrapy
from scrapy_splash import SplashRequest
from feedobject import FeedObject
import json


class RssSpider(Spider):


    name = "rssspider"

    def __init__(self, element_dict
                 , *args, **kwargs):
        super(RssSpider, self).__init__(*args, **kwargs)
        self.element_dict = json.loads(element_dict)
        self.start_urls = []
        self.allowed_domains = []
        self.fo = FeedObject()
        self.fo.set_element_dict(self.element_dict)
        self.start_urls.append(self.fo.get_url()[0])
        self.allowed_domains.append(self.fo.get_url()[0])


    def start_requests(self):
        
        for url in self.fo.get_url():
            yield SplashRequest(url, callback=self.parse, args={'wait':0.5})

    def parse(self, response):

        self.fo.set_response(response.body)
        self.fo.generate_dom_elements()
        self.fo.prepare_result_dict()
        self.xml_tag = self.fo.gen_rss()
        self.fo.write_rss(self.xml_tag)



