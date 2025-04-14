from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_URL =  f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

app = Celery('celery_tasks', broker=REDIS_URL, backend=REDIS_URL, include=['fetch_market_data'])