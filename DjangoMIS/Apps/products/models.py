from django.db import models
from django.forms import model_to_dict
from Apps.suppliers.models import Supplier


class Category(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the category",
    )

    class Meta:
        # Table's name
        db_table = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

class Warehouse(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the category",
    )

    class Meta:
        db_table = "Warehouse"
        verbose_name_plural = "Warehouses"

    def __str__(self) -> str:
        return self.name

class RuleSupply(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo")
    )
    minimumAmount = models.FloatField()
    maximumQuantity = models.FloatField()
    supplier = models.ForeignKey(
        Supplier, models.DO_NOTHING, db_column='supplier', default= None,  null=True, blank=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the rule supply",
        default="INACTIVO"  # Puedes establecer un valor predeterminado según tus necesidades.
    )

    class Meta:
        db_table = "RuleSupply"
        verbose_name_plural = "Warehouses"

class Product(models.Model):
    STATUS_CHOICES = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the product",
    )
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.CASCADE, db_column='category')
    warehouse = models.ForeignKey(
        Warehouse, related_name="warehouse", on_delete=models.CASCADE, db_column='warehouse', default=None)
    ruleSupply = models.ForeignKey(
        RuleSupply, related_name="ruleSupply", on_delete=models.CASCADE, db_column='ruleSupply', default= None,  null=True, blank=True)
    price = models.FloatField(default=0)
    priceBuy = models.FloatField(default=0)
    quantity= models.FloatField(default=0)
    image = models.ImageField(upload_to='product_images/', default='default_image.jpg')


    class Meta:
        db_table = "Product"

    def __str__(self):
        return self.name

    def to_json(self):
        item = model_to_dict(self)
        item['id'] = self.id
        item['text'] = self.name
        item['category'] = self.category.name
        item['warehouse'] = self.warehouse.name
        item['ruleSupply'] = self.id
        item['quantity'] = 1
        item['total_product'] = 0
        return item