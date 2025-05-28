from main.MariaDBClient import MariaDBClient
from main.MarketScraper import MarketScraper
from main.GeminiClient import GeminiClient
from main.ResourceLockManager import ResourceLockManager
from main.celery_tasks import fetch_market_data
from main.celery_config import app
import pandas as pd
import asyncio
import logging
from datetime import datetime
import time


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
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.getLogger("google_ganai").setLevel(logging.WARNING)

#! Asyncio + Aiohttp Approach
async def async_scraping(supermercados):
    market_scraper = MarketScraper()

    async def process_supermercado(supermercado):
        logging.info(f"Scraping {supermercado}")
        data = await market_scraper.fetch_data(supermercado)
        items = await market_scraper.get_items(data)
        stats = await market_scraper.get_stats(data)
        elapsed = stats['elapsed_time_seconds'].iloc[0]
        logging.info(f"Scraping {supermercado} finalizado. {len(items)} productos recuperados en {elapsed} segundos")
        return items, stats

    tasks = [process_supermercado(s) for s in supermercados]
    return await asyncio.gather(*tasks)


def main():

    start_time = datetime.now()
    logging.info("Iniciando Web Scraping ...")

    mariadbclient = MariaDBClient()
    supermercados = mariadbclient.get_active_tables()

    results = asyncio.run(async_scraping(supermercados))

    total_items = [res[0] for res in results]
    total_stats = [res[1] for res in results]

    total_items_df = pd.concat(total_items, ignore_index=True)
    total_stats_df = pd.concat(total_stats, ignore_index=True)

    logging.info(f"Total de {len(total_items_df)} productos recuperados")
    
    lock_manager = ResourceLockManager()

    if lock_manager.acquire():
        logging.info("Locking BD")
        try:
            mariadbclient.insert_into_db("webscraping_info", total_stats_df)
            mariadbclient.insert_into_db("historico", total_items_df)

            #? Agrupacion de descripciones con Genemini

            new_items_df = total_items_df
            old_items_df = mariadbclient.get_products()

            new_only_df = new_items_df[~new_items_df['id_producto'].isin(old_items_df['id_producto'])] # type: ignore
            common_df = new_items_df[new_items_df['id_producto'].isin(old_items_df['id_producto'])]
            old_only_df = old_items_df[~old_items_df['id_producto'].isin(new_items_df['id_producto'])]

            logging.info(f"Nuevos productos: {new_only_df.shape[0]}")
            logging.info(f"Productos ya existentes: {common_df.shape[0]}")
            logging.info(f"Productos ya no existentes: {old_only_df.shape[0]}")
            mariadbclient.delete_products(old_only_df)
            logging.info(f"Se eliminaron {len(old_only_df)} productos")
            mariadbclient.update_products(common_df)
            logging.info(f"Se actualizaron {len(common_df)} productos")


            old_productos_to_update_subgroups_df = mariadbclient.get_products_by_groups(new_only_df)
            new_productos_to_update_subgroups_df = new_only_df[['id_producto', 'categoria', 'marca', 'descripcion', 'volumen', 'id_supermercado']]
            new_productos_to_update_subgroups_df = new_productos_to_update_subgroups_df.rename(columns={'id_supermercado': 'supermercado'})
            new_productos_to_update_subgroups_df['supermercado'] = new_productos_to_update_subgroups_df['supermercado'].map({
                1:"Atomo",
                2:"Blowmax",
                3:"ModoMarket",
                4:"Segal",
                5:"Supera"
            })
            all_productos_to_upsert_subgroups_df = pd.concat([new_productos_to_update_subgroups_df, old_productos_to_update_subgroups_df], ignore_index=True)
            all_productos_to_upsert_subgroups_df['producto_id'] = all_productos_to_upsert_subgroups_df['id_producto'].astype(str) + " - " + all_productos_to_upsert_subgroups_df['categoria'] + " - " + all_productos_to_upsert_subgroups_df['marca'] + " - " + all_productos_to_upsert_subgroups_df['descripcion'] + " - " + all_productos_to_upsert_subgroups_df['volumen'] + " - " + all_productos_to_upsert_subgroups_df['supermercado']

            logging.info(f"Hay {len(old_productos_to_update_subgroups_df)} productos que comparten subgrupo con los productos nuevos")
            logging.info(f"Hay {len(new_productos_to_update_subgroups_df)} productos nuevos que hay que asignar subgrupo")
            logging.info(f"Hay {len(all_productos_to_upsert_subgroups_df)} productos que hay que actualizar su subgrupo")

            grouped = all_productos_to_upsert_subgroups_df.groupby(['categoria', 'marca', 'volumen'])
            listas_productos = [group['producto_id'].tolist() for _, group in grouped]

            geminiclient = GeminiClient()
            geminiclient.api_keys

            total_elementos = sum(len(sublista) for sublista in listas_productos)
            all_responses = []

            indice = 0
            for lista_productos in listas_productos:
                prompt = listas_productos[indice]
                try:
                    if len(prompt) > 1:
                        respuesta = geminiclient.ask(prompt)
                        time.sleep(4.1)
                    else:
                        respuesta = [prompt]
                    all_responses.append(respuesta)
                    
                except Exception as e:
                    logging.error(f"Error al procesar el prompt: {prompt} . Error: {e}")
                if indice % 10 == 0:
                    logging.info(f"Gemini requests: {indice}/{len(listas_productos)}")
                indice += 1

            logging.info(f"Gemini tiene que agrupar {total_elementos} productos")
            total_agrupados = sum(len(subsublist) for sublist in all_responses for subsublist in sublist)
            logging.info(f"Gemini agrupo {total_agrupados} productos")

            if len(all_responses) > 0:
                olds_ids = set(old_productos_to_update_subgroups_df['id_producto'])
                news_ids = set(new_items_df['id_producto'])

                updates = []
                descartados = []

                new_items_index = {id_producto: idx for idx, id_producto in enumerate(new_items_df['id_producto'])}

                for respuesta in all_responses:
                    for j, subgrupo in enumerate(respuesta):
                        ids_productos = [item.partition(' - ')[0].strip() for item in subgrupo] 
                        
                        for id_producto_str in ids_productos:
                                id_producto = int(id_producto_str)
                                
                                if id_producto in olds_ids:
                                    updates.append({ 
                                        "id_producto": id_producto,
                                        "id_subgrupo": j
                                    })
                                elif id_producto in news_ids:
                                    idx = new_items_index[id_producto]
                                    new_only_df.at[idx, 'id_subgrupo'] = j
                                else:
                                    descartados.append(id_producto_str)

                mariadbclient.insert_into_productos(new_only_df)
                logging.info(f"Productos agregados: {len(updates)}")
                mariadbclient.update_product_subgroups(updates)
                logging.info(f"Productos con subgrupo actualizado: {len(new_only_df)}")
                logging.info(f"Productos descartados: {len(descartados)}")

            # ? FIN Agrupacion de descripciones con Genemini

        finally:
            lock_manager.release()
            logging.info("Liberando BD")
    else:
        logging.warning("No se pudo adquirir el lock para actualizar la base")


    end_time = datetime.now()
    elapsed = end_time - start_time
    logging.info(f"Finalizado en: {elapsed}")


if __name__ == "__main__":
    main()