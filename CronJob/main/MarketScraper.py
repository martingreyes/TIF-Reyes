import hashlib
import numpy
import pandas as pd # type: ignore
import os
from datetime import datetime
from dotenv import load_dotenv
import aiohttp
import requests
from zoneinfo import ZoneInfo


load_dotenv()

class MarketScraper:
    def __init__(self):
        self.host = os.getenv("ENDPOINT_HOST")
        self.port = os.getenv("ENDPOINT_PORT")
        self.url = 'http://{}:{}/crawl.json?start_requests=true&spider_name='.format(self.host, self.port)  

    # def fetch_data(self, spider_name: str) -> dict:
    #     response = requests.get(self.url+spider_name)
    #     response.raise_for_status()
    #     return response.json()

    async def fetch_data(self, spider_name: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + spider_name) as response:
                response.raise_for_status()
                return await response.json()
    
    async def get_items(self, data: dict) -> pd.DataFrame:
    # def get_items(self, data: dict) -> pd.DataFrame:
        timestamp = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
        spider_name = data.get("spider_name")
        items = data.get("items", [])
        df = pd.DataFrame(items)

        df["__ingestion_timestamp"] = timestamp

        df["id_producto"] = df.apply(
            lambda row: int(hashlib.sha256(
                f"{str(row['marca']).strip().lower().replace(' ', '')}_"
                f"{str(row['descripcion']).strip().lower().replace(' ', '')}_"
                f"{str(row['volumen'])}_"
                f"{str(row['tienda']).strip().lower().replace(' ', '')}".encode("utf-8")
            ).hexdigest()[:8], 16),
            axis=1
        )


        df = df.drop_duplicates(subset='id_producto', keep='first') 

        df["nombre"] = df["marca"].astype(str) + " " + df["descripcion"].astype(str) + " " + df["volumen"].astype(str)

        df["tienda"] = df["tienda"].map({
            "Atomo": 1,
            "Blowmax": 2,
            "ModoMarket": 3,
            "Segal": 4,
            "Supera": 5
        })

        df['id_grupo'] = df.apply(
            lambda row: int(hashlib.sha256(
                f"{row['marca'].strip().lower()}_{row['categoria'].strip().lower()}_{row['volumen'].strip().lower()}".encode("utf-8")
            ).hexdigest()[:8], 16), 
            axis=1
        )

        df['id_subgrupo'] = numpy.nan

 
        return df[
            ["__ingestion_timestamp", "nombre_crudo", "id_producto","categoria","nombre", "marca", "descripcion", "volumen", "precio", "tienda", "id_grupo", "id_subgrupo","url"]
        ].rename(columns={"tienda": "id_supermercado"})
    

    async def get_stats(self, data: dict) -> pd.DataFrame:
    # def get_stats(self, data: dict) -> pd.DataFrame:
        timestamp = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))

        stats = {
            "__ingestion_timestamp": timestamp,
            "spider_name": data.get("spider_name", None),
            "item_scraped_count": data.get("stats").get("item_scraped_count", None),
            "elapsed_time_seconds": data.get("stats").get("elapsed_time_seconds", None)
        }

        return pd.DataFrame([stats])
