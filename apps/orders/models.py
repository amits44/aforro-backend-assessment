from django.db import models 
from apps.store.models import Store
from apps.products.models import Products
 
class Orders(models.Model):
    store = models.ForeignKey(Store, verbose_name="store", on_delete=models.CASCADE)
    status_choices =(
        ('pending','pending'),
        ('confirmed','confirmed'),
        ('rejected','rejected'),
    )
    status= models.CharField(max_length=20, choices= status_choices,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store.name} {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Orders, verbose_name="orders", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name="products", on_delete=models.CASCADE)
    quantity_requested= models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} {self.quantity_requested}"