from django.contrib import admin

from .models import Sale, SaleDetail,CashRegisterOpening

admin.site.register(Sale)
admin.site.register(SaleDetail)
admin.site.register(CashRegisterOpening)
