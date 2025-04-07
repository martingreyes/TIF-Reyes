import scrapy
from marketscraper.items import MarketscraperItem
import logging

class AtomoSpider(scrapy.Spider):
    name = "atomo"
    allowed_domains = ["atomoconviene.com"]
    contador = 0
    start_urls = [
        ("https://atomoconviene.com/atomo-ecommerce/135-shampoo", "Shampoos"),
        ("https://atomoconviene.com/atomo-ecommerce/95-gaseosas", "Gaseosas"),
        ("https://atomoconviene.com/atomo-ecommerce/234-leches-larga-vida", "Leches"),
        ("https://atomoconviene.com/atomo-ecommerce/58-pan-lactal", "Panes"),
        ("https://atomoconviene.com/atomo-ecommerce/20-arroz", "Arroces"),
        ("https://atomoconviene.com/atomo-ecommerce/21-arroz-listo", "Arroces"),
        ("https://atomoconviene.com/atomo-ecommerce/151-jabones", "Jabones"),
        ("https://atomoconviene.com/atomo-ecommerce/49-yerba-mate", "Yerbas"),
        ("https://atomoconviene.com/atomo-ecommerce/32-pastas-secas-y-salsas","Fideos")
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'marketscraper.pipelines.AtomoPrecioPipeline': 290,
            'marketscraper.pipelines.AtomoPipeline': 300,
            "marketscraper.pipelines.NormalizarPipeline": 400
        }
    }


    def start_requests(self):
        for url, categoria in self.start_urls:
            yield scrapy.Request(url=url, meta={'categoria': categoria})

    def parse(self, response):  
        self.logger.info(f"Parsing URL: {response.url} - Response status: {response.status}")
        categoria = response.meta.get('categoria')
        articulos = response.css("article.product-miniature")

        for articulo in articulos:
            nombre_crudo = articulo.css("h2 a::text").get()

            if categoria == "Leches" and "CC." not in nombre_crudo and "LTS." not in nombre_crudo or "CHOCO" in nombre_crudo:
                continue

            if categoria == "Jabones" and "LIQUIDO" in nombre_crudo:
                continue

            if categoria == "Fideos" and "FIDEOS" not in nombre_crudo:
                continue

            precio = articulo.css("span.price::text").get()
            url = articulo.css("h2 a").attrib["href"]

            item = MarketscraperItem()
            item["nombre_crudo"] = nombre_crudo
            item["precio"] = precio 
            item["url"] = url 
            item["contador"] = self.contador
            item["categoria"] = categoria
            self.contador += 1
            
            yield item

        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta={'categoria': categoria})
