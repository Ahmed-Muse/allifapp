from django.db import models

# Create your models here.

########################## for testing purposes ########################

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_cost(self):
        return self.quantity * self.unit_cost

    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return self.name
