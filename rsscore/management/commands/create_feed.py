#!/usr/bin/python
# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from rsscore.models import Feed

import os
import sys
import logging
from scrapyd_api import ScrapydAPI
from rsscore.models import Feed
import json


elements = ["title","description","link","image"]

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
        element_dict = {}
        for element in elements:
            element_dict[element] = get_element_info(element,username,feedname)
        print element_dict
        scrapyd = ScrapydAPI("http://localhost:6800")
        jid = scrapyd.schedule("feedbot","rssspider",element_dict=json.dumps(element_dict))
        print jid 
        print json.dumps(element_dict)
        if "finished" in scrapyd.job_status("feedbot",jid):
            return 2




def get_element_info(element,user, feedname):

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

    return [feed_key, feed_type, feed_parent,feed_ptype, feed_url]

