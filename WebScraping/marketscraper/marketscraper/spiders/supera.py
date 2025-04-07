import scrapy
from marketscraper.items import MarketscraperItem
import re
import requests
from datetime import datetime
import os
import logging

class SuperaSpider(scrapy.Spider):
    name = "supera"
    allowed_domains = ["supera.com.ar"]
    contador = 0
    contador_paginas_shampoos = 1
    contador_paginas_gaseosas = 1
    contador_paginas_leches = 1
    contador_paginas_panes = 1
    contador_paginas_arroces = 1
    contador_paginas_jabones = 1
    contador_paginas_yerbas = 1
    contador_paginas_fideos = 1
    start_urls = [
                ("https://supera.com.ar/categoria-producto/perfumeria/cuidado-de-cabello/shampoo/", "Shampoos"),
                ("https://supera.com.ar/categoria-producto/bebidas/bebidas-sin-alcohol/gaseosas/", "Gaseosas"),
                ("https://supera.com.ar/categoria-producto/lacteos/leches-larga-vida/", "Leches"),
                ("https://supera.com.ar/categoria-producto/panificados-2/", "Panes"),
                ("https://supera.com.ar/categoria-producto/almacen/arroz/","Arroces"),
                ("https://supera.com.ar/categoria-producto/perfumeria/jabones/", "Jabones"),
                ("https://supera.com.ar/categoria-producto/almacen/yerbas/", "Yerbas"),
                ("https://supera.com.ar/categoria-producto/almacen/fideos/","Fideos")
                ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'marketscraper.pipelines.SuperaPrecioPipeline': 290,
            'marketscraper.pipelines.SuperaPipeline': 300,
            "marketscraper.pipelines.NormalizarPipeline": 350 
        }
    }

    def start_requests(self):
        for url, table_name in self.start_urls:
            yield scrapy.Request(url=url, meta={'custom_table_name': table_name})


    def parse(self, response): 
        custom_table_name = response.meta.get('custom_table_name')
        articulos = response.css("li.product")
        self.logger.info(f"Parsing URL: {response.url} - Response status: {response.status}")

        for articulo in articulos:
            nombre_crudo = articulo.css("h2 ::text").get()

            if "HAMBURGUESA" in nombre_crudo or "PANCHO" in nombre_crudo or "RALLADO" in nombre_crudo or "HAMBURGUESAS" in nombre_crudo or "PANCHOS" in nombre_crudo or "PIZZA" in nombre_crudo:
                continue
            
            if "LIQUIDO" in nombre_crudo or "LIQ" in nombre_crudo:
                continue
            
            if custom_table_name == "Fideos" and "FIDEOS" not in nombre_crudo:
                continue
            precio = articulo.css("bdi").get()
            expresion = r'\d{1,3}(?:\.\d{3})*(?:,\d+)?'
            match_precio = re.search(expresion, precio)
            precio = match_precio.group()
            url = articulo.css("a ::attr(href)").get()

            item = MarketscraperItem()

            item["nombre_crudo"] = nombre_crudo
            item["precio"] = precio 
            item["url"] = url 
            item["contador"] = self.contador
            item["categoria"] = custom_table_name
            self.contador = self.contador + 1

            yield item

            #Busca 16 articulos por vuelta

        next_page_url = None
    
        if custom_table_name == "Shampoos":
            self.contador_paginas_shampoos = self.contador_paginas_shampoos + 1
            next_page_url = "https://supera.com.ar/categoria-producto/cuidado-de-cabello/shampoo/{}/".format(self.contador_paginas_shampoos)
        elif custom_table_name == "Gaseosas":
            self.contador_paginas_gaseosas = self.contador_paginas_gaseosas + 1
            next_page_url = "https://supera.com.ar/categoria-producto/bebidas-sin-alcohol/gaseosas/{}/".format(self.contador_paginas_gaseosas)
        elif custom_table_name == "Leches":
            self.contador_paginas_leches = self.contador_paginas_leches + 1
            next_page_url = "https://supera.com.ar/categoria-producto/lacteos/leches-larga-vida/{}/".format(self.contador_paginas_leches)
        elif custom_table_name == "Panes":
            self.contador_paginas_panes = self.contador_paginas_panes + 1
            next_page_url = "https://supera.com.ar/categoria-producto/panificados-2/{}/".format(self.contador_paginas_panes)
        elif custom_table_name == "Arroces":
            self.contador_paginas_arroces = self.contador_paginas_arroces + 1
            next_page_url = "https://supera.com.ar/categoria-producto/almacen/arroz/{}/".format(self.contador_paginas_arroces)
        elif custom_table_name == "Jabones":
            self.contador_paginas_jabones = self.contador_paginas_jabones + 1
            next_page_url = "https://supera.com.ar/categoria-producto/perfumeria/jabones/{}/".format(self.contador_paginas_jabones) 
        elif custom_table_name == "Yerbas":
            self.contador_paginas_yerbas = self.contador_paginas_yerbas + 1
            next_page_url = "https://supera.com.ar/categoria-producto/almacen/yerbas/{}/".format(self.contador_paginas_yerbas)
        elif custom_table_name == "Fideos":
            self.contador_paginas_fideos = self.contador_paginas_fideos + 1
            next_page_url = "https://supera.com.ar/categoria-producto/almacen/fideos/{}/".format(self.contador_paginas_fideos)

        if next_page_url:
            respuesta = requests.get(next_page_url)
            if respuesta.status_code == 200:
                yield response.follow(next_page_url, callback=self.parse, meta={'custom_table_name': custom_table_name})