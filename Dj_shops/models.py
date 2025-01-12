from django.db import models

class EmallsShop(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(unique=True, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    products = models.JSONField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Emalls Shop'
        verbose_name_plural = 'Emalls Shops'


class Product(models.Model):
    related_shop = models.ForeignKey(EmallsShop, on_delete=models.CASCADE, null=True, blank=True)
    related_shop_token = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    url = models.URLField()
    image_url = models.URLField()
    store_count = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    