from django.db import models 
from apps.products.models import Products

class Store(models.Model):
    name= models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    store = models.ForeignKey(Store, verbose_name="store", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name="product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=[store,product], name="unique_store_product_inventory")
        ]
    
    def __str__(self):
        return f"{self.store.name} - {self.product.title} - {self.quantity}"