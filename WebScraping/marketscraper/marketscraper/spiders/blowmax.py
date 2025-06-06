from marketscraper.items import MarketscraperItem
import requests
from scrapy_redis.spiders import RedisSpider
import re
import json
from scrapy import signals

class BlowmaxSpider(RedisSpider):
    name = "blowmax"
    allowed_domains = ["blowmax.com.ar"]
    contador = 0
    contador_paginas_shampoos = 1
    contador_paginas_gaseosas = 1
    contador_paginas_leches = 1
    contador_paginas_panes = 1
    contador_paginas_arroces = 1
    contador_paginas_jabones = 1
    contador_paginas_yerbas = 1
    contador_paginas_fideos = 1
    redis_key = 'blowmax:start_urls'
    max_idle_time = 7

    start_urls = [
                ("https://blowmax.com.ar/categoria-producto/perfumeria/cuidado-de-cabello/shampoo/", "Shampoos"),
                ("https://blowmax.com.ar/categoria-producto/bebidas/bebidas-sin-alcohol/gaseosas/", "Gaseosas"),
                ("https://blowmax.com.ar/categoria-producto/lacteos/leches-larga-vida/","Leches"),
                ("https://blowmax.com.ar/categoria-producto/panificados/", "Panes"),
                ("https://blowmax.com.ar/categoria-producto/almacen/arroz/", "Arroces"),               
                ("https://blowmax.com.ar/categoria-producto/perfumeria/jabones/","Jabones"),
                # ("https://blowmax.com.ar/categoria-producto/almacen/fideos/","Fideos"),           
                # ("https://blowmax.com.ar/?s=arroz&post_type=product&dgwt_wcas=1" , "Arroces"),    
                ("https://blowmax.com.ar/?s=yerba&post_type=product&dgwt_wcas=1","Yerbas"),
                ("https://blowmax.com.ar/?s=fideos&post_type=product&dgwt_wcas=1","Fideos")
                ]
    
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 20,
        # 'RETRY_ENABLED': True,
        # 'RETRY_TIMES': 2,
        # 'REDIS_IDLE_BEFORE_CLOSE': 10,
        'ITEM_PIPELINES': {
            'marketscraper.pipelines.BlowmaxPrecioPipeline': 290,
            'marketscraper.pipelines.BlowmaxPipeline': 300,  
            "marketscraper.pipelines.NormalizarPipeline": 350     
        }
    }



    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BlowmaxSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider

    def spider_opened(self):
        self.logger.info(f"Spider abierto. Cargando urls en Redis ...")
        self.server.delete(self.redis_key)
        for url, categoria in self.start_urls:
            self.server.rpush(
                self.redis_key,
                json.dumps({
                    "url": url,
                    "meta": {"categoria": categoria}
                })
            )

        
    def closed(self, reason):
        self.logger.info(f"Spider cerrado con razón: {reason}. Limpiando claves Redis.")
        self.server.delete(self.redis_key)
        self.server.delete(f"{self.redis_key}:seen_urls")    

    def parse(self, response):
        self.logger.info(f"Parsing URL: {response.url} - Response status: {response.status}")
        categoria = response.meta.get('categoria')
        articulos = response.css("li.jet-woo-builder-product")

        for articulo in articulos:
            
            nombre_crudo = articulo.css("h2 a::text").get()

            if categoria == "Shampoos" and not nombre_crudo.startswith("SH"):
                continue

            if categoria == "Gaseosas" and "GASEOSA" not in nombre_crudo:
                continue

            if categoria == "Panes" and ("PANCHO" in nombre_crudo or "PAN DE MIGA" in nombre_crudo  or "TORTILLAS" in nombre_crudo or "PAN" not in nombre_crudo or "HAMBURGUESA" in nombre_crudo):
                continue

            if categoria == "Jabones" and ("LIQUIDO" in nombre_crudo or "LIQ" in nombre_crudo):
                continue
            
            # if categoria == "Arroces" and not nombre_crudo.startswith("ARROZ"):
            #     continue

            # if categoria == "Fideos" and not nombre_crudo.startswith("FIDEOS"):
            #     continue
        
            # if categoria == "Leches" and "CHOCO" in nombre_crudo:
            #     continue


            precio = articulo.css("bdi").get()
            match = re.search(r'\xa0(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)<\/bdi>', precio)
            precio = match.group(1)
            url = articulo.css("h2.elementor-heading-title ::attr(href)").get()

            item = MarketscraperItem()
            item["nombre_crudo"] = nombre_crudo
            item["precio"] = precio 
            item["url"] = url 
            item["contador"] = self.contador
            item["categoria"] = categoria
            self.contador += 1
           
            
            yield item 


        next_page_url = None
    
        if categoria == "Shampoos":
            self.contador_paginas_shampoos = self.contador_paginas_shampoos + 1
            next_page_url = "https://blowmax.com.ar/categoria-producto/perfumeria/cuidado-de-cabello/shampoo/page/{}/".format(self.contador_paginas_shampoos)
                    
                            
        elif categoria == "Gaseosas":
            self.contador_paginas_gaseosas = self.contador_paginas_gaseosas + 1
            next_page_url = "https://blowmax.com.ar/categoria-producto/bebidas/bebidas-sin-alcohol/gaseosas/page/{}/".format(self.contador_paginas_gaseosas)
                            
        elif categoria == "Leches":
            self.contador_paginas_leches = self.contador_paginas_leches + 1
            next_page_url = "https://blowmax.com.ar/categoria-producto/lacteos/leches-larga-vida/page/{}/".format(self.contador_paginas_leches)
        elif categoria == "Panes":
            self.contador_paginas_panes = self.contador_paginas_panes + 1
            next_page_url = "https://blowmax.com.ar/categoria-producto/panificados/page/{}/".format(self.contador_paginas_panes)
        elif categoria == "Arroces":
            self.contador_paginas_arroces = self.contador_paginas_arroces + 1
            next_page_url = "https://blowmax.com.ar/categoria-producto/almacen/arroz/page/{}/".format(self.contador_paginas_arroces)
                            
        elif categoria == "Jabones":
            self.contador_paginas_jabones = self.contador_paginas_jabones + 1
            next_page_url = "https://blowmax.com.ar/categoria-producto/perfumeria/jabones/page/{}/".format(self.contador_paginas_jabones)
        elif categoria == "Yerbas":
            self.contador_paginas_yerbas = self.contador_paginas_yerbas + 1
            next_page_url = "https://blowmax.com.ar/page/{}?s=yerba&post_type=product&dgwt_wcas=1".format(self.contador_paginas_yerbas)
        elif categoria == "Fideos":
            self.contador_paginas_fideos= self.contador_paginas_fideos + 1
            next_page_url = "https://blowmax.com.ar/page/{}/?s=fideos&post_type=product&dgwt_wcas=1".format(self.contador_paginas_fideos)
            # next_page_url = "https://blowmax.com.ar/categoria-producto/almacen/fideos/page/{}/".format(self.contador_paginas_fideos)

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
      




