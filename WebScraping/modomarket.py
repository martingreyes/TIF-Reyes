import scrapy


class ModomarketSpider(scrapy.Spider):
    name = "modomarket"
    allowed_domains = ["www.modomarket.com"]
    start_urls = ["https://www.modomarket.com"]

    def parse(self, response):
        pass
