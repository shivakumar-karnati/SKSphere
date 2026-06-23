from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone


class Order(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    PAYMENT_CHOICES = (
    ('COD', 'Cash On Delivery'),
    ('UPI', 'UPI Payment'),
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='COD'
        )
    STATUS_CHOICES = [

    ('payment Verification', 'payment Verification'),

    ('Processing', 'Processing'),

    ('Shipped', 'Shipped'),

    ('Delivered', 'Delivered'),

    ('Cancelled', 'Cancelled'),

    ]
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='payment Verification'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Order #{self.id}"
    

class OrderItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        return self.product.name
    

class Payment(models.Model):

    PAYMENT_STATUS = (

        ('Pending', 'Pending'),

        ('Verified', 'Verified'),

        ('Rejected', 'Rejected'),

    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    screenshot = models.ImageField(
        upload_to='payments/'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='Pending'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Payment #{self.id}"
    

class Coupon(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount = models.IntegerField(
        help_text="Percentage Discount"
    )

    minimum_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    active = models.BooleanField(
        default=True
    )

    expiry_date = models.DateField()

    def is_valid(self):

        return (
            self.active and
            self.expiry_date >= timezone.now().date()
        )

    def __str__(self):

        return self.code
    


@receiver(post_save, sender=Order)
def order_status_email(sender, instance, created, **kwargs):

    if not created:

        if instance.status == "Shipped":

            send_mail(
                f"Order #{instance.id} Shipped",

                    f"""
                Hello {instance.full_name},

                Your order has been shipped.

                Order ID: {instance.id}

                Thank you for shopping with SKSphere.
                        """,

                None,

                [instance.user.email]
            )
        elif instance.status == "Delivered":

            send_mail(
                    f"Order #{instance.id} Delivered",

                    f"""
            Hello {instance.full_name},

            Your order has been delivered.

            We hope you enjoy your purchase.

            Thank you for choosing SKSphere.
            """,

            None,

            [instance.user.email]
            )

        elif instance.status == "Cancelled":

            send_mail(
                f"Order #{instance.id} Cancelled",

                f"""
                Hello {instance.full_name},

                Your order has been cancelled.

                Order ID: {instance.id}

                If this was a mistake, please contact support.
                """,

                None,

                [instance.user.email]
            )