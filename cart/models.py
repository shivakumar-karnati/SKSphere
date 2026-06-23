from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.validators import MinValueValidator

class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=1,validators=[MinValueValidator(1)])

    added_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product_cart')
        ]
        indexes = [
        models.Index(fields=['user']),
    ]
    def __str__(self):
        return self.product.name
    

