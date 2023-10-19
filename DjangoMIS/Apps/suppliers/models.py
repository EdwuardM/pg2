from django.db import models
from django.forms import model_to_dict


class Supplier(models.Model):
    first_name = models.CharField(max_length=256)
    company_name = models.CharField(max_length=256, blank=True, null=True)
    address = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    assessment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'Suppliers'

    def __str__(self) -> str:
        return self.first_name + " " + self.company_name

    def get_full_name(self):
        return self.first_name + " de " + self.company_name

    def to_select2(self):
        item = {
            "label": self.get_full_name(),
            "value": self.id
        }
        return item
