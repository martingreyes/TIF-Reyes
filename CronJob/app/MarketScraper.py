from zoneinfo import ZoneInfo
import requests
import pandas as pd # type: ignore
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MarketScraper:
    def __init__(self):
        self.host = os.getenv("ENDPOINT_HOST")
        self.port = os.getenv("ENDPOINT_PORT")
        self.url = 'http://{}:{}/crawl.json?start_requests=true&spider_name='.format(self.host, self.port)  

    def fetch_data(self, spider_name: str) -> dict:
        response = requests.get(self.url+spider_name)
        response.raise_for_status()
        return response.json()
    
    def get_items(self, data: dict) -> pd.DataFrame:
      
        ARGENTINA_TZ = ZoneInfo("America/Argentina/Buenos_Aires")
        timestamp = datetime.now(ARGENTINA_TZ)
        spider_name = data.get("spider_name")
        items = data.get("items", [])
        df = pd.DataFrame(items)

        df["__ingestion_timestamp"] = timestamp
        df["nombre"] = df["marca"].astype(str) + " " + df["descripcion"].astype(str) + " " + df["volumen"].astype(str)

        df["tienda"] = df["tienda"].map({
            "Atomo": 1,
            "Blowmax": 2,
            "ModoMarket": 3,
            "Segal": 4,
            "Supera": 5
        })

 
        return df[
            ["__ingestion_timestamp", "nombre_crudo", "nombre", "marca", "descripcion", "volumen", "precio", "tienda", "url"]
        ].rename(columns={"tienda": "id_supermercado"})

    def get_stats(self, data: dict) -> pd.DataFrame:
        ARGENTINA_TZ = ZoneInfo("America/Argentina/Buenos_Aires")
        timestamp = datetime.now(ARGENTINA_TZ)

        stats = {
            "__ingestion_timestamp": timestamp,
            "spider_name": data.get("spider_name", None),
            "item_scraped_count": data.get("stats").get("item_scraped_count", None),
            "elapsed_time_seconds": data.get("stats").get("elapsed_time_seconds", None)
        }

        return pd.DataFrame([stats])
