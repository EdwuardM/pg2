from django.contrib import admin

from .models import Buy, BuyDetail,ShoppingList

admin.site.register(ShoppingList)
admin.site.register(BuyDetail)
admin.site.register(Buy)
