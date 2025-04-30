from app.MariaDBClient import MariaDBClient
from app.MarketScraper import MarketScraper
from app.celery_tasks import fetch_market_data
from app.celery_config import app
import pandas as pd
import asyncio
import logging
from datetime import datetime


#! Celery + Redis Approach
# mariadbclient = MariaDBClient()
# supermercados = mariadbclient.get_active_tables()
# resultados = [fetch_market_data.delay(super) for super in supermercados]
# total_items = []
# total_stats = []
# for resultado in resultados:
#     items_dicts, stats_dicts = resultado.get()
#     total_items.append(pd.DataFrame(items_dicts))
#     total_stats.append(pd.DataFrame(stats_dicts))
# total_items_df = pd.concat(total_items, ignore_index=True)
# total_stats_df = pd.concat(total_stats, ignore_index=True)
# mariadbclient.insert_into_productos(total_items_df)
# mariadbclient.insert_into_db("webscraping_info", total_stats_df)
# mariadbclient.insert_into_db("historico", total_items_df)

logging.basicConfig(
    level=logging.INFO,  # nivel INFO para ver los logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)


#! Asyncio + Aiohttp Approach
async def async_scraping(supermercados):
    market_scraper = MarketScraper()

    async def process_supermercado(supermercado):
        logging.info(f"Scraping {supermercado}")
        data = await market_scraper.fetch_data(supermercado)
        items = await market_scraper.get_items(data)
        stats = await market_scraper.get_stats(data)
        logging.info(f"Scraping {supermercado} finalizado")
        return items, stats

    tasks = [process_supermercado(s) for s in supermercados]
    return await asyncio.gather(*tasks)


def main():

    start_time = datetime.now()
    logging.info("Iniciando")

    mariadbclient = MariaDBClient()
    supermercados = mariadbclient.get_active_tables()

    results = asyncio.run(async_scraping(supermercados))

    total_items = [res[0] for res in results]
    total_stats = [res[1] for res in results]

    total_items_df = pd.concat(total_items, ignore_index=True)
    total_stats_df = pd.concat(total_stats, ignore_index=True)

    mariadbclient.insert_into_productos(total_items_df)
    mariadbclient.insert_into_db("webscraping_info", total_stats_df)
    mariadbclient.insert_into_db("historico", total_items_df)

    end_time = datetime.now()
    elapsed = end_time - start_time
    logging.info(f"Finalizado en: {elapsed}")


if __name__ == "__main__":
    main()
