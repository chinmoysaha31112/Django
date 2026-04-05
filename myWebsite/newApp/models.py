from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    PRODUCT_STATUS = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS, default='available')
    
    def __str__(self):
        return self.name

# One to many relationship
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Product : {self.product.name} - User : {self.user.username} - Rating : {self.rating} - Comment : {self.comment}"

# Many to many relationship
class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    product_varieties = models.ManyToManyField(Product, related_name='stores')

    def __str__(self):
        return self.name

#one to one relationship
class ProductCertificate(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    certificate_number = models.CharField(max_length=100)
    issued_date = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()

    def __str__(self):
        return f"Certificate for {self.product.name}"



