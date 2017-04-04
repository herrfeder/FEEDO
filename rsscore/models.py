from django.db import models
from htmldata import elementselection,request_type

class Feed(models.Model):
    def __str__(self):
        return self.feed_user+":"+self.feed_name

    feed_user = models.CharField(max_length=200)
    feed_name = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created')
    elements = elementselection

    title_dom_type = models.CharField(max_length=10, choices=elements)
    title_dom_key = models.CharField(max_length=200)
    title_dom_parent = models.CharField(max_length=200)
    title_dom_ptype = models.CharField(max_length=10, choices=elements)
    title_dom_url = models.CharField(max_length=200)

    desc_dom_type = models.CharField(max_length=10, choices=elements)
    desc_dom_key = models.CharField(max_length=200,null=True)
    desc_dom_parent = models.CharField(max_length=200,null=True)
    desc_dom_ptype = models.CharField(max_length=10,choices=elements)
    desc_dom_url = models.CharField(max_length=200)
     
    img_dom_type = models.CharField(max_length=10, choices=elements)
    img_dom_key = models.CharField(max_length=200)
    img_dom_parent = models.CharField(max_length=200)
    img_dom_ptype = models.CharField(max_length=10, choices=elements)
    img_dom_url = models.CharField(max_length=200)
    
    link_dom_type = models.CharField(max_length=10, choices=elements)
    link_dom_key = models.CharField(max_length=200)
    link_dom_parent = models.CharField(max_length=200)
    link_dom_ptype = models.CharField(max_length=10, choices=elements)
    link_dom_url = models.CharField(max_length=200)

    request_types = request_type

    request_type = models.CharField(max_length=4, choices=request_types)
    feed_link = models.CharField(max_length=200)
    feed_post_request = models.CharField(max_length=10000)

class EntryList(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    filename = models.CharField(max_length=200)

class Entry(models.Model):
    entrylist = models.ForeignKey(EntryList, on_delete=models.CASCADE)
    entry_title = models.CharField(max_length=400)
    entry_link = models.CharField(max_length=200)
    entry_description = models.CharField(max_length=400)
    entry_detail_img = models.CharField(max_length=200)
    entry_detail_text = models.CharField(max_length=1000)
