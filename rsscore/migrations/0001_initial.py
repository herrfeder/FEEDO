# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_title', models.CharField(max_length=400)),
                ('entry_link', models.CharField(max_length=200)),
                ('entry_description', models.CharField(max_length=400)),
                ('entry_detail_img', models.CharField(max_length=200)),
                ('entry_detail_text', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed_user', models.CharField(max_length=200)),
                ('feed_name', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField(verbose_name=b'date created')),
                ('title_dom_type', models.CharField(max_length=10, choices=[(b'html', b'HTML'), (b'head', b'HEAD'), (b'title', b'TITLE'), (b'body', b'BODY'), (b'div', b'DIV'), (b'h1', b'H1'), (b'h2', b'H2'), (b'h3', b'H3'), (b'p', b'P'), (b'ul', b'UL'), (b'ol', b'OL'), (b'li', b'LI'), (b'img', b'IMG'), (b'a', b'A')])),
                ('title_dom_key', models.CharField(max_length=200)),
                ('title_dom_parent', models.CharField(max_length=200)),
                ('title_dom_url', models.CharField(max_length=200)),
                ('desc_dom_type', models.CharField(max_length=10, choices=[(b'html', b'HTML'), (b'head', b'HEAD'), (b'title', b'TITLE'), (b'body', b'BODY'), (b'div', b'DIV'), (b'h1', b'H1'), (b'h2', b'H2'), (b'h3', b'H3'), (b'p', b'P'), (b'ul', b'UL'), (b'ol', b'OL'), (b'li', b'LI'), (b'img', b'IMG'), (b'a', b'A')])),
                ('desc_dom_key', models.CharField(max_length=200, null=True)),
                ('desc_dom_parent', models.CharField(max_length=200, null=True)),
                ('desc_dom_url', models.CharField(max_length=200)),
                ('img_dom_type', models.CharField(max_length=10, choices=[(b'html', b'HTML'), (b'head', b'HEAD'), (b'title', b'TITLE'), (b'body', b'BODY'), (b'div', b'DIV'), (b'h1', b'H1'), (b'h2', b'H2'), (b'h3', b'H3'), (b'p', b'P'), (b'ul', b'UL'), (b'ol', b'OL'), (b'li', b'LI'), (b'img', b'IMG'), (b'a', b'A')])),
                ('img_dom_key', models.CharField(max_length=200)),
                ('img_dom_parent', models.CharField(max_length=200)),
                ('img_dom_url', models.CharField(max_length=200)),
                ('request_type', models.CharField(max_length=4, choices=[(b'get', b'GET'), (b'post', b'POST')])),
                ('feed_link', models.CharField(max_length=200)),
                ('feed_post_request', models.CharField(max_length=10000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entrylist',
            name='feed',
            field=models.ForeignKey(to='rsscore.Feed'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='entrylist',
            field=models.ForeignKey(to='rsscore.EntryList'),
            preserve_default=True,
        ),
    ]
