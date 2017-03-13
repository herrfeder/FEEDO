# Scrapy settings for feedbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import sys
sys.path.insert(0, '/home/herrfeder/ownCloud/IT/Programmierung/Python/FEEDO/')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'FEEDO.settings'
import django ;django.setup()
BOT_NAME = 'feedbot'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['feedbot.spiders']
NEWSPIDER_MODULE = 'feedbot.spiders'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

ITEM_PIPELINES = {
    'feedbot.pipelines.FeedbotPipeline': 1000,
}

SPLASH_URL = 'http://127.0.0.1:8050'

SPIDER_MIDDLEWARES = {
        'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'


