from scrapy.spiders import Spider
from scrapy import Request
import pdb
import scrapy
from scrapy_splash import SplashRequest
import os

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


    def touch(self,file_path):
        try:
            os.utime(file_path, None)
        except OSError:
            open(file_path, 'a').close()

    def parse(self, response):

        file_path = '/home/herrfeder/django-rpi/FEEDO/rsscore/static/'+self.allowed_domains[0].split("://")[1].replace("/",".")+'.html'
        self.touch(file_path)
        #pdb.set_trace()
        print "TEST in parse"
        with open(file_path, 'w') as f:
            for line in response.body:
                f.write(line)
            f.close()
