from scrapy.spiders import Spider
from scrapy import Request
import pdb
import scrapy
from scrapy_splash import SplashRequest

class SiteSaveSpider(Spider):

    def __init__(self, domain='', *args, **kwargs):
        super(SiteSaveSpider, self).__init__(*args, **kwargs)
        self.start_urls = [domain]
        self.allowed_domains = [domain]
    name = "sitesavespider"


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, args={'wait':0.5})

            print "TEST after yield"

    def parse(self, response):
        #pdb.set_trace()
        print "TEST in parse"
        with open('/home/herrfeder/ownCloud/IT/Programmierung/Python/FEEDO/rsscore/static/'+self.allowed_domains[0].split("://")[1]+'.html', 'w') as f:
            for line in response.body:
                f.write(line)
