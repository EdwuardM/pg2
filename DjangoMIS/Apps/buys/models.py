from django.db import models
import django.utils.timezone
from Apps.products.models import Product
from django.contrib.auth.models import User
from Apps.suppliers.models import Supplier


class ShoppingList(models.Model):
    STATUS_CHOICES = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo")
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    grand_total = models.FloatField(default=0)
    opening_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the category",
    )

    class Meta:
        db_table = 'ShoppingList'

    def sum_items(self):
        details = BuyDetail.objects.filter(shoppinglist=self)
        return sum([d.quantity for d in details])


class BuyDetail(models.Model):
    shoppinglist = models.ForeignKey(
        ShoppingList, on_delete=models.CASCADE, related_name='buy_details')
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    total_detail = models.FloatField()

    class Meta:
        db_table = 'BuyDetails'


class Buy(models.Model):
    shoppinglist = models.ForeignKey(
        ShoppingList, on_delete=models.CASCADE)
    opening_date = models.DateTimeField(null=True, blank=True)
    grand_total = models.FloatField(default=0)


    class Meta:
        db_table = 'Buy'

