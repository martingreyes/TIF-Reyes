# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from marketscraper.pipelinesAtomo.pipelines import AtomoPrecioPipeline, AtomoPipeline
from marketscraper.pipelinesBlowmax.pipelines import BlowmaxPrecioPipeline, BlowmaxPipeline
from marketscraper.pipelinesSegal.pipelines import SegalPrecioPipeline, SegalPipeline
from marketscraper.pipelinesSupera.pipelines import SuperaPrecioPipeline, SuperaPipeline
from marketscraper.pipelinesModoMarket.pipelines import ModoMarketPrecioPipeline, ModoMarketPipeline
from marketscraper.pipelinesNormalizar.pipelines import NormalizarPipeline


class MarketscraperPipeline:
    def process_item(self, item, spider):
        return item
