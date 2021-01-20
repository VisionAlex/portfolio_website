from django.db import models
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class Portfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=3)
    cash_balance = models.DecimalField(max_digits=20,decimal_places=6, default =0.0)

    def __str__(self):
        return self.name

class Exchange(models.Model):
    mic = models.CharField("mic code", max_length=5, unique=True, primary_key=True)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=254)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Stock(models.Model):
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=254)
    exchange = models.ForeignKey(Exchange,on_delete=models.CASCADE, related_name="stocks")
    figi = models.CharField(max_length=100, blank=True)
    symbol = models.CharField(max_length=20, unique=True)
    stock_type = models.CharField("type", max_length=100)

    
    def __str__(self):
        return f"{self.symbol} - {self.description}"

class StockPrice(models.Model):
    timestamp = models.DateTimeField(db_index=True,)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=18, decimal_places=6)

    def __str__(self):
        return f"{str(self.stock)} - {self.price}"

    class Meta:
        ordering = ['-timestamp']
        get_latest_by = "timestamp"

class Position(models.Model):
    portfolio = models.ForeignKey(Portfolio,on_delete=models.CASCADE, related_name="positions")
    date = models.DateField(default=date.today)
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    units = models.PositiveIntegerField()
    cost_base = models.DecimalField(max_digits=18, decimal_places=6)

    def display_currency(self):
        return self.stock.currency
    display_currency.short_description = "Currency"

    def display_symbol(self):
        return self.stock.symbol
    display_symbol.short_description = "Symbol"

    def display_price(self):
        return f"{self.stock.prices.latest().price:.2f}"
    display_price.short_description = "Price"
    
    def __str__(self):
        return f"{str(self.portfolio)} - {str(self.stock)}"
    
    def display_market_value(self):
        price = self.stock.prices.latest().price
        if self.stock.currency != 'GBp':
            pair_string = "EUR" + self.stock.currency
        else:
            pair_string = "EUR" + "GBP"
        pair = CurrencyPair.objects.get(name=pair_string)
        rate = pair.rates.latest().price
        if self.stock.currency != "GBp" and self.stock.currency != "ILS":
            market_value = (price * self.units) / rate
        else:
            market_value = ((price * self.units )/ rate)/100
            
        return f"{market_value:.1f}"

    

class CurrencyPair(models.Model):
    name = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name
    
    def yahoo_code(self):
        return ''.join((self.name, "=X"))

class CurrencyRate(models.Model):
    timestamp = models.DateTimeField()
    pair = models.ForeignKey(CurrencyPair, on_delete=models.CASCADE, related_name="rates")
    price = models.DecimalField(max_digits=18, decimal_places=8)

    def __str__(self):
        return str(self.pair)
    
    class Meta:
        get_latest_by = "timestamp"

class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    buy_sell = models.CharField(max_length=4, choices=[('B', 'BUY'),('S','SELL')])
    quantity = models.IntegerField()
    price =models.DecimalField(max_digits=18, decimal_places=4)
    date = models.DateField()
    fee = models.DecimalField(max_digits=18, decimal_places=4)
    exchange_rate = models.DecimalField(max_digits=18, decimal_places=6)

    def __str__(self):
        return f"{self.buy_sell} - {self.quantity} - {str(self.stock)}"