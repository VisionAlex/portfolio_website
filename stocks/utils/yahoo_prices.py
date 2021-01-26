from datetime import datetime
import yfinance as yf
from yfinance import shared
import pytz

from stocks.models import Stock, StockPrice, Position


def latest():
    positions = Position.objects.exclude(stock__exchange__mic="XBSE")
    symbols = [pos.stock.symbol for pos in positions]

    symbols_string = ' '.join(symbols)
    data = yf.download(symbols_string, period="5d", interval="1m")
    data = data['Adj Close']

    for symbol in data.columns:
        stock_data = data[symbol]
        stock_data.ffill(inplace=True)
        last_item = stock_data.tail(1)
        if last_item.empty:
            print(f"ERROR={symbol}")
            continue
        try:
            timestamp = last_item.index.to_pydatetime()[0]
        except Exception as e:
            print(symbol)
            print(e)
            continue
        price = last_item.iloc[0]
        if not price or price == "NaN":
            continue
        stock = Stock.objects.get(symbol=symbol)
        try:
            StockPrice.objects.create(
                timestamp=timestamp,
                stock=stock,
                price=price,
            )
            print(f"{symbol} -added at {timestamp}")
        except Exception as e:
            print(symbol, e)

def historic_prices():
    positions = Position.objects.exclude(stock__exchange__mic="XBSE")
    symbols = [pos.stock.symbol for pos in positions]

    symbols_string = ' '.join(symbols)
    data = yf.download(symbols_string, period="10y", interval="1d")
    data = data['Adj Close']

    for symbol in data.columns:
        stock_data = data[symbol]
        stock_data.dropna(inplace=True)
        stock = Stock.objects.get(symbol=symbol)

        for date, price in stock_data.items():
            timestamp = pytz.utc.localize(date)
            if not price or price == "NaN":
                continue
            try:
                d, created = StockPrice.objects.get_or_create(
                    timestamp=timestamp,
                    stock=stock,
                    price=price
                    )
                print(f"{symbol} -added at {timestamp}")
            except Exception as e:
                print(symbol, e)
                

