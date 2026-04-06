from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from decimal import Decimal
from .models import Product, ProductFeedback, Order, OrderItem


# ─────────────────────────────────────────────
# Helper: get cart from session
# ─────────────────────────────────────────────
def get_cart(request):
    """Returns the cart dict from the session. Structure: {product_id_str: quantity}"""
    return request.session.get('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


# ─────────────────────────────────────────────
# Product listing
# ─────────────────────────────────────────────
def app(request):
    products = Product.objects.all()
    cart = get_cart(request)
    cart_count = sum(cart.values())
    return render(request, 'newApp/app.html', {
        'products': products,
        'cart_count': cart_count,
    })


# ─────────────────────────────────────────────
# Static pages
# ─────────────────────────────────────────────
def about(request):
    cart = get_cart(request)
    return render(request, 'newApp/about.html', {'cart_count': sum(cart.values())})


def contact(request):
    cart = get_cart(request)
    return render(request, 'newApp/contact.html', {'cart_count': sum(cart.values())})


# ─────────────────────────────────────────────
# Product detail
# ─────────────────────────────────────────────
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    gallery_images = list(product.images.all())
    cart = get_cart(request)
    cart_count = sum(cart.values())
    return render(request, 'newApp/product_detail.html', {
        'product': product,
        'gallery_images': gallery_images,
        'cart_count': cart_count,
    })


# ─────────────────────────────────────────────
# Feedback
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# Cart — Add
# ─────────────────────────────────────────────
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    key = str(product_id)
    try:
        qty = int(request.POST.get('quantity', 1))
        if qty < 1:
            qty = 1
    except (ValueError, TypeError):
        qty = 1

    cart[key] = cart.get(key, 0) + qty
    save_cart(request, cart)
    messages.success(request, f'"{product.name}" added to your cart!')

    # If "buy now", skip cart and go straight to checkout
    if request.POST.get('buy_now'):
        return redirect('newApp:checkout')
    return redirect('newApp:view_cart')


# ─────────────────────────────────────────────
# Cart — View
# ─────────────────────────────────────────────
def view_cart(request):
    cart = get_cart(request)
    cart_items = []
    grand_total = Decimal('0.00')

    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            subtotal = product.price * qty
            grand_total += subtotal
            cart_items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            pass

    return render(request, 'newApp/cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total,
        'cart_count': sum(cart.values()),
    })


# ─────────────────────────────────────────────
# Cart — Update quantity
# ─────────────────────────────────────────────
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = get_cart(request)
        key = str(product_id)
        try:
            qty = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            qty = 1
        if qty > 0:
            cart[key] = qty
        else:
            cart.pop(key, None)
        save_cart(request, cart)
    return redirect('newApp:view_cart')


# ─────────────────────────────────────────────
# Cart — Remove item
# ─────────────────────────────────────────────
def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    save_cart(request, cart)
    messages.success(request, 'Item removed from cart.')
    return redirect('newApp:view_cart')


# ─────────────────────────────────────────────
# Checkout
# ─────────────────────────────────────────────
def checkout(request):
    cart = get_cart(request)
    if not cart:
        messages.error(request, 'Your cart is empty. Add some products first!')
        return redirect('newApp:home')

    # Build cart items for display
    cart_items = []
    grand_total = Decimal('0.00')
    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            subtotal = product.price * qty
            grand_total += subtotal
            cart_items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            pass

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address_line1 = request.POST.get('address_line1', '').strip()
        address_line2 = request.POST.get('address_line2', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()

        if not all([full_name, phone, email, address_line1, city, state, pincode]):
            messages.error(request, 'Please fill in all required delivery fields.')
            return render(request, 'newApp/checkout.html', {
                'cart_items': cart_items,
                'grand_total': grand_total,
                'cart_count': sum(cart.values()),
                'form_data': request.POST,
            })

        # Create the order
        order = Order.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            pincode=pincode,
            total_amount=grand_total,
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product'].name,
                price=item['product'].price,
                quantity=item['quantity'],
            )

        # Clear the cart
        save_cart(request, {})
        return redirect('newApp:order_success', order_id=order.id)

    return render(request, 'newApp/checkout.html', {
        'cart_items': cart_items,
        'grand_total': grand_total,
        'cart_count': sum(cart.values()),
        'form_data': {},
    })


# ─────────────────────────────────────────────
# Order success confirmation
# ─────────────────────────────────────────────
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'newApp/order_success.html', {
        'order': order,
        'cart_count': 0,
    })
