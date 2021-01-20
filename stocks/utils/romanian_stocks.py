import requests
import os
import csv
from stocks.models import Exchange, Stock


def populate_stocks():
    if not os.path.exists('files/bvb_data.csv'):
        url ='https://www.bvb.ro/FinancialInstruments/Markets/SharesListForDownload.ashx?filetype.csv'
        response= requests.get(url)
        with open('files/bvb_data.csv', 'wb') as f:
            f.write(response.content)
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