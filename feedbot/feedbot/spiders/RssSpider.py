from scrapy.spiders import Spider
from scrapy import Request
from rsscore.models import Feed
from feedbot.items import EntryItem,EntryListItem
import pdb
import scrapy
from scrapy_splash import SplashRequest
class RssSpider(Spider):

    #def __init__(self):
    userfeeds = Feed.objects.all()

    name = "rssspider"
#    allowed_domains = [str(userfeeds[1].feed_link).split("//")[1]]
#    start_urls = [str(userfeeds[1].feed_link)]

    start_urls = "test"
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, args={'wait':0.5})

    def parse(self, response):
        pdb.set_trace()
        print response
        return EntryItem()
