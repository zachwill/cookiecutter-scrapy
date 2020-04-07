# -*- coding: utf-8 -*-
from fake_useragent import UserAgent


BOT_NAME = "{{cookiecutter.repo_name}}"
SPIDER_MODULES = ["{{cookiecutter.repo_name}}.spiders"]
NEWSPIDER_MODULE = "{{cookiecutter.repo_name}}.spiders"

LOG_FILE = "history.log"

# Do not obey robots.txt
ROBOTSTXT_OBEY = False

# Sometimes `fake_useragent` errors out...
try:
    user_agent = UserAgent().random
except:
    user_agent = UserAgent().chrome

USER_AGENT = user_agent

# Configure maximum concurrent requests performed by Scrapy (default: 16)
DOWNLOAD_DELAY = 0.1
CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN = 20

# Cookies
COOKIES_ENABLED = False

# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.cookies.CookiesMiddleware": 400,
    "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 300,
}

# Configure item pipelines
ITEM_PIPELINES = {
    "{{cookiecutter.repo_name}}.pipelines.ModelPipeline": 300,
}

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = True
# HTTPCACHE_DIR = ".cache"
# HTTPCACHE_GZIP = True
# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.RFC2616Policy"
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
