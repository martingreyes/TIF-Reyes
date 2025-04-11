import scrapy
from marketscraper.items import MarketscraperItem
import re
import requests
import logging
from scrapy_redis.spiders import RedisSpider
import json

# class SegalSpider(scrapy.Spider):
class SegalSpider(RedisSpider):
    name = "segal"
    allowed_domains = ["www.casa-segal.com"]
    contador = 0
    contador_paginas_shampoos = 1
    contador_paginas_gaseosas = 1
    contador_paginas_leches = 1
    contador_paginas_panes = 1
    contador_paginas_arroces = 1
    contador_paginas_jabones = 1
    contador_paginas_yerbas = 1
    contador_paginas_fideos = 1

    redis_key = 'segal:start_urls'
    max_idle_time = 7

    # start_urls = [
    #             ("https://www.casa-segal.com/categoria-producto/perfumeria/shampoos/", "Shampoos"),
    #             ("https://www.casa-segal.com/categoria-producto/bebidas/gaseosas/", "Gaseosas"),
    #             ("https://www.casa-segal.com/categoria-producto/almacen/leches/","Leches"),
    #             ("https://www.casa-segal.com/categoria-producto/almacen/panificados/lacteados/","Panes"),
    #             ("https://www.casa-segal.com/categoria-producto/almacen/arroz/", "Arroces"),
    #             ("https://www.casa-segal.com/categoria-producto/perfumeria/jabon-de-tocador/", "Jabones"),
    #             ("https://www.casa-segal.com/categoria-producto/almacen/yerbas/", "Yerbas"),
    #             ("https://www.casa-segal.com/categoria-producto/almacen/fideos/","Fideos")
    #             ]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'marketscraper.pipelines.SegalPrecioPipeline': 290,
            'marketscraper.pipelines.SegalPipeline': 300,
            "marketscraper.pipelines.NormalizarPipeline": 350 
        }
    }


    def start_requests(self):
        for url, table_name in self.start_urls:
            yield scrapy.Request(url=url, meta={'categoria': table_name})
    
    def parse(self, response): 
        self.logger.info(f"Parsing URL: {response.url} - Response status: {response.status}")
        categoria = response.meta.get('categoria')
        articulos = response.css("li.product-col")

        for articulo in articulos:    
            nombre_crudo = articulo.css("h3 ::text").get()

            if categoria == "Shampoos" and "ACONDICIONADOR" in nombre_crudo:
                continue

            if categoria == "Leches" and "ACONDICIONADOR" in nombre_crudo or "ALME" in nombre_crudo or "CONDENSADA" in nombre_crudo or "POLVO" in nombre_crudo or "LA LECHERA" in nombre_crudo or "PURÍSIMA" in nombre_crudo:
                continue

            if categoria == "Panes" and not "PAN" in nombre_crudo:
                continue

            precio = articulo.css("bdi").get()
            expresion = r'\d{1,3}(?:\.\d{3})*(?:,\d+)?'
            match_precio = re.search(expresion, precio)
            precio = match_precio.group()
            url = articulo.css("a.product-loop-title ::attr(href)").get()

            item = MarketscraperItem()
            item["nombre_crudo"] = nombre_crudo
            item["precio"] = precio 
            item["url"] = url 
            item["contador"] = self.contador
            item["categoria"] = categoria
            self.contador = self.contador + 1

            yield item

            #Busca 12 articulos por vuelta

        next_page_url = None
    
        if categoria == "Shampoos":
            self.contador_paginas_shampoos = self.contador_paginas_shampoos + 1
            next_page_url = "https://www.casa-segal.com/categoria-producto/perfumeria/shampoos/page/{}/?load_posts_only=1".format(self.contador_paginas_shampoos)
        elif categoria == "Gaseosas":
            self.contador_paginas_gaseosas = self.contador_paginas_gaseosas + 1
            next_page_url = "https://www.casa-segal.com/categoria-producto/bebidas/gaseosas/page/{}/?load_posts_only=1".format(self.contador_paginas_gaseosas)
        elif categoria == "Leches":
            self.contador_paginas_leches = self.contador_paginas_leches + 1
            next_page_url = "https://www.casa-segal.com/categoria-producto/almacen/leches/page/{}/?load_posts_only=1".format(self.contador_paginas_leches)
        elif categoria == "Panes":
            self.contador_paginas_panes = self.contador_paginas_panes + 1
            next_page_url = "https://www.casa-segal.com/categoria-producto/almacen/panificados/lacteados//page{}/?load_posts_only=1".format(self.contador_paginas_panes)
        elif categoria == "Arroces":
            self.contador_paginas_arroces = self.contador_paginas_arroces + 1
            next_page_url = "https://www.casa-segal.com/categoria-producto/almacen/arroz/page{}/?load_posts_only=1".format(self.contador_paginas_arroces)
        elif categoria == "Jabones":
            self.contador_paginas_jabones = self.contador_paginas_jabones + 1
            next_page_url = "https://www.casa-segal.com/categoria-producto/perfumeria/jabon-de-tocador/page{}/?load_posts_only=1".format(self.contador_paginas_jabones)
        elif categoria == "Yerbas":
            self.contador_paginas_yerbas = self.contador_paginas_yerbas + 1
            next_page_url = "https://www.casa-segal.com/categoria-producto/almacen/yerbas/page{}/?load_posts_only=1".format(self.contador_paginas_yerbas)
        elif categoria == "Fideos":
            self.contador_paginas_fideos= self.contador_paginas_fideos + 1
            next_page_url = "https://www.casa-segal.com/categoria-producto/almacen/fideos/page/{}/?load_posts_only=1".format(self.contador_paginas_fideos)


        if next_page_url:
            respuesta = requests.get(next_page_url)
            if respuesta.status_code == 200:
                url_key = f"{self.redis_key}:seen_urls"
                if not self.server.sismember(url_key, next_page_url):
                    self.server.sadd(url_key, next_page_url)
                    self.server.rpush(
                        self.redis_key,
                        json.dumps({
                            'url': next_page_url,
                            'meta': {'categoria': categoria}
                        })
                    )
                    # yield response.follow(next_page_url, callback=self.parse, meta={'categoria': categoria})