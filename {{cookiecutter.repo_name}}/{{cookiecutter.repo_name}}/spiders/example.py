# -*- coding: utf-8 -*-

"""
Scrape some sort of website...
"""

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from {{cookiecutter.repo_name}}.items import DefaultLoader


class ExampleSpider(CrawlSpider):

    name = "example"
    allowed_domains = ["example.com"]
    spider_url = "http://www.example.com?id={season}"

    rules = (
        Rule(
            LinkExtractor(
                allow=r"-p=\d+",
                restrict_css=[".linkNavigation a"],
            ),
            callback="parse_site",
            follow=True,
        ),
    )

    def start_requests(self):
        for _id in range(1, 10 + 1):
            url = self.spider_url.format(id=_id)
            meta = {"pass_through": True}
            yield Request(url, meta=meta, callback=self.parse_preseason)

    def parse_site(self, response):
        # Make sure this URL runs through the LinkExtractor...
        if "pass_through" in response.meta:
            yield Request(response.url, dont_filter=True, callback=self.parse)

        for row in response.css("#result").css("tr.odd, tr.even"):
            load = DefaultLoader({}, row)
            yield load.load_item()
