from celery import shared_task
from .utils import romanian_stocks

@shared_task
def hello():
    return "Hello"

@shared_task
def populate_romanian_stocks():
    romanian_stocks.populate_stocks()