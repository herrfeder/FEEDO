from django import forms
from rsscore.models import elementselection,request_type 

class PostRequest(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'size':40}))
class CreateFeedForm(forms.Form):

    feedname = forms.CharField(max_length=100, min_length=1, label="Feed Name")
   
    title_dom_type = forms.ChoiceField(widget=forms.Select,
                                       choices=elementselection,
                                       label = "Title Dom Type")   
    title_dom_key = forms.CharField(max_length=200,  
                                    required=False,
                                    label="Title Dom Key")
    title_dom_parent = forms.CharField(max_length=200,
                                       min_length=1,
                                       label="Parent of title")
    title_dom_ptype = forms.ChoiceField(widget=forms.Select,
                                       choices=elementselection,
                                       label = "Title Parent Type")   

    title_dom_url = forms.CharField(max_length=2,
                                    label="Url of title")


    desc_dom_type = forms.ChoiceField(widget=forms.Select,
                                      choices=elementselection,
                                      required=False,
                                      label="Description Dom Type")
    desc_dom_key = forms.CharField(max_length=1000, 
                                   required=False, 
                                   label="Description Dom Key")
    desc_dom_parent = forms.CharField(max_length=200,
                                      required=False,
                                      label="Parent of description")
    desc_dom_ptype = forms.ChoiceField(widget=forms.Select,
                                       choices=elementselection,
                                       required=False,
                                       label = "Desc Parent Type")   

    desc_dom_url = forms.CharField(max_length=200,
                                   required=False,
                                   label="Url of description")
    
    
    img_dom_type = forms.ChoiceField(widget=forms.Select,
                                      choices=elementselection,
                                      required=False,
                                      label="Image Dom Type")
    img_dom_key = forms.CharField(max_length=200, 
                                   required=False, 
                                   label="Image Dom Key")
    img_dom_parent = forms.CharField(max_length=200,
                                      required=False,
                                      label="Parent of image")
    img_dom_ptype = forms.ChoiceField(widget=forms.Select,
                                       choices=elementselection,
                                       required=False,
                                       label = "Img Parent Type")   
    img_dom_url = forms.CharField(max_length=200,
                                   required=False,
                                   label="Url of image")


    link_dom_type = forms.ChoiceField(widget=forms.Select,
                                      choices=elementselection,
                                      label="Link Dom Type") 
    link_dom_key = forms.CharField(max_length=200,
                                   required=False,
                                   label="Link Dom Key")
    link_dom_parent = forms.CharField(max_length=200,
                                      min_length=1,
                                      label="Parent of Link")
    link_dom_ptype = forms.ChoiceField(widget=forms.Select,
                                       choices=elementselection,
                                       label = "Link Parent Type")   

    link_dom_url = forms.CharField(max_length=200,
                                   label="Url of link")
    
    crawl_dom_type = forms.ChoiceField(widget=forms.Select,
                                      choices=elementselection,
                                      label="Crawl Dom Type")
 
    crawl_dom_key = forms.CharField(max_length=200,
                                   required=False,
                                   label="Crawl Dom Key")
    crawl_dom_parent = forms.CharField(max_length=200,
                                      required=False,
                                      label="Crawl of Link")
    crawl_dom_ptype = forms.ChoiceField(widget=forms.Select,
                                       choices=elementselection,
                                       required=False,
                                       label = "Crawl Parent Type")   
    crawl_max = forms.ChoiceField(widget=forms.Select,
                                       choices=((str(x), x) for x in
                                                range(1,32)),
                                       required=False,
                                       label = "Crawl Sites Maximum")   
    crawl_dom_url = forms.CharField(max_length=200,
                                   required=False,
                                   label="Url of Crawl")

    url_type = forms.ChoiceField(widget=forms.Select,
                                 choices=request_type,
                                 label="URL Type")
    

    feed_link = forms.CharField(max_length=1000, 
                               min_length=1, 
                               label="Feed Link")
    
    feed_post_request = \
    forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows':
                                                 3}),label="Post Request",required=False)
