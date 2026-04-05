from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ProductFeedback


def app(request):
    products = Product.objects.all()
    return render(request, 'newApp/app.html', {'products': products})


def about(request):
    return render(request, 'newApp/about.html')


def contact(request):
    return render(request, 'newApp/contact.html')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Collect all images: main image + gallery images
    gallery_images = list(product.images.all())
    return render(request, 'newApp/product_detail.html', {
        'product': product,
        'gallery_images': gallery_images,
    })


def submit_feedback(request, product_id):
    """Handles the feedback form POST for a specific product."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        try:
            rating = int(request.POST.get('rating', 5))
            if not (1 <= rating <= 5):
                rating = 5
        except (ValueError, TypeError):
            rating = 5
        if name and email and message:
            ProductFeedback.objects.create(
                product=product,
                name=name,
                email=email,
                rating=rating,
                message=message,
            )
            messages.success(request, 'Thank you! Your feedback has been submitted.')
        else:
            messages.error(request, 'Please fill in all fields.')
    return redirect('newApp:product_detail', product_id=product_id)
