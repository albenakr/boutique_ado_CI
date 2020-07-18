from django.contrib import admin
from .models import Product, Category

# Register your models here.


# these classes extend the built in model admin class
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    # sort the products by sku using the ordering attribute
    # has to be a tuple even if it's only one field
    # to reverse it simply stick a minus in front of sku
    ordering = ('sku',)

# if you want to change the order of columns in the admin
# change the order here in the list display attribute


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
