import json
import pickle

from stocks.models import Position, Portfolio, Stock

def unpickle():
    pickle_in = open('files/positions.pickle', 'rb')
    positions = pickle.load(pickle_in)


    for item in positions:
        if item['stock'][:-4] == '.ROM':
            symbol = item['stock'].replace('.ROM', '.RO')
        else:
            symbol = item['stock']
        try:
            portfolio = Portfolio.objects.get(name=item['portfolio'])
            stock = Stock.objects.get(symbol=symbol)
            obj, created = Position.objects.update_or_create(
                portfolio=portfolio,
                date=item['date'],
                stock=stock,
                units=item['units'],
                cost_base=item['cost_base'],
            )
            print(f"{item['stock']} {created}")
        except Exception as e:
            print(item)
            print(e)

