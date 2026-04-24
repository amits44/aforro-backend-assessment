from django.db import models

class Category(models.Model):
    name = models.CharField(max_length= 50)

    def __str__(self):
        return self.name

class Products(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField( max_length=50)
    price = models.DecimalField(max_length =10, decimal_place =2)
    category = models.ForeignKey(Category, verbose_name= "products", on_delete=models.CASCADE)

    def __str__(self):
        return self.title