from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
from django.http import JsonResponse
from .models import Feed
from .forms import CreateFeedForm
import os,sys
import datetime
import pdb
from scrapyd_api import ScrapydAPI
import re
import json

class FrameSite(object):

    def __init__(self):
        self._filename = ""
    @property
    def filename(self):
        return self._filename
    @filename.setter
    def filename(self, value):
        self._filename = value

class ClickCounter(object):

    def __init__(self):
        self._counter = 0

    def __callback__(self):
        return self._counter

    @property
    def counter(self):
        return self._counter

    def add(self):
        self._counter = self._counter + 1

    def sub(self):
        self._counter = self._counter - 1
        if self._counter < 0:
            self._counter == 0

    def reset(self):
        self._counter = 0

global cc
cc = ClickCounter()


global click_dict
click_dict = {}

global FrameObject
FrameObject = FrameSite()

def index(request):
    latest_rssfeed_list = Feed.objects.order_by('-id')[:5]
    template = loader.get_template('rsscore/index.html')
    context = {
        'latest_rssfeed_list':latest_rssfeed_list }
    return HttpResponse(template.render(context,request))

def processframe(request):
    iframe = request.POST.get('framedata',None)
    print iframe


def adapt_javascript(jsondata):
    
    crafted_base_html = \
        "<head><base href="+jsondata["siteurl"]

    temp_file = ""
    print "JSON_DATA:"+jsondata["filename"]
    infile="rsscore/static/"+jsondata["filename"]

    jsondata["filename"] = re.sub(r'\?','',jsondata["filename"])

    outfile="rsscore/static/"+"no_js"+jsondata["filename"]
    readfile = "no_js"+jsondata["filename"]
    with open(infile,"r") as f:
        temp_file = f.readlines()
        f.close()


    temp_file = re.sub(r'<script.+?script>', '',str(temp_file))
    temp_file = re.sub('\\\\n', '', str(temp_file))
    temp_file = re.sub('[\\\]{0,10}', '', str(temp_file))
    temp_file = re.sub('\',', '', str(temp_file))
    temp_file = re.sub('\'t{3,10}', '', str(temp_file))
    # fucking complicated regex
    #temp_file = re.sub(r"div>[\s*']{2,5}<", '',  str(temp_file))

    temp_file = re.sub(r'127.0.0.1:8000/static/',jsondata["siteurl"],str(temp_file))
    temp_file = re.sub(r'<head>',crafted_base_html,str(temp_file))
    with open(outfile,"w") as f:
        f.writelines(temp_file)


    FrameObject.filename = readfile
    return readfile

def loadproxysite(request):
    siteurl = request.POST.get('siteurl',None)
    clicked_html = request.POST.get('clicked_html',None)
    if str(clicked_html) == "0":
        cc.reset()
        # deleting files on system
        click_dict.clear()
        click_dict[cc.counter]=[siteurl,FrameObject.filename]
    elif str(clicked_html) != "0":
        click_dict[cc.counter]=[siteurl,FrameObject.filename,clicked_html]
    cc.add()
    if siteurl is None:
        return HttpResponse("none")
    else:
        scrapyd = ScrapydAPI("http://localhost:6800")
        jid = scrapyd.schedule("feedbot","sitesavespider",domain=siteurl)
        FrameObject.filename= siteurl.split("://")[1].replace("/",".")+".html"
        jsondata =  {"filename":FrameObject.filename,
                     "crawljob":jid,
                     "siteurl":siteurl,
                     "click_dict":click_dict}
        while(1):
            if "finished" in scrapyd.job_status("feedbot",jid):
                jsondata["filename"] = adapt_javascript(jsondata)
                return JsonResponse(jsondata)

    return HttpResponse("hello")

def createfeed(request):

    
    if request.method == "POST":
        form = CreateFeedForm(request.POST)
        print "FORM_ERROR"
        print form.errors.as_data()
        if form.is_valid():
            feed = Feed(
                feed_user = "test",
                feed_name = form.cleaned_data['feedname'],

                title_dom_type = form.cleaned_data['title_dom_type'],
                title_dom_key = form.cleaned_data['title_dom_key'],
                title_dom_parent = form.cleaned_data['title_dom_parent'],
                title_dom_ptype = form.cleaned_data['title_dom_ptype'],
                title_dom_url = form.cleaned_data['title_dom_url'],

                desc_dom_type = form.cleaned_data['desc_dom_type'],
                desc_dom_key = form.cleaned_data['desc_dom_key'],
                desc_dom_parent = form.cleaned_data['desc_dom_parent'],
                desc_dom_ptype = form.cleaned_data['desc_dom_ptype'],
                desc_dom_url = form.cleaned_data['desc_dom_url'],

                link_dom_type = form.cleaned_data['link_dom_type'],
                link_dom_key = form.cleaned_data['link_dom_key'],
                link_dom_parent = form.cleaned_data['link_dom_parent'],
                link_dom_ptype = form.cleaned_data['link_dom_ptype'],
                link_dom_url = form.cleaned_data['link_dom_url'],

                img_dom_type = form.cleaned_data['img_dom_type'],
                img_dom_key = form.cleaned_data['img_dom_key'],
                img_dom_parent = form.cleaned_data['img_dom_parent'],
                img_dom_ptype = form.cleaned_data['img_dom_ptype'],
                img_dom_url = form.cleaned_data['img_dom_url'],

                crawl_dom_type = form.cleaned_data['crawl_dom_type'],
                crawl_dom_key = form.cleaned_data['crawl_dom_key'],
                crawl_dom_parent = form.cleaned_data['crawl_dom_parent'],
                crawl_dom_ptype = form.cleaned_data['crawl_dom_ptype'],
                crawl_dom_url = form.cleaned_data['crawl_dom_url'],
                crawl_max = form.cleaned_data['crawl_max'],

                request_type = form.cleaned_data['url_type'],
                feed_link = form.cleaned_data['feed_link'],
                feed_post_request = form.cleaned_data['feed_post_request'],
                creation_date = datetime.datetime.now())
            feed.save()
        return HttpResponseRedirect('.')
    
    else:
        form = CreateFeedForm()

        #variables = RequestContext(request, {
        #    'form': form,
        #    'filename': FrameObject.filename})
        #FrameObject.filename="www.scenedownloads.pw.html"
        return render(request, 
                      'createfeed.html',
                      {'form':form,
                       'filename':FrameObject.filename})

    #template = loader.get_template('rsscore/createfeed.html')
    #return HttpResponse(template.render(request))

def showfeed(request):
    return HttpResponse("Hello thats showfeed site")


def dashboard(request,url_id):
    return HttpResponse("Hello thats dashboard site %s" % url_id)
