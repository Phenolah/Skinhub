
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.
class Order(models.Model):
    STATUS =(
        ("Out of Stock", "Out of Stock"),
        ("Pending", "Pending"),
        ("Delivered", "Delivered"),
    )
    customer = models.OneToOneField(User, max_length=100, null=True,on_delete=models.CASCADE )
    start_date = models.DateTimeField(auto_now_add=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True, null=True)
    ordered = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=30, choices=STATUS, null=True)

class Item(models.Model):
    SIZE= (
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large"),
    )
    tittle = models.CharField( max_length=100, null=True)
    brief_description = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=30, null=True)
    size = models.CharField(max_length=30, null=True, choices=SIZE)
    product_description = models.CharField(max_length=500, null=True )
    number_of_Products = models.CharField(max_length=30, null=True)
    product_image = CloudinaryField('image')
    #product_image = models.ImageField(upload_to='image/', blank=True)


    def __str__(self):
        return self.tittle or " "

class OrderItem(models.Model):
    pass


