from django.contrib import admin


from .models import Category, Product, Warehouse, RuleSupply

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(RuleSupply)