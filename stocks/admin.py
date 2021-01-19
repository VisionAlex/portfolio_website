from django.contrib import admin
from .models import (
    Exchange, Stock, Portfolio, Transaction, StockPrice, Position, CurrencyPair, CurrencyRate)

# Register your models here.
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'mic', 'code')
    search_fields = ('name','mic', 'code')

class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol','description','currency','figi', 'exchange', 'stock_type')
    search_fields = ('symbol', 'description')
    list_filter = ('currency','exchange', 'stock_type')

    

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'date','buy_sell','quantity','price','stock')
    autocomplete_fields = ('stock',)


class PositionAdmin(admin.ModelAdmin):
    autocomplete_fields = ('stock',)
    list_display = ('stock','units','cost_base', 'display_currency', 'display_price', 'display_market_value')
    list_filter = ('portfolio',)
    
class CurrencyPairAdmin(admin.ModelAdmin):
    pass

class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('timestamp','pair','price')
    list_filter = ('timestamp',)

    
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'stock', 'price')
    autocomplete_fields = ('stock',)
    search_fields = ('stock__symbol', 'stock__description')
    list_filter = ('timestamp','stock__exchange')





admin.site.register(Exchange,ExchangeAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Portfolio)
admin.site.register(StockPrice, StockPriceAdmin)
admin.site.register(Position,PositionAdmin)
admin.site.register(CurrencyPair, CurrencyPairAdmin)