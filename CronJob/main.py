from app.MariaDBClient import MariaDBClient
from app.celery_tasks import fetch_market_data
from app.celery_config import app
import pandas as pd

mariadbclient = MariaDBClient()
supermercados = mariadbclient.get_active_tables()

resultados = [fetch_market_data.delay(super) for super in supermercados]

total_items = []
total_stats = []

for resultado in resultados:
    items_dicts, stats_dicts = resultado.get()
    total_items.append(pd.DataFrame(items_dicts))
    total_stats.append(pd.DataFrame(stats_dicts))

total_items_df = pd.concat(total_items, ignore_index=True)
total_stats_df = pd.concat(total_stats, ignore_index=True)

mariadbclient.insert_into_productos(total_items_df)
mariadbclient.insert_into_db("webscraping_info", total_stats_df)
mariadbclient.insert_into_db("historico", total_items_df)
