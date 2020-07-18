from django.shortcuts import render
from .models import Product


def all_products(request):
    """A view to show all products, including sorting and searching"""
 
    products = Product.objects.all()

    # we need context since we need to send things back to the template
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)