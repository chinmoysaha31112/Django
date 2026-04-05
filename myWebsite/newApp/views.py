from django.shortcuts import render, get_object_or_404
from .models import Product

def app(request):
    products = Product.objects.all()        
    return render(request, 'newApp/app.html', {'products': products})

def about(request):
    return render(request, 'newApp/about.html')

def contact(request):
    return render(request, 'newApp/contact.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'newApp/product_detail.html', {'product': product})

# Create your views here.
