# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MarketscraperItem(scrapy.Item):
    nombre_crudo = scrapy.Field()
    contador = scrapy.Field()
    categoria = scrapy.Field()
    marca = scrapy.Field()
    descripcion = scrapy.Field()
    volumen = scrapy.Field()
    precio = scrapy.Field()
    url = scrapy.Field()
    tienda = scrapy.Field()
