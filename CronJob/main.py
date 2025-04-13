from app.MariaDBClient import MariaDBClient
from app.tasks import fetch_market_data
import pandas as pd
# from redlock import RedLock

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

# lock =  RedLock("distributed_lock")
# lock.acquire()
#TODO Con el back implententar Redlock de Redis
mariadbclient.insert_into_productos(total_items_df)
mariadbclient.insert_into_db("webscraping_info", total_stats_df)
mariadbclient.insert_into_db("historico", total_items_df)
# lock.release()