# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy_djangoitem import DjangoItem
from rsscore.models import Feed,Entry,EntryList

class FeedItem(DjangoItem):
    django_model = Feed

class EntryItem(DjangoItem):
    django_model = Entry

class EntryListItem(DjangoItem):
    django_model = EntryList

class FeedbotItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass
