from django.db import models
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Item(models.Model):
    SIZE= (
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large"),
    )
    tittle = models.CharField( max_length=100, null=True)
    brief_description = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    discount_price = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=30, null=True, choices=SIZE)
    product_description = models.CharField(max_length=500, null=True )
    product_image = CloudinaryField('image')
    slug = models.SlugField(null=True,blank=True, unique=True)

    def __str__(self):
        return self.tittle or " "

    def get_absolute_url(self):
        return reverse("details", kwargs={"slug": self.slug})

    def get_cart_url(self):
        return reverse("add-to-cart", kwargs={"slug": self.slug})

    def get_remove_cart_url(self):
        return reverse("remove-from-cart", kwargs={"slug": self.slug})



class OrderItem(models.Model):
    customer = models.ForeignKey(User, max_length=100, null=True,blank=True, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, default="", on_delete=models.CASCADE)
    number_of_Products = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        #return f"{self.number_of_Products} of {self.item.tittle}"
        return str(self.number_of_Products) + " of " + str(self.item.tittle)
    #def total_item_price(self):
        #total = int(self.number_of_Products) * int(self.item.price)
        #return total
    def total_item_price(self):
        try:
            num_products = int(self.number_of_Products)
        except ValueError:
            num_products = 0

        try:
            item_price = float(self.item.price)
        except ValueError:
            item_price = 0.0

        total = num_products * item_price
        return total

    def discount_total_price(self):
        total = int(self.number_of_Products) * int(self.item.discount_price)
        return total
    def money_saved(self):
        saved = self.total_item_price() -self.discount_total_price()
        return saved
    def final_price(self):
        if self.item.discount_price:
            return self.discount_total_price()
        return self.total_item_price()



class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    customer = models.ForeignKey(User, null=True,on_delete=models.SET_NULL, blank=True )
    amount = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.customer)

class DiscountCode(models.Model):
    code = models.CharField(max_length=16)
    amount = models.FloatField(default=0.0)
    def __str__(self):
        return self.code



class Order(models.Model):
    STATUS =(
        ("Out of Stock", "Out of Stock"),
        ("Pending", "Pending"),
        ("Delivered", "Delivered"),
    )
    customer = models.ForeignKey(User, max_length=100, null=True,on_delete=models.CASCADE )
    ref_code = models.CharField(max_length=20, null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True, null=True)
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=STATUS, null=True)
    payment = models.ForeignKey('Payment', null=True,on_delete=models.SET_NULL, blank=True )
    discount_coupon = models.ForeignKey(DiscountCode,on_delete=models.SET_NULL, blank=True, null=True )
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer)
    def get_total(self):
        total = 0
        order_item = self.items.all()
        for i in order_item:
            total += i.final_price()
        if self.discount_coupon:
            total -= int(self.discount_coupon.amount)
        return total
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


class Blog(models.Model):
    class Meta:
        verbose_name_plural = "blogs"
        verbose_name = 'blog'

    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    body = RichTextField(blank=True, null=True)
    # slug = models.SlugField(null=True, blank=True)
    image = CloudinaryField('image')
    #blog_image = CloudinaryField('image')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name or ""






