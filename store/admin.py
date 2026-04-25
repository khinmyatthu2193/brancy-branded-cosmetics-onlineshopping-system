from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Category, Brand, Product, Order, Profile, OrderItem, SubCategory

class ProductAdmin(admin.ModelAdmin):
    # Display the 'id', 'name', and other fields in the list view
    list_display = ('id', 'name', 'price', 'category', 'brand', 'subCategory')
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_address', 'customer_city', 'customer_phone', 'subtotal', 'shipping_fee', 'total', 'created_at')
    search_fields = ('order__id', 'customer_name', 'customer_address', 'customer_city', 'customer_phone')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')

    
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Profile)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
#################### K M T build profile #######################
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username","first_name","last_name","email"]
    inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)


from django.contrib import admin
from .models import Brand

# If Brand is already registered, unregister it first
admin.site.unregister(Brand)

# Register Brand with custom admin options
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'cover_image']


### For SkinType ####
from django.contrib import admin
from .models import SkinType  # Import the SkinType model

# Register the SkinType model
@admin.register(SkinType)
class SkinTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Fields to display in the admin list view
    search_fields = ('name',)  # Enable search by name
