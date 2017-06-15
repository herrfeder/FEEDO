from scrapy.spiders import Spider
from scrapy import Request
import pdb
import scrapy
from scrapy_splash import SplashRequest
import os

filepath='/home/herrfeder/django-rpi/FEEDO/rsscore/static/'
class SiteSaveSpider(Spider):

    def __init__(self, domain='',
                 filepath=filepath
                 , *args, **kwargs):
        super(SiteSaveSpider, self).__init__(*args, **kwargs)
        self.filepath = filepath
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

        file_path = self.filepath+self.allowed_domains[0].split("://")[1].replace("/",".")+'.html'
        self.touch(file_path)
        with open(file_path, 'w') as f:
            for line in response.body:
                f.write(line)
            f.close()
