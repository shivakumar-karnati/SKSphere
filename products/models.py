from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    image = models.ImageField(
        upload_to='products/'
    )

    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    featured = models.BooleanField(
        default=False,
        db_index=True
    )

    trending = models.BooleanField(
        default=False,
        db_index=True
    )

    best_seller = models.BooleanField(
        default=False,
        db_index=True
    )
    sold_count = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created_at']  
    

class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_wishlist"
            )
        ]
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(
            default=5,
            validators=[
                MinValueValidator(1),
                MaxValueValidator(5)
            ]
        )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:

        unique_together = (
            'product',
            'user'
        )

    def __str__(self):

        return f"{self.user.username} - {self.product.name}"
    