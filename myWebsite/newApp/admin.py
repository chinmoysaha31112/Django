from django.contrib import admin
from .models import Product, ProductReview, Store, ProductCertificate, ProductImage, ProductFeedback, Order, OrderItem


class ProductImageInline(admin.TabularInline):
    """Allows adding multiple gallery images directly on the Product admin page."""
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    filter_horizontal = ('product_varieties',)


@admin.register(ProductCertificate)
class ProductCertificateAdmin(admin.ModelAdmin):
    list_display = ('product', 'certificate_number', 'issued_date', 'valid_until')


@admin.register(ProductFeedback)
class ProductFeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'product', 'rating', 'submitted_at')
    readonly_fields = ('submitted_at',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'city', 'total_amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'price')
