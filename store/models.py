from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField

    
class Category(models.Model):
    name = models.CharField(max_length= 50)
    def __str__(self): 
        return self.name
    class Meta:
        verbose_name_plural = 'categories'

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="ccategories", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        # Check if `category` is not None before trying to access its name
        if self.category:
            return f"{self.name} (under {self.category.name})"
        else:
            return self.name  # Display only the subcategory name if no category is set


class Brand(models.Model):
    name = models.CharField(max_length= 50)
    cover_image = models.ImageField(upload_to='brand_covers/', null=True, blank=True)  # Add cover_image field

    
    def __str__(self): 
        return self.name
    class Meta:
        verbose_name_plural = 'brands'
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self): 
        return self.name
    
class SkinType(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Normal", "Dry", "Oily", etc.
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    pdID = models.CharField(max_length=10, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=7)
    subCategory = models.ForeignKey(SubCategory, related_name="products", on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    # description = models.TextField(blank=True, null=True)
    description = RichTextField(null=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=7)
    main_image = models.ImageField(upload_to='products/')
    secondary_image = models.ImageField(upload_to='products/', null=True, blank=True)
    extra_image1 = models.ImageField(upload_to='products/', null=True, blank=True)
    extra_image2 = models.ImageField(upload_to='products/', null=True, blank=True)
    key_ingredients = models.TextField(blank=True, null=True)
    how_to_use = models.TextField(blank=True, null=True)
    skin_type = models.ForeignKey(SkinType, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')  # Add this line

    def get_price(self):
        return self.sale_price if self.is_sale else self.price

    def __str__(self):
        return self.name

from django.utils import timezone
from django.conf import settings
# Customer Orders
class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    customer_name = models.CharField(max_length=100, default = "Default Name")
    customer_address = models.CharField(max_length=255, default="Default Address")
    customer_city = models.CharField(max_length=50, default="Default City")
    customer_phone = models.CharField(max_length=15, default = "Default Phone")
    created_at = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)

    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) in Order {self.order.id}"
    
####################### K M T profile and Login Logout #######################################
# Create Customer Profile
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	state = models.CharField(max_length=200, blank=True)
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)
	old_cart = models.CharField(max_length=20000, blank=True, null=True)
	old_wishlist = models.CharField(max_length=20000, blank=True, null=True)

	def __str__(self):
		return self.user.username
    

from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def get_total(self):
        return self.quantity * self.product.get_price()

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.name}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.product.name}"
    


