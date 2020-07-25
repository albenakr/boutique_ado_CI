from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            #  the reason for copying the sort parameter into a new variable called sortkey. 
            # Is because now we've preserved the original field. We want it to sort on name,  
            # but we have the actual field we're going to sort on, lower_name in the sort key variable.
            # If we had just renamed sort itself to lower_name we would have lost the original field name.
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                # Annotation allows us to add a temporary field on a model 
                products = products.annotate(lower_name=Lower('name'))
            # so that categories are sorted by name, instead of ID
            if sortkey == 'category':
            # __ syntax allows us to drill into a related model
               sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    # the '-' reverses the order to make it desc
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
       
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            # converting the list of strings of category names passed through the URL 
            # into a list of actual category objects
            #  so that we can access all their fields in the template.
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            # the i before contains makes it case it case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

#using current_sorting to return to the template
    current_sorting = f'{sort}_{direction}'

# contect returns info to the template
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        # if there is no sorting, the value of this would be None_None
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)