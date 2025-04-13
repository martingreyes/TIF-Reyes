from celery import Celery
from app.MarketScraper import MarketScraper
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_URL =  f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

app = Celery('celery_tasks', broker=REDIS_URL, backend=REDIS_URL)

@app.task
def fetch_market_data(supermercado):
    scraper = MarketScraper()
    data = scraper.fetch_data(supermercado)
    items = scraper.get_items(data)
    stats = scraper.get_stats(data)
    
    return items.to_dict(orient="records"), stats.to_dict(orient="records")
