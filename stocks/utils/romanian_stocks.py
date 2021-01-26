import requests
import os
import csv
import pytz
from bs4 import BeautifulSoup
from datetime import datetime
from stocks.models import Exchange, Stock, StockPrice


def get_stocks():
    try:
        url ='https://www.bvb.ro/FinancialInstruments/Markets/SharesListForDownload.ashx?filetype.csv'
        response= requests.get(url)
        with open('files/bvb_data.csv', 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(e)
    with open('files/bvb_data.csv') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['Status'] != "Tradeable":  continue
            try:
                exchange = Exchange.objects.get(pk="X" +row['Exchange segment'])
                d, created = Stock.objects.get_or_create(
                    currency='RON',
                    description=row['Security name'].upper() ,
                    exchange=exchange,
                    figi=row['ISIN'],
                    symbol=row['Symbol'] + '.' + exchange.code,
                    stock_type='Common Stock'

                )
                print(f"Data: {str(d)}, Created: {str(created)}")
            except Exception as e:
                print(row)
                print(e)
                continue

def get_prices():
    exchange = Exchange.objects.get(mic="XBSE")
    data = exchange.stocks.values_list('symbol')
    symbols = [symbol[0][:-3] for symbol in data]
    
    for symbol in symbols:
        try:
            url = f"https://www.bvb.ro/FinancialInstruments/Details/FinancialInstrumentsDetails.aspx?s={symbol}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            price = soup.find('strong').text
            stock = Stock.objects.get(symbol=(symbol + ".RO"))
            date_string = soup.select(".date .small")[0].text.strip()
            timestamp =datetime.strptime(date_string, "%m/%d/%Y %I:%M:%S %p")
            timestamp = pytz.timezone("Europe/Bucharest").localize(timestamp)
            StockPrice.objects.create(
                timestamp=timestamp,
                stock=stock,
                price=price,
            )
            print(f"{symbol} -added at {timestamp}")
        except Exception as e:
            print(e)
            break