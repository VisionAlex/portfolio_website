from celery import shared_task
from .utils import romanian_stocks, international_stocks, currencies, yahoo_prices

@shared_task
def hello():
    return "Hello"

@shared_task
def populate_exchange_rate_pairs():
    currencies.get_pairs("EUR")
    currencies.get_pairs("RON")
    currencies.get_pairs("GBP")
    currencies.get_pairs("USD")

@shared_task
def populate_exchange_rates():
    currencies.get_rates()

@shared_task
def populate_romanian_stocks():
    romanian_stocks.get_stocks()

@shared_task
def populate_romanian_prices():
    romanian_stocks.get_prices()

@shared_task
def populate_lse_stocks():
    international_stocks.get_lse_iob_stocks()
    international_stocks.get_stocks("L")

@shared_task
def populate_stocks():
    EXCHANGES = ['US','ME','MI','DE','SS','TA']
    for exchange in EXCHANGES:
        international_stocks.get_stocks(exchange)

@shared_task
def get_latest_prices():
    yahoo_prices.latest()
       