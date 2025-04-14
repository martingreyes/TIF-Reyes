from celery_config import app
from app.MarketScraper import MarketScraper

@app.task
def fetch_market_data(supermercado):
    scraper = MarketScraper()
    data = scraper.fetch_data(supermercado)
    items = scraper.get_items(data)
    stats = scraper.get_stats(data)
    
    return items.to_dict(orient="records"), stats.to_dict(orient="records")
