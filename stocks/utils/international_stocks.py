import requests
import os
import csv
import json
from bs4 import BeautifulSoup
import pandas as pd
import finnhub
from stocks.models import Exchange, Stock



def get_lse_iob_stocks():
    URL = "https://www.londonstockexchange.com/trade/equity-trading/international-order-book?lang=en"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "lxml")
    link_url = soup.select(".simple-document__title a.black-link")[0]['href']
    
    df = pd.read_excel(io=link_url, skiprows=lambda x: x in [0,1,2,4], usecols=[3,4,8,12,13,14])
    dictionary = df.to_dict(orient="records")
    exchange = Exchange.objects.get(pk='IOB')
    for item in dictionary:
        try:
            if "GDR" in item['Long Name']:
                stock_type = 'GDR'
            else:
                stock_type = 'ADR'
            d, created = Stock.objects.get_or_create(
                currency=item['Currency'],
                    description=item['Short Name'] + " " + item['Long Name'],
                    exchange=exchange,
                    figi=item['ISIN'],
                    symbol=item['Mnemonic'] + '.IL',
                    stock_type= stock_type
            )
            print(f"{item['Short Name']} - Created: {created}")
        except Exception as e:
            print(item['Mnemonic'])
            print(e)



def get_stocks(exchange):
    client = finnhub.Client(api_key=os.environ.get("FINNHUB"))
    data = client.stock_symbols(exchange)
    for item in data:
        if not item['mic']:
            continue
        try:
                exchange = Exchange.objects.get(pk=item['mic'])
                d, created = Stock.objects.get_or_create(
                    currency=item['currency'],
                    description=item['description'],
                    exchange=exchange,
                    figi=item['figi'],
                    symbol=item['symbol'],
                    stock_type=item['type']

                )
                print(f"Data: {str(d)}, Created: {str(created)}")
        except Exception as e:
            print(item)
            print(e)


# if __name__=="__main__":
#     get_lse_stocks()