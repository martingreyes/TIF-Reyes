import scrapy
from marketscraper.items import MarketscraperItem


class ModomarketSpider(scrapy.Spider):
    name = "modomarket"
    allowed_domains = ["www.modomarket.com"]
    contador_shampoos = 0
    contador_gaseosas = 0
    contador_leches = 0
    contador_panes = 0
    contador_arroces = 0
    contador_arroces2 = 0
    contador_jabones = 0
    contador_yerbas = 0
    contador_fideos = 0
    

    start_urls = [
    ("https://www.modomarket.com/api/catalog_system/pub/products/search/perfumeria/cuidado-capilar/shampoo?&_from=0&_to=17&O=OrderByScoreDESC","Shampoos"),
    ("https://www.modomarket.com/api/catalog_system/pub/products/search/bebidas/gaseosas?&_from=0&_to=17&O=OrderByScoreDESC", "Gaseosas"),
    ("https://www.modomarket.com/api/catalog_system/pub/products/search/lacteos/leches/leches-refrigeradas-y-lar?&_from=0&_to=17&O=OrderByScoreDESC", "Leches"),
    ("https://www.modomarket.com/api/catalog_system/pub/products/search/almacen/panificados/pan-lactal?&_from=0&_to=17&O=OrderByScoreDESC","Panes"),
    ("https://www.modomarket.com/api/catalog_system/pub/products/search/almacen/arroz-y-legumbres/arroz?&_from=0&_to=17&O=OrderByScoreDESC","Arroces"),
    ("https://www.modomarket.com/api/catalog_system/pub/products/search/almacen/arroz-y-legumbres/arroz-listo?&_from=0&_to=17&O=OrderByScoreDESC", "Arroces2"),
    ("https://www.modomarket.com/api/catalog_system/pub/products/search/perfumeria/cuidado-personal/jabones?&_from=0&_to=17&O=OrderByScoreDESC", "Jabones" ),
    ("https://www.modomarket.com/api/catalog_system/pub/products/search/almacen/desayuno-y-merienda/yerbas?&_from=0&_to=17&O=OrderByScoreDESC", "Yerbas"),
    ("https://www.modomarket.com/api/catalog_system/pub/products/search/almacen/pastas-secas-y-salsas?&_from=0&_to=17&O=OrderByScoreDESC", "Fideos")
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'marketscraper.pipelines.ModoMarketPrecioPipeline': 290,
            'marketscraper.pipelines.ModoMarketPipeline': 300,
            "marketscraper.pipelines.NormalizarPipeline": 350,
            # "marketscraper.pipelines.SaveToMariaDBPipeline": 400  
        }
    }


    #TODO Revisar Arroz, Jabones y Pastas


    def start_requests(self):
        for url, categoria in self.start_urls:
            yield scrapy.Request(url=url, meta={'categoria': categoria})


    def parse(self, response):
        categoria = response.meta.get('categoria')
        resp =response.json()

        if not resp:
            return

        for x in range(len(resp)):

            item = MarketscraperItem()
            item["nombre_crudo"] = resp[x]["productName"]
            nombre_crudo = resp[x]["productName"]
            
            if categoria == "Panes" and not nombre_crudo.startswith("Pan"):
                self.contador_panes += 1
                continue

            if categoria == "Shampoos" and not nombre_crudo.startswith("Shampoo"):
                self.contador_shampoos += 1
                continue
            
            if categoria == "Leches" and not nombre_crudo.startswith("Leche"):
                self.contador_leches += 1
                continue

            if categoria == "Pan" and not nombre_crudo.startswith("Pan"):
                self.contador_panes += 1
                continue

            if categoria == "Arroces" and not nombre_crudo.startswith("Arroz"):
                self.contador_arroces += 1
                continue

            if categoria == "Arroces2" and not nombre_crudo.startswith("Arroz"):
                self.contador_arroces2 += 1
                continue

            if categoria == "Jabones" and "Líquido" in nombre_crudo or "Liq" in nombre_crudo:
                self.contador_jabones += 1
                continue

            if categoria == "Yerbas" and "Mate Cocido" in nombre_crudo:
                self.contador_yerbas += 1
                continue

            if categoria == "Fideos" and "Fideos" not in nombre_crudo:
                self.contador_fideos += 1
                continue


            
            try:
                item["precio"] = resp[x]["items"][0]['sellers'][0]['commertialOffer']['Installments'][0]["Value"]
                item["url"] = resp[x]["link"]
                item["categoria"] = categoria
                if categoria == "Arroces2":
                    item["categoria"] = "Arroces"

            except IndexError:
                print(f"\nError: IndexError - No se puede acceder al elemento en la posición {x} de la lista.")
                continue

            if categoria == "Shampoos":
                item["contador"] = self.contador_shampoos
                self.contador_shampoos += 1
            if categoria == "Gaseosas":
                item["contador"] = self.contador_gaseosas
                self.contador_gaseosas += 1
            if categoria == "Leches":
                item["contador"] = self.contador_leches
                self.contador_leches += 1
            if categoria == "Panes":
                item["contador"] = self.contador_panes
                self.contador_panes += 1
            if categoria == "Arroces":
                item["contador"] = self.contador_arroces
                self.contador_arroces += 1
            if categoria == "Arroces2":
                item["contador"] = self.contador_arroces2
                self.contador_arroces2 += 1
            if categoria == "Jabones":
                item["contador"] = self.contador_jabones
                self.contador_jabones += 1
            if categoria == "Yerbas":
                item["contador"] = self.contador_yerbas
                self.contador_yerbas += 1
            if categoria == "Fideos":
                item["contador"] = self.contador_fideos
                self.contador_fideos += 1
            
            yield item
      
        if categoria == "Shampoos":
            next_page_url = f"{response.url.split('&_from=')[0]}&_from={self.contador_shampoos}&_to={self.contador_shampoos + 17}&O=OrderByScoreDESC"
        if categoria == "Gaseosas":
            next_page_url = f"{response.url.split('&_from=')[0]}&_from={self.contador_gaseosas}&_to={self.contador_gaseosas + 17}&O=OrderByScoreDESC"
        if categoria == "Leches":
            next_page_url = f"{response.url.split('&_from=')[0]}&_from={self.contador_leches}&_to={self.contador_leches + 17}&O=OrderByScoreDESC"
        if categoria == "Panes":
            next_page_url = f"{response.url.split('&_from=')[0]}&_from={self.contador_panes}&_to={self.contador_panes + 17}&O=OrderByScoreDESC"
        if categoria == "Arroces":
            next_page_url = f"{response.url.split('&_from=')[0]}&_from={self.contador_arroces}&_to={self.contador_arroces + 17}&O=OrderByScoreDESC"
        if categoria == "Arroces2":
            next_page_url = f"{response.url.split('&_from=')[0]}&_from={self.contador_arroces2}&_to={self.contador_arroces2 + 17}&O=OrderByScoreDESC"
        if categoria == "Jabones":
            next_page_url = f"{response.url.split('&_from=')[0]}&_from={self.contador_jabones}&_to={self.contador_jabones + 17}&O=OrderByScoreDESC"
        if categoria == "Yerbas":
            next_page_url = f"{response.url.split('&_from=')[0]}&_from={self.contador_yerbas}&_to={self.contador_yerbas + 17}&O=OrderByScoreDESC"
        if categoria == "Fideos":
            next_page_url = f"{response.url.split('&_from=')[0]}&_from={self.contador_fideos}&_to={self.contador_fideos + 17}&O=OrderByScoreDESC"

        yield scrapy.Request(url=next_page_url, callback=self.parse,meta={'categoria': categoria})



    #TODO La tienda ModoMarket utiliza AJAX (?) (scrollear para que se carguen mas productos). Para ello:
    #? https://pypi.org/project/scrapy-ajax-utils/
    #? https://codehunter.cc/a/python/can-scrapy-be-used-to-scrape-dynamic-content-from-websites-that-are-using-ajax
    #? sino con: https://docs.scrapy.org/en/latest/topics/dynamic-content.html
    #? https://www.youtube.com/watch?v=07FYDHTV73Y&ab_channel=Python360
    #? https://www.attilatoth.dev/posts/scrapy-ajax/

        # https://www.modomarket.com/api/catalog_system/pub/products/search/perfumeria/cuidado-capilar/shampoo?&_from=72&_to=89&O=OrderByScoreDESC
        

                # "https://www.modomarket.com/perfumeria/cuidado-capilar/shampoo"
                # "https://www.modomarket.com/bebidas/gaseosas",
                # "https://www.modomarket.com/lacteos/leches/leches-refrigeradas-y-lar",
                # "https://www.modomarket.com/almacen/panificados/pan-lactal",
                # "https://www.modomarket.com/almacen/arroz-y-legumbres/arroz",
                # "https://www.modomarket.com/almacen/arroz-y-legumbres/arroz-listo",
                # "https://www.modomarket.com/perfumeria/cuidado-personal/jabones",
                # "https://www.modomarket.com/almacen/desayuno-y-merienda/yerbas",
                # "https://www.modomarket.com/almacen/pastas-secas-y-salsas"  