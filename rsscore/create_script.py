#!/usr/bin/python
# coding: utf-8
from lxml import etree
import requests
import os
from copy import copy
from copy import deepcopy
import sys
import re
import pdb
from django.conf import settings
settings.configure(
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/home/herrfeder/ownCloud/IT/Programmierung/Python/FEEDO/db.sqlite3',
            }
        }
)
import django
django.setup()
sys.path.append(os.path.abspath("/home/herrfeder/ownCloud/IT/Programmierung/Python/FEEDO/"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'FEEDO.settings'

from rsscore.models import Feed

from bs4 import BeautifulSoup, BeautifulStoneSoup, Tag, NavigableString, CData

class FeedObject(object):
    def __init__(self):
        self.feed_list = []
        self.feed_element = {}
        self.index = 0
        self.raw_feed_list = []
        self.feed_type = None


    def add_element(self, feedtype="",  **kwargs):

        for key,value in kwargs.iteritems():
            self.feed_element[key] = value

        if feedtype == "":
            self.feed_type = None
            check_feed_type(feedtype)

        self.feed_list.append(self.feed_element)
        self.index =+ 1

    def check_feed_type(self,feedtype):
        pass

    def gen_feed(self):
        self.raw_feed_list = []
        if self.feed_type == None:
            for entry in self.feed_list:
                self.raw_feed_list.append(gen_rss(entry))


def gen_rss(record):

    description_blank_str = \
    '''
    <item>
    <title>Entry Title</title>
    <link>Link to the entry</link>
    <guid>http://example.com/item/123</guid>
    <pubDate>Sat, 9 Jan 2010 16:23:41 GMT</pubDate>
    <description>[CDATA[ This is the description. ]]</description>
    </item>
    '''
    description_xml_tag = BeautifulStoneSoup(description_blank_str)

    key_pair_locations = \
    [
        ("title", lambda x: x.name == u"title"),
        ("link", lambda x: x.name == u"link"),
        ("guid", lambda x: x.name == u"guid"),
        ("pubDate", lambda x: x.name == u"pubdate"),
        ("description", lambda x: x.name == u"description")
    ]

    tmp_description_tag_handle = deepcopy(description_xml_tag)

    for (key, location) in key_pair_locations:
        search_list = tmp_description_tag_handle.findAll(location)
        if(not search_list):
            continue
        tag_handle = search_list[0]
        tag_handle.clear()
        if(key == "description"):
            tag_handle.insert(0, CData(record[key]))
        else:
            tag_handle.insert(0, record[key])

    return tmp_description_tag_handle

test_dict = \
{
    "title" : "TEST",
    "link" : "TEST",
    "guid" : "TEST",
    "pubDate" : "TEST",
    "description" : "TEST"
}


def get_raw_html(how_to_get="file"):
    raw_html = ""
    if how_to_get == "file":
        temp_file = ""
        with open("static/www.filmtipps.at.html","r") as f:
            temp_file = f.readlines()
            f.close()
        raw_html = temp_file
    return raw_html



def generate_dom_elements(feedname,feedtitle,feedlink,feeddescription):
    
    
    # fetching the html page
    entryname = "filmtipps_new"
    # getting the items
    raw_html = get_raw_html()
    bsoup = BeautifulSoup(str(raw_html),'lxml')
    #print get_title("test",entryname)
    #print get_description("test",entryname)
    
    feed_element_parent = None

    if feed_element_parent == None:
        test=re.compile(r'Amoralisc')

        parent = bsoup.find_all(text=test)[0].parent
        while parent.attrs == {}:
            parent = parent.parent
            print "Parent-Attribute:"+str(parent.attrs)
            print "Parent-Name:"+str(parent.name)
        print bsoup.find_all(parent.name,parent.attrs)[4]

        #for element in bsoup.find_all(text=test)[0].parent.parent:
        #    print element

        #for element in bsoup.find_all('div',{'class':'smallteaser'}):
        #    print element.children()


def get_rss_data(feedname,feedtitle,feedlink,feeddescription):
    pass
    # fetching the html page
    # for each line in the table
    #for i in items:
    # getting the identifier
    #    ids = i.xpath('td[position()=1]/text()')
    #    idposte = 'empty' if len(ids) == 0 else ids[0]

    # getting the link
    #    links = i.xpath('td[position()=3]/a/@href')
    #    link = 'empty' if len(links) == 0 else links[0]

        # getting the description
    #    descriptions = i.xpath('td[position()=2]/text()')
    #    description = 'empty' if len(descriptions) == 0 else descriptions[0]

        # getting the title
    #    titles = i.xpath('td[position()=4]/text()')
    #    title = 'empty' if len(titles) == 0 else titles[0]

    #feed.add_item(
    #      title=title,
    #      link=link,
    #      description=description,
    #      unique_id=idposte
    #    )

    #print "Content-type: application/rss+xml; charset=utf8"
    #print ""
    #print feed.writeString('utf-8')




def get_title(user, feedname):
    
    feedtitle_key = Feed.objects.get(feed_name=feedname).title_dom_key
    feedtitle_type = Feed.objects.get(feed_name=feedname).title_dom_type
    
    return [feedtitle_type, feedtitle_key]
def get_description(user, feedname):
    
    feeddesc_key = Feed.objects.get(feed_name=feedname).desc_dom_key
    feeddesc_type = Feed.objects.get(feed_name=feedname).desc_dom_type
    
    return [feeddesc_type, feeddesc_key]


def get_link(user, feedname):
    
    feed_link = Feed.objects.get(feed_name=feedname).feed_link
    
    return [feed_link]

generate_dom_elements("","","","")

#print gen_xml(test_dict)
