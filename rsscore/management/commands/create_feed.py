#!/usr/bin/python
# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from rsscore.models import Feed

from lxml import etree
import requests
import os
from copy import copy
from copy import deepcopy
import sys
import re
import pdb
import logging
from scrapyd_api import ScrapydAPI
from rsscore.models import Feed

from bs4 import BeautifulSoup, BeautifulStoneSoup, Tag, NavigableString, CData
elements = ["title","description","link","image"]
filepath = "/home/herrfeder/django-rpi/FEEDO/rsscore/management/temp/"

rss_path = "/home/herrfeder/django-rpi/FEEDO/rsscore/static/"

class Command(BaseCommand):
    help = 'will generate python script or rssfeed from Feed info'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?')
        parser.add_argument('feedname', nargs='?')
        parser.add_argument(
            '--script',
            action='store_true',
            dest='script',
            default=False,
            help='Create Script for creating rssfeed'
        )

    def handle(self, *args, **options):
        username = options['username']
        feedname = options['feedname']
        fo = FeedObject()
        for element in elements:
            fo.get_element_info(element,username,feedname)

        fo.generate_dom_elements(username,feedname)
        fo.prepare_result_dict()
        xml_tag = fo.gen_rss()
        fo.write_rss(xml_tag)


class FeedObject(object):
    def __init__(self):
        self.feed_list = []
        self.feed_element = {}
        self.index = 0
        self.raw_feed_list = []
        self.feed_type = None
        self.element_dict = {}
        self.test_dict = \
        {
            "title" : "TEST",
            "link" : "TEST",
            "guid" : "TEST",
            "pubDate" : "TEST",
            "description" : "TEST"
        }


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


    def write_rss(self,data):
        with open(rss_path+"test_rss","w") as f:
            for line in data:
                f.write(line)
            f.close()


    def gen_rss(self):

        header ='<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="0.92">\n'
        header += '<channel>'
        header +=\
        '''
        <title>test</title>
        <link>https://www.hd-area.org</link>
        <description><![CDATA[test]]></description>

        <language>de-de</language>
        '''

        blank_str = \
        '''
        <item>
            <title><![CDATA[{0}]></title>
            <link>{1}</link>
            <description><![CData[{4}]]></description>
            <guid>{1}</guid>
            <pubDate>{3}</pubDate>
        </item>
        '''
        footer = '</channel>\n</rss>'
        rss_feed = ""

        #xml_tag = BeautifulStoneSoup(description_blank_str)

        #key_pair_locations = \
        #[
        #    ("title", lambda x: x.name == u"title"),
        #    ("link", lambda x: x.name == u"link"),
        #    ("guid", lambda x: x.name == u"guid"),
        #    ("pubDate", lambda x: x.name == u"pubdate"),
        #    ("description", lambda x: x.name == u"description")
        #]
        rss_feed+=header
        pdb.set_trace()
        for dicti in self.result_list: 
            #if "tmp_tag_handle" in locals():
            #    tmp_tag_handle = deepcopy(description_blank_str)
            #    pdb.set_trace()
            #else:
            #    tmp_tag_handle = deepcopy(xml_tag)
            #for (key, location) in key_pair_locations:
            #    search_list = tmp_tag_handle.findAll(location)
            #    if(not search_list):
            #        continue
            #    tag_handle = search_list[0]
            #    tag_handle.clear()
            # 
            #    tag_handle.insert(0, dicti[key])
            #pdb.set_trace()
            rss_entry =\
            blank_str.format(dicti["title"]
                             ,dicti["link"]
                             ,dicti["guid"]
                             ,dicti["pubDate"]
                             ,dicti["description"])
            rss_feed+=rss_entry
        return rss_feed+footer


    def parse_malformed_url(self, url):
        if not url.startswith("http"):
            url = "https://"+url
            return url




    def parse_element_dict_url(self):
        self.element_url = {}
        test_list = []
        for element in elements:
            self.element_url[element] = self.element_dict[element][4]
        for key,value in self.element_url.iteritems():
            test_list.append(value)
        if all(x==test_list[0] for x in test_list):
            self.global_url = self.parse_malformed_url(test_list[0])
            logging.info("Set global url %s"%(self.global_url))


    def get_raw_html(self,element=""):

        scrapyd = ScrapydAPI("http://localhost:6800")
        if self.global_url:
            url = self.global_url
        else:
            url = self.element_dict[element][4]

        jid = scrapyd.schedule("feedbot",
                               "sitesavespider",
                               domain=url,
                               filepath=filepath)

        filename= url.split("://")[1].replace("/",".")+".html"

        with open(filepath+filename,"r") as f:
            temp_file = f.readlines()
            f.close()
        raw_html = temp_file
        return raw_html

    def convert_str_to_dict(self,element):
        attr_dict = {}
        attr_str = str(self.element_dict[element][2])
        if not attr_str:
            return None

        el_list = attr_str.split(" ")
        for el in el_list:
            attr_dict[el.split(":")[0]]=el.split(":")[1]

        return attr_dict


    def generate_dom_elements(self,username,feedname):
        self.result_dict = {}
        global_bsoup = ""
        self.parse_element_dict_url()
        for element in elements:
            if self.global_url and not global_bsoup:
                global_bsoup = BeautifulSoup(str(self.get_raw_html()),'lxml')
            else:
                bsoup = BeautifulSoup(str(self.get_raw_html(element)),'lxml')
            
            if global_bsoup:
                bsoup = global_bsoup
            if self.element_dict[element][3]:
                feed_element_parent = True
            else:
                feed_element_parent = False

            p_dom_element = self.element_dict[element][3]
            dom_element = self.element_dict[element][1]

            attr_dict = self.convert_str_to_dict(element)

            all_ele = bsoup.findAll(p_dom_element,attr_dict)

            temp_list = []
            for ele in all_ele:
                try:
                    temp_list.append(str(ele.findAll(dom_element)[0].text))
                except:
                    temp_list.append(" ")
            self.result_dict[element] = temp_list
                

        if feed_element_parent == False:
            test=re.compile(r'')

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


    def prepare_result_dict(self):
        temp_list = []
        if not self.result_dict:
            return 

        for i in range(0,len(self.result_dict[elements[0]])):
            temp_dict = {}
            for element in elements:
                temp_dict[element] = self.result_dict[element][i]
            temp_dict["guid"] = ""
            temp_dict["pubDate"] = ""
            temp_list.append(temp_dict)
        self.result_list = temp_list




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




    def get_element_info(self,element,user, feedname):

        if element=="title":
            feed_key    = Feed.objects.get(feed_name=feedname).title_dom_key
            feed_type   = Feed.objects.get(feed_name=feedname).title_dom_type
            feed_parent = Feed.objects.get(feed_name=feedname).title_dom_parent
            feed_ptype  = Feed.objects.get(feed_name=feedname).title_dom_ptype
            feed_url    = Feed.objects.get(feed_name=feedname).title_dom_url
        elif element == "description":
            feed_key    = Feed.objects.get(feed_name=feedname).desc_dom_key
            feed_type   = Feed.objects.get(feed_name=feedname).desc_dom_type
            feed_parent = Feed.objects.get(feed_name=feedname).desc_dom_parent
            feed_ptype  = Feed.objects.get(feed_name=feedname).desc_dom_ptype
            feed_url    = Feed.objects.get(feed_name=feedname).desc_dom_url
        elif element == "image":
            feed_key    = Feed.objects.get(feed_name=feedname).img_dom_key
            feed_type   = Feed.objects.get(feed_name=feedname).img_dom_type
            feed_parent = Feed.objects.get(feed_name=feedname).img_dom_parent
            feed_ptype  = Feed.objects.get(feed_name=feedname).img_dom_ptype
            feed_url    = Feed.objects.get(feed_name=feedname).img_dom_url
        elif element == "link":
            feed_key    = Feed.objects.get(feed_name=feedname).link_dom_key
            feed_type   = Feed.objects.get(feed_name=feedname).link_dom_type
            feed_parent = Feed.objects.get(feed_name=feedname).link_dom_parent
            feed_ptype  = Feed.objects.get(feed_name=feedname).link_dom_ptype
            feed_url    = Feed.objects.get(feed_name=feedname).link_dom_url
        self.element_dict[element] = [feed_key, feed_type, feed_parent,
                                      feed_ptype, feed_url]

