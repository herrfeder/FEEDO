
from lxml import etree
import requests
import os
from copy import copy
from copy import deepcopy
import sys  
import re
import pdb
import logging
from time import strftime,gmtime
from bs4 import BeautifulSoup, BeautifulStoneSoup, Tag, NavigableString, CData


rss_path = "/home/herrfeder/django-rpi/FEEDO/rsscore/static/"

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



    def get_elements(self):
        self.elements = self.element_dict.keys()

    def set_element_dict(self,element_dict):
        self.element_dict = element_dict
        self.get_elements()
        self.parse_element_dict_url()
    
    def set_response(self,response):
        self.response = response


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
        with open(rss_path+"test_rss.rss","w") as f:
            for line in data:
                f.write(line)
            f.close()


    def gen_rss(self):

        header ='<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0">\n'
 	header += ' <channel>' 
        header +=\
        '''
        <title>test</title>
        <link>https://www.hd-area.org</link>
        <description><![CDATA[test]]></description>

        <language>de-de</language>
        '''

        blank_str = \
        '''<item>
            <title>{0}</title>
            <link>{1}</link> 
            <description>{4}</description>
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
                             ,"https://www."+dicti["link"]
                             ,dicti["guid"]
                             ,dicti["pubDate"]
                             ,dicti["description"].replace("\\x","")[0:100])
            rss_feed+=rss_entry
        return rss_feed+footer


    def parse_malformed_url(self, url):
        if not url.startswith("http"):
            url = "https://"+url
	    return url




    def parse_element_dict_url(self):
        self.element_url = {}
        test_list = []
        for element in self.elements:
            self.element_url[element] = self.element_dict[element][4]
        for key,value in self.element_url.iteritems():
            test_list.append(value)
        if all(x==test_list[0] for x in test_list):
            self.global_url = self.parse_malformed_url(test_list[0])
            logging.info("Set global url %s"%(self.global_url))

    def get_url(self):
        if self.global_url:
            return [self.global_url]





    def convert_str_to_dict(self,element):
        ''' converts attribute string like
            class: top & id:center to a dict of attributes'''

        attr_dict = {}
        attr_str = str(self.element_dict[element][2])
        if not attr_str:
            return None

        el_list = attr_str.split(" &")
        for el in el_list:
            attr_dict[el.split(":")[0]]=el.split(":")[1]

        return attr_dict


    def generate_dom_elements(self):
        self.result_dict = {}
        global_bsoup = ""
        self.parse_element_dict_url()

        for element in  self.elements:
            if self.global_url and not global_bsoup:
                global_bsoup = BeautifulSoup(str(self.response),'lxml')
            else:
                bsoup = BeautifulSoup(str(self.response),'lxml')

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
            #    prinnt element

            #for element in bsoup.find_all('div',{'class':'smallteaser'}):
            #    print element.children()


    def prepare_result_dict(self):
        temp_list = []
        if not self.result_dict:
            return

        for i in range(0,len(self.result_dict[self.elements[0]])):
            temp_dict = {}
            for element in self.elements:
                temp_dict[element] = self.result_dict[element][i]
                temp_dict["guid"] = ""
                temp_dict["pubDate"] = strftime("%a, %d %b %Y %X +0000", gmtime())
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

