import yfinance as yf
from datetime import datetime
import pytz
from stocks.models import Stock, CurrencyPair, CurrencyRate


def get_pairs(main_currency):
    currencies = [pair[0] for pair in Stock.objects.values_list('currency').distinct()]
    if 'GBp' in currencies:
        currencies.remove('GBp')
    
    for currency in currencies:
        pair_name = main_currency + currency
        if main_currency == currency or not currency:
            continue
        else:
            try:
                d, created = CurrencyPair.objects.get_or_create(name=pair_name)
                print(f"{d} - Created:{created}")
            except Exception as e:
                print(e)


def get_rates():
    pairs = CurrencyPair.objects.all()
    yahoo_pairs = [pair.yahoo_code() for pair in pairs]
    yahoo_string = ' '.join(yahoo_pairs)
    start = CurrencyRate.objects.latest().timestamp
    end = datetime.now()
    data = yf.download(yahoo_string, start=start, end=end, interval="1d")
    
    data = data['Adj Close']
    for symbol in data.columns:
        pair_data = data[symbol]
        pair_data.dropna(inplace=True)
        pair = CurrencyPair.objects.get(name=symbol[:-2]) # remove the =X
        for date, rate in pair_data.items():
            date = pytz.utc.localize(date)
            try:
                d, created = CurrencyRate.objects.get_or_create(
                    timestamp=date,
                    pair=pair,
                    price=rate,
                )
                print(f"{pair} - created")
            except Exception as e:
                print(e)
                print(date,rate)
