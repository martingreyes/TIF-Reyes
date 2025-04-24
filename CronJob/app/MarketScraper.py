import hashlib
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
      
        timestamp = datetime.now()
        spider_name = data.get("spider_name")
        items = data.get("items", [])
        df = pd.DataFrame(items)

        df["__ingestion_timestamp"] = timestamp

        df["id_producto"] = df.apply(
            lambda row: int(hashlib.sha256(
                f"{row['marca']}_{row['descripcion']}_{row['volumen']}_{row['tienda']}".encode("utf-8")
            ).hexdigest()[:8], 16),  # Tomamos solo los primeros 8 caracteres
            axis=1
        )

        df["nombre"] = df["marca"].astype(str) + " " + df["descripcion"].astype(str) + " " + df["volumen"].astype(str)

        df["tienda"] = df["tienda"].map({
            "Atomo": 1,
            "Blowmax": 2,
            "ModoMarket": 3,
            "Segal": 4,
            "Supera": 5
        })

        #TODO DROP DUPLCATES ID_PRODUCTO (QUE SOLO QUEDE 1) 

 
        return df[
            ["__ingestion_timestamp", "nombre_crudo", "id_producto","categoria","nombre", "marca", "descripcion", "volumen", "precio", "tienda", "url"]
        ].rename(columns={"tienda": "id_supermercado"})
    

    def get_stats(self, data: dict) -> pd.DataFrame:
        timestamp = datetime.now()

        stats = {
            "__ingestion_timestamp": timestamp,
            "spider_name": data.get("spider_name", None),
            "item_scraped_count": data.get("stats").get("item_scraped_count", None),
            "elapsed_time_seconds": data.get("stats").get("elapsed_time_seconds", None)
        }

        return pd.DataFrame([stats])
